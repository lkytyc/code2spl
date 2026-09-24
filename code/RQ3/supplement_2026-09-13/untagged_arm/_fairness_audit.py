"""Audit whether the supplement's arm differs from frozen `miniswe_spl_both` only in notation.

The claim under test: every agent-visible artifact of the unstructured arm is the
frozen artifact with SPL tag notation removed -- nothing added, nothing dropped,
no budget changed.

A raw line diff cannot test that, because the prose renderer also reflows text,
so line counts move for reasons that have nothing to do with content.  Each
artifact is therefore compared in its own terms:

  * markdown / text -- both sides are notation-normalized and whitespace-collapsed,
    then split into content units (sentences and bullets) and compared as
    multisets.  Anything left over is a real content difference.
  * JSON            -- compared structurally, key by key, entry by entry.
  * Python tools    -- the declared substitution list is re-checked mechanically;
    the remainder of the file must still match.

Budgets, card selection and token volumes are checked separately, because a
budget difference would not show up as a text diff at all -- which is exactly the
kind of unfairness a diff would hide.

Read-only over the frozen tree.  Usage:
  python $PROJECT_ROOT/code/RQ3/supplement_2026-09-13/untagged_arm/_fairness_audit.py [unit ...]
"""

from __future__ import annotations

import collections
import json
import os
import re
import sys
from pathlib import Path
from typing import Any

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
TRIAL = HERE / "data/raw_results/exp3_swebench/random218_untagged_both/units"
CONFIG_ROOT = HERE / "data/raw_results/exp3_swebench/random218_untagged_both/configs"
FROZEN_CONFIGS = (
    ROOT
    / "spl_reproducibility_package/exp3_swebench/results/random218/configs"
)
PROMPTS = HERE / "frozen_original_prompts"

UNITS = [
    "unit_001_pydata__xarray-3151",
    "unit_095_astropy__astropy-13579",
    "unit_201_django__django-14140",
    "unit_099_pytest-dev__pytest-10051",
]

TEXT_ARTIFACTS = [
    "mini_config.yaml",
    "payload_tools/patch_plan.md",
    "payload_tools/source_bound_cards.md",
    "payload_tools/spl_context.txt",
]
JSON_ARTIFACTS = ["payload_tools/spl_index.json"]
TOOL_ARTIFACTS = ["payload_tools/spl_search.py", "payload_tools/spl_show.py"]

# Budget wording must survive verbatim or the arms are not comparable.
BUDGET_PATTERNS = [
    r"at most \d+ (?:SPL )?cards?",
    r"only the \d+ (?:SPL )?cards?",
    r"\b\d+ characters\b",
    r"[Mm]aximum of \d+",
]


def long(path: Path | str) -> str:
    text = str(path)
    if os.name != "nt" or text.startswith("\\\\?\\"):
        return text
    return "\\\\?\\" + str(Path(text).absolute())


def exists(path: Path) -> bool:
    """Long-path-safe existence check.

    `Path.is_file()` answers False for the `scikit-learn__scikit-learn-*` and
    `matplotlib__matplotlib-*` result paths, which are longer than MAX_PATH.
    """
    try:
        return Path(long(path)).is_file()
    except OSError:
        return False


def read(path: Path) -> str:
    with open(long(path), encoding="utf-8", errors="replace") as fh:
        return fh.read()


_RE_BULLET = re.compile(r"^(\s*[-*]\s*)(.*)$")


def normalize(text: str) -> str:
    """Notation-normalize, then collapse all whitespace.

    Applied to *both* sides, so it is idempotent on the supplement's own output;
    running it on the frozen side therefore measures exactly one thing -- whether
    removing notation is sufficient to explain the difference.

    Bullets go through the same `strip_checkpoint` the builder uses.  Normalizing
    them any other way would be asymmetric: the builder turns `[COMMAND X RESULT
    y]` into `X; results: y`, so a normalizer that merely deleted `RESULT` would
    report every checkpoint as a content difference.
    """
    out = str(text)
    for scope in ("plan", "card", "controller", "document", "index", "config"):
        out = U.neutralize(out, scope, strict=False)

    lines: list[str] = []
    for line in out.splitlines():
        match = _RE_BULLET.match(line)
        if match and (U.tag_hits(line) or "RESULT" in line):
            body = match.group(2)
            try:
                body = U.strip_checkpoint(body)
            except AssertionError:
                # Embedded YAML line-continuations can leave a tag mid-line; the
                # builder never sees those (the config is rewritten whole), so a
                # plain strip is the right fallback here.
                body = U.strip_tags(body)
            lines.append(match.group(1) + body)
        else:
            lines.append(line)
    out = "\n".join(lines)
    out = re.sub(r"\s+", " ", out)
    return out.strip()


def content_units(text: str) -> list[str]:
    """Sentences and bullets, whitespace-free -- the comparable content."""
    normalized = normalize(text)
    # Keep bullets/sentences whole; split only on hard terminators.
    parts = re.split(r"(?<=[.;:!?])\s+(?=[A-Z\-\[<])", normalized)
    return [re.sub(r"\s+", " ", p).strip() for p in parts if len(p.strip()) > 2]


def compare_text(frozen: str, mine: str) -> dict:
    a, b = collections.Counter(content_units(frozen)), collections.Counter(content_units(mine))
    missing = list((a - b).elements())
    added = list((b - a).elements())
    return {"frozen_units": sum(a.values()), "mine_units": sum(b.values()),
            "missing": missing, "added": added}


_RE_PATH = re.compile(r"[\w./\\-]+\.(?:py|md|txt|cfg|yaml|json|rst)")
# Code-shaped tokens only.  A bare lowercase word is prose and moves under any
# reflow, which would drown the signal in noise -- the first version of this
# audit reported "SIGNAL LOST: same" as if it mattered.  Requiring an underscore
# or a dot restricts the comparison to things that can actually be localized to.
_RE_IDENT = re.compile(r"\b(?:[A-Za-z_][A-Za-z0-9_]*_[A-Za-z0-9_]+|[A-Za-z_]\w*\.[A-Za-z_]\w*)\b")
_RE_NUM = re.compile(r"\b\d+(?:\.\d+)?\b")


# The tag grammar itself.  These tokens are UPPER_SNAKE, so the identifier regex
# matches them, but their disappearance is the treatment rather than a content
# loss -- removing them is what "unstructured" means.
_TAG_VOCABULARY = {
    "DEFINE_WORKER", "END_WORKER", "INPUTS", "END_INPUTS", "OUTPUTS",
    "END_OUTPUTS", "MAIN_FLOW", "END_MAIN_FLOW", "SEQUENTIAL_BLOCK",
    "END_SEQUENTIAL_BLOCK", "ALTERNATIVE_FLOW", "END_ALTERNATIVE_FLOW",
    "EXCEPTION_FLOW", "END_EXCEPTION_FLOW", "COMMAND", "CONDITION", "RETURN",
    "THROW", "LOG", "REF", "CLASS", "SPL",
}


def is_notation(signal: str) -> bool:
    """True when a signal is tag notation rather than content."""
    token = signal.split(":", 1)[1] if ":" in signal else signal
    return token in _TAG_VOCABULARY


def signals(text: str) -> collections.Counter:
    """Atomic content: paths, code identifiers, numbers.

    Rendering reshapes sentences, so a sentence-level comparison cannot tell
    "paraphrased" from "lost".  These atoms are what localization actually
    depends on -- a function name, a file path, a line range -- so if they all
    survive, the renderer reorganised the text without dropping content.
    """
    normalized = normalize(text)
    found: collections.Counter = collections.Counter()
    found.update(f"path:{m}" for m in _RE_PATH.findall(normalized))
    found.update(f"num:{m}" for m in _RE_NUM.findall(normalized))
    found.update(f"ident:{m}" for m in _RE_IDENT.findall(normalized))
    return found


def flatten(node: Any, prefix: str = "") -> dict[str, Any]:
    out: dict[str, Any] = {}
    if isinstance(node, dict):
        for key, value in node.items():
            out.update(flatten(value, f"{prefix}.{key}"))
    elif isinstance(node, list):
        for index, value in enumerate(node):
            out.update(flatten(value, f"{prefix}[{index}]"))
    else:
        out[prefix] = node
    return out


def compare_json(frozen: str, mine: str) -> dict:
    try:
        a, b = json.loads(frozen), json.loads(mine)
    except json.JSONDecodeError as exc:
        return {"error": str(exc), "missing": [], "added": []}
    fa, fb = flatten(a), flatten(b)
    missing, added, changed = [], [], []
    for key, value in fa.items():
        if key not in fb:
            missing.append(f"{key} = {str(value)[:80]}")
        elif fb[key] != value:
            changed.append(f"{key}: {str(value)[:60]!r} -> {str(fb[key])[:60]!r}")
    for key, value in fb.items():
        if key not in fa:
            added.append(f"{key} = {str(value)[:80]}")
    return {"missing": missing, "added": added, "changed": changed}


_RE_EXCERPT = re.compile(
    r"Editable source excerpt \d+:([^\n]*)\n```[a-z]*\n(.*?)\n```", flags=re.S
)


def excerpts(text: str) -> list[tuple[str, str]]:
    """The editable source blocks, which are the decision-relevant part of a card.

    These must be byte-identical between arms: they are the code the agent is
    told to patch, so any drift here would be a content difference no amount of
    notation-stripping could excuse.
    """
    return [(header.strip(), body) for header, body in _RE_EXCERPT.findall(text)]


def budget_fingerprint(text: str) -> dict[str, int]:  # noqa: D103 (see module docstring)
    found: collections.Counter = collections.Counter()
    for pattern in BUDGET_PATTERNS:
        for match in re.finditer(pattern, text):
            found[match.group(0)] += 1
    return dict(found)


def denotate(text: str) -> str:
    out = str(text)
    for scope in ("plan", "card", "controller", "document", "index", "config"):
        out = U.neutralize(out, scope, strict=False)
    return out


# Routing keys name the arm or its own output paths; they are supposed to differ.
CONFIG_ROUTING_LEAVES = {"out_dir", "run_id", "condition", "mode", "payload_dir"}


def compare_parsed_config(frozen_text: str, mine_text: str) -> dict:
    """Compare `mini_config.yaml` as the agent receives it, i.e. after parsing.

    Raw-text comparison is misleading here: the frozen runner writes the prompt
    template with escaped `\\n`, so the identical agent-visible string spans one
    line on one side and many on the other.  Parsing first removes that artifact
    and leaves only real value differences -- the model, temperature, step limit,
    protocol and budgets as the agent actually experiences them.
    """
    import yaml

    try:
        a, b = yaml.safe_load(frozen_text), yaml.safe_load(mine_text)
    except yaml.YAMLError as exc:
        return {"error": str(exc)}
    fa, fb = flatten(a), flatten(b)
    only_frozen = sorted(set(fa) - set(fb))
    only_mine = sorted(set(fb) - set(fa))
    changed, notation = [], []
    for key in sorted(set(fa) & set(fb)):
        if fa[key] == fb[key]:
            continue
        if key.rsplit(".", 1)[-1] in CONFIG_ROUTING_LEAVES:
            continue
        x, y = fa[key], fb[key]
        if isinstance(x, str) and isinstance(y, str):
            strip = lambda s: " ".join(denotate(s).split())
            if strip(x) == strip(y):
                notation.append(key)
                continue
        changed.append(key)
    return {
        "equal": len(set(fa) & set(fb)) - len(changed) - len(notation),
        "total": len(set(fa) & set(fb)),
        "notation_only": notation,
        "changed": changed,
        "only_frozen": only_frozen,
        "only_mine": only_mine,
        # A change that is *not* explained by the arm's vocabulary would be a real
        # config difference, so the diff body is kept for each one.  An empty
        # string means the values agree once notation is set aside.
        "changed_detail": {key: vocabulary_diff(fa[key], fb[key]) for key in changed},
    }


# The template = the arm's own workflow section + generated scaffold + rendered
# payload.  Only the first two are hand-authored, so only they can carry an
# unintended instruction change; the payload is certified artifact by artifact.
# Splitting at the plan heading separates the authored part from the rendered one.
_PAYLOAD_MARKERS = ("## SPL Patch Production Plan", "## Patch Production Plan")


def split_authored(template: str) -> str:
    """The hand-authored part of a template: everything before the payload."""
    cut = len(template)
    for marker in _PAYLOAD_MARKERS:
        found = template.find(marker)
        if found != -1:
            cut = min(cut, found)
    return template[:cut]


def swap_workflow(template: str, old_prompt: str, new_prompt: str) -> str | None:
    """Replace a template's workflow section with another arm's prompt file.

    The section is located by its own heading and runs to the next `## ` heading,
    which is the generated scaffold.  Doing the swap by block rather than by
    word-level diff matters: a word-level rewrite of `SPL` would fire on every
    occurrence in the file, including ones the arm's prompt never touched, and
    the resulting "residual" would be an artifact of the method rather than a
    property of the templates.
    """
    heading = old_prompt.splitlines()[0].strip()
    start = template.find(heading)
    if start == -1:
        return None
    end = template.find("\n## ", start + len(heading))
    if end == -1:
        return None
    return template[:start] + new_prompt.strip("\n") + "\n" + template[end + 1:]


def compare_template(frozen: str, mine: str, frozen_prompt: str,
                     mine_prompt: str) -> dict:
    """Do the two templates differ, once the arm's own prompt section is used?

    The authored part of the template is compared on its own, because it is the
    only place an instruction could be added, dropped or reworded without the
    artifact-level payload comparison noticing.  The test is a substitution, not
    a diff: take the frozen template, swap in the arm's workflow section, and see
    whether what remains matches.  If it does, the scaffold around the section is
    untouched and every remaining difference is in the prompt pair -- which is
    diffed and reviewed separately.
    """
    import difflib

    collapse = lambda s: " ".join(denotate(s).split())
    authored_frozen = split_authored(frozen)
    authored_mine = split_authored(mine)

    swapped = swap_workflow(authored_frozen, frozen_prompt, mine_prompt)
    if swapped is None:
        # Some units carry no workflow section at all -- django-15127 builds an
        # empty controller block, so neither template has one and there is
        # nothing to swap.  That is agreement, not a failure to check, so it is
        # reported as not applicable with a full-shaped record.
        return {
            "error": "workflow heading absent from both templates",
            "authored_frozen_chars": len(authored_frozen),
            "authored_mine_chars": len(authored_mine),
            "residual": [],
            "missing_words": [],
            "added_words": [],
            "explained": None,
        }
    transformed, target = collapse(swapped), collapse(authored_mine)

    missing = collections.Counter(transformed.split()) - collections.Counter(
        target.split()
    )
    added = collections.Counter(target.split()) - collections.Counter(
        transformed.split()
    )
    residual = [
        " ".join(transformed.split()[i1:i2])
        + (" | " + " ".join(target.split()[j1:j2]) if tag == "replace" else "")
        for tag, i1, i2, j1, j2 in difflib.SequenceMatcher(
            None, transformed.split(), target.split(), autojunk=False
        ).get_opcodes()
        if tag != "equal"
    ]
    return {
        "authored_frozen_chars": len(authored_frozen),
        "authored_mine_chars": len(authored_mine),
        "residual": residual,
        "missing_words": sorted(missing.elements()),
        "added_words": sorted(added.elements()),
        "explained": not missing and not added,
    }


def vocabulary_diff(a, b) -> str:
    """The unified diff between two values, or "" if notation explains them.

    Every remaining difference in `agent.instance_template` is the arm's own
    naming -- "SPL"/"checkpoint"/"card" on one side, "behavior notes"/"note" on
    the other.  Keeping the diff makes that claim checkable instead of asserted;
    an empty string means the shared normalizer already reconciled the two.
    """
    import difflib

    if not isinstance(a, str) or not isinstance(b, str):
        return f"{a!r} -> {b!r}"
    strip = lambda s: " ".join(denotate(s).split())
    if strip(a) == strip(b):
        return ""
    return "\n".join(
        difflib.unified_diff(
            a.splitlines(), b.splitlines(), "frozen", "mine", lineterm="", n=0
        )
    )


def worker_names(text: str) -> list[str]:
    """Card headings, in order -- which cards were selected, and how many."""
    return re.findall(r"^#+\s*(?:SPL )?Controller Card\s*(\d+)", text, flags=re.M)


def index_entries(text: str) -> list[str]:
    try:
        data = json.loads(text)
    except json.JSONDecodeError:
        return []
    return [str(e.get("worker_name") or "") for e in (data.get("entries") or [])]


# The index records why each entry matched, and the renderer renames the notation
# in those labels along with everything else.  The rename is the treatment; what
# must not change is *which* terms matched, because that is what the ranker saw.
# A term is `<token>:<role>/<role>/...`, and only the role path carries notation.
_TERM_ROLE_RENAME = {"spl": "notes"}


def normalize_term(term: str) -> str:
    """Map a matched-term label onto its notation-free equivalent."""
    token, sep, roles = str(term).partition(":")
    if not sep:
        return token
    parts = [_TERM_ROLE_RENAME.get(p, p) for p in roles.split("/")]
    return f"{token}:" + "/".join(parts)


def matched_term_sets(text: str) -> list[set[str]]:
    try:
        data = json.loads(text)
    except json.JSONDecodeError:
        return []
    out = []
    for entry in data.get("entries") or []:
        out.append({normalize_term(t) for t in (entry.get("matched_terms") or [])})
    return out


def main(argv: list[str]) -> int:
    units = argv[1:] or UNITS
    report = []
    for unit in units:
        instance = unit.split("_", 2)[2]
        fz = FROZEN_UNITS / unit / "runs" / instance / TAGGED
        my = TRIAL / unit / instance / MODE
        print("=" * 78)
        print(f"{instance}")
        print("=" * 78)
        entry: dict[str, Any] = {"instance": instance, "residual": 0}

        for rel in TEXT_ARTIFACTS:
            # One artifact can legitimately be absent on one or both sides: for
            # django-15127 the controller block is empty, so neither arm writes a
            # `patch_plan.md`.  Symmetric absence is not a difference; asymmetric
            # absence is, and is recorded as one.
            fz_has, my_has = exists(fz / rel), exists(my / rel)
            if not fz_has and not my_has:
                print(f"  {rel:<45} absent in both arms")
                continue
            if fz_has != my_has:
                side = "supplement" if my_has else "frozen"
                print(f"  {rel:<45} PRESENT ONLY IN {side.upper()}")
                entry["residual"] += 1
                continue
            frozen_text, mine_text = read(fz / rel), read(my / rel)
            cmp = compare_text(frozen_text, mine_text)
            residual = len(cmp["missing"]) + len(cmp["added"])
            entry["residual"] += residual

            # The decisive measure: did any atomic content go missing?  Tag
            # keywords are separated out, because their absence is the treatment.
            fa, fb = signals(frozen_text), signals(mine_text)
            lost_all = fa - fb
            lost = collections.Counter(
                {k: v for k, v in lost_all.items() if not is_notation(k)}
            )
            lost_notation = sum(lost_all.values()) - sum(lost.values())
            gained = collections.Counter(
                {k: v for k, v in (fb - fa).items() if not is_notation(k)}
            )
            entry["signals_lost"] = entry.get("signals_lost", 0) + sum(lost.values())
            entry["signals_gained"] = entry.get("signals_gained", 0) + sum(
                gained.values()
            )
            entry["signals_notation"] = entry.get("signals_notation", 0) + lost_notation
            # Character volume, per artifact, on both sides.  The two arms are
            # given the same character budget, so equal sizes here mean the budget
            # was honoured; the interesting consequence is that prose spends
            # fewer characters on notation and therefore fits more code
            # identifiers into the same budget.  That direction matters, so it is
            # measured rather than left implicit.
            lengths = (len(frozen_text), len(mine_text))
            entry.setdefault("lengths", {})[rel] = lengths
            entry.setdefault("gained_detail", {})[rel] = sorted(gained.elements())[:12]
            print(f"  {rel:<40} units {cmp['frozen_units']:>4} -> {cmp['mine_units']:>4}  "
                  f"chars {lengths[0]:>6} -> {lengths[1]:>6}  "
                  f"residual={residual}  content signals lost={sum(lost.values())} "
                  f"gained={sum(gained.values())} "
                  f"(tag keywords removed={lost_notation})")
            for text in list(lost.elements())[:6]:
                print(f"      CONTENT LOST: {text}")
            for text in list(gained.elements())[:3]:
                print(f"      signal added: {text}")
            for text in cmp["missing"][:2]:
                print(f"      MISSING (sentence): {text[:130]}")

        for rel in JSON_ARTIFACTS:
            if not (exists(fz / rel) and exists(my / rel)):
                print(f"  {rel:<40} absent in one arm")
                continue
            cmp = compare_json(read(fz / rel), read(my / rel))
            residual = len(cmp.get("missing", [])) + len(cmp.get("added", [])) + len(
                cmp.get("changed", [])
            )
            entry["residual"] += residual
            print(f"  {rel:<40} field-diffs missing={len(cmp.get('missing', []))} "
                  f"added={len(cmp.get('added', []))} changed={len(cmp.get('changed', []))}")
            for text in (cmp.get("missing") or [])[:3]:
                print(f"      MISSING: {text}")
            for text in (cmp.get("added") or [])[:3]:
                print(f"      ADDED:   {text}")
            for text in (cmp.get("changed") or [])[:3]:
                print(f"      CHANGED: {text}")

        for rel in TOOL_ARTIFACTS:
            if not (exists(fz / rel) and exists(my / rel)):
                print(f"  {rel:<40} absent in one arm")
                continue
            a, b = read(fz / rel), read(my / rel)
            entry["residual"] += 0 if a != b else -1  # unchanged tool = expected
            print(f"  {rel:<40} {'UNCHANGED' if a == b else 'rewired (declared)'}"
                  f"  {len(a)} -> {len(b)} bytes")

        cfg_f, cfg_m = read(fz / "mini_config.yaml"), read(my / "mini_config.yaml")
        bf, bm = budget_fingerprint(cfg_f), budget_fingerprint(cfg_m)
        same = bf == bm
        entry["budget_equal"] = same
        print(f"  budget wording identical: {same}")
        if same:
            for phrase, count in sorted(bf.items()):
                print(f"      '{phrase}' x{count}")

        parsed = compare_parsed_config(cfg_f, cfg_m)
        entry["parsed_config"] = {
            "keys_equal": parsed.get("equal"),
            "keys_total": parsed.get("total"),
            "notation_only": parsed.get("notation_only"),
            "changed": parsed.get("changed"),
            "only_frozen": parsed.get("only_frozen"),
            "only_mine": parsed.get("only_mine"),
            "changed_detail": parsed.get("changed_detail"),
        }
        import yaml

        # The parsed values, not the YAML text: the frozen runner escapes the
        # template's newlines, so the raw file is one long line there and many
        # here.  Parsing first makes the two comparable as the agent sees them.
        template = compare_template(
            yaml.safe_load(cfg_f)["agent"]["instance_template"],
            yaml.safe_load(cfg_m)["agent"]["instance_template"],
            read(PROMPTS / f"{TAGGED}.md"), read(PROMPTS / f"{MODE}.md"),
        )
        entry["template_explained"] = template["explained"]
        entry["template_missing_words"] = template["missing_words"]
        entry["template_added_words"] = template["added_words"]
        if template.get("error"):
            entry["template_error"] = template["error"]
        print(f"  instance_template authored part: "
              f"{template['authored_frozen_chars']} -> "
              f"{template['authored_mine_chars']} chars, "
              f"vocabulary explains it: {template['explained']}"
              + (f" ({template['error']})" if template.get("error") else ""))
        if template["explained"] is False:
            print(f"      MISSING WORDS: {template['missing_words'][:20]}")
            print(f"      ADDED WORDS:   {template['added_words'][:20]}")
            for text in template["residual"][:6]:
                print(f"      RESIDUAL: {text[:150]}")

        # `instance_template` is the arm's prompt file plus rendered payload, so
        # the parsed-key check above flags it by design; `template_explained`
        # is the check that decides whether that flag is benign.
        unexplained = [
            key for key, diff in (parsed.get("changed_detail") or {}).items()
            if diff and key != ".agent.instance_template"
        ]
        entry["parsed_config_unexplained"] = unexplained
        print(f"  config parsed: {parsed.get('equal')}/{parsed.get('total')} keys equal, "
              f"{len(parsed.get('notation_only') or [])} notation-only, "
              f"{len(parsed.get('changed') or [])} changed "
              f"(unexplained by the arm's vocabulary: {unexplained or 'NONE'})")
        for key in (parsed.get("changed") or []):
            if key in unexplained:
                print(f"      UNEXPLAINED {key}")
                for line in (parsed["changed_detail"][key] or "").splitlines()[:12]:
                    print(f"        {line}")

        for rel, sig in (
            ("payload_tools/source_bound_cards.md", worker_names),
            ("payload_tools/spl_index.json", index_entries),
        ):
            if not (exists(fz / rel) and exists(my / rel)):
                print(f"  selection ({rel.split('/')[-1]}): absent in one arm")
                continue
            a, b = sig(read(fz / rel)), sig(read(my / rel))
            entry[f"selection:{rel}"] = a == b
            print(f"  selection identical ({rel.split('/')[-1]}): {a == b} "
                  f"(n={len(a)}/{len(b)})")

        # The ranker's input, per entry: the same terms must have matched, or the
        # arms were not fed the same evidence and the selection agreement above
        # would be a coincidence rather than a property.
        ta = matched_term_sets(read(fz / "payload_tools/spl_index.json"))
        tb = matched_term_sets(read(my / "payload_tools/spl_index.json"))
        # `exists` was checked above; both arms always ship an index.
        term_ok = ta == tb
        entry["matched_terms_identical"] = term_ok
        differing = [i for i, (x, y) in enumerate(zip(ta, tb)) if x != y]
        print(f"  matched-term sets identical: {term_ok} "
              f"(entries {len(ta)}/{len(tb)}, differing={differing[:5]})")
        for index in differing[:2]:
            print(f"      entry {index}: only frozen={sorted(ta[index] - tb[index])[:4]}"
                  f"  only mine={sorted(tb[index] - ta[index])[:4]}")

        # The source code the agent is told to patch must not drift at all.
        for rel in ("payload_tools/source_bound_cards.md", "payload_tools/patch_plan.md"):
            if not (exists(fz / rel) and exists(my / rel)):
                print(f"  editable excerpts ({rel.split('/')[-1]}): absent in one arm")
                continue
            a = excerpts(read(fz / rel))
            b = excerpts(read(my / rel))
            same = a == b and len(a) == len(b)
            entry[f"excerpts:{rel}"] = same
            print(f"  editable excerpts identical ({rel.split('/')[-1]}): {same} "
                  f"(n={len(a)}/{len(b)})")
            if not same:
                for (ha, _), (hb, _) in zip(a, b):
                    if ha != hb:
                        print(f"      header drift: {ha!r} vs {hb!r}")

        # Every config key is compared against the frozen one, so "the settings
        # were not tuned for this arm" is a checked fact rather than a promise.
        # Only routing keys may differ; a change to model, temperature, step
        # limit, protocol or any budget would show up here by name.
        allowed = {
            "conditions", "run_dir", "swebench_harness_run_id_prefix",
            "smoke_run_id", "experiment_label", "api_key_pool_file",
        }
        frozen_cfg = json.loads(
            (FROZEN_CONFIGS / f"{unit}.json").read_text(encoding="utf-8")
        )
        mine_cfg = json.loads(
            (CONFIG_ROOT / f"{unit}.json").read_text(encoding="utf-8")
        )
        diffs = {
            key: (frozen_cfg.get(key), mine_cfg.get(key))
            for key in sorted(set(frozen_cfg) | set(mine_cfg))
            if frozen_cfg.get(key) != mine_cfg.get(key)
        }
        unexpected = {k: v for k, v in diffs.items() if k not in allowed}
        entry["config_diffs"] = {k: [str(a), str(b)] for k, (a, b) in diffs.items()}
        entry["config_unexpected"] = sorted(unexpected)
        print(f"  config keys differing from frozen: {sorted(diffs)}")
        print(f"  of which non-routing (would be unfair): {sorted(unexpected) or 'NONE'}")
        for key, (a, b) in sorted(unexpected.items()):
            print(f"      UNFAIR {key}: {a!r} -> {b!r}")

        report.append(entry)
        print(f"  >>> residual content differences: {entry['residual']}\n")

    out = HERE / "data/raw_results/exp3_swebench/random218_untagged_both/audits/fairness_audit.json"
    out.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"total residual content differences across {len(report)} units: "
          f"{sum(e['residual'] for e in report)}")
    print(f"budgets identical in all units: {all(e['budget_equal'] for e in report)}")
    print(f"matched-term sets identical in all units: "
          f"{all(e['matched_terms_identical'] for e in report)}")
    print(f"non-routing config differences: "
          f"{sum(len(e['config_unexpected']) for e in report)}")
    print(f"config values differing beyond the arm's vocabulary: "
          f"{sum(len(e['parsed_config_unexplained']) for e in report)}")
    print(f"content identifiers lost / gained across all artifacts: "
          f"{sum(e['signals_lost'] for e in report)} / "
          f"{sum(e['signals_gained'] for e in report)}")
    excerpt_checks = [v for e in report for k, v in e.items() if k.startswith("excerpts:")]
    excerpt_units = [e["instance"] for e in report if any(k.startswith("excerpts:") for k in e)]
    print(f"editable source excerpts identical: {all(excerpt_checks)} "
          f"({len(excerpt_checks)} artifact checks over {len(excerpt_units)} units; "
          f"units whose cards document is absent in both arms are not compared)")
    # `None` means the unit carries no workflow section in either template, so
    # there was nothing to swap -- it is excluded from the all() rather than
    # counted as either pass or fail.
    judged = [e["template_explained"] for e in report if e["template_explained"] is not None]
    print(f"template scaffold untouched: {all(judged)} "
          f"({len(judged)} units judged, "
          f"{len(report) - len(judged)} with no workflow section to compare)")
    print(f"wrote {out.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
