"""Compare the supplement's patches against the five frozen arms, patch by patch.

Resolution is the headline number, but it does not say *how* the arms differ.
This does: for every instance, hash each arm's `patch.diff` and report how often
the arms produced byte-identical patches.  Two arms agreeing on a patch are
making the same decision, whatever the tests then say about it; the interesting
cells are the ones where the supplement diverges from `spl_both` and the verdict
moves with it.

Line endings are normalised before hashing.  The frozen runner wrote CRLF
patches in some arms and the harness rewrites line endings when it applies them,
so a raw md5 would report "different" for patches a reader would call identical.

Read-only.
Usage: python $PROJECT_ROOT/code/RQ3/supplement_2026-09-13/untagged_arm/scripts/analyze_unstructured_both_patches.py
"""

from __future__ import annotations

import hashlib
import json
from collections import Counter
from itertools import combinations
from pathlib import Path

HERE = Path(__file__).resolve().parent
EXP6 = HERE.parents[4]
FROZEN_UNITS = EXP6 / "data/raw_results/exp3_swebench/random218_compact/units"
SUPP_UNITS = EXP6 / "data/raw_results/exp3_swebench/random218_untagged_both/units"

FROZEN = (
    "miniswe_original",
    "miniswe_free_summary",
    "miniswe_spl_localization",
    "miniswe_spl_repair",
    "miniswe_spl_both",
)
SUPPLEMENT = "miniswe_spl_unstructured_both"
ARMS = FROZEN + (SUPPLEMENT,)
SHORT = {
    "miniswe_original": "original",
    "miniswe_free_summary": "free_summary",
    "miniswe_spl_localization": "spl_localization",
    "miniswe_spl_repair": "spl_repair",
    "miniswe_spl_both": "spl_both",
    SUPPLEMENT: "unstructured_both",
}
OUT = EXP6 / "data/raw_results/exp3_swebench/random218_untagged_both/audits/patch_identity.json"


def long(path: Path) -> str:
    text = str(path)
    return text if text.startswith("\\\\?\\") else "\\\\?\\" + str(path.absolute())


def digest(path: Path) -> str | None:
    if not path.is_file():
        return None
    with open(long(path), "r", encoding="utf-8", errors="replace") as fh:
        text = fh.read()
    text = text.replace("\r\n", "\n").replace("\r", "\n").strip()
    if not text:
        return None
    return hashlib.md5(text.encode("utf-8")).hexdigest()


def main() -> int:
    units = sorted(p.name for p in SUPP_UNITS.glob("unit_*"))
    per_instance: dict[str, dict[str, str | None]] = {}
    resolved: dict[str, dict[str, bool]] = {}

    for unit in units:
        instance = unit.split("_", 2)[2]
        digests: dict[str, str | None] = {}
        for arm in FROZEN:
            digests[arm] = digest(
                FROZEN_UNITS / unit / f"runs/{instance}/{arm}/patch.diff"
            )
        digests[SUPPLEMENT] = digest(SUPP_UNITS / unit / f"{instance}/{SUPPLEMENT}/patch.diff")
        per_instance[instance] = digests

        flags: dict[str, bool] = {}
        frozen_eval = FROZEN_UNITS / unit / "runs/evaluation.json"
        if frozen_eval.is_file():
            for row in json.loads(frozen_eval.read_text(encoding="utf-8")):
                flags[row["condition"]] = bool(
                    row.get("evaluation_available") and row.get("resolved")
                )
        supp_eval = SUPP_UNITS / unit / "evaluation.json"
        if supp_eval.is_file():
            for row in json.loads(supp_eval.read_text(encoding="utf-8")):
                flags[row["condition"]] = bool(
                    row.get("evaluation_available") and row.get("resolved")
                )
        resolved[instance] = flags

    print(f"units with a supplement patch on disk: "
          f"{sum(1 for d in per_instance.values() if d[SUPPLEMENT])}/{len(per_instance)}")

    print("\n## Patch identity (per-instance, " + str(len(per_instance)) + " instances)")
    print()
    print("| Comparison | instances byte-identical | share |")
    print("|---|---:|---:|")
    rows = []
    for left, right in combinations(ARMS, 2):
        both = sum(
            1
            for d in per_instance.values()
            if d[left] is not None and d[left] == d[right]
        )
        rows.append((left, right, both))
    for left, right, both in sorted(rows, key=lambda r: (r[0] != SUPPLEMENT, -r[2])):
        print(f"| {SHORT[left]} vs {SHORT[right]} | {both} | {both/len(per_instance):.1%} |")

    print("\n## Supplement arm vs each frozen arm: patch same/different × verdict (only instances where both arms generated a patch)")
    print()
    verdicts = Counter()
    for instance, d in per_instance.items():
        if d[SUPPLEMENT] is None:
            continue
        flags = resolved.get(instance, {})
        for arm in FROZEN:
            if d[arm] is None:
                continue
            same = d[arm] == d[SUPPLEMENT]
            mine = flags.get(SUPPLEMENT)
            theirs = flags.get(arm)
            verdicts[(arm, same, mine, theirs)] += 1
    print("| Control arm | Patch | Supplement resolved | Control resolved | Instances |")
    print("|---|---|---:|---:|---:|")
    for arm in FROZEN:
        for same in (True, False):
            for mine in (True, False):
                for theirs in (True, False):
                    n = verdicts.get((arm, same, mine, theirs), 0)
                    if not n:
                        continue
                    print(
                        f"| {SHORT[arm]} | {'same' if same else 'different'} | "
                        f"{'✓' if mine else '✗'} | {'✓' if theirs else '✗'} | {n} |"
                    )

    OUT.write_text(
        json.dumps(
            {
                "instances": len(per_instance),
                "digests": per_instance,
                "resolved": resolved,
                "identical_pairs": [
                    {"left": l, "right": r, "identical": n} for l, r, n in rows
                ],
                "verdict_cells": [
                    {
                        "arm": arm,
                        "same_patch": same,
                        "supplement_resolved": mine,
                        "control_resolved": theirs,
                        "n": verdicts.get((arm, same, mine, theirs), 0),
                    }
                    for arm in FROZEN
                    for same in (True, False)
                    for mine in (True, False)
                    for theirs in (True, False)
                ],
            },
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    print(f"\nwrote {OUT.relative_to(EXP6.parents[1])}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
