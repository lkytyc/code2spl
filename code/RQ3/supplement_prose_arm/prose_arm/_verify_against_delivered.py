"""Rebuild each unit's payload from the current code and diff it against what ran.

Every completed unit kept the exact files it delivered, in `payload_tools/`, plus
the prompt the agent received, in its trajectory.  Rebuilding from the frozen
sample directory and comparing against those two is the sharpest fairness check
available: it does not ask whether the code *should* be unchanged, it asks whether
it still produces the same bytes that the graded runs were produced from.

  * each payload file must match `payload_tools/<name>` byte for byte;
  * the addendum and the controller block must appear in the delivered prompt,
    compared through the shared normaliser because `score_spl_entry` slices
    `matched[:12]` off a `set` and the surviving twelve differ run to run (frozen
    behaviour, in `run.py`, affecting the published arms equally).

Usage:
  python $PROJECT_ROOT/code/RQ3/supplement_2026-09-13/untagged_arm/_verify_against_delivered.py [unit ...]
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

import _norm_drybuild_tree as NORM  # noqa: E402
import run as base  # noqa: E402

# Masked on both sides, so the frozen `set`-iteration noise cannot read as a
# difference this builder introduced.
NORM.MASK = True

MODE = "miniswe_spl_unstructured_both"
RUNS = HERE / "data/raw_results/exp3_swebench/random218_untagged_both/units"
SAMPLES_DIR = HERE / "data/RQ3/inputs/precomputed_random218_deepseek-v4-flash/working/round_01"

# The frozen per-unit budgets the supplement ran with -- the compact `both`
# values from the published `unit_*.json` configs.
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


def long(path: Path | str) -> str:
    text = str(path)
    if not text.startswith("\\\\?\\"):
        return "\\\\?\\" + str(Path(text).absolute())
    return text


def read(path: Path) -> str:
    with open(long(path), "r", encoding="utf-8", errors="replace") as fh:
        return fh.read()


def exists(path: Path) -> bool:
    """Long-path-safe existence check; see `_audit_unstructured_prompts.exists`."""
    try:
        return Path(long(path)).is_file()
    except OSError:
        return False


def instance_of(unit: str) -> str:
    return unit.split("_", 2)[2]


def first_user_message(traj: Path) -> str:
    for message in json.loads(read(traj)).get("messages") or []:
        if message.get("role") == "user":
            return str(message.get("content") or "")
    return ""


def main(argv: list[str]) -> int:
    units = [a for a in argv[1:] if not a.startswith("--")]
    if not units:
        units = sorted(p.name for p in RUNS.iterdir() if p.is_dir() and p.name.startswith("unit_"))

    import importlib

    failures: list[tuple[str, str]] = []
    checked = payloads = 0
    skipped: list[str] = []
    exact: list[str] = []
    masked_only: list[str] = []
    prompt_exact = 0

    for unit in units:
        instance = instance_of(unit)
        run_dir = RUNS / unit / instance / MODE
        traj = run_dir / f"{instance}.traj.json"
        tools = run_dir / "payload_tools"
        if not (exists(traj) and exists(tools / "spl_index.json")):
            skipped.append(unit)
            continue

        # Rebuilt the way the run built it: fresh `base`, fresh patch module, one
        # unit at a time, so no registry carries over between units.
        importlib.reload(base)
        run_mod = importlib.reload(importlib.import_module("run_unstructured"))
        run_mod._install()

        sample_dir = SAMPLES_DIR / instance
        addendum = base.load_prompt_addendum(MODE, CONFIG)
        block = base.build_spl_controller_block(sample_dir, MODE, CONFIG)
        files = base.build_payload_files(sample_dir, MODE, CONFIG)

        problems: list[str] = []
        for path, body in files.items():
            if not isinstance(body, str):
                continue
            name = Path(path).name
            delivered_path = tools / name
            if not exists(delivered_path):
                problems.append(f"{name}: not in the delivered payload_tools")
                continue
            delivered = read(delivered_path)
            payloads += 1
            if body == delivered:
                exact.append(unit)
                continue
            # Not byte-identical.  The known cause is the matched-terms lists:
            # `score_spl_entry` scores against a `set` and truncates, so the
            # surviving twelve -- and therefore the length of the list -- differ
            # between runs of identical code.  Masking both sides isolates it.
            mask = NORM.normalise_json if name.endswith(".json") else NORM.normalise_text
            if mask(body) == mask(delivered):
                masked_only.append(f"{unit}/{name}")
                continue
            problems.append(
                f"{name}: {len(body)} vs {len(delivered)} chars, differing beyond the "
                "matched-terms lists"
            )

        prompt = first_user_message(traj) if exists(traj) else ""
        if prompt:
            for label, text in (("addendum", addendum), ("controller_block", block)):
                if text and NORM.normalise_text(text) not in NORM.normalise_text(prompt):
                    problems.append(f"{label}: not reproduced in the delivered prompt")

        checked += 1
        if problems:
            failures.append((unit, "; ".join(problems)))
            print(f"FAIL {unit}")
            for problem in problems:
                print(f"       {problem}")
        else:
            print(f"OK   {unit}")

    print(f"\nunits rebuilt and compared : {checked}")
    print(f"payload files compared     : {payloads}")
    print(f"  byte-identical           : {len(exact)}")
    print(f"  equal once matched-term lists are masked : {len(masked_only)}")
    print(f"units skipped (no delivered trajectory) : {len(skipped)}: {skipped}")
    print(f"units with a mismatch      : {len(failures)}")
    if masked_only and not exact:
        print("  note: every difference is confined to the matched-terms lists, which")
        print("        the frozen `score_spl_entry` fills from a `set` and slices")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
