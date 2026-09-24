from __future__ import annotations

import importlib.util
from pathlib import Path


def main() -> None:
    """Reuse the Experiment 4 SWE-bench/SPL sample builder for mini-SWE-agent.

    Experiment 6 intentionally uses the same SWE-bench Verified sample schema as
    Experiment 4 so results are directly comparable while the run/evaluation
    pipeline remains independent.
    """
    prepare_path = Path(__file__).resolve().parents[1] / "04_swebench_lite_agentless" / "prepare.py"
    spec = importlib.util.spec_from_file_location("exp4_swebench_prepare_for_exp6", prepare_path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot load prepare module: {prepare_path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    module.main()


if __name__ == "__main__":
    main()
