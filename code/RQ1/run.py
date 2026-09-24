from __future__ import annotations

import argparse
import json
import string
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from common.paths import ensure_dir, read_config, read_json, resolve_in_project, write_json, write_text
from common.prompt_store import has_prompt, load_prompt as load_prompt_template
from common.spl_class_spec import (
    build_class_spec,
    render_class_spec_for_skeleton,
    render_class_spec_for_spl_only,
)
from common.spl_adapter import format_inline_spl_cards_generic
from common.providers import GenerationConfig, ModelClient
from common.run_utils import generation_kwargs, run_ordered, selected_items
from common.usage import UsageTotals, generation_metadata


EXPERIMENT_DIR = Path(__file__).resolve().parent
EXPERIMENT_NAME = EXPERIMENT_DIR.name


def load_prompt(condition: str) -> str:
    return load_prompt_template(EXPERIMENT_DIR, EXPERIMENT_NAME, condition, "prompt.md")


PROMPTS = {
    condition: load_prompt(condition)
    for condition in [
        "skeleton_holistic",
        "skeleton_incremental",
        "spl_only",
        "free_summary",
        "structured_summary",
        "spl_scaffold",
        "skeleton_spl",
        "spl_only_compact",
        "skeleton_spl_compact",
    ]
    if has_prompt(EXPERIMENT_DIR, EXPERIMENT_NAME, condition, "prompt.md")
}

ALLOWED_PROMPT_FIELDS = {
    "skeleton_holistic": {"skeleton", "class_name"},
    "skeleton_incremental": {"skeleton", "methods_info"},
    "spl_only": {"spl_inline"},
    "free_summary": {"summary"},
    "structured_summary": {"structured_summary"},
    "spl_scaffold": {"spl_inline", "scaffold"},
    "skeleton_spl": {"skeleton", "spl_inline"},
    "spl_only_compact": {"spl_compact"},
    "skeleton_spl_compact": {"skeleton", "spl_compact"},
}


def render_prompt(condition: str, template: str, fields: dict[str, str]) -> str:
    allowed = ALLOWED_PROMPT_FIELDS[condition]
    used = {name for _, name, _, _ in string.Formatter().parse(template) if name}
    disallowed = sorted(used - allowed)
    if disallowed:
        raise ValueError(
            f"Prompt for condition '{condition}' uses disallowed fields {disallowed}. "
            f"Allowed fields are {sorted(allowed)}."
        )
    return template.format(**{name: fields[name] for name in used})


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", required=True)
    args = parser.parse_args()

    config = read_config(resolve_in_project(args.config))
    artifact_dir = resolve_in_project(config["artifact_dir"])
    run_dir = ensure_dir(resolve_in_project(config["run_dir"]))
    manifest = selected_items(read_json(artifact_dir / "manifest.json"), config)
    # Code reconstruction needs visible code, not an unbounded reasoning-only
    # response. Keep this separate from SPL construction's thinking policy.
    client = ModelClient(
        GenerationConfig(**generation_kwargs(config, thinking_key="generation_thinking"))
    )
    expected_model = str(config.get("model", ""))
    resume_outputs = bool(config.get("resume_nonempty_outputs", True))

    def read_attempts(path: Path) -> list[dict]:
        if not path.exists():
            return []
        try:
            metadata = read_json(path)
        except Exception:
            return []
        attempts = metadata.get("attempts")
        if isinstance(attempts, list):
            return [row for row in attempts if isinstance(row, dict)]
        if metadata:
            copied = dict(metadata)
            copied["empty_visible_text"] = True
            return [copied]
        return []

    def retry_client() -> ModelClient:
        retry_config = dict(config)
        retry_config["generation_thinking"] = "disabled"
        return ModelClient(
            GenerationConfig(**generation_kwargs(retry_config, thinking_key="generation_thinking"))
        )

    def generate_nonempty_code(prompt: str, metadata_path: Path, condition: str):
        attempts = read_attempts(metadata_path)
        max_attempts = max(1, int(config.get("output_empty_max_attempts", 3)))
        while len(attempts) < max_attempts:
            use_thinking_fallback = bool(attempts)
            result = (retry_client() if use_thinking_fallback else client).generate_with_metrics(prompt)
            attempt = generation_metadata(result, role="classeval_reconstruction", condition=condition)
            attempt["empty_visible_text"] = not bool((result.text or "").strip())
            attempt["thinking_fallback"] = use_thinking_fallback
            attempts.append(attempt)
            if (result.text or "").strip():
                totals = UsageTotals()
                for row in attempts:
                    totals.add(row)
                metadata = generation_metadata(result, role="classeval_reconstruction", condition=condition)
                metadata.update(totals.to_dict())
                metadata["attempts"] = attempts
                metadata["empty_retries"] = sum(bool(row.get("empty_visible_text")) for row in attempts)
                metadata["used_thinking_fallback"] = any(bool(row.get("thinking_fallback")) for row in attempts)
                return result.text, metadata
        totals = UsageTotals()
        for row in attempts:
            totals.add(row)
        write_json(
            metadata_path,
            {
                **totals.to_dict(),
                "role": "classeval_reconstruction",
                "condition": condition,
                "model": expected_model,
                "attempts": attempts,
                "empty_retries": len(attempts),
                "status": "empty_visible_text",
            },
        )
        raise RuntimeError(f"empty visible code after {len(attempts)} attempts")

    def work(item: dict) -> str:
        sample_dir = resolve_in_project(item["sample_dir"])
        task_run_dir = ensure_dir(run_dir / item["task_id"])
        spl = (sample_dir / "spl.txt").read_text(encoding="utf-8")
        # Per-method SPL map for inline-card construction
        spl_by_method_path = sample_dir / "spl_by_method.json"
        spl_by_method = read_json(spl_by_method_path) if spl_by_method_path.exists() else {}
        summary_path = sample_dir / "free_summary.txt"
        summary = summary_path.read_text(encoding="utf-8") if summary_path.exists() else ""
        structured_summary_path = sample_dir / "structured_summary.txt"
        structured_summary = structured_summary_path.read_text(encoding="utf-8") if structured_summary_path.exists() else ""
        scaffold_path = sample_dir / "minimal_scaffold.txt"
        scaffold = scaffold_path.read_text(encoding="utf-8") if scaffold_path.exists() else ""
        skeleton = (sample_dir / "skeleton.txt").read_text(encoding="utf-8")
        if not skeleton.strip():
            print(f"WARNING: skeleton.txt is empty for {item['task_id']}. skeleton_holistic and skeleton_spl prompts will be degraded.")
        methods_info = json.dumps(read_json(sample_dir / "task.json").get("methods_info", []), ensure_ascii=False, indent=2)
        task_json = read_json(sample_dir / "task.json")
        class_name = task_json.get("class_name", "")
        # Build per-method inline SPL cards for each source representation.
        spl_inline_by_condition: dict[str, str] = {}
        if spl_by_method:
            class_spec = build_class_spec(spl_by_method, class_name=class_name)
            spl_inline_by_condition["spl_only"] = format_inline_spl_cards_generic(
                "", spl_by_method, "python", include_source=False,
            )
            spl_inline_by_condition["skeleton_spl"] = format_inline_spl_cards_generic(
                skeleton, spl_by_method, "python", source_code_label="Skeleton",
            )
            spl_inline_by_condition["spl_scaffold"] = format_inline_spl_cards_generic(
                scaffold, spl_by_method, "python", source_code_label="Scaffold",
            )
            spl_compact_by_condition = {
                "spl_only_compact": render_class_spec_for_spl_only(class_spec),
                "skeleton_spl_compact": render_class_spec_for_skeleton(class_spec, skeleton),
            }
        else:
            spl_compact_by_condition = {}
        fields = {
            "spl": spl,
            "spl_inline": spl,  # fallback; overridden per-condition below
            "summary": summary,
            "structured_summary": structured_summary,
            "scaffold": scaffold,
            "skeleton": skeleton,
            "methods_info": methods_info,
            "class_name": class_name,
            "spl_compact": "",
        }
        for condition in config.get("conditions", PROMPTS.keys()):
            summary_pending = (sample_dir / ".summary_pending.json").exists()
            if condition in {"free_summary", "structured_summary"} and summary_pending:
                raise RuntimeError(
                    f"Summaries not yet generated for {item['task_id']} "
                    f"(.summary_pending.json exists). "
                    "Run generate_free_summary.py before the run phase."
                )
            if condition == "free_summary" and not summary.strip():
                raise RuntimeError(
                    f"free_summary.txt is empty or missing for {item['task_id']}. "
                    "Run generate_free_summary.py before running the run phase."
                )
            if condition == "structured_summary" and not structured_summary.strip():
                raise RuntimeError(
                    f"structured_summary.txt is empty or missing for {item['task_id']}. "
                    "Run generate_free_summary.py before running the run phase. "
                    "The structured_summary condition must not silently fall back to free_summary."
                )
            # Select the appropriate inline SPL for this condition.
            if condition in spl_inline_by_condition:
                fields["spl_inline"] = spl_inline_by_condition[condition]
            else:
                fields["spl_inline"] = spl
            fields["spl_compact"] = spl_compact_by_condition.get(condition, "")
            prompt = render_prompt(condition, PROMPTS[condition], fields)
            condition_dir = ensure_dir(task_run_dir / condition)
            write_text(condition_dir / "prompt.txt", prompt)
            output_path = condition_dir / "output.txt"
            metadata_path = condition_dir / "call_metadata.json"
            if resume_outputs and output_path.exists() and output_path.read_text(encoding="utf-8").strip() and metadata_path.exists():
                try:
                    if str(read_json(metadata_path).get("model")) == expected_model:
                        continue
                except Exception:
                    pass
            try:
                output_text, output_metadata = generate_nonempty_code(prompt, metadata_path, condition)
            except Exception as exc:
                write_json(condition_dir / "generation_error.json", {"error": str(exc), "condition": condition, "task_id": item["task_id"]})
                print(f"ERROR: LLM generation failed for {item['task_id']}/{condition}: {exc}")
                continue
            write_text(output_path, output_text)
            write_json(metadata_path, output_metadata)
            error_path = condition_dir / "generation_error.json"
            if error_path.exists():
                error_path.unlink()
        return item["task_id"]

    _results, errors = run_ordered(manifest, work, int(config.get("max_workers", 1)), bool(config.get("continue_on_error", True)))
    if errors:
        write_json(run_dir / "run_errors.json", errors)
    elif (run_dir / "run_errors.json").exists():
        (run_dir / "run_errors.json").unlink()
    print(f"Wrote ClassEval runs to {run_dir}")


if __name__ == "__main__":
    main()
