from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from common.paths import PROJECT_ROOT, ensure_dir, read_json, resolve_in_project, write_json, write_text

from prepare import extract_last_code_block, extract_question, guess_language, iter_core_prompt_items


def _sha256_ids(ids: list[str]) -> str:
    payload = "\n".join(ids).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Freeze only the pre-registered CoRe sample inputs into the paper bundle."
    )
    parser.add_argument("--sample-file", required=True)
    parser.add_argument("--source-repo", required=True)
    parser.add_argument("--output-dir", required=True)
    args = parser.parse_args()

    sample_path = resolve_in_project(args.sample_file)
    sample_spec = read_json(sample_path)
    selected_ids = list(sample_spec.get("execution_order_ids") or sample_spec["sample_ids"])
    selected_set = set(selected_ids)
    if len(selected_set) != len(selected_ids):
        raise ValueError("Frozen sample file contains duplicate IDs")

    source_repo = Path(args.source_repo).resolve()
    workspace_root = PROJECT_ROOT.parent.resolve()
    if source_repo != workspace_root and workspace_root not in source_repo.parents:
        raise ValueError(f"Source repo must remain under the experiment workspace: {source_repo}")
    lite_path = source_repo / "lite.json"
    if not lite_path.exists() or not (source_repo / "prompts").exists():
        raise FileNotFoundError(f"Incomplete CoRe source repository: {source_repo}")

    candidates: dict[str, dict] = {}
    for index, item in enumerate(iter_core_prompt_items(source_repo, lite_path)):
        official_prompt = str(item.get("prompt", ""))
        code = extract_last_code_block(official_prompt) or str(item.get("code", ""))
        benchmark_task_id = str(item.get("id") or item.get("task_id") or f"core_{index:05d}")
        mode = str(item.get("_mode", item.get("category", "")))
        sample_key = f"{benchmark_task_id.replace('/', '_')}::{mode}"
        if sample_key in selected_set:
            candidates[sample_key] = {
                "index": index,
                "item": item,
                "code": code,
                "official_prompt": official_prompt,
                "benchmark_task_id": benchmark_task_id,
                "mode": mode,
            }

    missing = [sample_id for sample_id in selected_ids if sample_id not in candidates]
    if missing:
        raise ValueError(f"Selected CoRe IDs missing from official prompts: {missing[:10]}")

    output_dir = ensure_dir(resolve_in_project(args.output_dir))
    manifest: list[dict] = []
    for position, sample_key in enumerate(selected_ids):
        entry = candidates[sample_key]
        item = entry["item"]
        benchmark_task_id = entry["benchmark_task_id"]
        mode = entry["mode"]
        task_id = f"{benchmark_task_id.replace('/', '_')}__{mode}"
        sample_dir = ensure_dir(output_dir / task_id)
        code = entry["code"]
        write_text(sample_dir / "raw_code.txt", code)
        write_text(sample_dir / "official_prompt.txt", entry["official_prompt"])
        write_text(sample_dir / "question.txt", extract_question(entry["official_prompt"]))
        write_text(
            sample_dir / "gold.txt",
            json.dumps(item.get("groundtruth", item.get("label", "")), ensure_ascii=False),
        )
        write_json(sample_dir / "item.json", item)
        manifest.append(
            {
                "task_id": task_id,
                "benchmark_task_id": benchmark_task_id,
                "sample_key": sample_key,
                "mode": mode,
                "task_type": item.get("_task_type", ""),
                "language": guess_language(item, code),
                "index": int(entry["index"]),
                "execution_position": position,
                "sample_dir": str(sample_dir.relative_to(PROJECT_ROOT)),
            }
        )

    write_json(output_dir / "manifest.json", manifest)
    write_json(
        output_dir / "INPUT_BUNDLE_METADATA.json",
        {
            "experiment": "Exp02 CoRe multi-function reasoning",
            "source_population": int(sample_spec.get("N_total", 0)),
            "sample_size": len(selected_ids),
            "seed": sample_spec.get("seed"),
            "stratification": sample_spec.get("stratification"),
            "sampling_formula": sample_spec.get("params", {}).get("formula"),
            "selection_order": "execution_order_ids",
            "ordered_ids_sha256": _sha256_ids(selected_ids),
            "sample_file": str(sample_path.relative_to(PROJECT_ROOT)),
            "upstream_source_repo": str(source_repo),
            "contains_spl": False,
            "contains_model_outputs": False,
        },
    )
    print(f"Frozen {len(manifest)} sampled CoRe inputs at {output_dir}")


if __name__ == "__main__":
    main()
