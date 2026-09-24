"""Rewrite data/KEY_CHECKSUMS.csv for this package.

    python code/tools/build_key_checksums.py

`data/KEY_CHECKSUMS.csv` is the package's checksum list: the headline tables,
the aggregate records the headline numbers are computed from, and the
configurations that produced them.  Checking those cells alone is enough to
tell whether a number in `data/results_tables/` still rests on the run it
claims to; an archive of the package carries its own transport checksums for
everything else.

The tree is walked with `os.walk` on an extended-length path rather than with
`Path.rglob`: SWE-bench instance ids push recorded paths past the Win32 limit,
and `rglob` stops descending into them without reporting an error.
"""

from __future__ import annotations

import csv
import hashlib
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / "data" / "KEY_CHECKSUMS.csv"

# Whole trees that count as key material.
PREFIXES = ("data/results_tables/",)

# Aggregate records, by file name, inside the result trees.
AGGREGATES = {
    "usage_summary.json", "cost_summary.json", "metrics_by_mode.json",
    "enhanced_statistics.json", "stage_usage_summary.json", "summary.json",
    "final_analysis.json", "final_analysis_unstructured_both.json",
    "budget80_summary.json", "structure_ablation_comparison.json",
    "exp1_full100_results.csv", "exp1_full100_significance.csv",
    "original_vs_full_semantic_summary.json",
}

TREES_WITH_AGGREGATES = ("data/results/", "data/raw_results/")


def extended(path) -> str:
    """The path carrying the Windows extended-length prefix."""
    text = str(path)
    if os.name != "nt" or text.startswith("\\\\?\\"):
        return text
    return "\\\\?\\" + str(Path(text).absolute())


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with open(extended(path), "rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            value.update(block)
    return value.hexdigest()


def key_files() -> list[Path]:
    found = []
    for dirpath, dirnames, filenames in os.walk(extended(ROOT)):
        dirnames[:] = [d for d in dirnames if d != "__pycache__"]
        for name in filenames:
            full = Path(dirpath) / name
            relative = os.path.relpath(str(full), extended(ROOT)).replace(
                os.sep, "/")
            keep = relative.startswith(PREFIXES)
            if not keep and name in AGGREGATES and relative.startswith(
                    TREES_WITH_AGGREGATES):
                keep = True
            if not keep and relative.startswith("data/") and "/settings/" in relative:
                keep = True
            if keep and full.name != "KEY_CHECKSUMS.csv":
                found.append(ROOT / relative)
    return sorted(found, key=lambda p: p.relative_to(ROOT).as_posix())


def main() -> None:
    files = key_files()
    with open(extended(OUTPUT), "w", encoding="utf-8-sig", newline="") as stream:
        writer = csv.writer(stream)
        writer.writerow(["relative_path", "size_bytes", "sha256"])
        for path in files:
            writer.writerow([path.relative_to(ROOT).as_posix(),
                             os.path.getsize(extended(path)), digest(path)])
    print(f"wrote {OUTPUT.name} with {len(files):,} entries")


if __name__ == "__main__":
    main()
