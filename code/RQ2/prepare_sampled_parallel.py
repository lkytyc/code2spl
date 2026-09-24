from __future__ import annotations

import argparse
import copy
import json
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from common.paths import PROJECT_ROOT, ensure_dir, read_config, read_json, resolve_in_project, write_json
from common.spl_snapshot import (
    build_snapshot_manifest,
    sample_snapshot_dir,
    snapshot_sample_assets,
)


REQUIRED_SAMPLE_FILES = (
    "raw_code.txt",
    "official_prompt.txt",
    "question.txt",
    "gold.txt",
    "item.json",
    "spl.txt",
    "spl_metadata.json",
    "spl_by_method.json",
    "spl_source_binding.json",
)


def partition(values: list[str], count: int) -> list[list[str]]:
    shards = [[] for _ in range(max(1, min(count, len(values))))]
    for index, value in enumerate(values):
        shards[index % len(shards)].append(value)
    return [shard for shard in shards if shard]


def sample_complete(sample_dir: Path, expected_model: str) -> bool:
    if any(not (sample_dir / name).exists() for name in REQUIRED_SAMPLE_FILES):
        return False
    if not (sample_dir / "spl.txt").read_text(encoding="utf-8", errors="replace").strip():
        return False
    try:
        metadata = json.loads((sample_dir / "spl_metadata.json").read_text(encoding="utf-8"))
        method_map = json.loads((sample_dir / "spl_by_method.json").read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return False
    return metadata.get("model") == expected_model and bool(method_map)


def run_prepare(config_path: Path, log_path: Path) -> tuple[int, str]:
    command = [
        sys.executable,
        "-u",
        str(PROJECT_ROOT / "code" / "RQ2" / "prepare.py"),
        "--config",
        str(config_path.relative_to(PROJECT_ROOT)),
    ]
    with log_path.open("w", encoding="utf-8") as log:
        result = subprocess.run(
            command,
            cwd=str(PROJECT_ROOT),
            stdout=log,
            stderr=subprocess.STDOUT,
            text=True,
            encoding="utf-8",
            errors="replace",
        )
    return result.returncode, str(log_path)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Build sampled Exp02 SPL in bounded parallel shards and merge a strict manifest."
    )
    parser.add_argument("--config", required=True)
    parser.add_argument("--workers", type=int, default=12)
    parser.add_argument("--max-rounds", type=int, default=5)
    args = parser.parse_args()

    config_path = resolve_in_project(args.config)
    base_config = read_config(config_path)
    sample_spec = read_json(resolve_in_project(base_config["sample_ids_file"]))
    expected_ids = list(sample_spec.get("execution_order_ids") or sample_spec["sample_ids"])
    input_root = resolve_in_project(base_config["prepared_input_seed_dir"])
    input_manifest = read_json(input_root / "manifest.json")
    input_by_key = {str(row["sample_key"]): row for row in input_manifest}
    missing_inputs = [sample_id for sample_id in expected_ids if sample_id not in input_by_key]
    if missing_inputs:
        raise ValueError(f"Frozen input bundle is missing sampled IDs: {missing_inputs[:10]}")

    artifact_root = ensure_dir(resolve_in_project(base_config["artifact_dir"]))
    snapshot_root = ensure_dir(resolve_in_project(base_config["spl_snapshot_dir"]))
    control_root = ensure_dir(artifact_root.parent / "_parallel_prepare")
    expected_model = str(base_config["spl_model"])

    def incomplete_ids() -> list[str]:
        return [
            sample_id
            for sample_id in expected_ids
            if not sample_complete(artifact_root / str(input_by_key[sample_id]["task_id"]), expected_model)
        ]

    remaining = incomplete_ids()
    for round_index in range(1, args.max_rounds + 1):
        if not remaining:
            break
        shards = partition(remaining, args.workers)
        round_root = ensure_dir(control_root / f"round_{round_index:02d}")
        jobs: list[tuple[Path, Path]] = []
        for shard_index, shard_ids in enumerate(shards):
            sample_file = round_root / f"sample_ids_{shard_index:02d}.json"
            shard_config_path = round_root / f"config_{shard_index:02d}.json"
            log_path = round_root / f"prepare_{shard_index:02d}.log"
            write_json(
                sample_file,
                {
                    "experiment": "core_multifunction_parallel_prepare_shard",
                    "parent_sample_file": base_config["sample_ids_file"],
                    "round": round_index,
                    "shard": shard_index,
                    "sample_ids": shard_ids,
                },
            )
            shard_config = copy.deepcopy(base_config)
            shard_config["sample_ids_file"] = str(sample_file.relative_to(PROJECT_ROOT))
            shard_config["strict_sample_ids"] = True
            shard_config["generate_summaries"] = False
            shard_config["reuse_spl_snapshot"] = True
            write_json(shard_config_path, shard_config)
            jobs.append((shard_config_path, log_path))

        results: list[dict] = []
        with ThreadPoolExecutor(max_workers=len(jobs)) as executor:
            futures = {
                executor.submit(run_prepare, shard_config_path, log_path): shard_config_path
                for shard_config_path, log_path in jobs
            }
            for future in as_completed(futures):
                returncode, log_path = future.result()
                results.append(
                    {
                        "config": str(futures[future].relative_to(PROJECT_ROOT)),
                        "returncode": returncode,
                        "log": str(Path(log_path).relative_to(PROJECT_ROOT)),
                    }
                )
        write_json(round_root / "process_results.json", results)
        remaining = incomplete_ids()
        write_json(
            round_root / "completion.json",
            {
                "expected": len(expected_ids),
                "complete": len(expected_ids) - len(remaining),
                "remaining": len(remaining),
                "remaining_ids": remaining,
            },
        )
        print(
            f"Prepare round {round_index}: {len(expected_ids) - len(remaining)}/{len(expected_ids)} complete; "
            f"{len(remaining)} remaining"
        )

    if remaining:
        raise RuntimeError(
            f"SPL preparation incomplete after {args.max_rounds} rounds: {len(remaining)} samples; "
            f"see {control_root}"
        )

    merged_manifest: list[dict] = []
    for sample_key in expected_ids:
        frozen = input_by_key[sample_key]
        sample_dir = artifact_root / str(frozen["task_id"])
        merged_manifest.append(
            {
                "task_id": frozen["task_id"],
                "benchmark_task_id": frozen["benchmark_task_id"],
                "sample_key": sample_key,
                "index": int(frozen["index"]),
                "language": frozen["language"],
                "task_type": frozen["task_type"],
                "mode": frozen["mode"],
                "has_internal_call_chain": True,
                "sample_dir": str(sample_dir.relative_to(PROJECT_ROOT)),
            }
        )
    write_json(artifact_root / "manifest.json", merged_manifest)
    for row in merged_manifest:
        sample_id = str(row["task_id"])
        if not sample_snapshot_dir(snapshot_root, sample_id).exists():
            snapshot_sample_assets(
                resolve_in_project(row["sample_dir"]),
                snapshot_root,
                sample_id,
                [
                    "raw_code.txt",
                    "spl.txt",
                    "spl_metadata.json",
                    "spl_by_method.json",
                    "spl_regeneration_audit.json",
                ],
                provenance={
                    "experiment": "Exp02",
                    "dataset": "CoRe",
                    "spl_model": expected_model,
                    "recovered_by_parallel_merger": True,
                },
            )
    build_snapshot_manifest(
        snapshot_root,
        metadata={
            "experiment": "Exp02",
            "dataset": "CoRe",
            "sample_size": len(expected_ids),
            "spl_model": expected_model,
            "sampling_seed": sample_spec.get("seed"),
        },
    )
    write_json(
        control_root / "FINAL_COMPLETION.json",
        {
            "status": "complete",
            "expected": len(expected_ids),
            "complete": len(expected_ids),
            "spl_model": expected_model,
            "artifact_manifest": str((artifact_root / "manifest.json").relative_to(PROJECT_ROOT)),
            "snapshot_manifest": str((snapshot_root / "manifest.json").relative_to(PROJECT_ROOT)),
        },
    )
    print(f"Prepared and merged {len(merged_manifest)} sampled CoRe SPL artifacts")


if __name__ == "__main__":
    main()
