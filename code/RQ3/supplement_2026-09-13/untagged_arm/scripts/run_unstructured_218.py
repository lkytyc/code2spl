"""Runner for the Exp3 supplement: 218 units x 1 condition, agent + harness phases.

The supplement is one extra arm, `miniswe_spl_unstructured_both`, over the same
218 SWE-bench Verified instances the five published conditions ran.  It is
executed by the same `run.py` and `evaluate.py` the published arms used -- the
supplement only swaps in its own mode, which `run_unstructured.py` installs by
monkey-patching the renderer.  Reuse rather than reimplementation is the point:
the protocol, budgets, model and harness invocation are the frozen ones by
construction, not by a promise to keep them in sync.

Divergences from `run_random218.py`, all deliberate:

  * `EXP6_WINDOWS_SHORT_PROJECT_ROOT` is set here rather than inherited.  The
    published run picked it up from the launching shell, which means a re-run
    from a different shell could silently drop the short root and start failing
    on the long `scikit-learn__scikit-learn-*` names again.
  * The agent phase writes to the supplement's own `run_dir`, and the eval phase
    scores only the supplement's patch.  Nothing under
    `.../random218/` is written to.

Resume: a completed unit is skipped in both phases, so the command can be re-run
after an interruption without redoing work or re-spending API calls.

Usage:
  python $PROJECT_ROOT/code/RQ3/supplement_2026-09-13/untagged_arm/scripts/run_unstructured_218.py run  [unit ...]
  python $PROJECT_ROOT/code/RQ3/supplement_2026-09-13/untagged_arm/scripts/run_unstructured_218.py eval [unit ...]
  python $PROJECT_ROOT/code/RQ3/supplement_2026-09-13/untagged_arm/scripts/run_unstructured_218.py status
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
EXP6 = ROOT
BASE = EXP6 / "data/raw_results/exp3_swebench/random218_untagged_both"
CONFIGS = BASE / "configs"
LOG_DIR = BASE / "execution"
RUNS = BASE / "runs"
MODE = "miniswe_spl_unstructured_both"

PY = sys.executable or r"C:\conda\python.exe"


def discover_units() -> list[str]:
    return sorted(p.stem for p in CONFIGS.glob("unit_*.json"))


def base_env() -> dict[str, str]:
    env = os.environ.copy()
    env.setdefault("PYTHONUTF8", "1")
    env.setdefault("PYTHONIOENCODING", "utf-8")
    env.setdefault("PYTHONUNBUFFERED", "1")
    # Without this the long instance names exceed MAX_PATH on Windows; the
    # published run relied on the launching shell exporting it.
    env.setdefault("EXP6_WINDOWS_SHORT_PROJECT_ROOT", r"C:\e")
    return env


def condition_dir(unit: str) -> Path:
    instance = unit.split("_", 2)[2]
    return RUNS / unit / instance / MODE


def agent_done(unit: str) -> bool:
    marker = condition_dir(unit) / "condition_complete.json"
    if not marker.is_file():
        return False
    try:
        return bool(json.loads(marker.read_text(encoding="utf-8")).get("complete"))
    except (OSError, json.JSONDecodeError):
        return False


def eval_done(unit: str) -> bool:
    return (RUNS / unit / "evaluation.json").is_file()


def run_one(unit: str, phase: str) -> tuple[str, str]:
    if phase == "run":
        if agent_done(unit):
            return unit, "skipped"
        script = EXP6 / "run_unstructured.py"
    else:
        if eval_done(unit):
            return unit, "skipped"
        script = EXP6 / "evaluate.py"

    LOG_DIR.mkdir(parents=True, exist_ok=True)
    label = f"{phase}_unstructured_{unit}"
    env = base_env()
    # Re-running must skip finished conditions instead of redoing them.
    env["EXP6_FORCE_RESUME_EXISTING_CONDITIONS"] = "1"
    with (LOG_DIR / f"{label}.stdout.log").open("w", encoding="utf-8") as out, (
        LOG_DIR / f"{label}.stderr.log"
    ).open("w", encoding="utf-8") as err:
        rc = subprocess.run(
            [PY, str(script), "--config", str(CONFIGS / f"{unit}.json")],
            cwd=str(ROOT),
            env=env,
            stdout=out,
            stderr=err,
            check=False,
        ).returncode
    return unit, f"rc={rc}"


def phase_run(phase: str, max_workers: int, units: list[str]) -> None:
    done = skipped = failed = 0
    with ThreadPoolExecutor(max_workers=max_workers) as ex:
        for unit, status in ex.map(lambda u: run_one(u, phase), units):
            if status == "skipped":
                skipped += 1
            else:
                done += 1
                if status != "rc=0":
                    failed += 1
            print(
                f"[{phase}] {unit} {status}  "
                f"(done={done} skipped={skipped} failed={failed})",
                flush=True,
            )
    print(f"[{phase}] finished: done={done} skipped={skipped} failed={failed}", flush=True)


def phase_status(units: list[str]) -> None:
    agent = sum(1 for u in units if agent_done(u))
    evaluated = sum(1 for u in units if eval_done(u))
    resolved = patched = 0
    for unit in units:
        path = RUNS / unit / "evaluation.json"
        if not path.is_file():
            continue
        try:
            rows = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue
        for row in rows:
            if isinstance(row, dict) and row.get("patch_generated"):
                patched += 1
                resolved += 1 if row.get("resolved") else 0
    total = len(units)
    print(f"agent complete : {agent}/{total}")
    print(f"evaluated      : {evaluated}/{total}")
    print(f"resolved       : {resolved}/{patched} patched")


def main(argv: list[str]) -> int:
    which = argv[1] if len(argv) > 1 else "run"
    selected = [a for a in argv[2:] if not a.startswith("--")]
    units = discover_units()
    if selected:
        units = [u for u in units if u in selected]
    print(f"units: {len(units)}", flush=True)

    if which == "run":
        phase_run("run", int(os.environ.get("UNSTRUCTURED_MAX_WORKERS", "3")), units)
    elif which == "eval":
        phase_run("eval", int(os.environ.get("UNSTRUCTURED_EVAL_MAX_WORKERS", "3")), units)
    elif which == "status":
        phase_status(units)
    else:
        print(__doc__, file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
