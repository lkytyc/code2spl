"""Derive per-instance configs for the Exp3 supplement without editing any frozen file.

The frozen per-unit configs under
`spl_reproducibility_package/exp3_swebench/results/random218/configs/`
are the record of how the five published conditions ran, so they are read-only
here.  This script copies one of them and changes exactly three things:

  * `conditions` becomes just the new mode, so only the new arm is executed --
    the other five already exist and are the comparison;
  * `run_dir` is redirected under the supplement's own tree, so nothing lands on
    top of a published run;
  * the harness run-id prefix and smoke id are made unique, so the harness
    reports cannot collide with the frozen ones.

Everything else (protocol, budgets, model, temperature, step limit, source scope,
harness command) is copied verbatim, which is what keeps the comparison fair.

Usage:
  python $PROJECT_ROOT/code/RQ3/supplement_2026-09-13/untagged_arm/_make_unstructured_configs.py \
      unit_001_pydata__xarray-3151 unit_095_astropy__astropy-13579
  python $PROJECT_ROOT/code/RQ3/supplement_2026-09-13/untagged_arm/_make_unstructured_configs.py --all
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
FROZEN_CONFIGS = (
    ROOT
    / "spl_reproducibility_package/exp3_swebench/results/random218/configs"
)
OUT_ROOT = HERE / "data/raw_results/exp3_swebench/random218_untagged_both"

MODE = "miniswe_spl_unstructured_both"
# Copied from the working copy so the supplement stays self-contained; the key
# pool itself is read by run.py, never by this script.
KEY_POOL = HERE / "data/results/reproduced_runs/random218/configs/api_key_pool.json"

MUTATED = (
    "conditions",
    "run_dir",
    "swebench_harness_run_id_prefix",
    "smoke_run_id",
    "experiment_label",
)


def build(unit: str) -> dict:
    src = FROZEN_CONFIGS / f"{unit}.json"
    if not src.is_file():
        raise SystemExit(f"frozen config not found: {src}")
    config = json.loads(src.read_text(encoding="utf-8"))

    config["conditions"] = [MODE]
    config["run_dir"] = str(
        (OUT_ROOT / "runs" / unit).relative_to(ROOT)
    ).replace("\\", "/")
    config["swebench_harness_run_id_prefix"] = f"exp6_unstructured_both_{unit}"
    config["smoke_run_id"] = f"exp6_unstructured_both_{unit}"
    if KEY_POOL.is_file():
        config["api_key_pool_file"] = str(KEY_POOL.relative_to(ROOT)).replace("\\", "/")
    config["experiment_label"] = (
        "Exp3 supplement: SPL content without tag notation, aligned to the frozen "
        "miniswe_spl_both budgets and protocol."
    )
    return config


def main(argv: list[str]) -> int:
    if "--all" in argv:
        units = sorted(p.stem for p in FROZEN_CONFIGS.glob("unit_*.json"))
        if not units:
            raise SystemExit(f"no frozen configs under {FROZEN_CONFIGS}")
    else:
        units = argv[1:] or ["unit_001_pydata__xarray-3151"]
    (OUT_ROOT / "configs").mkdir(parents=True, exist_ok=True)
    for unit in units:
        config = build(unit)
        frozen = json.loads((FROZEN_CONFIGS / f"{unit}.json").read_text(encoding="utf-8"))
        drift = {
            k: (frozen.get(k), config[k])
            for k in frozen
            if k not in MUTATED and frozen[k] != config.get(k)
        }
        if drift:
            raise SystemExit(f"{unit}: unexpected config drift: {drift}")
        target = OUT_ROOT / "configs" / f"{unit}.json"
        target.write_text(
            json.dumps(config, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
        )
        print(f"{unit}: wrote {target.relative_to(ROOT)}")
        print(f"   conditions={config['conditions']} run_dir={config['run_dir']}")
        print(
            "   budgets: "
            f"cards={config.get('mini_spl_both_controller_cards')} "
            f"spl_chars={config.get('mini_spl_both_controller_spl_chars')} "
            f"prompt_cards={config.get('mini_spl_both_prompt_cards')} "
            f"source_chars={config.get('mini_spl_both_source_bound_source_chars')}"
        )
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
