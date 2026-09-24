from __future__ import annotations

import argparse
import hashlib
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from common.paths import PROJECT_ROOT, ensure_dir, iter_json_or_jsonl, read_config, read_json, resolve_in_project, write_json
from common.providers import GenerationConfig, ModelClient
from common.run_utils import generation_kwargs, run_ordered, selected_items
from common.spl_adapter import SPLConfig, SPLGenerator
from common.spl_snapshot import build_snapshot_manifest, restore_sample_snapshot, snapshot_sample_assets
from common.token_utils import summary_control_metrics
from common.usage import UsageTotals, generation_metadata


def task_id(task: dict, index: int) -> str:
    return str(task.get("task_id") or task.get("id") or f"classeval_{index:04d}").replace("/", "_")


def scaffold_from_task(task: dict) -> dict:
    return {
        "import_statement": task.get("import_statement", ""),
        "class_name": task.get("class_name", ""),
        "class_constructor": task.get("class_constructor", ""),
        "fields": task.get("fields", ""),
    }


def minimal_scaffold_text(task: dict) -> str:
    parts = [
        str(task.get("import_statement", "") or "").strip(),
        str(task.get("class_constructor", "") or "").strip(),
        str(task.get("fields", "") or "").strip(),
    ]
    skeleton = str(task.get("skeleton", "") or "").strip()
    if skeleton:
        parts.append(skeleton)
    return "\n\n".join(part for part in parts if part)


def iter_tasks(dataset_path: Path):
    paths = [dataset_path] if dataset_path.is_file() else sorted(dataset_path.rglob("*"))
    for path in paths:
        if path.suffix.lower() not in {".json", ".jsonl"}:
            continue
        yield from iter_json_or_jsonl(path)


FREE_SUMMARY_PROTOCOL = "free_summary"


FREE_SUMMARY_PROMPT = """Summarize what the code does in ordinary natural language.

Rules:
- Describe behavior, inputs, outputs, and important method/class interactions.
- Do not copy large code spans.
- Do not infer requirements that are not present in the code.
- Do not write replacement code.
- Output only the summary text.

CODE:
{code}
"""

FREE_SUMMARY_PROMPT_SHA256 = hashlib.sha256(FREE_SUMMARY_PROMPT.encode("utf-8")).hexdigest()

STRUCTURED_SUMMARY_PROMPT = """You are generating an information-controlled structured natural-language baseline.

Task: describe the class with enough detail to reconstruct method behavior and method/field dependencies, but do not use SPL tags or SPL syntax.

Rules:
- Use ordinary natural language with stable section headings.
- Cover constructor behavior, fields, public methods, inputs, outputs, side effects, branches, exceptions, and inter-method calls when present.
- Do not copy large code spans.
- Do not invent behavior not supported by the code.
- Output only the structured description.

CODE:
{code}
"""


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", required=True)
    args = parser.parse_args()

    config = read_config(resolve_in_project(args.config))
    dataset_path = resolve_in_project(config["dataset_path"])
    if not dataset_path.exists():
        raise FileNotFoundError(
            f"ClassEval dataset path not found: {dataset_path}. Run experiments/download_resources.py or set dataset_path."
        )
    artifact_dir = ensure_dir(resolve_in_project(config["artifact_dir"]))
    snapshot_root = resolve_in_project(config["spl_snapshot_dir"]) if config.get("spl_snapshot_dir") else None
    spl_model = str(config.get("spl_model", "gpt-4o-2024-11-20"))
    summary_model = str(config.get("summary_model", config.get("model", "gpt-4o-2024-11-20")))
    conditions = set(config.get("conditions", []))
    need_free_summary = "free_summary" in conditions
    need_structured_summary = "structured_summary" in conditions
    resume_prepared = bool(config.get("resume_prepared", True))

    def metadata_matches(
        path: Path,
        model: str,
        protocol: str | None = None,
        prompt_sha256: str | None = None,
    ) -> bool:
        if not path.exists():
            return False
        try:
            metadata = read_json(path)
            return (
                str(metadata.get("model")) == model
                and (protocol is None or metadata.get("protocol") == protocol)
                and (prompt_sha256 is None or metadata.get("prompt_sha256") == prompt_sha256)
            )
        except Exception:
            return False

    def has_visible_text(path: Path) -> bool:
        if not path.exists():
            return False
        try:
            return bool(path.read_text(encoding="utf-8").strip())
        except Exception:
            return False

    def new_spl_generator() -> SPLGenerator:
        return SPLGenerator(
            SPLConfig(
                mode=config.get("spl_mode", "openai"),
                model=spl_model,
                max_output_tokens=int(config.get("spl_max_output_tokens", 2048)),
                api_key=config.get("api_key"),
                api_key_env=config.get("api_key_env", "OPENAI_API_KEY"),
                base_url=config.get("base_url"),
                raw_http=bool(config.get("openai_raw_http", config.get("raw_http", False))),
                timeout_seconds=int(config.get("openai_timeout_seconds", config.get("timeout_seconds", 180))),
                max_retries=int(config.get("max_retries", 3)),
                api_keys=list(config.get("api_keys") or []),
                max_per_key=int(config.get("max_per_key", 1)),
                api_key_pool_file=config.get("api_key_pool_file"),
                thinking=config.get("thinking"),
            )
        )

    def new_summary_client(max_output_tokens: int | None = None) -> ModelClient:
        summary_config = dict(config)
        summary_config["provider"] = config.get("summary_provider", config.get("provider", "openai"))
        if max_output_tokens is not None:
            summary_config["summary_max_output_tokens"] = max_output_tokens
        return ModelClient(
            GenerationConfig(
                **generation_kwargs(
                    summary_config,
                    model_key="summary_model",
                    max_tokens_key="summary_max_output_tokens",
                    thinking_key="summary_thinking",
                )
            )
        )

    def summary_attempts_from_metadata(path: Path) -> list[dict]:
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

    def generate_nonempty_summary(
        prompt: str,
        metadata_path: Path,
        *,
        role: str,
        condition: str,
        protocol: str | None = None,
        prompt_sha256: str | None = None,
    ) -> tuple[str, dict]:
        attempts = summary_attempts_from_metadata(metadata_path)
        base_tokens = int(config.get("summary_max_output_tokens", 1024))
        retry_count = max(1, int(config.get("summary_empty_max_attempts", 3)))
        for retry_index in range(retry_count):
            max_tokens = base_tokens * (2**retry_index)
            result = new_summary_client(max_tokens).generate_with_metrics(prompt)
            attempt = generation_metadata(result, role=role, condition=condition)
            attempt["max_output_tokens"] = max_tokens
            attempt["empty_visible_text"] = not bool((result.text or "").strip())
            attempts.append(attempt)
            text = (result.text or "").strip()
            if text:
                totals = UsageTotals()
                for row in attempts:
                    totals.add(row)
                metadata = generation_metadata(result, role=role, condition=condition)
                metadata.update(totals.to_dict())
                metadata["attempts"] = attempts
                metadata["empty_retries"] = sum(bool(row.get("empty_visible_text")) for row in attempts)
                metadata["successful_max_output_tokens"] = max_tokens
                if protocol:
                    metadata["protocol"] = protocol
                if prompt_sha256:
                    metadata["prompt_sha256"] = prompt_sha256
                return text, metadata
            totals = UsageTotals()
            for row in attempts:
                totals.add(row)
            write_json(
                metadata_path,
                {
                    **attempt,
                    **totals.to_dict(),
                    "attempts": attempts,
                    "empty_retries": len(attempts),
                    "status": "empty_visible_text",
                },
            )
        raise RuntimeError(
            f"{condition} generation returned empty visible text after {retry_count} retries "
            f"with {summary_model}"
        )
    all_tasks = []
    for index, task in enumerate(iter_tasks(dataset_path)):
        code = task.get("solution_code")
        if not code:
            continue
        all_tasks.append({"index": index, "task": task})

    selected = selected_items(all_tasks, config)

    def prepare_entry(entry: dict) -> dict:
        index = int(entry["index"])
        task = entry["task"]
        code = task.get("solution_code")
        sample_id = task_id(task, index)
        sample_dir = ensure_dir(artifact_dir / sample_id)
        (sample_dir / "raw_code.py").write_text(code, encoding="utf-8")
        (sample_dir / "raw_solution.py").write_text(code, encoding="utf-8")
        (sample_dir / "skeleton.txt").write_text(str(task.get("skeleton", "")), encoding="utf-8")
        (sample_dir / "minimal_scaffold.txt").write_text(minimal_scaffold_text(task), encoding="utf-8")
        (sample_dir / "class_test.py").write_text(task.get("test", ""), encoding="utf-8")
        write_json(sample_dir / "task.json", task)
        write_json(sample_dir / "scaffold.json", scaffold_from_task(task))
        write_json(
            sample_dir / "metadata.json",
            {
                "task_id": sample_id,
                "class_name": task.get("class_name", ""),
                "method_count": len(task.get("methods_info", []) or []),
                "dependency_types": sorted(
                    {
                        str(dep)
                        for method in task.get("methods_info", []) or []
                        for dep in (method.get("dependencies", []) if isinstance(method.get("dependencies", []), list) else [method.get("dependencies", "")])
                        if dep
                    }
                ),
                "original_solution_path": str((sample_dir / "raw_solution.py").relative_to(PROJECT_ROOT)),
            },
        )
        restored = bool(
            snapshot_root
            and config.get("reuse_spl_snapshot", True)
            and restore_sample_snapshot(snapshot_root, sample_id, sample_dir)
        )
        spl_ready = (
            resume_prepared
            and (sample_dir / "spl.txt").exists()
            and (sample_dir / "spl.txt").stat().st_size > 0
            and (sample_dir / "spl_by_method.json").exists()
            and metadata_matches(sample_dir / "spl_metadata.json", spl_model)
        )
        if restored and not metadata_matches(sample_dir / "spl_metadata.json", spl_model):
            restored = False
        if restored or spl_ready:
            spl_text = (sample_dir / "spl.txt").read_text(encoding="utf-8")
            spl_by_method = read_json(sample_dir / "spl_by_method.json")
        else:
            spl = new_spl_generator()
            spl_result, spl_by_method = spl.generate_for_code_with_metrics_and_map(code, "python", sample_id)
            spl_text = spl_result.text
            (sample_dir / "spl.txt").write_text(spl_text, encoding="utf-8")
            write_json(sample_dir / "spl_metadata.json", spl_result.metadata)
            write_json(sample_dir / "spl_by_method.json", spl_by_method)
            if snapshot_root:
                snapshot_sample_assets(
                    sample_dir,
                    snapshot_root,
                    sample_id,
                    ["raw_code.py", "spl.txt", "spl_metadata.json", "spl_by_method.json"],
                    provenance={"experiment": "Exp01", "dataset": "ClassEval"},
                )
        free_summary = ""
        structured_summary = ""
        if need_free_summary:
            summary_ready = (
                resume_prepared
                and has_visible_text(sample_dir / "free_summary.txt")
                and metadata_matches(
                    sample_dir / "free_summary_metadata.json",
                    summary_model,
                    FREE_SUMMARY_PROTOCOL,
                    FREE_SUMMARY_PROMPT_SHA256,
                )
            )
            if summary_ready:
                free_summary = (sample_dir / "free_summary.txt").read_text(encoding="utf-8").strip()
            else:
                summary_prompt = FREE_SUMMARY_PROMPT.format(code=code)
                free_summary, summary_metadata = generate_nonempty_summary(
                    summary_prompt,
                    sample_dir / "free_summary_metadata.json",
                    role="free_summary_generation",
                    condition="free_summary",
                    protocol=FREE_SUMMARY_PROTOCOL,
                    prompt_sha256=FREE_SUMMARY_PROMPT_SHA256,
                )
                (sample_dir / "free_summary_prompt.txt").write_text(summary_prompt, encoding="utf-8")
                (sample_dir / "free_summary.txt").write_text(free_summary + "\n", encoding="utf-8")
                write_json(sample_dir / "free_summary_metadata.json", summary_metadata)
        if need_structured_summary:
            structured_ready = (
                resume_prepared
                and has_visible_text(sample_dir / "structured_summary.txt")
                and metadata_matches(sample_dir / "structured_summary_metadata.json", summary_model)
            )
            if structured_ready:
                structured_summary = (sample_dir / "structured_summary.txt").read_text(encoding="utf-8").strip()
            else:
                structured_prompt = STRUCTURED_SUMMARY_PROMPT.format(code=code)
                structured_summary, structured_metadata = generate_nonempty_summary(
                    structured_prompt,
                    sample_dir / "structured_summary_metadata.json",
                    role="structured_summary_generation",
                    condition="structured_summary",
                )
                (sample_dir / "structured_summary_prompt.txt").write_text(structured_prompt, encoding="utf-8")
                (sample_dir / "structured_summary.txt").write_text(structured_summary + "\n", encoding="utf-8")
                write_json(sample_dir / "structured_summary_metadata.json", structured_metadata)
        write_json(sample_dir / "summary_control_metrics.json", summary_control_metrics(code, spl_text, free_summary, structured_summary, "", config))
        pending = sample_dir / ".summary_pending.json"
        if pending.exists():
            pending.unlink()
        return {"index": index, "task_id": sample_id, "sample_dir": str(sample_dir.relative_to(PROJECT_ROOT))}

    prepared, errors = run_ordered(
        selected,
        prepare_entry,
        int(config.get("prepare_max_workers", config.get("max_workers", 1))),
        bool(config.get("continue_on_error", True)),
    )
    if errors:
        write_json(artifact_dir / "prepare_errors.json", errors)
    elif (artifact_dir / "prepare_errors.json").exists():
        (artifact_dir / "prepare_errors.json").unlink()

    write_json(artifact_dir / "manifest.json", prepared)
    if snapshot_root:
        build_snapshot_manifest(
            snapshot_root,
            metadata={"experiment": "Exp01", "dataset": "ClassEval"},
        )
    print(f"Prepared {len(prepared)}/{len(selected)} ClassEval samples at {artifact_dir}")


if __name__ == "__main__":
    main()
