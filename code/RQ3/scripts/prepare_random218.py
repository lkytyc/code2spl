from __future__ import annotations

"""Prepare the ready-to-run random218 x 5-condition V2 (guarded) experiment.

This script ONLY generates files. It does NOT run agents, does NOT build SPL,
and does NOT pull Docker images. Everything it produces is a small, deterministic
JSON manifest/config that points at the ALREADY-BUILT assets:

  - sample_dir  -> data/RQ3/inputs/precomputed_random218_deepseek-v4-flash/working/round_01/<instance>
                   (contains spl_context.txt, spl_index.json, free_summary_context.txt,
                    swebench_instance.jsonl, problem_statement.txt, source_files/, gold_patch.diff)
  - dataset     -> data/RQ3/inputs/precomputed_random218_deepseek-v4-flash/dataset/swebench_verified_test_500.jsonl
  - SPL assets  -> reused via reuse_prebuilt_spl_assets=true (NEVER rebuilt)

The V2 guard is the only protocol change vs the holdout30 template:
  mini_spl_protocol = "spl_guarded_protocol"
It applies to the three SPL conditions; miniswe_original / miniswe_free_summary
are unaffected (non-SPL).

Outputs:
  inputs/reproduced_units/random218/unit_NNN_<instance>/manifest.json
  data/results/reproduced_runs/random218/configs/unit_NNN_<instance>.json
  data/results/reproduced_runs/random218/configs/api_key_pool.json
"""

import json
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
EXP6 = ROOT
OUT_ROOT = EXP6 / "data/raw_results/exp3_swebench/random218_compact"
OUT_CONFIGS = OUT_ROOT / "configs"
OUT_ARTIFACTS = EXP6 / "data/RQ3/inputs/unit_manifests_random218"

WORK = EXP6 / "data/RQ3/inputs/precomputed_random218_deepseek-v4-flash/working/round_01"
ORDER_FILE = EXP6 / "data/RQ3/inputs/precomputed_random218_deepseek-v4-flash/configs/execution_order_218_ids.json"

GUARDED_PROTOCOL = "spl_guarded_protocol"
CONDITIONS = [
    "miniswe_original",
    "miniswe_free_summary",
    "miniswe_spl_localization",
    "miniswe_spl_repair",
    "miniswe_spl_both",
]
MODEL = "deepseek-v4-pro"          # agent inference model (matches paper reference)
SPL_MODEL = "deepseek-v4-flash"    # prebuilt SPL provenance (reused, not rebuilt)

# Known-good isolated-copy template (holdout30): already has pro agent + flash SPL/summary
# + all five conditions + the 500-row local dataset path + short-path wiring.
TEMPLATE = EXP6 / "data/results/reproduced_runs/holdout30_seed12630/plan/configs/unit_12_django__django-14493.json"
POOL_SRC = EXP6 / "data/results/reproduced_runs/holdout30_seed12630/plan/configs/api_key_pool.json"

SNAPSHOT_DIR = "$PROJECT_ROOT/data/RQ3/spl_assets/random218_deepseek-v4-flash"


def read_json(p: Path):
    return json.loads(p.read_text(encoding="utf-8"))


def write_json(p: Path, d) -> None:
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(d, ensure_ascii=False, indent=2), encoding="utf-8", newline="\n")


def unit_name(pos: int, instance_id: str) -> str:
    return f"unit_{pos + 1:03d}_{instance_id}"


def load_metadata(instance_id: str) -> tuple[str, str, list[str]]:
    """Return (repo, base_commit, source_files) for one instance."""
    inst = read_json(WORK / instance_id / "instance.json")
    repo = str(inst.get("repo") or "")
    base_commit = str(inst.get("base_commit") or "")
    ga = WORK / instance_id / "gold_patch_analysis.json"
    source_files: list[str] = []
    if ga.exists():
        source_files = [str(s) for s in read_json(ga).get("source_files", []) or []]
    return repo, base_commit, source_files


def make_manifest(pos: int, instance_id: str) -> None:
    unit = unit_name(pos, instance_id)
    dst = OUT_ARTIFACTS / unit
    dst.mkdir(parents=True, exist_ok=True)
    repo, base_commit, source_files = load_metadata(instance_id)
    sample_dir = (
        f"$PROJECT_ROOT/data/RQ3/inputs/precomputed_random218_deepseek-v4-flash"
        f"/working/round_01/{instance_id}"
    )
    manifest = [
        {
            "index": pos,
            "instance_id": instance_id,
            "sample_dir": sample_dir,
            "repo": repo,
            "base_commit": base_commit,
            "source_files": source_files,
            "spl_source_scope": "legacy_gold_patch_scope",
        }
    ]
    write_json(dst / "manifest.json", manifest)


def make_config(pos: int, instance_id: str) -> None:
    unit = unit_name(pos, instance_id)
    cfg = read_json(TEMPLATE)

    artifact_dir = f"$PROJECT_ROOT/data/RQ3/inputs/unit_manifests_random218/{unit}"
    run_dir = f"$PROJECT_ROOT/data/raw_results/exp3_swebench/random218_compact/units/{unit}/runs"

    cfg["artifact_dir"] = artifact_dir
    cfg["run_dir"] = run_dir
    cfg["indices"] = [pos]
    cfg["model"] = MODEL
    cfg["spl_model"] = SPL_MODEL
    cfg["summary_model"] = SPL_MODEL
    cfg["mini_spl_protocol"] = GUARDED_PROTOCOL
    cfg["conditions"] = list(CONDITIONS)
    cfg["resume_existing_conditions"] = False
    cfg["resume_existing_evaluations"] = False
    cfg["force_rerun_swebench_harness"] = True
    cfg["spl_snapshot_dir"] = SNAPSHOT_DIR
    cfg["spl_snapshot_source_dirs"] = [SNAPSHOT_DIR]
    cfg["swebench_harness_run_id_prefix"] = f"exp6_random218_{unit}"
    cfg["smoke_run_id"] = f"exp6_random218_{unit}"
    cfg["swebench_harness_command"] = cfg.get("swebench_harness_command", "").replace(
        "--clean true", "--clean false"
    )
    cfg["api_key_pool_file"] = (
        "$PROJECT_ROOT/data/raw_results/exp3_swebench"
        "random218/configs/api_key_pool.json"
    )
    # Docker pulls are the long pole for a 218-instance run; pre-pull separately
    # and give a generous timeout so a fresh image never aborts at 60s.
    cfg["mini_docker_pull_timeout_seconds"] = 1800
    cfg["mini_environment_timeout_seconds"] = 300
    cfg["experiment_label"] = (
        "Exp6 random218 full sample x 5 conditions, V2 guarded protocol "
        f"({GUARDED_PROTOCOL}), agent={MODEL}, prebuilt SPL/summary={SPL_MODEL} (reused)."
    )
    write_json(OUT_CONFIGS / f"{unit}.json", cfg)


def make_pool() -> None:
    pool = read_json(POOL_SRC)
    pool["run_id"] = "exp6_random218"
    pool["lease_dir"] = (
        "$PROJECT_ROOT/data/raw_results/exp3_swebench"
        "random218/configs/api_key_leases"
    )
    pool["event_log"] = (
        "$PROJECT_ROOT/data/raw_results/exp3_swebench"
        "random218/execution/api_key_leases.jsonl"
    )
    (OUT_ROOT / "execution").mkdir(parents=True, exist_ok=True)
    write_json(OUT_CONFIGS / "api_key_pool.json", pool)


def main() -> None:
    order = read_json(ORDER_FILE)["sample_ids"]
    assert len(order) == 218, f"expected 218 execution-order IDs, got {len(order)}"
    print(f"preparing {len(order)} units (5 conditions each) ...")

    for pos, instance_id in enumerate(order):
        make_manifest(pos, instance_id)
        make_config(pos, instance_id)
        print(f"  [{pos + 1:3d}/218] {instance_id}")

    make_pool()
    print(f"done: manifests + configs under {OUT_ARTIFACTS.relative_to(ROOT)} and {OUT_CONFIGS.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
