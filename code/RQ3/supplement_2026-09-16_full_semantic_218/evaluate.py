from __future__ import annotations

import importlib.util
import os
from pathlib import Path


def main() -> None:
    """Evaluate mini-SWE-agent patches with the same SWE-bench harness path as Exp4."""
    os.environ.setdefault("PYTHONUTF8", "1")
    os.environ.setdefault("PYTHONIOENCODING", "utf-8")
    evaluate_path = Path(__file__).resolve().parents[1] / "04_swebench_lite_agentless" / "evaluate.py"
    spec = importlib.util.spec_from_file_location("exp4_swebench_evaluate_for_exp6", evaluate_path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot load evaluate module: {evaluate_path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    module.main()


if __name__ == "__main__":
    main()
