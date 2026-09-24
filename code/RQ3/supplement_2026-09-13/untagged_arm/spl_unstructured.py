"""Deterministically convert Exp6 SPL payloads into tag-free prose.

This is the Exp3 supplement's representation layer.  It does **not** call a
model: every byte it emits is a pure function of the frozen
`spl_assets/random218_deepseek-v4-flash` material, so the unstructured
condition cannot drift from the tagged one through a second generation pass and
nothing has to be rebuilt (the project constraint is that SPL is never rebuilt).

Two jobs, kept separate so each can be audited on its own:

1. **Notation removal** -- card text goes through
   `experiments/common/spl_card_summary.render_card_as_summary`, the same
   renderer the Exp2 supplement used, which reports a per-card audit
   (`steps` / `alternatives` / `exceptions` counts and any unparsed tag line).
   Its `passthrough` path returns the input unchanged, which is correct for Exp2
   (65 cards there were raw `# JSON_PARSE_ERROR` dumps carrying no tags) but
   wrong here, where the condition must be *provably* tag-free -- so a card that
   passes through while still containing tags is tag-stripped instead and
   flagged as `stripped`.

2. **Label neutralization** -- the strings Exp6's own machinery writes around
   the payload ("## SPL Controller Cards", "Map one SPL checkpoint to visible
   source", ...).  These are *not* notation; they are names.  They have to go
   anyway, because leaving them would tell the agent to look for a representation
   that the payload no longer contains.  The rule applied throughout is:
   **preserve the directive's force, change only the structure-referring noun.**
   Each rule below carries the reason it exists.

Residual-risk check: `residual_spl_mentions` re-scans the finished text for any
surviving `SPL`/`spl` occurrence that is not part of a `/tmp/spl_tools/...`
filesystem path.  Those paths are deliberately left byte-identical to the
tagged arm -- renaming them would introduce a second change and could break the
agent's ability to find the files it is told to open -- so they are allowlisted,
and everything else must be empty.
"""

from __future__ import annotations

import collections
import functools
import re
import sys
from pathlib import Path
from typing import Any

_REPO_ROOT = Path(__file__).resolve().parents[2]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from common.spl_card_summary import render_card_as_summary  # noqa: E402

__all__ = [
    "TAG_PATTERNS",
    "NEUTRALIZE_RULES",
    "token_count",
    "fit_tokens",
    "fit_chars",
    "tag_hits",
    "strip_tags",
    "to_unstructured",
    "to_unstructured_blocks",
    "neutralize",
    "residual_spl_mentions",
    "assert_clean",
]


# --- token accounting -------------------------------------------------------
#
# Characters are the wrong unit here: a bracketed tag costs several tokens for
# the same words that prose spends one or two on, so truncating both at 750
# characters would hand the prose arm more content than the tagged arm.  Budgets
# are therefore compared in tokens.


@functools.lru_cache(maxsize=1)
def _encoder():
    try:
        import tiktoken

        return tiktoken.get_encoding("cl100k_base")
    except Exception:  # pragma: no cover - fallback keeps the module usable
        return None


def token_count(text: str) -> int:
    enc = _encoder()
    if enc is None:
        return len(re.findall(r"\w+|[^\w\s]", str(text)))
    return len(enc.encode(str(text)))


def fit_tokens(text: str, budget: int) -> tuple[str, bool]:
    """Truncate `text` to at most `budget` tokens, cutting on line boundaries.

    The marker is the frozen `trim_text` marker (run.py:358), so the only
    difference between the two arms' truncation is *where* it lands, not how it
    reads.  Cutting on a line boundary can only remove more, never less.
    """
    text = str(text or "")
    if budget <= 0 or token_count(text) <= budget:
        return text, False
    marker = "\n...[truncated]\n"
    keep: list[str] = []
    for line in text.splitlines():
        candidate = "\n".join([*keep, line])
        if token_count(candidate + marker) > budget:
            break
        keep.append(line)
    if not keep:  # a single line already blows the budget
        words = text.split()
        keep = [" ".join(words[: max(1, budget // 2)])]
    return "\n".join(keep) + marker, True


def fit_chars(text: str, budget: int) -> tuple[str, bool]:
    """Truncate `text` to at most `budget` characters, cutting on line boundaries.

    Needed because the frozen builders re-trim the entry text to `spl_chars` on
    the way into the prompt.  Fitting here makes that later trim a no-op, so no
    content is lost to a double truncation.
    """
    text = str(text or "")
    if budget <= 0 or len(text) <= budget:
        return text, False
    marker = "\n...[truncated]\n"
    keep: list[str] = []
    for line in text.splitlines():
        candidate = "\n".join([*keep, line])
        if len(candidate) + len(marker) > budget:
            break
        keep.append(line)
    if not keep:
        keep = [text[: max(1, budget - len(marker))]]
    return "\n".join(keep) + marker, True


# --- notation removal -------------------------------------------------------

TAG_PATTERNS = [
    ("DEFINE_WORKER", r"\[DEFINE_WORKER\s*:"),
    ("END_WORKER", r"\[END_WORKER\]"),
    ("INPUTS", r"\[INPUTS\]"),
    ("END_INPUTS", r"\[END_INPUTS\]"),
    ("OUTPUTS", r"\[OUTPUTS\]"),
    ("END_OUTPUTS", r"\[END_OUTPUTS\]"),
    ("MAIN_FLOW", r"\[MAIN_FLOW\]"),
    ("END_MAIN_FLOW", r"\[END_MAIN_FLOW\]"),
    ("SEQUENTIAL_BLOCK", r"\[SEQUENTIAL_BLOCK\]"),
    ("END_SEQUENTIAL_BLOCK", r"\[END_SEQUENTIAL_BLOCK\]"),
    ("ALTERNATIVE_FLOW", r"\[ALTERNATIVE_FLOW\s*:"),
    ("END_ALTERNATIVE_FLOW", r"\[END_ALTERNATIVE_FLOW\]"),
    ("EXCEPTION_FLOW", r"\[EXCEPTION_FLOW\s*:"),
    ("END_EXCEPTION_FLOW", r"\[END_EXCEPTION_FLOW\]"),
    ("COMMAND", r"\[COMMAND\s+"),
    ("LOG", r"\[LOG\s+\""),
    ("THROW", r"\[THROW\s+"),
    ("REF", r"</?REF>"),
    ("RESULT", r"\s+RESULT\s+"),
]


def tag_hits(text: str) -> list[str]:
    """Names of the tag patterns present in `text` (empty means tag-free)."""
    text = str(text or "")
    return [name for name, pat in TAG_PATTERNS if re.search(pat, text)]


def strip_tags(text: str) -> str:
    """Last-resort removal for cards the prose renderer could not parse.

    Drops the tag keywords and unwraps `<REF>x</REF>` to `x`, keeping the
    payload words, so the condition degrades to "same words, no notation"
    instead of losing content.
    """
    out = str(text or "")
    out = re.sub(r"<REF>\s*(.*?)\s*</REF>", r"\1", out, flags=re.S)
    out = re.sub(r"\s*RESULT\s+", " -> ", out)
    out = re.sub(r"\[DEFINE_WORKER\s*:", "\nFunction:", out)
    for _name, pat in TAG_PATTERNS:
        out = re.sub(pat + r"[^\]]*\]?", "", out)
    out = re.sub(r"\[(?:END_)?[A-Z_]+\]", "", out)
    out = re.sub(r"[ \t]+", " ", out)
    out = re.sub(r"\n{3,}", "\n\n", out)
    return out.strip()


def to_unstructured(
    spl_text: str,
    *,
    token_budget: int | None = None,
    char_budget: int | None = None,
) -> tuple[str, dict[str, Any]]:
    """Turn one frozen SPL card into tag-free prose.

    `token_budget` is the token count the tagged arm spends on the same entry and
    `char_budget` the character cap the frozen builders apply on injection.  Both
    are enforced so the unstructured arm never receives *more* material than the
    control, and so the downstream character trim cannot cut the prose in half.
    """
    original = str(spl_text or "")
    prose, audit = render_card_as_summary(original)
    mode = str(audit.get("mode"))

    if mode != "rendered" and tag_hits(prose):
        prose = strip_tags(original)
        mode = "stripped"
        audit = {**audit, "mode": mode, "reason": "renderer passed through a card that still carried tags"}

    truncated = False
    if token_budget is not None:
        prose, hit = fit_tokens(prose, token_budget)
        truncated = truncated or hit
    if char_budget is not None:
        prose, hit = fit_chars(prose, char_budget)
        truncated = truncated or hit

    leftovers = tag_hits(prose)
    audit = {
        **audit,
        "mode": mode,
        "tag_hits_in_input": tag_hits(original),
        "tag_hits_in_output": leftovers,
        "tokens_in": token_count(original),
        "tokens_out": token_count(prose),
        "truncated": truncated,
        "token_budget": token_budget,
        "char_budget": char_budget,
        "chars_out": len(prose),
    }
    if leftovers:
        raise AssertionError(f"unstructured payload still carries tags {leftovers}: {prose[:200]!r}")
    return prose, audit


_RE_CARD_SPLIT = re.compile(r"(?<=\[END_WORKER\])")
_RE_FILE_HEADER = re.compile(r"^#\s*FILE:\s*(.+?)\s*$", flags=re.M)


def to_unstructured_blocks(text: str, *, char_budget: int | None = None) -> tuple[str, dict[str, Any]]:
    """Convert a whole `spl_context.txt` (a sequence of cards) to prose.

    Used for the in-container payload, which the frozen code injects by trimming
    the raw file to `entry_limit * entry_max_chars`.  The budget is matched in
    tokens against that trimmed tagged text so the two arms carry the same
    information.

    The `# FILE:` header is carried across explicitly.  It sits in front of the
    card rather than inside it, so the card renderer drops it -- and the source
    path is one of the strongest localization signals in the payload.  Losing it
    would handicap this arm with an information deficit that has nothing to do
    with notation, which is exactly what a fair comparison must avoid.
    """
    raw = str(text or "")
    trimmed = raw if not char_budget else raw[:char_budget]

    blocks: list[str] = []
    modes: dict[str, int] = {}
    for chunk in _RE_CARD_SPLIT.split(raw):
        if not chunk.strip():
            continue
        files = _RE_FILE_HEADER.findall(chunk)
        body = _RE_FILE_HEADER.sub("", chunk).strip()
        if tag_hits(body):
            prose, audit = render_card_as_summary(body)
            if str(audit.get("mode")) != "rendered" and tag_hits(prose):
                prose, audit = strip_tags(body), {**audit, "mode": "stripped"}
            modes[str(audit.get("mode"))] = modes.get(str(audit.get("mode")), 0) + 1
        else:
            prose, audit = body, {"mode": "already_prose"}
            modes["already_prose"] = modes.get("already_prose", 0) + 1
        header = "".join(f"File: {path}\n" for path in files)
        blocks.append((header + prose.strip()).strip())

    joined = "\n\n".join(b for b in blocks if b)
    joined, truncated = fit_tokens(joined, token_count(trimmed))
    joined, hit = fit_chars(joined, len(trimmed))
    leftovers = tag_hits(joined)
    if leftovers:
        raise AssertionError(f"spl_context payload still carries tags {leftovers}")
    return joined, {
        "mode": "blocks",
        "cards": len(blocks),
        "card_modes": modes,
        "tokens_in": token_count(raw),
        "tokens_out": token_count(joined),
        "truncated": truncated or hit,
    }


# --- label neutralization ---------------------------------------------------
#
# Rule applied to every entry: keep the directive's force, replace only the noun
# that refers to the tagged representation.  `why` records what would break if
# the rule were dropped.

NEUTRALIZE_RULES: list[tuple[str, str, str, str]] = [
    # (old, new, why, scope) -- scope names the one producer in run.py that
    # emits the string, so each pass neutralizes exactly its own contribution.
    # -- plan heading and body (run.py render_spl_patch_production_plan) ------
    (
        "## SPL Patch Production Plan",
        "## Patch Production Plan",
        "the addendum points the agent at 'the embedded Patch Production Plan'; a mismatched heading would make it unfindable",
        "plan",
    ),
    (
        "Purpose: use SPL to reduce search steps and produce a patch within the fixed step limit.",
        "Purpose: use these source notes to reduce search steps and produce a patch within the fixed step limit.",
        "names the payload; force unchanged",
        "plan",
    ),
    (
        "- Guard: SPL checkpoints describe PRE-FIX (current, possibly buggy) behavior.",
        "- Guard: the behavior notes describe PRE-FIX (current, possibly buggy) behavior.",
        "the PRE-FIX warning must survive verbatim in force -- it is what stops the agent treating buggy behavior as spec",
        "plan",
    ),
    (
        "A condition/threshold or variable-lifecycle (init/reset/update) checkpoint is a fix candidate, not a spec to preserve;",
        "A condition/threshold or variable-lifecycle (init/reset/update) statement is a fix candidate, not a spec to preserve;",
        "'checkpoint' is the tagged representation's word for a note",
        "plan",
    ),
    (
        "- SPL checkpoints to map onto source:",
        "- Behavior notes to map onto source:",
        "label only",
        "plan",
    ),
    (
        "Step 2: If it owns the behavior, edit the smallest source construct in that file/function. Do not inspect unrelated SPL cards.",
        "Step 2: If it owns the behavior, edit the smallest source construct in that file/function. Do not inspect unrelated behavior notes.",
        "run.py:1082, an unconditional plan line; 'SPL cards' names the artifact the agent must not read",
        "plan",
    ),
    # -- inlined card block (run.py render_source_bound_card_lines) -----------
    (
        "### SPL Controller Card",
        "### Controller Card",
        "label only",
        "card",
    ),
    (
        "SPL score: ",
        "Match score: ",
        "label only",
        "card",
    ),
    (
        "Use this card as: real source owner + SPL behavior checklist. Patch only the source excerpt/file, never the SPL text.",
        "Use this card as: real source owner + behavior checklist. Patch only the source excerpt/file, never the note text.",
        "states the source-only patch rule; must survive",
        "card",
    ),
    (
        "SPL checkpoints:",
        "Behavior notes:",
        "label only",
        "card",
    ),
    (
        "- No compact checkpoint extracted; use the summary only as a source-inspection hint.",
        "- No compact note extracted; use the summary only as a source-inspection hint.",
        "fallback text; keep the hint that the summary is weak evidence",
        "card",
    ),
    (
        "SPL checklist excerpt:",
        "Behavior notes excerpt:",
        "label only",
        "card",
    ),
    (
        "Editable source excerpt: UNRESOLVED. Open the real file and map this SPL card to source before editing.",
        "Editable source excerpt: UNRESOLVED. Open the real file and map these notes to source before editing.",
        "keeps the 'verify against real source' instruction",
        "card",
    ),
    # -- controller block header (run.py build_spl_controller_block) ----------
    (
        "## SPL Controller Cards",
        "## Controller Notes",
        "label only",
        "controller",
    ),
    (
        "These source-bound cards were selected from the full SPL index using the issue text and bound to real source excerpts when possible.",
        "These source-bound notes were selected from the full behavior index using the issue text and bound to real source excerpts when possible.",
        "describes how the payload was chosen; force unchanged",
        "controller",
    ),
    (
        "SPL is a structured natural-language view of source behavior. Here it is used to shorten the path to a patch, not to add broad extra context.",
        "These notes are a source-derived description of behavior. Here they are used to shorten the path to a patch, not to add broad extra context.",
        "'structured' would advertise a representation the payload no longer has",
        "controller",
    ),
    (
        "Step 1: Follow the SPL Patch Production Plan first. Run its first source command before broad repository search.",
        "Step 1: Follow the Patch Production Plan first. Run its first source command before broad repository search.",
        "heading reference; must match the neutralized heading",
        "controller",
    ),
    (
        "Step 2: Map one SPL checkpoint to visible source. If it maps, edit the smallest source construct that conflicts with the issue.",
        "Step 2: Map one behavior note to visible source. If it maps, edit the smallest source construct that conflicts with the issue.",
        "same directive, different noun",
        "controller",
    ),
    # -- full-card document (run.py build_source_bound_cards_document) --------
    (
        "# Source-Bound SPL Cards",
        "# Source-Bound Behavior Notes",
        "the addendum tells the agent to open this file; its title must not promise tags",
        "document",
    ),
    (
        "Each card binds one issue-ranked SPL entry to the corresponding real source excerpt when the source anchor can be resolved.",
        "Each card binds one issue-ranked behavior entry to the corresponding real source excerpt when the source anchor can be resolved.",
        "label only",
        "document",
    ),
    # -- tool index note (run.py load_trimmed_spl_index) ---------------------
    (
        "Issue-ranked source-derived SPL entries for mini-SWE-agent tool use.",
        "Issue-ranked source-derived behavior entries for mini-SWE-agent tool use.",
        "this string is served to the agent by spl_show.py / spl_search.py",
        "index",
    ),
    # -- progress rule (run.py build_mini_config) ----------------------------
    (
        "If this is an SPL variant and you have already edited source code:",
        "If this is a behavior-notes variant and you have already edited source code:",
        "the rule itself is discipline, not notation -- only its self-name changes",
        "config",
    ),
    # -- misleading guard (run.py SPL_MISLEADING_GUARD) ----------------------
    (
        "WARNING — SPL describes PRE-FIX behavior, not a spec: the [COMMAND]/[CONDITION]/[RETURN]/[THROW] checkpoints below were extracted from the CURRENT (possibly buggy) source,",
        "WARNING — these notes describe PRE-FIX behavior, not a spec: they were extracted from the CURRENT (possibly buggy) source,",
        "names the tag vocabulary inline; the PRE-FIX warning is preserved word for word",
        "card",
    ),
    (
        "Checkpoints are descriptive, not authoritative.",
        "These notes are descriptive, not authoritative.",
        "label only",
        "card",
    ),
    (
        "In particular, a checkpoint about a condition expression",
        "In particular, a note about a condition expression",
        "label only",
        "card",
    ),
]


# A few strings the frozen builders emit only under a condition, so a given
# instance can legitimately never contain them.  Keys are the rule's exact `old`
# text -- `_verify_conditional_rules` enforces that, because a near-miss key
# would otherwise silently switch off the drift check it was meant to exempt.
CONDITIONAL_RULES: dict[str, str] = {
    "- Guard: SPL checkpoints describe PRE-FIX (current, possibly buggy) behavior.":
        "run.py:1020 -- appended only when uses_misleading_guard(config)",
    "A condition/threshold or variable-lifecycle (init/reset/update) checkpoint is a fix candidate, not a spec to preserve;":
        "run.py:1023-1024 -- continuation of the same guarded block",
    "- SPL checkpoints to map onto source:":
        "run.py:1027 -- appended only when the extractor found checkpoints",
    "- No compact checkpoint extracted; use the summary only as a source-inspection hint.":
        "run.py:1131 -- else-branch when an entry has no extractable checkpoints",
    "Editable source excerpt: UNRESOLVED. Open the real file and map this SPL card to source before editing.":
        "run.py:1125-1128 -- else-branch when the source anchor could not be bound",
    "If this is an SPL variant and you have already edited source code:":
        "run.py:1424-1442 -- the whole <spl_progress_rule> is appended only when "
        "build_spl_controller_block returned a non-empty block; django__django-15127 "
        "is the one frozen spl_both unit where it is empty, so 217/218 carry the rule",
}

SKIPPED_RULES: collections.Counter = collections.Counter()

_NOT_VOCABULARY: dict[str, str] = {
    "spl": "notes",
}
# The scorer annotates each matched term with the fields it was found in, e.g.
# `main:spl, array:summary/spl, astropy:file` (see run.py:468).  Here `spl` is a
# *field name*, so the word reaches the agent as vocabulary even though the
# notation is gone.  Only the part after `:` or `/` is rewritten, so a term that
# is literally `spl` survives, and `/tmp/spl_tools/...` is untouched because
# `spl_tools` continues with `_` rather than ending the token.
_RE_FIELD_NAME = re.compile(
    r"(?<=[:/])(" + "|".join(sorted(_NOT_VOCABULARY)) + r")(?=$|[/,\s])"
)


def neutralize_matched_terms(text: str) -> str:
    """Rename scoring provenance fields that name the tagged representation."""
    return _RE_FIELD_NAME.sub(lambda m: _NOT_VOCABULARY[m.group(1)], str(text or ""))


def _verify_conditional_rules() -> None:
    """Every exemption must name a real rule, or the check is quietly weaker."""
    patterns = {r[0] for r in NEUTRALIZE_RULES}
    unknown = sorted(set(CONDITIONAL_RULES) - patterns)
    if unknown:
        raise AssertionError(
            f"CONDITIONAL_RULES key(s) match no rule (typo would disable a drift "
            f"check): {unknown}"
        )


_verify_conditional_rules()


def neutralize(text: str, scope: str, strict: bool = True) -> str:
    """Apply the rules belonging to `scope`. Raises if an unconditional one misses.

    Scoping is required, not cosmetic: `build_spl_controller_block` embeds the
    output of `render_spl_patch_production_plan` and `render_source_bound_card_lines`,
    which have already neutralized themselves, so an unscoped pass would "miss"
    those rules and the loud failure would fire on correct input.

    Failing loudly on a no-op rule is deliberate: this module is pinned to a
    frozen `run.py`, and if that file's wording ever shifts, a silent miss could
    leave the tagged arm's vocabulary in the treatment.  The rules whose text
    contains no `SPL` token are the reason the check has to be here at all --
    `residual_spl_mentions` cannot see those.  Rules in `CONDITIONAL_RULES` are
    exempt from the failure and counted instead, because the frozen builder
    itself may not emit them for a given instance.

    `strict=False` is for the fairness audit, which applies the rules to single
    lines: a line cannot contain every rule, so completeness there is meaningless.
    Production callers must keep the default.
    """
    rules = [r for r in NEUTRALIZE_RULES if r[3] == scope]
    if not rules:
        raise AssertionError(f"no neutralization rules carry scope {scope!r}")
    out = str(text or "")
    misses = []
    for old, new, _why, _scope in rules:
        if old not in out:
            if old in CONDITIONAL_RULES:
                SKIPPED_RULES[old] += 1
                continue
            misses.append(old)
            continue
        out = out.replace(old, new)
    if misses and strict:
        raise AssertionError(
            f"scope {scope!r}: {len(misses)} rule(s) matched nothing: {misses[:3]}"
        )
    return neutralize_matched_terms(out)


def strip_checkpoint(text: str) -> str:
    """Remove notation from one already-truncated checkpoint string.

    Used so the plan's bullets are chosen by the *frozen* extractor on the same
    tagged card the control arm uses, and only the notation differs -- picking
    them from prose instead would silently change *which* behavior is shown.

    The extractor truncates to `max_len` *before* this runs, so a checkpoint can
    arrive with its closing bracket cut off.  Everything is therefore handled by
    keyword rather than by bracket, and `RESULT` becomes a sentence fragment
    because it is notation the audit would otherwise reject.
    """
    out = str(text or "")
    out = re.sub(r"<REF>\s*(.*?)\s*</REF>", r"\1", out, flags=re.S)
    # The frozen extractor admits COMMAND, CONDITION, RETURN, THROW,
    # EXCEPTION_FLOW and ALTERNATIVE_FLOW lines, and truncates at `max_len`
    # before this runs, so a checkpoint can arrive with its closing bracket cut
    # off.  Everything is therefore keyed on the tag word, not on the bracket.
    out = re.sub(
        r"^\s*\[(?:COMMAND|CONDITION|RETURN|THROW|LOG|"
        r"ALTERNATIVE_FLOW|EXCEPTION_FLOW|SEQUENTIAL_BLOCK|MAIN_FLOW)\b[:\s]*",
        "",
        out,
    )
    out = re.sub(r"[.;]?\s+RESULT\s+", "; results: ", out)
    out = re.sub(r"\s*\]\s*$", "", out)
    out = re.sub(r"\s+(?:END_(?:MAIN_FLOW|SEQUENTIAL_BLOCK|ALTERNATIVE_FLOW|EXCEPTION_FLOW))\s*$", "", out)
    out = re.sub(r"[ \t]+", " ", out).strip()
    if tag_hits(out):
        raise AssertionError(f"checkpoint still tagged after stripping: {out[:120]!r}")
    return out


def trim_prose_by_tokens(prose: str, tagged: str, max_chars: int) -> str:
    """Trim `prose` to the token count the tagged arm keeps at `max_chars`.

    A character cap is the wrong yardstick once the brackets are gone: a tag
    costs more characters than it does meaning, so matching characters would hand
    the unstructured arm extra content.  Matching tokens keeps the delivered
    information the same and lets the frozen builder's own character cap stay in
    force as a ceiling.
    """
    budget = token_count(str(tagged or "")[:max_chars])
    trimmed, _hit = fit_tokens(prose, budget)
    if len(trimmed) > len(prose):
        return prose
    return trimmed


# --- residual-vocabulary audit ---------------------------------------------

_RE_SPL_WORD = re.compile(r"\bSPL\b|\bspl\b")
_RE_TOOL_PATH = re.compile(r"/tmp/spl_tools/[A-Za-z0-9_.\-]+")


def residual_spl_mentions(text: str, *, carried_from: str | None = None) -> list[str]:
    """`SPL`/`spl` occurrences outside an allowlisted `/tmp/spl_tools/...` path.

    `carried_from` is the frozen text the prose was derived from.  A token that
    text already contains is *content*, not notation: sympy's codegen has an
    `SPL` (statements per line), and one Django card renders the SQL compiler as
    an "SPL compiler".  The conversion removes notation and can never add it, so
    an occurrence with no counterpart in the source is the only kind that can be a
    leak -- and each source occurrence excuses at most one delivered occurrence,
    so a repeat cannot be laundered through a single genuine one.
    """
    text = str(text or "")
    allow = [(m.start(), m.end()) for m in _RE_TOOL_PATH.finditer(text)]

    def inside(m: re.Match[str]) -> bool:
        return any(a <= m.start() and m.end() <= b for a, b in allow)

    budget: collections.Counter = collections.Counter()
    if carried_from:
        budget.update(_RE_SPL_WORD.findall(str(carried_from)))

    residual: list[str] = []
    for match in _RE_SPL_WORD.finditer(text):
        if inside(match):
            continue
        token = match.group(0)
        if budget[token] > 0:
            budget[token] -= 1
            continue
        residual.append(token)
    return residual


def assert_clean(
    text: str, where: str, *, carried_from: str | None = None
) -> dict[str, Any]:
    """Raise unless `text` is tag-free and carries no stray SPL vocabulary.

    `carried_from` excuses card payload the frozen text also contains, and only
    that; see `residual_spl_mentions`.  Builder-authored wording has no such
    source, so it never gets the exemption.
    """
    tags = tag_hits(text)
    residual = residual_spl_mentions(text, carried_from=carried_from)
    if tags or residual:
        raise AssertionError(
            f"{where}: tags={tags} residual_spl={residual[:8]}"
        )
    return {
        "where": where,
        "tokens": token_count(text),
        "chars": len(str(text)),
        # Recorded so the audit can disclose how much of the payload's `SPL`
        # vocabulary is carried-over source content rather than notation the
        # conversion failed to remove.
        "carried_spl": len(_RE_SPL_WORD.findall(str(carried_from or ""))),
    }
