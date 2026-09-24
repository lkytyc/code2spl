from __future__ import annotations

import argparse
import json
import re
import string
import subprocess
import sys
from pathlib import Path
from typing import Any

from common.method_project import build_method_config
from common.paths import PROJECT_ROOT, ensure_dir, read_config, read_json, resolve_in_project, write_json, write_text
from common.prompt_store import central_prompt_path
from common.providers import GenerationConfig, ModelClient
from common.run_utils import generation_kwargs, run_ordered, selected_items
from common.spl_adapter import format_inline_spl_cards_generic
from common.usage import write_generation_result


# ── per-experiment field allowlists ──────────────────────────────────────
# Each condition may only reference the fields listed here.  The renderer
# parses the prompt template with string.Formatter and raises ValueError if
# a template uses a field outside this set.  This prevents accidental SPL
# (or other representation) leakage into a baseline that must not see it.

ALLOWED_PROMPT_FIELDS: dict[int, dict[str, set[str]]] = {
    1: {
        "skeleton_holistic": {"skeleton", "class_name"},
        "skeleton_incremental": {"skeleton", "methods_info"},
        "spl_only": {"spl_inline"},
        "free_summary": {"summary"},
        "structured_summary": {"structured_summary"},
        "spl_scaffold": {"spl_inline", "scaffold"},
        "skeleton_spl": {"skeleton", "spl_inline"},
    },
    2: {
        "official_raw": {"official_prompt"},
        "compressed_raw": {"task_prompt", "compressed_raw"},
        "nl_summary": {"task_prompt", "summary"},
        "raw_free_summary": {"official_prompt", "summary"},
        "structured_summary": {"task_prompt", "structured_summary"},
        "raw_structured_summary": {"official_prompt", "structured_summary"},
        "spl_only": {"task_prompt", "spl_inline"},
        "raw_spl": {"official_prompt", "spl_inline"},
    },
    3: {
        "gzoltar_ochiai": set(),
        "autofl_original": {
            "covered_classes",
            "method_index",
            "trigger_tests",
            "failing_trace",
            "max_inspect",
            "inspected_cards",
            "candidate_methods",
        },
        "autofl_spl": {
            "covered_classes",
            "method_index",
            "trigger_tests",
            "failing_trace",
            "max_inspect",
            "inspected_cards",
            "candidate_methods",
            "failure_keywords",
        },
        "gpt_raw": {"raw", "candidates", "trigger_tests", "relevant_tests"},
        "gpt_raw_spl": {"trigger_tests", "relevant_tests", "spl_descriptions", "failure_keywords"},
    },
}


def read_text_if_exists(path: Path, default: str = "") -> str:
    return path.read_text(encoding="utf-8") if path.exists() else default


def strip_target_code_block(official_prompt: str) -> str:
    """Keep task/question text while removing the target program from CoRe prompts."""
    matches = list(re.finditer(r"```[^\n]*\n.*?```", official_prompt, flags=re.DOTALL))
    if not matches:
        return official_prompt
    last = matches[-1]
    return (
        official_prompt[: last.start()]
        + "[PROGRAM REPRESENTATION IS PROVIDED BY THIS EXPERIMENT CONDITION BELOW]\n"
        + official_prompt[last.end() :]
    ).strip()


def render_template(
    template: str,
    values: dict[str, Any],
    *,
    condition: str | None = None,
    experiment_id: int | None = None,
) -> str:
    """Render a prompt template with field-allowlist enforcement.

    When *condition* and *experiment_id* are both provided the renderer
    parses the template, finds every ``{field_name}`` placeholder, and
    verifies that each one is listed in ``ALLOWED_PROMPT_FIELDS`` for that
    experiment + condition.  This is the same guard used by the
    experiment-level ``run.py`` scripts.
    """
    if condition is not None and experiment_id is not None:
        table = ALLOWED_PROMPT_FIELDS.get(experiment_id, {})
        allowed = table.get(condition)
        if allowed is not None:
            used = {name for _, name, _, _ in string.Formatter().parse(template) if name}
            disallowed = sorted(used - allowed)
            if disallowed:
                raise ValueError(
                    f"Prompt for condition '{condition}' (experiment {experiment_id}) "
                    f"uses disallowed fields {disallowed}. "
                    f"Allowed fields are {sorted(allowed)}."
                )
    # Render with all values, substituting empty string for None.
    return template.format(
        **{key: "" if value is None else value for key, value in values.items()}
    )


def load_classeval_values(sample_dir: Path) -> dict[str, Any]:
    task = read_json(sample_dir / "task.json")
    spl = read_text_if_exists(sample_dir / "spl.txt")
    spl_by_method_path = sample_dir / "spl_by_method.json"
    spl_by_method = read_json(spl_by_method_path) if spl_by_method_path.exists() else {}
    spl_inline = format_inline_spl_cards_generic("", spl_by_method, "python", include_source=False) if spl_by_method else spl
    return {
        "spl": spl,
        "spl_inline": spl_inline,
        "summary": read_text_if_exists(sample_dir / "free_summary.txt"),
        "structured_summary": read_text_if_exists(sample_dir / "structured_summary.txt"),
        "scaffold": read_text_if_exists(sample_dir / "scaffold.json"),
        "skeleton": read_text_if_exists(sample_dir / "skeleton.txt"),
        "methods_info": json.dumps(task.get("methods_info", []), ensure_ascii=False, indent=2),
        "class_name": task.get("class_name", ""),
    }


def load_core_values(sample_dir: Path) -> dict[str, Any]:
    raw = read_text_if_exists(sample_dir / "raw_code.txt")
    question = read_text_if_exists(sample_dir / "question.txt")
    official_prompt = read_text_if_exists(
        sample_dir / "official_prompt.txt",
        f"Given the program and question, answer using the required CoRe label format only.\n\nPROGRAM:\n{raw}\n\nQUESTION:\n{question}",
    )
    spl = read_text_if_exists(sample_dir / "spl.txt")
    spl_by_method_path = sample_dir / "spl_by_method.json"
    spl_by_method = read_json(spl_by_method_path) if spl_by_method_path.exists() else {}
    spl_inline = format_inline_spl_cards_generic("", spl_by_method, "python", include_source=False) if spl_by_method else spl
    return {
        "raw": raw,
        "compressed_raw": read_text_if_exists(sample_dir / "compressed_raw.txt", raw),
        "spl": spl,
        "spl_inline": spl_inline,
        "summary": read_text_if_exists(sample_dir / "free_summary.txt"),
        "structured_summary": read_text_if_exists(sample_dir / "structured_summary.txt"),
        "question": question,
        "official_prompt": official_prompt,
        "task_prompt": strip_target_code_block(official_prompt),
    }


def load_defects4j_values(sample_dir: Path) -> dict[str, Any]:
    test_context = read_json(sample_dir / "test_context.json")
    candidates = "\n".join(read_json(sample_dir / "candidate_methods.json"))
    return {
        "raw": read_text_if_exists(sample_dir / "raw_bundle.java"),
        "spl": read_text_if_exists(sample_dir / "spl_bundle.txt"),
        "candidates": candidates,
        "trigger_tests": "\n".join(test_context.get("live_failing_tests") or test_context.get("trigger_tests") or ["<none>"]),
        "relevant_tests": "\n".join(test_context.get("relevant_tests") or ["<none>"]),
    }


def sample_id(item: dict[str, Any], experiment_id: int) -> str:
    if experiment_id == 1:
        return str(item["task_id"])
    if experiment_id == 2:
        return str(item["task_id"])
    if experiment_id == 3:
        return str(item["bug_id"])
    return str(item.get("instance_id") or item.get("task_id") or item.get("id"))


def load_values(sample_dir: Path, experiment_id: int) -> dict[str, Any]:
    if experiment_id == 1:
        return load_classeval_values(sample_dir)
    if experiment_id == 2:
        return load_core_values(sample_dir)
    if experiment_id == 3:
        return load_defects4j_values(sample_dir)
    raise ValueError(f"Standalone LLM method runtime is not defined for experiment {experiment_id}.")


def run_non_llm_localization(method: dict[str, Any], item: dict[str, Any], sample_dir: Path, out_dir: Path) -> bool:
    condition = method.get("condition", method["method_name"])
    if condition != "gzoltar_ochiai":
        return False
    ranking = read_json(sample_dir / "gzoltar_method_ranking.json") if (sample_dir / "gzoltar_method_ranking.json").exists() else []
    status = read_json(sample_dir / "gzoltar_status.json") if (sample_dir / "gzoltar_status.json").exists() else {"available": False, "source": "missing_status"}
    preds = [row["method_id"] for row in ranking[:5] if row.get("method_id")]
    write_text(out_dir / "prompt.txt", "Non-LLM baseline: GZoltar/Ochiai method ranking loaded from artifact.")
    write_text(out_dir / "output.txt", json.dumps(preds, ensure_ascii=False))
    write_json(out_dir / "baseline_status.json", status)
    write_json(out_dir / "call_metadata.json", {"role": "gzoltar_ochiai", "condition": condition, "provider": "non_llm", "elapsed_seconds": 0.0, "llm_elapsed_seconds": 0.0, "input_tokens": None, "output_tokens": None, "reasoning_tokens": None, "total_tokens": None, "calls": 0, "raw_usage": status})
    return True


def run_method_llm(method_dir: Path, method: dict[str, Any], config: dict[str, Any]) -> None:
    experiment_id = int(method["experiment_id"])
    artifact_dir = resolve_in_project(config["artifact_dir"])
    run_dir = ensure_dir(resolve_in_project(config["run_dir"]))
    manifest = selected_items(read_json(artifact_dir / "manifest.json"), config)
    relative_prompt = Path(method.get("prompt_file", "prompts/prompt.md"))
    prompt_name = relative_prompt.name
    prompt_file = method_dir / relative_prompt
    try:
        method_name = method_dir.name
        experiment_name = method_dir.parent.parent.name
        central_file = central_prompt_path(experiment_name, method_name, prompt_name)
        if central_file.exists():
            prompt_file = central_file
    except IndexError:
        pass
    prompt_template = prompt_file.read_text(encoding="utf-8")
    client = ModelClient(GenerationConfig(**generation_kwargs(config, max_tokens_key="max_output_tokens")))
    condition = method.get("condition", method["method_name"])

    def work(item: dict[str, Any]) -> str:
        sample_dir = resolve_in_project(item["sample_dir"])
        out_dir = ensure_dir(run_dir / sample_id(item, experiment_id) / condition)
        if experiment_id == 3 and run_non_llm_localization(method, item, sample_dir, out_dir):
            return sample_id(item, experiment_id)
        values = load_values(sample_dir, experiment_id)
        prompt = render_template(prompt_template, values, condition=condition, experiment_id=experiment_id)
        write_text(out_dir / "prompt.txt", prompt)
        result = client.generate_with_metrics(prompt)
        role = str(method.get("role") or method.get("experiment_slug") or condition)
        write_generation_result(out_dir, result, role=role, condition=condition)
        return sample_id(item, experiment_id)

    _results, errors = run_ordered(manifest, work, int(config.get("max_workers", 1)), bool(config.get("continue_on_error", True)))
    if errors:
        write_json(run_dir / "run_errors.json", errors)
    print(f"Wrote standalone method '{method['method_name']}' runs to {run_dir}")


def main(method_dir: Path) -> None:
    parser = argparse.ArgumentParser(description="Run a complete standalone method project.")
    parser.add_argument("--phase", "--phases", default="run,evaluate", help="Comma-separated phases. Supported: run,evaluate.")
    parser.add_argument("--config", help="Override base config.")
    parser.add_argument("--run-dir", help="Override output run_dir.")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--continue-on-error", action="store_true")
    args = parser.parse_args()

    method = read_config(method_dir / "method.yaml")
    base_config_path = resolve_in_project(args.config) if args.config else None
    resolved_config = build_method_config(method_dir, method, base_config_path=base_config_path, run_dir=args.run_dir)
    config = read_config(resolved_config)
    phases = [part.strip() for part in args.phase.split(",") if part.strip()]

    for phase in phases:
        if phase == "run":
            if args.dry_run:
                print(f"[dry-run] would run standalone method {method['method_name']} with {resolved_config}")
            else:
                run_method_llm(method_dir, method, config)
            continue
        if phase == "evaluate":
            evaluator = method.get("engine", {}).get("evaluate")
            if not evaluator:
                print(f"No evaluator configured for {method['method_name']}; skipping.")
                continue
            command = [sys.executable, str(resolve_in_project(evaluator)), "--config", str(resolved_config)]
            print(f"[{method['method_name']}:evaluate] {' '.join(command)}")
            if args.dry_run:
                continue
            result = subprocess.run(command, cwd=str(PROJECT_ROOT))
            if result.returncode != 0 and not args.continue_on_error:
                raise SystemExit(result.returncode)
            continue
        raise ValueError(f"Unsupported phase for standalone method project: {phase}")
