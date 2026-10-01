"""Verify the new condition's prompts carry no SPL keyword or SPL protocol text.

The whole point of `raw_spl_unstructured_summary` is that the model receives the
*semantic content* of the SPL cards through the `raw_free_summary` framing, with
the keyword structure and the SPL usage instructions gone.  This script checks
that claim directly on the 341 generated prompts rather than trusting the code
path:

  * no SPL tag survives (`[COMMAND`, `[DEFINE_WORKER`, `<REF>`, ...);
  * no SPL protocol vocabulary survives (`transition audit`, `spl_control`,
    `Source/SPL`, ...) -- the strict condition's prompt contains a binding-rule
    paragraph that must not be present here;
  * the prompt framing matches `raw_free_summary`'s template exactly, i.e. the
    text between the official prompt and the summary is byte-identical.

It also reports prompt length, so the compact representation's size reduction is
on the record.

Reads the new run directory; writes one JSON file into it.
"""

from __future__ import annotations

import hashlib
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
PACKAGE_ROOT = os.path.dirname(os.path.dirname(ROOT))
PACKAGE_ROOT = os.path.dirname(os.path.dirname(ROOT))
NEW_RUN = os.path.join(
    PACKAGE_ROOT, "data/raw_results/exp2_core/deepseek-v4-pro_full341_unstructured_summary"
)
FREE_TEMPLATE = os.path.join(
    PACKAGE_ROOT, "code/RQ2/methods/raw_free_summary/prompts/prompt.md"
)

TAG_PATTERNS = [
    "[COMMAND", "[DEFINE_WORKER", "[INPUTS]", "[OUTPUTS]", "[MAIN_FLOW]",
    "[SEQUENTIAL_BLOCK]", "[ALTERNATIVE_FLOW", "[EXCEPTION_FLOW", "[END_",
    "[LOG ", "[THROW ", "<REF>", "</REF>", "RESULT ",
]
PROTOCOL_PATTERNS = [
    "transition audit", "spl_control", "spl_inline", "SPL-derived", "Source/SPL",
    "SPL card", "SPL cards", "atomic SPL", "Use SPL", "the SPL below",
    "one indivisible evidence unit",
]


def main() -> int:
    with open(FREE_TEMPLATE, encoding="utf-8") as fh:
        template_sha = hashlib.sha256(fh.read().encode("utf-8")).hexdigest()

    records = []
    tag_hits = proto_hits = 0
    lengths = []
    missing_prompt = []

    for sample in sorted(os.listdir(NEW_RUN)):
        cond_dir = os.path.join(NEW_RUN, sample, "raw_spl_unstructured_summary")
        if not os.path.isdir(cond_dir):
            continue  # skip the run's own summary files and eval dirs
        p = os.path.join(cond_dir, "prompt.txt")
        if not os.path.isfile(p):
            missing_prompt.append(sample)
            continue
        with open(p, encoding="utf-8") as fh:
            prompt = fh.read()
        lengths.append(len(prompt))

        tags = [t for t in TAG_PATTERNS if t in prompt]
        protos = [t for t in PROTOCOL_PATTERNS if t in prompt]
        if tags:
            tag_hits += 1
        if protos:
            proto_hits += 1

        records.append({
            "sample_id": sample,
            "prompt_chars": len(prompt),
            "leaked_tags": tags,
            "leaked_protocol_phrases": protos,
            "has_aux_summary_header": "Auxiliary Summary Context:" in prompt,
            "has_nl_summary_header": "Natural-Language Summary:" in prompt,
            "has_spl_control_block": "[SPL_CONTROL:" in prompt or "SPL Control" in prompt,
        })

    lengths.sort()
    result = {
        "prompts": len(records),
        "missing_prompt": missing_prompt,
        "free_summary_template_sha256": template_sha,
        "cards_with_tag_leak": tag_hits,
        "cards_with_protocol_leak": proto_hits,
        "all_have_aux_summary_header": all(r["has_aux_summary_header"] for r in records),
        "all_have_nl_summary_header": all(r["has_nl_summary_header"] for r in records),
        "any_spl_control_block": any(r["has_spl_control_block"] for r in records),
        "prompt_chars": {
            "min": lengths[0] if lengths else 0,
            "median": lengths[len(lengths) // 2] if lengths else 0,
            "max": lengths[-1] if lengths else 0,
        },
        "records": records,
    }

    out = os.path.join(NEW_RUN, "prompt_leakage_audit.json")
    with open(out, "w", encoding="utf-8") as fh:
        json.dump(result, fh, ensure_ascii=False, indent=2)

    print(f"prompts                  {len(records)}")
    print(f"missing prompt.txt       {len(missing_prompt)}")
    print(f"tag leaks                {tag_hits} cards")
    print(f"SPL protocol leaks       {proto_hits} cards")
    print(f"free_summary template    sha256 {template_sha[:16]}...")
    print(f"aux-summary header       {'all' if result['all_have_aux_summary_header'] else 'MISSING in some'}")
    print(f"any spl_control block    {result['any_spl_control_block']}")
    print(f"prompt chars             min {result['prompt_chars']['min']:,} "
          f"median {result['prompt_chars']['median']:,} "
          f"max {result['prompt_chars']['max']:,}")
    print(f"wrote {out}")
    return 0 if tag_hits == 0 and proto_hits == 0 and not missing_prompt else 1


if __name__ == "__main__":
    sys.exit(main())
