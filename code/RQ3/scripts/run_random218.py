from __future__ import annotations

"""Runner for the random218 x 5-condition V2 (guarded) AGENT phase only.

This runs run.py per unit (218 units x 5 conditions = 1090 patch generations).
It does NOT evaluate (no harness) and does NOT pre-pull images; the agent phase
pulls each swebench environment on demand (with the 1800s pull timeout already
baked into the configs).

Usage:
  python scripts/run_random218.py run [unit ...]      # generate patches
  python scripts/run_random218.py status              # per-unit completion summary

Concurrency is bounded by TOP218_MAX_WORKERS (default 3 instances; each run.py
runs its 5 conditions with the config's internal max_workers).
"""

import os
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
EXP6 = ROOT
CONFIGS = EXP6 / "data/raw_results/exp3_swebench/random218_compact/configs"
LOG_DIR = EXP6 / "data/raw_results/exp3_swebench/random218_compact/execution"

PY = sys.executable


def discover_units() -> list[str]:
    return sorted(p.stem for p in CONFIGS.glob("unit_*.json"))


def base_env() -> dict[str, str]:
    env = os.environ.copy()
    env.setdefault("PYTHONUTF8", "1")
    env.setdefault("PYTHONIOENCODING", "utf-8")
    env.setdefault("PYTHONUNBUFFERED", "1")
    # Re-running must skip already-completed conditions instead of redoing them.
    env["EXP6_FORCE_RESUME_EXISTING_CONDITIONS"] = "1"
    return env


def run_one(label: str, command: list[str], timeout: int) -> int:
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    with (LOG_DIR / f"{label}.stdout.log").open("w", encoding="utf-8") as out, (
        LOG_DIR / f"{label}.stderr.log"
    ).open("w", encoding="utf-8") as err:
        completed = subprocess.run(
            command, cwd=ROOT, env=base_env(), stdout=out, stderr=err, check=False, timeout=timeout
        )
    print(f"[{label}] returncode={completed.returncode}", flush=True)
    return completed.returncode


def phase_run(max_workers: int, units: list[str]) -> None:
    def work(unit: str) -> None:
        cfg = CONFIGS / f"{unit}.json"
        rc = run_one(f"run_{unit}", [PY, str(EXP6 / "run.py"), "--config", str(cfg)], 7200)
        print(f"RUN {unit} rc={rc}", flush=True)

    with ThreadPoolExecutor(max_workers=max_workers) as ex:
        list(ex.map(work, units))


def phase_status(units: list[str]) -> None:
    import json
    done = 0
    total_cond = 0
    done_cond = 0
    for unit in units:
        inst = unit.split("_", 2)[2]
        runs = EXP6 / "data/raw_results/exp3_swebench/random218_compact/units" / unit / "runs" / inst
        if not runs.exists():
            continue
        for mode in ("miniswe_original", "miniswe_free_summary", "miniswe_spl_localization",
                     "miniswe_spl_repair", "miniswe_spl_both"):
            cc = runs / mode / "condition_complete.json"
            if cc.exists():
                d = json.loads(cc.read_text(encoding="utf-8"))
                total_cond += 1
                if d.get("complete"):
                    done_cond += 1
    print(f"conditions completed: {done_cond} / {total_cond} materialized", flush=True)


def main() -> int:
    which = sys.argv[1] if len(sys.argv) > 1 else "run"
    selected = sys.argv[2:] if len(sys.argv) > 2 else None
    units = discover_units()
    if selected:
        units = [u for u in units if u in selected]
    print(f"units: {len(units)}", flush=True)

    if which == "run":
        phase_run(int(os.environ.get("TOP218_MAX_WORKERS", "3")), units)
    elif which == "status":
        phase_status(units)
    else:
        print("usage: run_random218.py [run|status] [unit ...]", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
