"""Did the harness path-length retry succeed, and did it leave the rest alone?

Prints the 15 retried units' new verdicts next to the run id the harness used,
and re-checks that every other unit's row still carries a verdict from the
original pass.  Writes `harness_path_retry.json` so the before/after pair ships
with the results.
"""

from __future__ import annotations

import json
import os
from pathlib import Path

HERE = Path(__file__).resolve().parent
BASE = HERE / "data/results/reproduced_runs/unstructured_both"
SRC = BASE / "runs"
MODE = "miniswe_spl_unstructured_both"
BEFORE = BASE / "harness_path_failures_before.json"
OUT = BASE / "harness_path_retry.json"


def long(path: Path) -> str:
    text = str(path)
    if os.name != "nt" or text.startswith("\\\\?\\"):
        return text
    return "\\\\?\\" + str(Path(text).absolute())


def row_for(unit: str) -> dict | None:
    path = SRC / unit / "evaluation.json"
    if not Path(long(path)).is_file():
        return None
    for row in json.loads(Path(long(path)).read_text(encoding="utf-8")):
        if isinstance(row, dict) and row.get("condition") == MODE:
            return row
    return None


def main() -> int:
    before = {u["unit"]: u for u in json.loads(
        Path(long(BEFORE)).read_text(encoding="utf-8"))["units"]}
    retried = list(before)

    records = []
    resolved = unevaluated = failed = 0
    print(f"{'unit':<46} {'evaluated':<10} {'resolved':<9} {'errored':<8} run_id")
    for unit in retried:
        row = row_for(unit) or {}
        status = row.get("eval_status") or {}
        avail = row.get("evaluation_available")
        if not avail:
            unevaluated += 1
        elif row.get("resolved"):
            resolved += 1
        else:
            failed += 1
        print(f"{unit:<46} {str(avail):<10} {str(row.get('resolved')):<9} "
              f"{str(status.get('harness_errored')):<8} {status.get('run_id')}")
        records.append({
            "unit": unit,
            "instance_id": row.get("instance_id"),
            "before": {
                "run_id": before[unit].get("run_id"),
                "run_id_chars": before[unit].get("run_id_chars"),
                "harness_errored": before[unit].get("harness_errored"),
                "error": before[unit].get("error"),
            },
            "after": {
                "run_id": status.get("run_id"),
                "run_id_chars": len(status.get("run_id") or ""),
                "harness_errored": status.get("harness_errored"),
                "evaluation_available": bool(avail),
                "resolved": row.get("resolved"),
            },
        })
    print(f"\nretried: {len(retried)}  resolved: {resolved}  "
          f"ran and failed: {failed}  still no verdict: {unevaluated}")

    units = sorted(p.name for p in SRC.iterdir()
                   if p.is_dir() and p.name.startswith("unit_"))
    have = sum(1 for u in units if (row_for(u) or {}).get("evaluation_available"))
    print(f"units with a verdict overall: {have}/{len(units)}")

    others = [u for u in units if u not in retried]
    polluted = []
    for unit in others:
        row = row_for(unit) or {}
        rid = str((row.get("eval_status") or {}).get("run_id") or "")
        if rid and not rid.startswith("exp6_unstructured_both_"):
            polluted.append((unit, rid))
    print(f"non-retried units whose run_id changed: {len(polluted)}")
    for unit, rid in polluted[:10]:
        print(f"  {unit}: {rid}")

    payload = {
        "condition": MODE,
        "cause": "SWE-bench harness log directory exceeded the Windows path limit "
                 "(WinError 206); the run id built from smoke_run_id was longer than "
                 "the frozen arms' by five characters",
        "remedy": "smoke_run_id replaced by 'h' + sha256(original)[:12], following "
                  "retry_harness_infrastructure_failures.py; evaluation-side key only",
        "retried": len(retried),
        "resolved_after_retry": resolved,
        "ran_and_failed": failed,
        "still_without_verdict": unevaluated,
        "verdicts_overall": have,
        "units": len(units),
        "non_retried_units_whose_run_id_changed": [u for u, _ in polluted],
        "records": records,
    }
    with open(long(OUT), "w", encoding="utf-8", newline="\n") as fh:
        json.dump(payload, fh, ensure_ascii=False, indent=2)
        fh.write("\n")
    print(f"wrote {OUT.relative_to(HERE.parents[1])}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
