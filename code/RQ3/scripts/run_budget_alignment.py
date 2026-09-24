from __future__ import annotations

"""Budget-probe orchestrator: re-run miniswe_spl_both over the full 218 sample
with its context budget matched to repair/localization (4 cards / 2 inline /
750 spl chars / 1400 source chars), keeping EVERYTHING else identical
(protocol, frozen workflow addendum, model, step limit). SPL assets are REUSED,
never rebuilt.

Subcommands:
  configs   generate 218 probe configs under random218_budget_aligned/configs
  run       agent phase (run.py per unit) — only miniswe_spl_both
  eval      evaluation phase (evaluate.py per unit)
  status    per-unit completion summary

Usage:
  python scripts/run_budget_alignment.py configs
  python scripts/run_budget_alignment.py run [unit ...]
  python scripts/run_budget_alignment.py eval [unit ...]
  python scripts/run_budget_alignment.py status
"""

import json
import os
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
EXP6 = ROOT
SRC_CONFIGS = EXP6 / "data/raw_results/exp3_swebench/random218_compact/configs"
PROBE_CONFIGS = EXP6 / "data/raw_results/exp3_swebench/random218_budget_aligned/configs"
PROBE_UNITS = EXP6 / "data/raw_results/exp3_swebench/random218_budget_aligned/units"
LOG_DIR = EXP6 / "data/raw_results/exp3_swebench/random218_budget_aligned/execution"

PY = r"C:\conda\python.exe"

BUDGET_PATCH = {
    "mini_spl_both_controller_cards": 4,
    "mini_spl_both_controller_spl_chars": 750,
    "mini_spl_both_prompt_cards": 2,
    "mini_spl_both_source_bound_source_chars": 1400,
}


def discover_source_units() -> list[str]:
    return sorted(p.stem for p in SRC_CONFIGS.glob("unit_*.json"))


def phase_configs() -> None:
    PROBE_CONFIGS.mkdir(parents=True, exist_ok=True)
    # fresh api-key pool: same keys, isolated lease dir / event log
    src_pool = json.loads((SRC_CONFIGS / "api_key_pool.json").read_text(encoding="utf-8"))
    probe_pool = dict(src_pool)
    probe_pool["run_id"] = "exp6_budget_alignment"
    probe_pool["lease_dir"] = str(PROBE_CONFIGS / "api_key_leases")
    probe_pool["event_log"] = str(LOG_DIR / "api_key_leases.jsonl")
    (PROBE_CONFIGS / "api_key_pool.json").write_text(
        json.dumps(probe_pool, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )

    n = 0
    for unit in discover_source_units():
        src = json.loads((SRC_CONFIGS / f"{unit}.json").read_text(encoding="utf-8"))
        src.update(BUDGET_PATCH)
        src["conditions"] = ["miniswe_spl_both"]
        src["run_dir"] = f"$PROJECT_ROOT/data/raw_results/exp3_swebench/random218_budget_aligned/units/{unit}/runs"
        prefix = f"exp6_budget_alignment_{unit}"
        src["swebench_harness_run_id_prefix"] = prefix
        src["smoke_run_id"] = prefix
        src["api_key_pool_file"] = "runs/_secrets/api_key_pool.json"
        src["experiment_label"] = (
            "BUDGET PROBE: miniswe_spl_both budget matched to repair/localization "
            "(4/750/2/1400); protocol/model/step-limit/frozen-workflow unchanged; "
            "prebuilt SPL/summary reused (not rebuilt)."
        )
        (PROBE_CONFIGS / f"{unit}.json").write_text(
            json.dumps(src, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
        n += 1
    print(f"generated {n} probe configs under {PROBE_CONFIGS}")


def base_env() -> dict[str, str]:
    env = os.environ.copy()
    env.setdefault("PYTHONUTF8", "1")
    env.setdefault("PYTHONIOENCODING", "utf-8")
    env.setdefault("PYTHONUNBUFFERED", "1")
    env["EXP6_WINDOWS_SHORT_PROJECT_ROOT"] = r"C:\e"
    env["EXP6_FORCE_RESUME_EXISTING_CONDITIONS"] = "1"
    return env


def run_one(unit: str, phase: str, timeout: int) -> tuple[str, str]:
    cfg = PROBE_CONFIGS / f"{unit}.json"
    script = "run.py" if phase == "run" else "evaluate.py"
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    with (LOG_DIR / f"{phase}_{unit}.stdout.log").open("w", encoding="utf-8") as out, (
        LOG_DIR / f"{phase}_{unit}.stderr.log"
    ).open("w", encoding="utf-8") as err:
        rc = subprocess.run(
            [PY, str(EXP6 / script), "--config", str(cfg)],
            cwd=ROOT,
            env=base_env(),
            stdout=out,
            stderr=err,
            check=False,
            timeout=timeout,
        ).returncode
    return unit, f"rc={rc}"


def phase_run(max_workers: int, units: list[str]) -> None:
    done = 0
    with ThreadPoolExecutor(max_workers=max_workers) as ex:
        for unit, status in ex.map(lambda u: run_one(u, "run", 7200), units):
            done += 1
            print(f"[run {done}/{len(units)}] {unit} {status}", flush=True)


def phase_eval(max_workers: int, units: list[str]) -> None:
    done = 0
    with ThreadPoolExecutor(max_workers=max_workers) as ex:
        for unit, status in ex.map(lambda u: run_one(u, "eval", 5400), units):
            done += 1
            print(f"[eval {done}/{len(units)}] {unit} {status}", flush=True)


def phase_status(units: list[str]) -> None:
    done = resolved = patch = 0
    for unit in units:
        ep = PROBE_UNITS / unit / "runs" / "evaluation.json"
        if not ep.exists():
            continue
        done += 1
        rows = json.loads(ep.read_text(encoding="utf-8"))
        for row in rows:
            if isinstance(row, dict) and row.get("condition") == "miniswe_spl_both":
                if row.get("patch_generated"):
                    patch += 1
                if row.get("resolved"):
                    resolved += 1
    print(f"evaluated: {done}/{len(units)}  |  patch: {patch}  |  resolved: {resolved}")


def main() -> int:
    which = sys.argv[1] if len(sys.argv) > 1 else "configs"
    selected = sys.argv[2:] if len(sys.argv) > 2 else None
    units = discover_source_units()
    if selected:
        units = [u for u in units if u in selected]
    print(f"units: {len(units)}", flush=True)

    if which == "configs":
        phase_configs()
    elif which == "run":
        phase_run(int(os.environ.get("PROBE_MAX_WORKERS", "6")), units)
    elif which == "eval":
        phase_eval(int(os.environ.get("PROBE_EVAL_MAX_WORKERS", "4")), units)
    elif which == "status":
        phase_status(units)
    else:
        print("usage: run_budget_alignment.py [configs|run|eval|status] [unit ...]", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
