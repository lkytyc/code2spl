from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from common.code_utils import has_multifunction_signal
from common.paths import PROJECT_ROOT, ensure_dir, iter_json_or_jsonl, read_config, read_json, resolve_in_project, write_json
from common.providers import GenerationConfig, ModelClient
from common.run_utils import selected_items
from common.run_utils import generation_kwargs
from common.spl_adapter import SPLConfig, SPLGenerator
from common.spl_binding import (
    bind_spl_to_source,
    normalize_numbered_source,
    python2_compatibility_source,
    source_for_named_owner,
)
from common.spl_snapshot import build_snapshot_manifest, restore_sample_snapshot, snapshot_sample_assets
from common.token_utils import compress_code_to_token_budget, summary_control_metrics, token_count
from common.usage import generation_metadata


SUMMARY_PROMPT = """You are performing code summarization following the CodeXGLUE/CodeSearchNet code-to-text task style.
Given the source code, generate a concise natural-language summary of what the code does.
Do not use structured tags, XML, JSON, YAML, tables, or SPL-like fields.
Do not list every line mechanically.
Do not infer behavior that is not supported by the code.
Return only the summary.

CODE:
{code}
"""

STRUCTURED_SUMMARY_PROMPT = """You are generating an information-controlled structured natural-language baseline.

Task: describe the code with enough detail to answer static analysis questions, but do not use SPL tags or SPL syntax.

Rules:
- Use ordinary natural language with stable section headings.
- Cover inputs, outputs, control flow branches, loops, function calls, and data dependencies when present.
- Do not copy large code spans.
- Do not invent behavior not supported by the code.
- Output only the structured description.

CODE:
{code}
"""


def build_spl_config(config: dict) -> SPLConfig:
    """Route SPL construction independently from task inference.

    The unprefixed keys remain backward compatible. New experiments can use
    ``spl_*`` transport and credential keys without changing the inference
    model, endpoint, or key pool.
    """
    return SPLConfig(
        mode=config.get("spl_mode", "openai"),
        model=config.get("spl_model", "gpt-4o-2024-11-20"),
        max_output_tokens=int(config.get("spl_max_output_tokens", 2048)),
        api_key=config.get("spl_api_key", config.get("api_key")),
        api_key_env=config.get(
            "spl_api_key_env", config.get("api_key_env", "OPENAI_API_KEY")
        ),
        base_url=config.get("spl_base_url", config.get("base_url")),
        raw_http=bool(config.get(
            "spl_openai_raw_http",
            config.get("openai_raw_http", config.get("raw_http", False)),
        )),
        timeout_seconds=int(config.get(
            "spl_timeout_seconds",
            config.get("openai_timeout_seconds", config.get("timeout_seconds", 180)),
        )),
        max_retries=int(config.get("spl_max_retries", config.get("max_retries", 3))),
        api_keys=list(config.get("spl_api_keys", config.get("api_keys", [])) or []),
        max_per_key=int(config.get("spl_max_per_key", config.get("max_per_key", 1))),
        api_key_pool_file=config.get(
            "spl_api_key_pool_file", config.get("api_key_pool_file")
        ),
        thinking=config.get("spl_thinking"),
    )


def collect_lite_ids(lite_data: object) -> set[str]:
    ids: set[str] = set()
    if isinstance(lite_data, str):
        ids.add(lite_data)
    elif isinstance(lite_data, list):
        for item in lite_data:
            ids.update(collect_lite_ids(item))
    elif isinstance(lite_data, dict):
        for value in lite_data.values():
            ids.update(collect_lite_ids(value))
    return ids


def iter_jsonl(path: Path):
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.strip():
            yield json.loads(line)


def extract_last_code_block(prompt: str) -> str:
    blocks = re.findall(r"```(?:[A-Za-z+#]*)\s*\n(.*?)```", prompt, flags=re.DOTALL)
    return blocks[-1].strip() if blocks else ""


def extract_question(prompt: str) -> str:
    marker = "**Question**:"
    if marker in prompt:
        return prompt.split(marker, 1)[1].strip()
    print("WARNING: **Question** marker not found in official prompt, using last 2000 chars as fallback.")
    return prompt[-2000:]


def guess_language(item: dict, code: str) -> str:
    lang = str(item.get("language") or item.get("lang") or item.get("_language") or "").lower()
    if lang in {"python", "java", "cpp"}:
        return lang
    if lang in {"c", "c++", "cc"}:
        return "cpp"
    if "public class " in code or "private " in code:
        return "java"
    if "#include" in code or "::" in code:
        return "cpp"
    return "python"


def iter_core_prompt_items(repo_root: Path, lite_path: Path):
    lite_ids = collect_lite_ids(json.loads(lite_path.read_text(encoding="utf-8")))
    prompt_dir = repo_root / "prompts"
    for prompt_file in sorted(prompt_dir.glob("*.jsonl")):
        stem = prompt_file.stem
        parts = stem.split("_")
        task_type = parts[0] if parts else ""
        language = parts[1] if len(parts) > 2 else ""
        mode = parts[-1] if parts else ""
        for item in iter_jsonl(prompt_file):
            task_id = str(item.get("task_id", ""))
            if lite_ids and task_id not in lite_ids:
                continue
            item["_task_type"] = "infoflow" if task_type.startswith("infoflow") else task_type
            item["_language"] = language
            item["_mode"] = mode
            yield item


def load_prepared_input_candidates(seed_root: Path) -> list[dict]:
    """Load immutable task inputs from a frozen artifact bundle.

    This deliberately ignores every prior SPL/summary file. It exists so a
    compact reproduction bundle can rebuild representations without shipping
    the full upstream CoRe prompt corpus.
    """
    manifest_path = seed_root / "manifest.json"
    if not manifest_path.exists():
        raise FileNotFoundError(f"Frozen input manifest not found: {manifest_path}")
    candidates: list[dict] = []
    for position, manifest_item in enumerate(read_json(manifest_path)):
        task_id = str(manifest_item["task_id"])
        sample_dir = seed_root / task_id
        required = [
            "raw_code.txt", "official_prompt.txt", "question.txt", "item.json", "gold.txt",
        ]
        missing = [name for name in required if not (sample_dir / name).exists()]
        if missing:
            raise FileNotFoundError(
                f"Frozen input bundle is incomplete for {task_id}: {missing}"
            )
        item = read_json(sample_dir / "item.json")
        benchmark_task_id = str(
            manifest_item.get("benchmark_task_id")
            or item.get("task_id")
            or task_id.rsplit("__", 1)[0]
        )
        mode = str(manifest_item.get("mode") or item.get("_mode") or item.get("category") or "")
        item["_mode"] = mode
        item.setdefault("_task_type", manifest_item.get("task_type", ""))
        item.setdefault("_language", manifest_item.get("language", ""))
        candidates.append({
            "task_id": task_id,
            "benchmark_task_id": benchmark_task_id,
            "sample_key": str(
                manifest_item.get("sample_key") or f"{benchmark_task_id.replace('/', '_')}::{mode}"
            ),
            "index": int(manifest_item.get("index", position)),
            "item": item,
            "code": (sample_dir / "raw_code.txt").read_text(encoding="utf-8"),
            "official_prompt": (sample_dir / "official_prompt.txt").read_text(encoding="utf-8"),
            "frozen_question": (sample_dir / "question.txt").read_text(encoding="utf-8"),
            "frozen_gold": (sample_dir / "gold.txt").read_text(encoding="utf-8"),
            "input_seed_dir": str(sample_dir),
        })
    return candidates


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", required=True)
    args = parser.parse_args()

    config = read_config(resolve_in_project(args.config))
    dataset_path = resolve_in_project(config["dataset_path"])
    if not dataset_path.exists():
        repo_root = resolve_in_project("datasets/core/repo")
        matches = list(repo_root.rglob("lite.json")) if repo_root.exists() else []
        if matches:
            dataset_path = matches[0]
        else:
            raise FileNotFoundError(
                f"CoRe dataset file not found: {dataset_path}. Run experiments/download_resources.py or set dataset_path."
            )
    artifact_dir = ensure_dir(resolve_in_project(config["artifact_dir"]))
    snapshot_root = resolve_in_project(config["spl_snapshot_dir"]) if config.get("spl_snapshot_dir") else None
    seed_snapshot_roots = [
        resolve_in_project(path)
        for path in config.get("spl_seed_snapshot_dirs", [])
    ]
    spl = SPLGenerator(build_spl_config(config))
    generate_summaries = bool(config.get("generate_summaries", True))
    summary_client = None
    if generate_summaries:
        summary_config = dict(config)
        summary_config["provider"] = config.get("summary_provider", config.get("provider", "openai"))
        summary_client = ModelClient(
            GenerationConfig(
                **generation_kwargs(
                    summary_config,
                    model_key="summary_model",
                    max_tokens_key="summary_max_output_tokens",
                )
            )
        )
    manifest = []

    input_seed_dir = config.get("prepared_input_seed_dir")
    if input_seed_dir:
        candidates = load_prepared_input_candidates(resolve_in_project(input_seed_dir))
    else:
        repo_root = dataset_path.parent if dataset_path.name == "lite.json" else resolve_in_project("datasets/core/repo")
        source_iter = iter_core_prompt_items(repo_root, dataset_path) if dataset_path.name == "lite.json" else iter_json_or_jsonl(dataset_path)

        candidates = []
        for index, item in enumerate(source_iter):
            official_prompt = str(item.get("prompt", ""))
            code = extract_last_code_block(official_prompt) or str(item.get("code", ""))
            if not code or not has_multifunction_signal(code):
                continue
            benchmark_task_id = str(item.get("id") or item.get("task_id") or f"core_{index:05d}")
            mode = str(item.get("_mode", item.get("category", "")))
            sample_id = f"{benchmark_task_id.replace('/', '_')}__{mode}"
            candidates.append({
                "task_id": sample_id,
                "benchmark_task_id": benchmark_task_id,
                "sample_key": f"{benchmark_task_id.replace('/', '_')}::{mode}",
                "index": index,
                "item": item,
                "code": code,
                "official_prompt": official_prompt,
            })

    for entry in selected_items(candidates, config):
        index = int(entry["index"])
        item = entry["item"]
        code = entry["code"]
        official_prompt = entry["official_prompt"]
        benchmark_task_id = str(entry["benchmark_task_id"])
        mode = str(item.get("_mode", item.get("category", "")))
        sample_key = str(entry["sample_key"])
        sample_id = str(entry["task_id"])
        language = guess_language(item, code)
        sample_dir = ensure_dir(artifact_dir / sample_id)
        (sample_dir / "raw_code.txt").write_text(code, encoding="utf-8")
        (sample_dir / "official_prompt.txt").write_text(official_prompt, encoding="utf-8")
        (sample_dir / "question.txt").write_text(
            str(entry.get("frozen_question") or extract_question(official_prompt)), encoding="utf-8"
        )
        frozen_gold = entry.get("frozen_gold")
        (sample_dir / "gold.txt").write_text(
            str(frozen_gold) if frozen_gold is not None
            else json.dumps(item.get("groundtruth", item.get("label", "")), ensure_ascii=False),
            encoding="utf-8",
        )
        write_json(sample_dir / "item.json", item)
        summary_result = None
        structured_summary = ""
        summary_complete = bool(
            (sample_dir / "free_summary.txt").exists()
            and (sample_dir / "structured_summary_metadata.json").exists()
        )
        if summary_client is not None and not summary_complete:
            summary_prompt = SUMMARY_PROMPT.format(code=code)
            summary_result = summary_client.generate_with_metrics(summary_prompt)
            (sample_dir / "free_summary_prompt.txt").write_text(summary_prompt, encoding="utf-8")
            (sample_dir / "free_summary.txt").write_text((summary_result.text or "").strip() + "\n", encoding="utf-8")
            write_json(sample_dir / "free_summary_metadata.json", generation_metadata(summary_result, role="core_free_summary_generation", condition="raw_free_summary"))
            # Generate structured summary only when a compared condition needs it.
            structured_prompt = STRUCTURED_SUMMARY_PROMPT.format(code=code)
            structured_result = summary_client.generate_with_metrics(structured_prompt)
            structured_summary = (structured_result.text or "").strip()
            (sample_dir / "structured_summary_prompt.txt").write_text(structured_prompt, encoding="utf-8")
            (sample_dir / "structured_summary.txt").write_text(structured_summary + "\n", encoding="utf-8")
            write_json(sample_dir / "structured_summary_metadata.json", generation_metadata(structured_result, role="core_structured_summary_generation", condition="structured_summary"))
        restored_from = None
        restored = bool(
            snapshot_root
            and config.get("reuse_spl_snapshot", True)
            and restore_sample_snapshot(snapshot_root, sample_id, sample_dir)
        )
        if restored:
            restored_from = snapshot_root
        if not restored and config.get("reuse_spl_snapshot", True):
            for seed_root in seed_snapshot_roots:
                try:
                    if restore_sample_snapshot(seed_root, sample_id, sample_dir):
                        restored = True
                        restored_from = seed_root
                        break
                except (FileExistsError, FileNotFoundError, ValueError) as exc:
                    print(f"WARNING: rejected seed SPL snapshot {seed_root}: {exc}")
        if restored:
            spl_text = (sample_dir / "spl.txt").read_text(encoding="utf-8")
            spl_by_method = read_json(sample_dir / "spl_by_method.json")
            _bound, _provenance, restored_binding = bind_spl_to_source(
                code, spl_by_method, language,
            )
            restored = bool(_bound)
            if restored and snapshot_root and restored_from != snapshot_root:
                snapshot_sample_assets(
                    sample_dir,
                    snapshot_root,
                    sample_id,
                    [
                        "raw_code.txt", "spl.txt", "spl_metadata.json",
                        "spl_by_method.json", "spl_regeneration_audit.json",
                    ],
                    provenance={
                        "experiment": "Exp02",
                        "dataset": "CoRe",
                        "reused_from_snapshot": str(restored_from),
                    },
                )
        if not restored:
            target_owner = str(item.get("funname") or "")
            owner_source, owner_audit = source_for_named_owner(
                code,
                language,
                target_owner,
                source_start_line=item.get("start"),
                source_end_line=item.get("end"),
            ) if target_owner else ("", {})
            normalized_source, _line_map, numbered = normalize_numbered_source(code)
            generation_source = owner_source or normalized_source
            compatibility_audit = {"applied": False, "reason": "not_needed"}
            if language == "python":
                generation_source, compatibility_audit = python2_compatibility_source(
                    generation_source,
                )
            spl_result, spl_by_method = spl.generate_for_code_with_metrics_and_map(
                generation_source, language, sample_id,
            )
            spl_text = spl_result.text
            (sample_dir / "spl.txt").write_text(spl_text, encoding="utf-8")
            write_json(sample_dir / "spl_metadata.json", spl_result.metadata)
            write_json(sample_dir / "spl_by_method.json", spl_by_method)
            write_json(sample_dir / "spl_regeneration_audit.json", {
                "reason": "missing_or_unbound_snapshot" if snapshot_root else "initial_build",
                "target_owner": target_owner or None,
                "target_owner_only": bool(owner_source),
                "numbered_source_normalized": numbered,
                "owner_audit": owner_audit,
                "compatibility_audit": compatibility_audit,
            })
            if snapshot_root:
                snapshot_sample_assets(
                    sample_dir,
                    snapshot_root,
                    sample_id,
                    [
                        "raw_code.txt", "spl.txt", "spl_metadata.json",
                        "spl_by_method.json", "spl_regeneration_audit.json",
                    ],
                    provenance={"experiment": "Exp02", "dataset": "CoRe"},
                )
        bound_spl, _source_provenance, binding_audit = bind_spl_to_source(
            code, spl_by_method, language,
        )
        write_json(sample_dir / "spl_source_binding.json", binding_audit)
        if not bound_spl:
            print(
                f"WARNING: no source-bound SPL owner for {sample_id}; "
                "SPL conditions will use their declared baseline fallback."
            )
        compressed_raw = compress_code_to_token_budget(code, token_count(spl_text))
        if compressed_raw.strip() == code.strip():
            print(f"WARNING: compressed_raw equals full raw code for {sample_id}. SPL may be as large or larger than the original code.")
        (sample_dir / "compressed_raw.txt").write_text(compressed_raw, encoding="utf-8")
        if summary_result is not None:
            write_json(sample_dir / "summary_control_metrics.json", summary_control_metrics(code, spl_text, summary_result.text.strip(), structured_summary, compressed_raw, config))
        manifest.append(
            {
                "task_id": sample_id,
                "benchmark_task_id": benchmark_task_id,
                "sample_key": sample_key,
                "index": index,
                "language": language,
                "task_type": item.get("_task_type", ""),
                "mode": mode,
                "has_internal_call_chain": True,
                "sample_dir": str(sample_dir.relative_to(PROJECT_ROOT)),
            }
        )

    write_json(artifact_dir / "manifest.json", manifest)
    if snapshot_root:
        build_snapshot_manifest(
            snapshot_root,
            metadata={"experiment": "Exp02", "dataset": "CoRe"},
        )
    print(f"Prepared {len(manifest)} CoRe multi-function samples at {artifact_dir}")


if __name__ == "__main__":
    main()
