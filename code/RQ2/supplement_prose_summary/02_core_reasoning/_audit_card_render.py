"""Audit the unstructured-summary renderer over all 341 frozen Exp2 cards.

Two independent checks, both intended to be quotable evidence in the supplement:

1. *Content preservation* -- every payload extracted from the tagged card (worker
   description, contract entries, each COMMAND text and its RESULT, each flow
   condition, each LOG/THROW message) must appear verbatim in the rendered
   prose.  A miss means the ablation removed content along with structure, which
   would invalidate the comparison; the script reports it rather than hiding it.

2. *Tag leakage* -- the rendered summary must contain no SPL keyword.  If a tag
   survived, the condition would not in fact be "SPL without keyword structure".

Cards that carry no SPL structure at all (the `# JSON_PARSE_ERROR` dumps) are
passed through verbatim and counted separately, so the passthrough rate is
disclosed rather than being silently folded into the rendered count.

Reads the frozen snapshot; writes one JSON file into the new run directory.
"""

from __future__ import annotations

import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
PACKAGE_ROOT = os.path.dirname(os.path.dirname(ROOT))
PACKAGE_ROOT = os.path.dirname(os.path.dirname(ROOT))
SNAPSHOT = os.path.join(PACKAGE_ROOT, "data/RQ2/spl_assets/full341/instances")
NEW_RUN = os.path.join(
    PACKAGE_ROOT, "data/raw_results/exp2_core/deepseek-v4-pro_full341_unstructured_summary"
)

sys.path.insert(0, os.path.join(PACKAGE_ROOT, "code"))

from common.spl_card_summary import (  # noqa: E402
    audit_content_preservation,
    render_card_as_summary,
)

LEAK_PATTERNS = [
    "[COMMAND", "[DEFINE_WORKER", "[INPUTS]", "[OUTPUTS]", "[MAIN_FLOW]",
    "[SEQUENTIAL_BLOCK]", "[ALTERNATIVE_FLOW", "[EXCEPTION_FLOW", "[END_",
    "[LOG ", "[THROW ", "<REF>", "</REF>",
]


def main() -> int:
    cards = []
    for inst in sorted(os.listdir(SNAPSHOT)):
        path = os.path.join(SNAPSHOT, inst, "assets", "spl.txt")
        if os.path.isfile(path):
            cards.append((inst.split("--")[0], path))

    records = []
    rendered = passed = failed = 0
    leak_hits = 0
    total_checked = 0

    for sample_id, path in cards:
        with open(path, encoding="utf-8") as fh:
            card = fh.read()
        summary, audit = render_card_as_summary(card)
        if audit["mode"] == "passthrough":
            passed += 1
        else:
            rendered += 1

        preservation = audit_content_preservation(card, summary)
        total_checked += preservation["checked"]
        if not preservation["ok"]:
            failed += 1

        leaks = [p for p in LEAK_PATTERNS if p in summary]
        if leaks:
            leak_hits += 1

        records.append({
            "sample_id": sample_id,
            "mode": audit["mode"],
            "chars_in": audit["chars_in"],
            "chars_out": audit["chars_out"],
            "payloads_checked": preservation["checked"],
            "content_ok": preservation["ok"],
            "missing": preservation["missing"],
            "leaked_tags": leaks,
            "worker_name": audit.get("worker_name", ""),
            "steps": audit.get("steps", 0),
            "alternatives": audit.get("alternatives", 0),
            "exceptions": audit.get("exceptions", 0),
            "unknown_tag_lines": audit.get("unknown_tag_lines", []),
        })

    empty_desc = sum(1 for r in records if r["mode"] == "rendered" and not r["worker_name"])
    unparsed = sum(1 for r in records if r["unknown_tag_lines"])
    sizes = sorted(r["chars_out"] for r in records if r["mode"] == "rendered")

    result = {
        "cards_total": len(records),
        "rendered": rendered,
        "passthrough_json_parse_error": passed,
        "content_preservation_failures": failed,
        "tag_leak_cards": leak_hits,
        "payloads_checked_total": total_checked,
        "empty_worker_name": empty_desc,
        "cards_with_unparsed_tag_lines": unparsed,
        "rendered_chars": {
            "min": sizes[0] if sizes else 0,
            "median": sizes[len(sizes) // 2] if sizes else 0,
            "max": sizes[-1] if sizes else 0,
        },
        "records": records,
    }

    os.makedirs(NEW_RUN, exist_ok=True)
    out = os.path.join(NEW_RUN, "card_render_audit.json")
    with open(out, "w", encoding="utf-8") as fh:
        json.dump(result, fh, ensure_ascii=False, indent=2)

    print(f"cards                  {len(records)}")
    print(f"  rendered             {rendered}")
    print(f"  passthrough (JSONERR) {passed}")
    print(f"content preservation   "
          f"{rendered - failed}/{rendered} ok   ({total_checked:,} payloads checked)")
    print(f"tag leakage            {leak_hits} cards")
    print(f"empty worker name      {empty_desc}")
    print(f"unparsed tag lines     {unparsed} cards")
    print(f"rendered chars         min {result['rendered_chars']['min']} "
          f"median {result['rendered_chars']['median']} "
          f"max {result['rendered_chars']['max']}")
    print(f"wrote {out}")
    return 0 if failed == 0 and leak_hits == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
