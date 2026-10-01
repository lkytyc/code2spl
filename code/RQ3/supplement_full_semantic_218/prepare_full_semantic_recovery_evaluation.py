"""Create the final, full-set evaluation config after Docker recovery."""

from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))  # the package's code/ directory
from common.env import expand  # noqa: E402


HERE = Path(__file__).resolve().parent
PROJECT = HERE.parents[1]
SOURCE = Path(expand(
    "$PROJECT_ROOT/data/RQ3/settings/configs/random218_full_semantic_summary"
    "/full_semantic_summary_218_evaluation_config.json"
))
TARGET = SOURCE.with_name("full_semantic_summary_218_recovery_evaluation_config.json")
MODE = "miniswe_full_semantic_summary"


def main() -> None:
    config = json.loads(SOURCE.read_text(encoding="utf-8"))
    # The old evaluation.json contains the Docker-interrupted rows.  Recompute
    # the full condition so the canonical metrics file is internally
    # consistent; this reruns local harness tests only, never agent/API calls.
    config["indices"] = []
    config["conditions"] = [MODE]
    config["resume_existing_evaluations"] = False
    config["rerun_conditions"] = [MODE]
    config["experiment_label"] = (
        "Final post-Docker-recovery official evaluation of all 218 frozen "
        "full-semantic-summary agent outcomes. No agent generation is run."
    )
    TARGET.write_text(
        json.dumps(config, ensure_ascii=False, indent=2), encoding="utf-8", newline="\n"
    )
    print(TARGET)


if __name__ == "__main__":
    main()
