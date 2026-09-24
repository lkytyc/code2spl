from __future__ import annotations

"""Runner for the random218 x 5-condition V2 (guarded) EVALUATION phase.

This runs evaluate.py per unit (218 units) to score each condition's patch.diff
with the SWE-bench harness. It does NOT touch the agent phase and does NOT make
any LLM calls (harness runs test suites in the pre-pulled eval images).

Resume: a unit is skipped if its `runs/evaluation.json` already exists.

Usage:
  python scripts/eval_random218.py run [unit ...]
  python scripts/eval_random218.py status

Concurrency is bounded by TOP218_EVAL_MAX_WORKERS (default 3 units).
Must be launched with EXP6_WINDOWS_SHORT_PROJECT_ROOT=C:/e set (inherited).
"""

import json
import os
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
EXP6 = ROOT
CONFIGS = EXP6 / "data/raw_results/exp3_swebench/random218_compact/configs"
LOG_DIR = EXP6 / "data/raw_results/exp3_swebench/random218_compact/execution"
UNITS = EXP6 / "data/raw_results/exp3_swebench/random218_compact/units"

PY = sys.executable


def discover_units() -> list[str]:
    return sorted(p.stem for p in CONFIGS.glob("unit_*.json"))


def eval_done(unit: str) -> bool:
    return (UNITS / unit / "runs" / "evaluation.json").exists()


def base_env() -> dict[str, str]:
    env = os.environ.copy()
    env.setdefault("PYTHONUTF8", "1")
    env.setdefault("PYTHONIOENCODING", "utf-8")
    env.setdefault("PYTHONUNBUFFERED", "1")
    env.setdefault("EXP6_WINDOWS_SHORT_PROJECT_ROOT", r"C:\e")
    return env


def run_one(unit: str) -> tuple[str, str]:
    if eval_done(unit):
        return unit, "skipped"
    cfg = CONFIGS / f"{unit}.json"
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    with (LOG_DIR / f"eval_{unit}.stdout.log").open("w", encoding="utf-8") as out, (
        LOG_DIR / f"eval_{unit}.stderr.log"
    ).open("w", encoding="utf-8") as err:
        rc = subprocess.run(
            [PY, str(EXP6 / "evaluate.py"), "--config", str(cfg)],
            cwd=ROOT,
            env=base_env(),
            stdout=out,
            stderr=err,
            check=False,
        ).returncode
    return unit, f"rc={rc}"


def phase_run(max_workers: int, units: list[str]) -> None:
    done = skipped = 0
    with ThreadPoolExecutor(max_workers=max_workers) as ex:
        for unit, status in ex.map(run_one, units):
            if status == "skipped":
                skipped += 1
            else:
                done += 1
            print(f"[{unit}] {status}  (done={done} skipped={skipped})", flush=True)


def phase_status(units: list[str]) -> None:
    done = 0
    total_cond = 0
    resolved_cond = 0
    for unit in units:
        ep = UNITS / unit / "runs" / "evaluation.json"
        if not ep.exists():
            continue
        done += 1
        rows = json.loads(ep.read_text(encoding="utf-8"))
        for row in rows:
            if not isinstance(row, dict):
                continue
            if row.get("patch_generated"):
                total_cond += 1
                if row.get("resolved"):
                    resolved_cond += 1
    print(f"units evaluated: {done}/{len(units)}  |  resolved: {resolved_cond}/{total_cond} patched conditions")


def main() -> int:
    which = sys.argv[1] if len(sys.argv) > 1 else "run"
    selected = sys.argv[2:] if len(sys.argv) > 2 else None
    units = discover_units()
    if selected:
        units = [u for u in units if u in selected]
    print(f"eval units: {len(units)}", flush=True)

    if which == "run":
        phase_run(int(os.environ.get("TOP218_EVAL_MAX_WORKERS", "3")), units)
    elif which == "status":
        phase_status(units)
    else:
        print("usage: eval_random218.py [run|status] [unit ...]", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
