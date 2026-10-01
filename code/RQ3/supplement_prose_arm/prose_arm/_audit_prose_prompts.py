"""Scan the 218 delivered prompts of both arms for SPL notation and vocabulary.

The fairness audit compares the *artifacts* the two arms build.  This one reads
the string the agent actually received -- the first `user` message of the stored
trajectory -- which is the only place where a payload, a builder or a tool
description could smuggle notation through after the artifact check passed.

The frozen `miniswe_spl_both` arm is scanned alongside as a positive control:
an audit that reported zero hits on both arms would be measuring nothing.

Read-only.  Usage:
  python $PROJECT_ROOT/code/RQ3/supplement_2026-09-13/untagged_arm/_audit_unstructured_prompts.py
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import spl_unstructured as U  # noqa: E402

ROOT = HERE.parents[1]
MODE = "miniswe_spl_unstructured_both"
TAGGED = "miniswe_spl_both"
FROZEN_UNITS = (
    ROOT
    / "spl_reproducibility_package/exp3_swebench/results/random218/units"
)
SUPP_UNITS = HERE / "data/raw_results/exp3_swebench/random218_untagged_both/units"
OUT = HERE / "data/raw_results/exp3_swebench/random218_untagged_both/audits/prompt_leakage_audit.json"

# Vocabulary that only the tagged arm's reading protocol uses.  Each pattern is
# something the conversion is supposed to remove, so a hit is a failure of the
# conversion, not of the agent.
PROTOCOL_PATTERNS = [
    (r"\bspl_control\b", "spl_control section"),
    (r"transition audit", "transition audit protocol"),
    (r"\bSource/SPL\b", "Source/SPL header"),
    (r"the SPL below", "SPL-below pointer"),
    (r"SPL card", "SPL card wording"),
    (r"SPL cards", "SPL cards wording"),
    (r"\bSPL\b", "bare SPL token"),
]


def long(path: Path | str) -> str:
    text = str(path)
    if not text.startswith("\\\\?\\"):
        return "\\\\?\\" + str(Path(text).absolute())
    return text


def read(path: Path) -> str:
    with open(long(path), "r", encoding="utf-8", errors="replace") as fh:
        return fh.read()


def exists(path: Path) -> bool:
    """Existence check that survives a path longer than MAX_PATH.

    The `scikit-learn__scikit-learn-*` and `matplotlib__matplotlib-*` instance
    names push the result path past 260 characters, where `Path.is_file()` says
    False for a file that is plainly there -- which read as "no trajectory" for
    32 units until this was fixed.
    """
    try:
        return Path(long(path)).is_file()
    except OSError:
        return False


def task_prompt(traj_path: Path) -> str:
    """The first user message -- the task prompt with the arm's payload in it.

    `messages[0]` is the shared system template, which is identical in both arms
    and carries no payload; scanning it would make the audit look clean while
    measuring nothing.

    Returns "" for a trajectory with no user turn.  A few instances stop before
    the first exchange, and those units have no prompt to audit -- they are
    counted and named below rather than dropped, because "no prompt scanned" is
    not the same claim as "prompt scanned and clean".
    """
    data = json.loads(read(traj_path))
    for message in data.get("messages") or []:
        if message.get("role") == "user":
            return str(message.get("content") or "")
    return ""


def scan(text: str) -> dict:
    tags = U.tag_hits(text)
    residual = U.residual_spl_mentions(text)
    protocol = {
        label: len(re.findall(pattern, text))
        for pattern, label in PROTOCOL_PATTERNS
        if re.search(pattern, text)
    }
    return {"tags": tags, "residual_spl": residual, "protocol": protocol}


def main() -> int:
    rows = []
    for unit_dir in sorted(SUPP_UNITS.glob("unit_*")):
        unit = unit_dir.name
        instance = unit.split("_", 2)[2]
        mine_traj = unit_dir / instance / MODE / f"{instance}.traj.json"
        frozen_traj = (
            FROZEN_UNITS / unit / "runs" / instance / TAGGED / f"{instance}.traj.json"
        )
        row: dict = {"unit": unit, "instance": instance}
        if not exists(mine_traj):
            row["error"] = "supplement trajectory missing"
            rows.append(row)
            continue
        prompt = task_prompt(mine_traj)
        if not prompt:
            row["empty_trajectory"] = True
            rows.append(row)
            continue
        mine = scan(prompt)
        row["mine"] = mine
        if exists(frozen_traj):
            frozen_prompt = task_prompt(frozen_traj)
            if frozen_prompt:
                frozen = scan(frozen_prompt)
                row["frozen_control"] = {
                    "tags": frozen["tags"],
                    "residual_spl": len(frozen["residual_spl"]),
                    "protocol": frozen["protocol"],
                }
        rows.append(row)

    audited = [r for r in rows if "mine" in r]
    empty = [r for r in rows if r.get("empty_trajectory")]
    clean = [r for r in audited if not r["mine"]["tags"] and not r["mine"]["residual_spl"]
             and not r["mine"]["protocol"]]
    control_hits = [
        r for r in rows
        if r.get("frozen_control", {}).get("tags")
        or r.get("frozen_control", {}).get("residual_spl")
    ]

    print(f"units with a supplement trajectory : {len(rows) - sum(1 for r in rows if 'error' in r)}/{len(rows)}")
    print(f"prompts actually scanned           : {len(audited)}")
    print(f"  no user turn (nothing to scan)   : {len(empty)}: "
          f"{[r['instance'] for r in empty]}")
    print(f"prompts free of tag notation       : "
          f"{sum(1 for r in audited if not r['mine']['tags'])}/{len(audited)}")
    print(f"prompts free of SPL vocabulary     : "
          f"{sum(1 for r in audited if not r['mine']['residual_spl'])}/{len(audited)}")
    print(f"prompts free of protocol wording   : "
          f"{sum(1 for r in audited if not r['mine']['protocol'])}/{len(audited)}")
    print(f"prompts clean on all three         : {len(clean)}/{len(audited)}")
    print(f"positive control: frozen spl_both prompts carrying notation/vocabulary: "
          f"{len(control_hits)}/{sum(1 for r in audited if 'frozen_control' in r)}")
    for row in audited:
        mine = row["mine"]
        if mine["tags"] or mine["residual_spl"] or mine["protocol"]:
            print(f"  LEAK {row['instance']}: tags={mine['tags']} "
                  f"spl={mine['residual_spl'][:6]} protocol={mine['protocol']}")

    OUT.write_text(json.dumps(rows, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"wrote {OUT.relative_to(ROOT)}")
    return 0 if len(clean) == len(audited) and audited else 1


if __name__ == "__main__":
    raise SystemExit(main())
