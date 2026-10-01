"""Build the new condition's prompt for a couple of instances and audit it.

No model call, no Docker, no harness -- this only exercises the prompt
construction path so that a broken neutralization rule or a tag that survived
conversion is caught before anything costs money.

For each instance it builds the *tagged* `miniswe_spl_both` arm and the new
*unstructured* arm from the same frozen assets and the same aligned config, then
reports:

  - whether the unstructured text is tag-free and free of stray SPL vocabulary
  - how many tokens each arm spends on the SPL payload (the fairness budget)
  - the neutralization rules that fired
  - a unified diff of the two controller blocks, so every wording change is
    visible rather than asserted

Usage:
  python $PROJECT_ROOT/code/RQ3/supplement_2026-09-13/untagged_arm/_drybuild_unstructured.py
"""

from __future__ import annotations

import difflib
import os
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

import run as base  # noqa: E402
import spl_unstructured as U  # noqa: E402

MODE = "miniswe_spl_unstructured_both"
BOTH = "miniswe_spl_both"
OUT = HERE / "data/results/reproduced_runs/unstructured_both_drybuild"

SAMPLES = [
    "astropy__astropy-13579",
    "pydata__xarray-3151",
]

# Instance ids may be given on the command line and the output redirected, so the
# same builder can be snapshotted before and after a change and the two trees
# compared byte-for-byte.  That is how a change to the neutralization rules is
# shown to leave every already-completed unit's prompt untouched.
if len(sys.argv) > 1:
    SAMPLES = [a for a in sys.argv[1:] if not a.startswith("--")]
if os.environ.get("DRYBUILD_OUT"):
    OUT = Path(os.environ["DRYBUILD_OUT"])

# Budgets copied from the frozen per-unit configs the `miniswe_spl_both` results
# were produced with (spl_reproducibility_package/exp3_swebench/results/
# random218/configs/unit_*.json).  These are the *compact* `both` values, not
# the larger budget-probe ones: rebuilding `both` from the same sample dir with
# them reproduces the frozen run's `patch_plan.md` and `spl_context.txt`
# byte-for-byte, and reproduces its single inlined card. The larger probe values
# produce two cards and four truncation markers, which the frozen prompt does not
# have.  Matching the frozen arm is the whole point, so these are the values.
CONFIG = {
    "mini_spl_protocol": "spl_guarded_protocol",
    "mini_spl_controller_cards": 4,
    "mini_spl_controller_spl_chars": 750,
    "mini_spl_prompt_cards": 2,
    "mini_source_bound_source_chars": 1400,
    "mini_spl_both_controller_cards": 3,
    "mini_spl_both_controller_spl_chars": 600,
    "mini_spl_both_prompt_cards": 1,
    "mini_spl_both_source_bound_source_chars": 1200,
    "mini_spl_entry_limit": 8,
    "mini_spl_entry_max_chars": 1800,
    "conditions": [MODE],
}


def sample_dir_for(instance_id: str) -> Path:
    return (
        HERE
        / "data/RQ3/inputs/precomputed_random218_deepseek-v4-flash/working/round_01"
        / instance_id
    )


def build(sample_dir: Path, mode: str) -> dict[str, str]:
    return {
        "addendum": base.load_prompt_addendum(mode, CONFIG),
        "controller_block": base.build_spl_controller_block(sample_dir, mode, CONFIG),
        "cards_document": base.build_source_bound_cards_document(sample_dir, mode, CONFIG),
        "payload_files": base.build_payload_files(sample_dir, mode, CONFIG),
    }


def report(label: str, text: str) -> dict:
    """Coarse re-scan of a delivered string.

    Tags are never allowed.  A bare `SPL` token is only a finding if the
    builder's own `assert_clean` would reject it, and any run that gets this far
    has already passed that check for every string here -- so the residual count
    printed below is informational: it says how much *source* vocabulary (sympy
    codegen's per-line `SPL`, a Django card calling the SQL compiler an "SPL
    compiler") the condition legitimately carries, not that something leaked.
    `assert_clean` is the gate; this is the receipt.
    """
    tags = U.tag_hits(text)
    residual = U.residual_spl_mentions(text)
    print(
        f"    {label:<28} chars={len(text):>7,}  tokens={U.token_count(text):>7,}  "
        f"tags={len(tags)}  bare_SPL_from_source={len(residual)}"
    )
    if residual:
        print(f"        carried source vocabulary: {sorted(set(residual))[:10]}")
    return {"chars": len(text), "tokens": U.token_count(text), "tags": tags, "residual": residual}


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    summary: dict[str, dict] = {}

    for instance in SAMPLES:
        sample_dir = sample_dir_for(instance)
        if not sample_dir.is_dir():
            print(f"!! sample dir missing: {sample_dir}")
            continue
        print(f"\n{'='*78}\n{instance}\n{'='*78}")

        # --- tagged arm, using the frozen code exactly as-is -----------------
        tagged = build(sample_dir, BOTH)

        # --- unstructured arm ------------------------------------------------
        import run_unstructured as RU

        RU._install()
        unstructured = build(sample_dir, MODE)
        # restore the frozen module so the next iteration starts clean
        import importlib

        importlib.reload(base)
        base_modes = None  # noqa: F841

        print("  TAGGED (miniswe_spl_both):")
        t_stats = {
            key: report(key, val)
            for key, val in tagged.items()
            if isinstance(val, str)
        }
        print("  UNSTRUCTURED:")
        u_stats = {
            key: report(key, val)
            for key, val in unstructured.items()
            if isinstance(val, str)
        }
        for key, val in unstructured["payload_files"].items():
            if isinstance(val, str):
                tag_n = len(U.tag_hits(val))
                res = len(U.residual_spl_mentions(val))
                flag = "   <-- PROBLEM" if tag_n else ""
                print(
                    f"    payload {key.replace('/tmp/spl_tools/',''):<24} "
                    f"chars={len(val):>7,} tags={tag_n} bare_SPL_from_source={res}{flag}"
                )

        # --- what actually changed ------------------------------------------
        diff = list(
            difflib.unified_diff(
                tagged["controller_block"].splitlines(),
                unstructured["controller_block"].splitlines(),
                fromfile="tagged/controller_block",
                tofile="unstructured/controller_block",
                lineterm="",
                n=0,
            )
        )
        (OUT / f"{instance}.controller_block.diff").write_text("\n".join(diff), encoding="utf-8")
        print(f"  controller-block diff: {len(diff)} lines -> {instance}.controller_block.diff")

        for arm, data in (("tagged", tagged), ("unstructured", unstructured)):
            arm_dir = OUT / instance / arm
            arm_dir.mkdir(parents=True, exist_ok=True)
            (arm_dir / "addendum.md").write_text(data["addendum"], encoding="utf-8")
            (arm_dir / "controller_block.md").write_text(data["controller_block"], encoding="utf-8")
            (arm_dir / "cards_document.md").write_text(data["cards_document"], encoding="utf-8")
            for name, body in data["payload_files"].items():
                if isinstance(body, str):
                    (arm_dir / Path(name).name).write_text(body, encoding="utf-8")

        summary[instance] = {
            "tagged": t_stats,
            "unstructured": u_stats,
            "controller_diff_lines": len(diff),
        }

    (OUT / "drybuild_summary.json").write_text(
        json.dumps(summary, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    print(f"\nwrote {OUT}")

    problems = []
    for instance, data in summary.items():
        for arm in ("tagged", "unstructured"):
            for key, row in data[arm].items():
                # Only notation is a hard failure here.  Bare `SPL` is judged by
                # `assert_clean` inside the builder, with the source text it came
                # from; re-judging it without that context would fail every unit
                # whose domain uses the letters (sympy codegen, Django's SQL
                # compiler) and say nothing about leakage.
                if arm == "unstructured" and row["tags"]:
                    problems.append(f"{instance}/{arm}/{key}: tags={row['tags']}")
    if problems:
        print("\nPROBLEMS:")
        for p in problems:
            print("  ", p)
    else:
        print("\nRESULT: PASS -- unstructured arms are tag-free and the builder's own")
        print("        vocabulary audit accepted every delivered string")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
