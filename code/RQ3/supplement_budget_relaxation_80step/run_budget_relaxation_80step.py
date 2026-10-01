from __future__ import annotations

import json
import os
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
EXP = ROOT
STUDY = EXP / "data/raw_results/exp3_swebench/budget_relaxation_80step_stratified30"
CONFIGS = STUDY / "configs"
LOGS = STUDY / "execution"
STATUS = STUDY / "pipeline_status.json"


def now() -> str:
    return datetime.now(timezone.utc).astimezone().isoformat()


def save_status(data: dict) -> None:
    STATUS.parent.mkdir(parents=True, exist_ok=True)
    tmp = STATUS.with_suffix(".tmp")
    tmp.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    tmp.replace(STATUS)


def run_stage(name: str, command: list[str], state: dict) -> int:
    LOGS.mkdir(parents=True, exist_ok=True)
    state["current_stage"] = name
    state["stages"][name] = {"status": "running", "started_at": now()}
    save_status(state)
    with (LOGS / f"{name}.stdout.log").open("a", encoding="utf-8") as out, (
        LOGS / f"{name}.stderr.log"
    ).open("a", encoding="utf-8") as err:
        completed = subprocess.run(command, cwd=ROOT, env=os.environ.copy(), stdout=out, stderr=err)
    state["stages"][name].update(
        {"status": "complete" if completed.returncode == 0 else "failed", "returncode": completed.returncode, "finished_at": now()}
    )
    save_status(state)
    return completed.returncode


def main() -> int:
    if not os.environ.get("OPENAI_API_KEY"):
        raise RuntimeError("OPENAI_API_KEY is required in this process")
    os.environ.setdefault("PYTHONUTF8", "1")
    os.environ.setdefault("PYTHONIOENCODING", "utf-8")
    os.environ.setdefault("PYTHONUNBUFFERED", "1")
    os.environ.setdefault("EXP6_WINDOWS_SHORT_PROJECT_ROOT", r"C:\e")
    state = {
        "study": STUDY.name,
        "pid": os.getpid(),
        "started_at": now(),
        "status": "running",
        "current_stage": None,
        "stages": {},
        "credential_source": "isolated process environment",
    }
    save_status(state)
    stages = [
        (
            "generate_main_five",
            [sys.executable, str(EXP / "run.py"), "--config", str(CONFIGS / "generation_main_five.json")],
        ),
        (
            "generate_full_semantic",
            [sys.executable, str(EXP / "run_full_semantic_summary.py"), "--config", str(CONFIGS / "generation_full_semantic.json")],
        ),
        (
            "evaluate_all_six",
            [sys.executable, str(EXP / "evaluate.py"), "--config", str(CONFIGS / "evaluation_all_six.json")],
        ),
    ]
    for name, command in stages:
        if run_stage(name, command, state) != 0:
            state.update({"status": "failed", "finished_at": now(), "current_stage": name})
            save_status(state)
            return 1
    state.update({"status": "complete", "finished_at": now(), "current_stage": None})
    save_status(state)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
