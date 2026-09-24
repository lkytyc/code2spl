from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
EXP = ROOT
RESULTS = EXP / "data/raw_results/exp3_swebench/budget_relaxation_80step_stratified30"
SOURCE_CONFIG = RESULTS / "configs/evaluation_all_six.json"
RETRY_CONFIG = RESULTS / "configs/evaluation_retry_unavailable.json"


def main() -> int:
    config = json.loads(SOURCE_CONFIG.read_text(encoding="utf-8"))
    config["resume_existing_evaluations"] = True
    config["rerun_unavailable_evaluations"] = True
    config["force_rerun_swebench_harness"] = False
    RETRY_CONFIG.write_text(
        json.dumps(config, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    env = os.environ.copy()
    env.setdefault("PYTHONUTF8", "1")
    env.setdefault("PYTHONIOENCODING", "utf-8")
    env.setdefault("PYTHONUNBUFFERED", "1")
    env.setdefault("EXP6_WINDOWS_SHORT_PROJECT_ROOT", r"C:\e")
    log = RESULTS / "execution/evaluate_retry_unavailable.log"
    with log.open("w", encoding="utf-8") as stream:
        return subprocess.run(
            [sys.executable, str(EXP / "evaluate.py"), "--config", str(RETRY_CONFIG)],
            cwd=ROOT,
            env=env,
            stdout=stream,
            stderr=subprocess.STDOUT,
            check=False,
        ).returncode


if __name__ == "__main__":
    raise SystemExit(main())
