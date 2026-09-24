from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
WORKSPACE_ROOT = ROOT.parent
EXP6_DIR = Path(__file__).resolve().parent
EXP4_PREPARE = ROOT / "experiments" / "04_swebench_lite_agentless" / "prepare.py"
EXP1_PREPARE = ROOT / "code" / "RQ1" / "prepare.py"
BASE_CONFIG = EXP6_DIR / "config.smoke.json"
FROZEN_SAMPLE = EXP6_DIR / "samples" / "swebench_verified_random_eps005_218_ids.json"
PRECOMPUTE_ROOT = EXP6_DIR / "precomputed" / "random218_deepseek-v4-flash"
CONFIG_ROOT = PRECOMPUTE_ROOT / "configs"
SNAPSHOT_ROOT = EXP6_DIR / "spl" / "random218_deepseek-v4-flash"
DATASET_FILE = PRECOMPUTE_ROOT / "dataset" / "swebench_verified_test_500.jsonl"
KEY_POOL = ROOT / "runs" / "_secrets" / "api_key_pool.json"
MODEL = "deepseek-v4-flash"
EXPECTED_COUNT = 218
EXPECTED_SET_SHA256 = "4e64c77ab55eac9b4cc5a7b4e19fe9db360bc10cf7b832eddc2c899b9f1523f4"
EXPECTED_ORDER_SHA256 = "ef4c51da9eb98d66f6e58547394a058570f434837a6b6bc4a0c9f4667d921bc2"


def read_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8", errors="replace"))


def write_json(path: Path, data) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=True, indent=2) + "\n", encoding="utf-8")


def relative(path: Path) -> str:
    return path.resolve().relative_to(ROOT).as_posix()


def ids_sha256(ids: list[str]) -> str:
    return hashlib.sha256(("\n".join(ids) + "\n").encode("utf-8")).hexdigest()


def load_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def validate_protocol() -> tuple[dict, list[str], str]:
    sample = read_json(FROZEN_SAMPLE)
    sample_ids = [str(value) for value in sample.get("sample_ids", [])]
    order_ids = [str(value) for value in sample.get("execution_order_ids", [])]
    if len(sample_ids) != EXPECTED_COUNT or len(set(sample_ids)) != EXPECTED_COUNT:
        raise RuntimeError("Frozen Exp6 sample is not the expected 218 unique IDs.")
    if ids_sha256(sample_ids) != EXPECTED_SET_SHA256:
        raise RuntimeError("Frozen Exp6 sample membership hash changed.")
    if len(order_ids) != EXPECTED_COUNT or set(order_ids) != set(sample_ids):
        raise RuntimeError("Frozen Exp6 execution order is invalid.")
    if ids_sha256(order_ids) != EXPECTED_ORDER_SHA256:
        raise RuntimeError("Frozen Exp6 execution-order hash changed.")

    exp1 = load_module(EXP1_PREPARE, "exp1_prepare_for_exp6_asset_check")
    exp4 = load_module(EXP4_PREPARE, "exp4_prepare_for_exp6_asset_check")
    if exp4.FREE_FILE_SUMMARY_PROMPT != exp1.FREE_SUMMARY_PROMPT:
        raise RuntimeError("Exp6 free-summary prompt is not aligned with the current Exp1 prompt.")
    return sample, order_ids, exp4.FREE_FILE_SUMMARY_PROMPT_SHA256


def ensure_frozen_dataset() -> None:
    if DATASET_FILE.is_file():
        line_count = sum(1 for line in DATASET_FILE.open("r", encoding="utf-8") if line.strip())
        if line_count != 500:
            raise RuntimeError(f"Frozen local SWE-bench dataset has {line_count} rows, expected 500.")
        return
    cache_roots = [
        WORKSPACE_ROOT / "artifacts" / "hf_cache" / "datasets",
        Path.home() / ".cache" / "huggingface" / "datasets",
    ]
    arrows: list[Path] = []
    for cache_root in cache_roots:
        arrows.extend(
            cache_root.glob(
                "SWE-bench___swe-bench_verified/default/0.0.0/*/swe-bench_verified-test.arrow"
            )
        )
    source_arrow = max(arrows, key=lambda path: path.stat().st_mtime) if arrows else None
    if source_arrow is not None:
        from datasets import Dataset

        rows = [dict(row) for row in Dataset.from_file(str(source_arrow))]
        source = {"type": "existing_huggingface_arrow", "path": str(source_arrow)}
    else:
        exp4 = load_module(EXP4_PREPARE, "exp4_prepare_for_exp6_dataset_materialization")
        (PRECOMPUTE_ROOT / "hf_cache" / "datasets").mkdir(parents=True, exist_ok=True)
        loader_config = read_json(BASE_CONFIG)
        loader_config.update(
            {
                "dataset_path": None,
                "use_huggingface": True,
                "hf_home": relative(PRECOMPUTE_ROOT / "hf_cache"),
                "hf_datasets_cache": relative(PRECOMPUTE_ROOT / "hf_cache" / "datasets"),
                "hf_offline": False,
            }
        )
        rows = exp4.load_swebench_items(loader_config)
        source = {"type": "huggingface_download", "dataset": "SWE-bench/SWE-bench_Verified"}
    if len(rows) != 500:
        raise RuntimeError(f"Downloaded SWE-bench Verified test split has {len(rows)} rows, expected 500.")
    DATASET_FILE.parent.mkdir(parents=True, exist_ok=True)
    temporary = DATASET_FILE.with_suffix(".jsonl.tmp")
    with temporary.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=True) + "\n")
    temporary.replace(DATASET_FILE)
    write_json(
        DATASET_FILE.parent / "provenance.json",
        source | {"rows": len(rows), "frozen_jsonl": relative(DATASET_FILE)},
    )


def build_config(sample_file: Path, artifact_dir: Path, max_workers: int) -> dict:
    config = read_json(BASE_CONFIG)
    for key in ("random_sample", "random_seed", "limit", "indices", "start_index", "end_index"):
        config.pop(key, None)
    config.update(
        {
            "experiment_label": "Exp6 frozen random218 reusable SPL and free-summary assets",
            "sample_ids_file": relative(sample_file),
            "strict_sample_ids": True,
            "dataset_path": relative(DATASET_FILE),
            "use_huggingface": False,
            "artifact_dir": relative(artifact_dir),
            "provider": "openai",
            "model": MODEL,
            "spl_mode": "openai",
            "spl_model": MODEL,
            "summary_provider": "openai",
            "summary_model": MODEL,
            "base_url": "https://api.deepseek.com",
            "temperature": 0,
            "summary_max_output_tokens": 512,
            "spl_max_output_tokens": 4096,
            "max_workers": max(1, max_workers),
            "max_per_key": 2,
            "api_key_pool_file": relative(KEY_POOL),
            "continue_on_error": True,
            "fail_on_spl_error": True,
            "fail_on_summary_error": True,
            "max_retries": 5,
            "openai_timeout_seconds": 900,
            "source_fetch_timeout_seconds": 120,
            "generate_spl_context": True,
            "spl_source_scope": "legacy_gold_patch_scope",
            "spl_snapshot_dir": relative(SNAPSHOT_ROOT),
            "spl_snapshot_source_dirs": [],
            "reuse_spl_snapshot": True,
            "reuse_prebuilt_spl_assets": True,
            "reuse_prebuilt_summary_assets": True,
            "save_spl_snapshot": True,
            "build_spl_snapshot_manifest_on_prepare": True,
            "hf_offline": True,
            "run_swebench_harness": False,
        }
    )
    return config


def snapshot_entry(snapshot_module, instance_id: str) -> Path:
    return snapshot_module.sample_snapshot_dir(SNAPSHOT_ROOT, f"{instance_id}::construction")


def audit(order_ids: list[str], prompt_sha256: str) -> dict:
    sys.path.insert(0, str(ROOT / "code"))
    from common import spl_snapshot

    complete: list[str] = []
    missing: list[str] = []
    invalid: list[dict] = []
    totals = {
        "spl_input_tokens": 0,
        "spl_output_tokens": 0,
        "spl_reasoning_tokens": 0,
        "spl_total_tokens": 0,
        "spl_calls": 0,
        "spl_elapsed_seconds": 0.0,
        "summary_input_tokens": 0,
        "summary_output_tokens": 0,
        "summary_total_tokens": 0,
        "summary_calls": 0,
        "summary_elapsed_seconds": 0.0,
    }
    for instance_id in order_ids:
        entry = snapshot_entry(spl_snapshot, instance_id)
        if not entry.exists():
            missing.append(instance_id)
            continue
        try:
            manifest = spl_snapshot.verify_sample_snapshot(entry)
            by_path = {row["path"]: row for row in manifest.get("files", [])}
            required = {
                "spl_context.txt",
                "spl_index.json",
                "spl_metadata.json",
                "free_summary_context.txt",
                "free_summary_metadata.json",
            }
            absent = sorted(required - set(by_path))
            if absent:
                raise ValueError(f"missing snapshot assets: {absent}")
            assets = entry / "assets"
            spl_meta = read_json(assets / "spl_metadata.json")
            summary_meta = read_json(assets / "free_summary_metadata.json")
            if spl_meta.get("model") != MODEL:
                raise ValueError(f"SPL model is {spl_meta.get('model')!r}")
            if summary_meta.get("model") != MODEL:
                raise ValueError(f"summary model is {summary_meta.get('model')!r}")
            if summary_meta.get("prompt_sha256") != prompt_sha256:
                raise ValueError("free-summary prompt hash mismatch")
            if not (assets / "spl_context.txt").read_text(encoding="utf-8", errors="replace").strip():
                raise ValueError("empty SPL context")
            if not (assets / "free_summary_context.txt").read_text(encoding="utf-8", errors="replace").strip():
                raise ValueError("empty free-summary context")
            if any(not row.get("ok") for row in spl_meta.get("files", [])):
                raise ValueError("SPL metadata contains failed files")
            if any(not row.get("ok") for row in summary_meta.get("files", [])):
                raise ValueError("free-summary metadata contains failed files")
            complete.append(instance_id)
            for source, prefix in ((spl_meta, "spl"), (summary_meta, "summary")):
                for key in ("input_tokens", "output_tokens", "total_tokens", "calls"):
                    totals[f"{prefix}_{key}"] += int(source.get(key, 0) or 0)
                totals[f"{prefix}_elapsed_seconds"] += float(source.get("elapsed_seconds", 0) or 0)
            totals["spl_reasoning_tokens"] += int(spl_meta.get("reasoning_tokens", 0) or 0)
        except Exception as exc:
            invalid.append({"instance_id": instance_id, "error": repr(exc)})
    return {
        "expected": len(order_ids),
        "complete": len(complete),
        "missing": missing,
        "invalid": invalid,
        "complete_ids": complete,
        "usage": totals,
    }


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Build reusable deepseek-v4-flash SPL and free-summary assets for frozen Exp6 random218."
    )
    parser.add_argument("--execute", action="store_true")
    parser.add_argument("--limit", type=int)
    parser.add_argument("--max-workers", type=int, default=22)
    parser.add_argument("--max-rounds", type=int, default=4)
    args = parser.parse_args()

    sample, order_ids, prompt_sha256 = validate_protocol()
    if args.limit is not None:
        if args.limit < 1 or args.limit > EXPECTED_COUNT:
            raise ValueError(f"--limit must be in [1, {EXPECTED_COUNT}]")
        order_ids = order_ids[: args.limit]

    PRECOMPUTE_ROOT.mkdir(parents=True, exist_ok=True)
    CONFIG_ROOT.mkdir(parents=True, exist_ok=True)
    SNAPSHOT_ROOT.mkdir(parents=True, exist_ok=True)
    selection_file = CONFIG_ROOT / f"execution_order_{len(order_ids)}_ids.json"
    write_json(
        selection_file,
        {
            "sample_ids": order_ids,
            "sample_ids_sha256": ids_sha256(order_ids),
            "parent_sample_ids_sha256": sample["sample_ids_sha256"],
            "parent_execution_order_ids_sha256": sample["execution_order_ids_sha256"],
            "selection": "prefix of frozen execution_order_ids" if len(order_ids) < EXPECTED_COUNT else "all frozen execution_order_ids",
        },
    )
    protocol = {
        "created_at": datetime.now(timezone.utc).isoformat(),
        "model": MODEL,
        "sample_count": len(order_ids),
        "sample_set_sha256": EXPECTED_SET_SHA256,
        "execution_order_sha256": EXPECTED_ORDER_SHA256,
        "free_summary_protocol": "free_summary",
        "free_summary_prompt_sha256": prompt_sha256,
        "spl_source_scope": "legacy_gold_patch_scope",
        "artifact_policy": "immutable checksum-verified per-instance snapshots",
        "historical_snapshot_reuse": False,
        "max_instance_workers": max(1, args.max_workers),
        "api_key_capacity": 28,
    }
    write_json(PRECOMPUTE_ROOT / "protocol.json", protocol)

    initial = audit(order_ids, prompt_sha256)
    write_json(PRECOMPUTE_ROOT / "status.json", initial | {"protocol": protocol})
    print(json.dumps({"execute": args.execute, "initial": {k: v for k, v in initial.items() if k != "complete_ids"}}, indent=2))
    if not args.execute or initial["complete"] == len(order_ids):
        return 0

    ensure_frozen_dataset()

    lock_path = PRECOMPUTE_ROOT / "RUNNING.lock"
    if lock_path.exists():
        raise RuntimeError(f"Another Exp6 precompute appears active: {lock_path}")
    lock_path.write_text(f"pid={__import__('os').getpid()}\n", encoding="utf-8")
    try:
        pending = initial["missing"] + [row["instance_id"] for row in initial["invalid"]]
        for round_no in range(1, max(1, args.max_rounds) + 1):
            if not pending:
                break
            retry_file = CONFIG_ROOT / f"round_{round_no:02d}_pending_ids.json"
            write_json(retry_file, {"sample_ids": pending})
            artifact_dir = PRECOMPUTE_ROOT / "working" / f"round_{round_no:02d}"
            config_path = CONFIG_ROOT / f"round_{round_no:02d}.json"
            write_json(config_path, build_config(retry_file, artifact_dir, args.max_workers))
            log_stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
            log_path = PRECOMPUTE_ROOT / f"round_{round_no:02d}_{log_stamp}.log"
            with log_path.open("w", encoding="utf-8") as log:
                completed = subprocess.run(
                    [sys.executable, str(EXP4_PREPARE), "--config", str(config_path)],
                    cwd=ROOT,
                    stdout=log,
                    stderr=subprocess.STDOUT,
                    check=False,
                )
            status = audit(order_ids, prompt_sha256)
            status["round"] = round_no
            status["prepare_exit_code"] = completed.returncode
            status["updated_at"] = datetime.now(timezone.utc).isoformat()
            write_json(PRECOMPUTE_ROOT / "status.json", status | {"protocol": protocol})
            pending = status["missing"] + [row["instance_id"] for row in status["invalid"]]
            print(json.dumps({"round": round_no, "complete": status["complete"], "pending": len(pending)}, indent=2), flush=True)

        final = audit(order_ids, prompt_sha256)
        sys.path.insert(0, str(ROOT / "code"))
        from common.spl_snapshot import build_snapshot_manifest

        build_snapshot_manifest(SNAPSHOT_ROOT, metadata=protocol)
        write_json(
            PRECOMPUTE_ROOT / "final_report.json",
            final | {"protocol": protocol, "completed_at": datetime.now(timezone.utc).isoformat()},
        )
        return 0 if final["complete"] == len(order_ids) else 2
    finally:
        lock_path.unlink(missing_ok=True)


if __name__ == "__main__":
    raise SystemExit(main())
