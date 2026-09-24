"""Prepare a non-destructive recovery for Docker-interrupted semantic runs.

Only completion records whose mini-SWE-agent process failed while invoking
``docker run`` are selected.  The original interrupted records are copied into
an immutable recovery snapshot before the normal resume mechanism replaces
their per-instance output directories.
"""

from __future__ import annotations

import copy
import json
import shutil
from datetime import datetime
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))  # the package's code/ directory
from common.env import expand  # noqa: E402


HERE = Path(__file__).resolve().parent
PROJECT = HERE.parents[1]
RUN_DIR = Path(expand("$PROJECT_ROOT/data/raw_results/exp3_swebench/random218_full_semantic_summary/runs"))
BASE_CONFIG = Path(expand(
    "$PROJECT_ROOT/data/RQ3/settings/configs/random218_full_semantic_summary"
    "/full_semantic_summary_218_config.json"
))
RECOVERY_CONFIG = BASE_CONFIG.with_name("full_semantic_summary_218_docker_recovery_config.json")
MODE = "miniswe_full_semantic_summary"


def docker_interrupted(status: dict) -> bool:
    failure = status.get("failure") or {}
    stderr = str(failure.get("stderr_tail") or "")
    return (
        failure.get("returncode") not in (None, 0)
        and "CalledProcessError" in stderr
        and "['docker', 'run'" in stderr
    )


def main() -> None:
    selected: list[tuple[int, str, Path]] = []
    for instance_dir in sorted(RUN_DIR.iterdir(), key=lambda p: p.name):
        status_path = instance_dir / MODE / "baseline_status.json"
        handoff_path = instance_dir / MODE / "handoff.json"
        if not status_path.is_file() or not handoff_path.is_file():
            continue
        status = json.loads(status_path.read_text(encoding="utf-8", errors="replace"))
        if not docker_interrupted(status):
            continue
        handoff = json.loads(handoff_path.read_text(encoding="utf-8", errors="replace"))
        item = handoff.get("item") or {}
        selected.append((int(item["index"]), str(item["instance_id"]), instance_dir))

    if not selected:
        raise SystemExit("No Docker-interrupted instances found; recovery not prepared.")

    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    # Keep the archive one level above the very deep per-run directory.  This
    # avoids Windows MAX_PATH failures while retaining the same experiment
    # root and preserving every interrupted record.
    snapshot = RUN_DIR.parent / f"semantic_docker_snapshot_{stamp}"
    snapshot.mkdir(parents=True, exist_ok=False)
    for index, instance_id, instance_dir in selected:
        source = instance_dir / MODE
        destination = snapshot / instance_dir.name / MODE
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copytree(source, destination)

    # Preserve the incomplete report/summary too, so the recovered output can
    # replace their canonical names without erasing the interrupted attempt.
    for name in (
        "ORIGINAL_VS_FULL_SEMANTIC_218_REPORT.md",
        "original_vs_full_semantic_summary.json",
        "original_vs_full_semantic_per_instance.csv",
        "PIPELINE_COMPLETE.json",
    ):
        source = RUN_DIR / name
        if source.is_file():
            shutil.copy2(source, snapshot / name)

    config = json.loads(BASE_CONFIG.read_text(encoding="utf-8"))
    config = copy.deepcopy(config)
    config["indices"] = [index for index, _instance_id, _directory in selected]
    config["run_swebench_harness"] = False
    config["resume_existing_conditions"] = True
    config["experiment_label"] = (
        "Recovery of only Docker-interrupted full-semantic-summary runs; "
        "all non-Docker agent outcomes and all original-system results are reused unchanged."
    )
    RECOVERY_CONFIG.write_text(
        json.dumps(config, ensure_ascii=False, indent=2), encoding="utf-8", newline="\n"
    )
    manifest = {
        "recovery_reason": "Docker Desktop interruption before mini-SWE-agent startup",
        "mode": MODE,
        "selected_count": len(selected),
        "selected": [
            {"index": index, "instance_id": instance_id}
            for index, instance_id, _directory in selected
        ],
        "snapshot_dir": str(snapshot),
        "recovery_config": str(RECOVERY_CONFIG),
        "non_docker_outcomes_reused": True,
    }
    (snapshot / "recovery_manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8", newline="\n"
    )
    print(f"docker_interrupted={len(selected)}")
    print(f"snapshot={snapshot}")
    print(f"config={RECOVERY_CONFIG}")


if __name__ == "__main__":
    main()
