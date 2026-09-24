"""Did the two arms hand the agent the same cards, in the same roles?

`_fairness_audit.py` compares card *content*.  This compares card *order and
role*, which is a separate thing the agent sees: `selected_spl_controller_cards`
promotes the first card that is not demoted to PRIMARY, so a reordering changes
which card is labelled the primary owner.

The known cause of a reordering is in the frozen runner, not in this supplement:
`score_spl_entry` collects matched terms into a `set` and keeps `matched[:12]`,
and `spl_card_role` reads those twelve to decide whether a constructor worker is
demoted.  Which twelve survive depends on the process's string-hash seed, so two
runs of identical code can order the cards differently.  `_probe_hashseed_cards.py`
demonstrates that on the frozen arm alone; this script measures how often it lands
on the supplement.

Read-only.  Usage:
  python $PROJECT_ROOT/code/RQ3/supplement_2026-09-13/untagged_arm/scripts/analyze_unstructured_both_card_order.py
"""

from __future__ import annotations

import json
import os
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
EXP6 = HERE.parent
ROOT = EXP6.parents[1]
MODE = "miniswe_spl_unstructured_both"
TAGGED = "miniswe_spl_both"
SUPP = EXP6 / "data/raw_results/exp3_swebench/random218_untagged_both/units"
FROZEN = ROOT / "spl_reproducibility_package/exp3_swebench/results/random218/units"
OUT = EXP6 / "data/raw_results/exp3_swebench/random218_untagged_both/audits/card_order_audit.json"

RE_FUNCTION = re.compile(r"^Function: (.+)$", re.M)
RE_ROLE = re.compile(r"^Role: (.+)$", re.M)
RE_RANGE = re.compile(r"^Source excerpt[^\n]*?([\w/]+\.py:\d+-\d+)", re.M)


def long(path: Path) -> str:
    text = str(path)
    if os.name != "nt" or text.startswith("\\\\?\\"):
        return text
    return "\\\\?\\" + str(Path(text).absolute())


def read(path: Path) -> str:
    with open(long(path), encoding="utf-8", errors="replace") as fh:
        return fh.read()


def exists(path: Path) -> bool:
    try:
        return Path(long(path)).is_file()
    except OSError:
        return False


def card_sequence(text: str) -> list[dict[str, str]]:
    """(function, role, source range) for each controller card, in document order."""
    out = []
    for block in re.split(r"(?=^### )", text, flags=re.M)[1:]:
        function = RE_FUNCTION.search(block)
        role = RE_ROLE.search(block)
        source = RE_RANGE.search(block)
        out.append({
            "function": function.group(1).strip() if function else "",
            "role": role.group(1).strip() if role else "",
            "source": source.group(1) if source else "",
        })
    return out


def main() -> int:
    rows = []
    units = sorted(p.name for p in SUPP.iterdir() if p.is_dir() and p.name.startswith("unit_"))
    for unit in units:
        instance = unit.split("_", 2)[2]
        rel = Path("payload_tools/source_bound_cards.md")
        mine_path = SUPP / unit / instance / MODE / rel
        frozen_path = FROZEN / unit / "runs" / instance / TAGGED / rel
        row: dict = {"unit": unit, "instance": instance}
        if not (exists(mine_path) and exists(frozen_path)):
            row["status"] = "no bound-cards document in one or both arms"
            rows.append(row)
            continue
        mine = card_sequence(read(mine_path))
        frozen = card_sequence(read(frozen_path))
        # The supplement relabels the role lines?  No -- roles are the same
        # vocabulary in both arms; only the heading loses the `SPL ` prefix.
        same_order = [c["function"] for c in mine] == [c["function"] for c in frozen]
        same_roles = [c["role"] for c in mine] == [c["role"] for c in frozen]
        same_sources = [c["source"] for c in mine] == [c["source"] for c in frozen]
        # The cards themselves: which worker, bound to which source range.  Role
        # is deliberately excluded here -- a role label changes with the order,
        # so including it would make "the same three cards" unanswerable.
        same_pairs = sorted(
            (c["function"], c["source"]) for c in mine
        ) == sorted((c["function"], c["source"]) for c in frozen)
        row.update({
            "status": "ok",
            "cards": len(mine),
            "same_order": same_order,
            "same_roles": same_roles,
            "same_source_ranges": same_sources,
            "same_multiset_of_cards": same_pairs,
            "mine": mine,
            "frozen": frozen,
        })
        rows.append(row)

    ok = [r for r in rows if r["status"] == "ok"]
    reordered = [r for r in ok if not r["same_order"] or not r["same_roles"]]
    differing = [r for r in ok if not r["same_multiset_of_cards"]]

    print(f"units compared                     : {len(ok)}/{len(rows)}")
    print(f"same card order and roles          : {len(ok) - len(reordered)}/{len(ok)}")
    print(f"reordered or re-roled              : {len(reordered)}")
    for row in reordered:
        print(f"  {row['instance']}: order={row['same_order']} roles={row['same_roles']} "
              f"ranges={row['same_source_ranges']}")
        for side in ("frozen", "mine"):
            print(f"     {side:<6}: " + " | ".join(
                f"{c['function']}/{c['role']}" for c in row[side]))
    print(f"same set of cards (any order)      : {len(ok) - len(differing)}/{len(ok)}")
    for row in differing:
        print(f"  DIFFERENT CARD SET {row['instance']}")

    OUT.write_text(json.dumps(rows, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"wrote {OUT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
