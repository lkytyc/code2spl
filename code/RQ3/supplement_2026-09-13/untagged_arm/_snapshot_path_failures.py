"""Keep the receipts for the 15 harness path-length deaths before the retry.

The retry overwrites each affected row with a fresh verdict, which would erase
the evidence that these units failed for an infrastructure reason and not
because their patches were wrong.  This writes the pre-retry rows out verbatim.
"""

from __future__ import annotations

import json
import os
from pathlib import Path

HERE = Path(__file__).resolve().parent
BASE = HERE / "data/results/reproduced_runs/unstructured_both"
SRC = BASE / "runs"
MODE = "miniswe_spl_unstructured_both"
OUT = BASE / "harness_path_failures_before.json"


def long(path: Path) -> str:
    text = str(path)
    if os.name != "nt" or text.startswith("\\\\?\\"):
        return text
    return "\\\\?\\" + str(Path(text).absolute())


def main() -> int:
    kept = []
    for unit_dir in sorted(p for p in SRC.iterdir()
                           if p.is_dir() and p.name.startswith("unit_")):
        path = unit_dir / "evaluation.json"
        if not Path(long(path)).is_file():
            continue
        for row in json.loads(Path(long(path)).read_text(encoding="utf-8")):
            if (isinstance(row, dict) and row.get("condition") == MODE
                    and row.get("patch_generated") and not row.get("evaluation_available")):
                status = row.get("eval_status") or {}
                kept.append({
                    "unit": unit_dir.name,
                    "instance_id": row.get("instance_id"),
                    "patch_chars": row.get("patch_chars"),
                    "run_id": status.get("run_id"),
                    "run_id_chars": len(status.get("run_id") or ""),
                    "harness_returncode": status.get("harness_returncode"),
                    "harness_errored": status.get("harness_errored"),
                    "error": status.get("error"),
                    "stdout_tail": status.get("stdout_tail"),
                    "stderr_tail": status.get("stderr_tail"),
                })
                break
    OUT.parent.mkdir(parents=True, exist_ok=True)
    with open(long(OUT), "w", encoding="utf-8", newline="\n") as fh:
        json.dump({"condition": MODE, "units": kept}, fh, ensure_ascii=False, indent=2)
        fh.write("\n")
    print(f"snapshotted {len(kept)} pre-retry rows -> {OUT.relative_to(HERE.parents[1])}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
