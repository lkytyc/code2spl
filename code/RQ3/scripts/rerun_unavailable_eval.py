from __future__ import annotations

"""Re-run only the conditions whose harness eval was unavailable (resolved=None).

Uses evaluate.py's own resume+rerun mechanism: set resume_existing_evaluations=True
and rerun_unavailable_evaluations=True in each affected unit's config, so the
already-resolved conditions are skipped and only the patch_generated-but-unavailable
conditions are re-evaluated in place (evaluation.json is rewritten with merged rows).

Usage:
  EXP6_WINDOWS_SHORT_PROJECT_ROOT=C:/e python scripts/rerun_unavailable_eval.py
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
UNITS = EXP6 / "data/raw_results/exp3_swebench/random218_compact/units"

PY = sys.executable

TARGETS = [
    ("unit_003_scikit-learn__scikit-learn-10908", "miniswe_free_summary"),
    ("unit_004_django__django-16502", "miniswe_original"),
    ("unit_005_scikit-learn__scikit-learn-10844", "miniswe_free_summary"),
    ("unit_027_django__django-15268", "miniswe_spl_localization"),
    ("unit_097_django__django-14493", "miniswe_free_summary"),
    ("unit_205_django__django-11848", "miniswe_spl_repair"),
    ("unit_206_matplotlib__matplotlib-26291", "miniswe_spl_localization"),
]


def base_env() -> dict[str, str]:
    env = os.environ.copy()
    env.setdefault("PYTHONUTF8", "1")
    env.setdefault("PYTHONIOENCODING", "utf-8")
    env.setdefault("PYTHONUNBUFFERED", "1")
    env.setdefault("EXP6_WINDOWS_SHORT_PROJECT_ROOT", r"C:\e")
    return env


def rerun_one(unit: str) -> tuple[str, str]:
    cfg = CONFIGS / f"{unit}.json"
    data = json.loads(cfg.read_text(encoding="utf-8"))
    data["resume_existing_evaluations"] = True
    data["rerun_unavailable_evaluations"] = True
    cfg.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8", newline="\n")
    log = EXP6 / "data/raw_results/exp3_swebench/random218_compact/execution" / f"rerun_eval_{unit}.log"
    log.parent.mkdir(parents=True, exist_ok=True)
    with log.open("w", encoding="utf-8") as fh:
        rc = subprocess.run(
            [PY, str(EXP6 / "evaluate.py"), "--config", str(cfg)],
            cwd=ROOT,
            env=base_env(),
            stdout=fh,
            stderr=subprocess.STDOUT,
            check=False,
        ).returncode
    return unit, f"rc={rc}"


def main() -> int:
    units = [u for u, _ in TARGETS]
    print(f"rerun units: {len(units)}", flush=True)
    with ThreadPoolExecutor(max_workers=int(os.environ.get("RERUN_MAX_WORKERS", "3"))) as ex:
        for unit, status in ex.map(rerun_one, units):
            print(f"[{unit}] {status}", flush=True)
    # report the final state of the 7 targeted conditions
    print("\n=== final status of the 7 conditions after the re-run ===", flush=True)
    for unit, mode in TARGETS:
        ep = UNITS / unit / "runs" / "evaluation.json"
        if not ep.exists():
            print(f"{unit}/{mode}: (no evaluation.json)", flush=True)
            continue
        for r in json.loads(ep.read_text(encoding="utf-8")):
            if isinstance(r, dict) and r.get("condition") == mode:
                print(
                    f"{unit}/{mode}: resolved={r.get('resolved')} "
                    f"evaluation_available={r.get('evaluation_available')}",
                    flush=True,
                )
                break
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
