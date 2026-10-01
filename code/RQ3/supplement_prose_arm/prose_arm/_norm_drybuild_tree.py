"""Normalise a dry-build snapshot tree so two runs can be compared for content.

`_spl_matched_terms` returns a `set` of matched terms, so the order they are
printed in varies between runs of the *same* code (see the fairness audit).  That
noise swamps a byte comparison of the trees, so both sides are put through the
same normaliser: matched-term lists are sorted, JSON keys are emitted sorted.
Everything else -- the prose, the checkpoints, the cards, the tool scripts -- is
left exactly as written.

Usage:
  python $PROJECT_ROOT/code/RQ3/supplement_2026-09-13/untagged_arm/_norm_drybuild_tree.py SRC DST
"""

from __future__ import annotations

import json
import re
import shutil
import sys
from pathlib import Path

# The `.controller_block.diff` files carry the same lines prefixed by `+`/`-`,
# so the marker is allowed for and preserved.
RE_MATCHED = re.compile(r"^([+-]?Matched terms:\s*)(.*)$")

# `--mask-matched` drops the matched-term payload outright.  Two runs of the
# *same* code disagree on which twelve terms survive `matched[:12]`, because
# `score_spl_entry` iterates a `set` and truncates afterwards; masking is what
# makes "the change is text-neutral" a checkable statement rather than a claim.
MASK = False


def normalise_text(text: str) -> str:
    out = []
    for line in text.splitlines():
        m = RE_MATCHED.match(line)
        if m:
            terms = [t.strip() for t in m.group(2).split(",") if t.strip()]
            line = m.group(1) + ("<masked>" if MASK else ", ".join(sorted(terms)))
        out.append(line)
    return "\n".join(out) + "\n"


def normalise_json(text: str) -> str:
    try:
        data = json.loads(text)
    except json.JSONDecodeError:
        return normalise_text(text)

    def walk(node):
        if isinstance(node, dict):
            for key, value in node.items():
                if key == "matched_terms" and isinstance(value, list):
                    node[key] = ["<masked>"] if MASK else sorted(str(v) for v in value)
                else:
                    walk(value)
        elif isinstance(node, list):
            for value in node:
                walk(value)

    walk(data)
    return json.dumps(data, ensure_ascii=False, indent=2, sort_keys=True) + "\n"


def main(argv: list[str]) -> int:
    global MASK
    MASK = "--mask-matched" in argv
    rest = [a for a in argv[1:] if not a.startswith("--")]
    src, dst = Path(rest[0]), Path(rest[1])
    if dst.exists():
        shutil.rmtree(dst)
    for path in sorted(src.rglob("*")):
        if not path.is_file():
            continue
        rel = path.relative_to(src)
        target = dst / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        text = path.read_text(encoding="utf-8")
        if path.suffix == ".json":
            target.write_text(normalise_json(text), encoding="utf-8")
        else:
            target.write_text(normalise_text(text), encoding="utf-8")
    print(f"normalised {src} -> {dst}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
