"""Re-evaluate the supplement patches the harness never got to run.

Fifteen units ended with `patch_generated: true, evaluation_available: false` and
no verdict.  They are all `scikit-learn`, and the harness traceback says why:

    FileNotFoundError: [WinError 206] The filename or extension is too long.:
    'logs\\run_evaluation\\<run_id>\\<mode>\\<instance_id>'

The harness runs with cwd = `common.paths.PROJECT_ROOT` and makes its per-instance
log directory out of the run id.  `run_id = <smoke_run_id>_<mode>_<instance_id>`,
and this supplement's `smoke_run_id` is longer than the frozen arms' by five
characters, so fifteen units landed past the length the Win32 layer accepts and
died before a single test ran.  The measured split is clean: every one of the 180
evaluated units is at relative path length <= 197, every one of the 15 casualties
at 209.

`smoke_run_id` is read in exactly one place outside the config -- `evaluate.py`
line 428, to name the harness run -- and never by `run.py`, the agent prompt or
the delivered payload.  `retry_harness_infrastructure_failures.py` in this same
repository already treats it that way: for patches with no harness report it
rewrites the config with `smoke_run_id = "h" + sha256(original)[:12]` and re-runs.
This script follows that precedent on the affected units only.

Usage:
  python $PROJECT_ROOT/code/RQ3/supplement_2026-09-13/untagged_arm/_retry_harness_path_failures.py [--dry-run]
"""

from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
BASE = HERE / "data/raw_results/exp3_swebench/random218_untagged_both"
SRC = BASE / "runs"
CONFIGS = BASE / "configs"
RETRY_CONFIGS = CONFIGS / "retry_harness_path"
LOGS = BASE / "execution"
MODE = "miniswe_spl_unstructured_both"
PY = sys.executable


def long(path: Path) -> str:
    text = str(path)
    if os.name != "nt" or text.startswith("\\\\?\\"):
        return text
    return "\\\\?\\" + str(Path(text).absolute())


def read_json(path: Path):
    with open(long(path), encoding="utf-8") as fh:
        return json.load(fh)


def write_json(path: Path, data) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(long(path), "w", encoding="utf-8", newline="\n") as fh:
        json.dump(data, fh, ensure_ascii=False, indent=2)
        fh.write("\n")


def affected_units() -> list[str]:
    out = []
    for unit_dir in sorted(p for p in SRC.iterdir() if p.is_dir() and p.name.startswith("unit_")):
        path = unit_dir / "evaluation.json"
        if not Path(long(path)).is_file():
            continue
        for row in read_json(path):
            if (isinstance(row, dict) and row.get("condition") == MODE
                    and row.get("patch_generated") and not row.get("evaluation_available")):
                out.append(unit_dir.name)
                break
    return out


def make_retry_config(unit: str) -> Path:
    source = CONFIGS / f"{unit}.json"
    config = read_json(source)
    original = str(config.get("smoke_run_id") or config.get("run_id") or unit)
    short = "h" + hashlib.sha256(original.encode("utf-8")).hexdigest()[:12]
    config["smoke_run_id"] = short
    config["swebench_harness_run_id_prefix"] = short
    # Same flags the repository's own infrastructure-retry path sets: keep every
    # row that already has a verdict, redo only the ones that never got one.
    config["resume_existing_evaluations"] = True
    config["rerun_unavailable_evaluations"] = True
    config["rerun_evaluation_conditions"] = []
    target = RETRY_CONFIGS / f"{unit}.json"
    write_json(target, config)
    return target


def retry_one(unit: str) -> tuple[str, int]:
    config_path = make_retry_config(unit)
    LOGS.mkdir(parents=True, exist_ok=True)
    log = LOGS / f"retry_harness_path_{unit}.log"
    env = os.environ.copy()
    env.setdefault("PYTHONUTF8", "1")
    env.setdefault("PYTHONIOENCODING", "utf-8")
    env.setdefault("PYTHONUNBUFFERED", "1")
    env.setdefault("EXP6_WINDOWS_SHORT_PROJECT_ROOT", r"C:\e")
    with open(long(log), "w", encoding="utf-8", newline="\n") as fh:
        rc = subprocess.run(
            [PY, str(HERE / "evaluate.py"), "--config", str(config_path)],
            cwd=str(ROOT),
            env=env,
            stdout=fh,
            stderr=subprocess.STDOUT,
            check=False,
        ).returncode
    return unit, rc


def verdicts(unit: str) -> tuple[str, str]:
    path = SRC / unit / "evaluation.json"
    if not Path(long(path)).is_file():
        return unit, "no evaluation.json"
    for row in read_json(path):
        if isinstance(row, dict) and row.get("condition") == MODE:
            status = row.get("eval_status") or {}
            return unit, (f"available={row.get('evaluation_available')} "
                          f"resolved={row.get('resolved')} "
                          f"errored={status.get('harness_errored')} "
                          f"run_id={status.get('run_id')}")
    return unit, "no row"


def main(argv: list[str]) -> int:
    dry_run = "--dry-run" in argv
    units = affected_units()
    print(f"units with a generated patch and no harness verdict: {len(units)}")
    for unit in units:
        print(f"  {unit}")

    if dry_run:
        for unit in units:
            config = read_json(CONFIGS / f"{unit}.json")
            print(f"  {unit}: smoke_run_id {config['smoke_run_id']!r} "
                  f"({len(config['smoke_run_id'])}) -> hashed short form (13)")
        return 0

    if not units:
        print("nothing to retry")
        return 0

    workers = int(os.environ.get("RETRY_MAX_WORKERS", "3"))
    with ThreadPoolExecutor(max_workers=workers) as pool:
        for unit, rc in pool.map(retry_one, units):
            print(f"[retry] {unit} rc={rc}", flush=True)

    print("\n=== verdicts after retry ===")
    still_bad = 0
    for unit in units:
        _, text = verdicts(unit)
        print(f"  {unit}: {text}")
        if "available=True" not in text:
            still_bad += 1
    print(f"\nstill without a verdict: {still_bad}/{len(units)}")
    return 1 if still_bad else 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
