"""Entry point for the Exp3 supplement: SPL content without the tag notation.

Why this file exists instead of a patch to `run.py`
---------------------------------------------------
The frozen `run.py` is experiment-2/3 evidence and must stay byte-identical, so
the new condition is expressed by importing it and overriding exactly the
functions that touch SPL representation, then delegating `main()` back to it.
Every override is a *post-process* of the frozen function's own output rather
than a reimplementation, so if `run.py` changes underneath, the overrides keep
working and the neutralization rules fail loudly (see
`spl_unstructured.neutralize`) instead of silently drifting.

What the new condition changes, and what it does not
----------------------------------------------------
Aligned with the frozen `miniswe_spl_both` arm: same protocol
`spl_guarded_protocol`, same model/temperature/step limit, same owner
pointer and first-source command, same guarded PRE-FIX warning, same progress
rule.  Budgets are not re-declared here -- the mode is routed through `both`'s
branch of `spl_controller_budget` / `source_bound_source_budget` /
`prompt_card_limit`, so whatever the per-instance config gives `both` (3 selected
cards, 1 inlined, 600 SPL chars/card, 1200 source chars, matching the frozen
`random218` unit configs) is what this condition gets.  The single substantive
difference is that every SPL payload reaches the agent as tag-free prose.

Card selection is deliberately *not* re-implemented: `ranked_entries` still
scores the frozen tagged cards exactly as the control does, and only then is the
text of the selected entries converted.  That way both arms see the same cards
in the same order, and the conversion cannot influence which cards are chosen.

Card conversion is deterministic -- no model call -- so nothing is rebuilt, in
keeping with the project constraint that SPL is never regenerated.
"""

from __future__ import annotations

import json
import os
import shutil
import sys
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

import run as base  # noqa: E402
import spl_unstructured as U  # noqa: E402

MODE = "miniswe_spl_unstructured_both"
BOTH = "miniswe_spl_both"

CONVERSION_LOG: list[dict[str, Any]] = []


def _log(where: str, text: str, carried_from: str | None = None) -> str:
    audit = U.assert_clean(text, where, carried_from=carried_from)
    CONVERSION_LOG.append(audit)
    return text


def _carried_card_text(*, with_checkpoints: bool = False) -> str:
    """The tagged cards this pass converted, for the carry-over audit.

    Card payload is copied verbatim except for notation, so an `SPL` token in the
    delivered prose that also sits in the tagged card is source content the card
    happens to contain -- sympy's codegen `SPL` (statements per line), or a
    Django card that renders the SQL compiler as an "SPL compiler".  Only those
    occurrences are excused; wording the builders wrote never appears here.

    `with_checkpoints` also counts the bullets the *frozen* extractor pulls out of
    the same cards, because those are delivered too -- inline in the plan and as
    the index's `checkpoints` field -- and a card that legitimately contains `SPL`
    contributes it once to the prose and once again to the bullets taken from it.
    Counting that copy is what keeps the budget honest instead of merely larger.
    """
    parts = [tagged for _converted, tagged in _RANKED_TAGGED]
    if with_checkpoints:
        parts.extend(
            "\n".join(_base_extract_spl_checkpoints(tagged, limit=4))
            for _converted, tagged in _RANKED_TAGGED
        )
    return "\n".join(parts)


# --- 1. budgets: the new mode takes `both`'s branch -------------------------

_base_spl_controller_budget = base.spl_controller_budget
_base_source_bound_source_budget = base.source_bound_source_budget
_base_prompt_card_limit = base.prompt_card_limit


def spl_controller_budget(mode: str, config: dict[str, Any]):
    return _base_spl_controller_budget(BOTH if mode == MODE else mode, config)


def source_bound_source_budget(mode: str, config: dict[str, Any]) -> int:
    return _base_source_bound_source_budget(BOTH if mode == MODE else mode, config)


def prompt_card_limit(mode: str, config: dict[str, Any]) -> int:
    return _base_prompt_card_limit(BOTH if mode == MODE else mode, config)


# --- 2. notation removal, applied where the cards are ranked ----------------

_base_ranked_entries = base.ranked_spl_entries

# prose payload -> the tagged card it came from.  The frozen builders hand
# `entry["spl"]` around as a bare string, so a registry is the only way to let
# the two places that must stay notation-matched (the plan's checkpoint bullets
# and the injected character cap) recover the tagged twin.
_PROSE_TO_TAGGED: dict[str, str] = {}


def ranked_spl_entries(sample_dir: Path, config: dict[str, Any]) -> list[dict[str, Any]]:
    entries = _base_ranked_entries(sample_dir, config)
    if not _is_new_mode(config):
        return entries
    out = []
    _RANKED_TAGGED.clear()
    for entry in entries:
        tagged = str(entry.get("spl") or "")
        # Convert the *whole* card and leave trimming to the frozen builders, as
        # in the control arm.  Trimming here instead would starve
        # `extract_spl_checkpoints`, which reads the untrimmed entry and would
        # then find no checkpoints at all -- the plan would lose its bullets
        # while the tagged arm kept them.
        prose, audit = U.to_unstructured(tagged)
        audit["file"] = entry.get("file")
        audit["worker_name"] = entry.get("worker_name")
        CONVERSION_LOG.append(audit)
        _PROSE_TO_TAGGED[prose] = tagged
        converted = {**entry, "spl": prose, "_spl_tagged": tagged}
        _RANKED_TAGGED.append((converted, tagged))
        out.append(converted)
    return out


def _is_new_mode(config: dict[str, Any] | None = None) -> bool:
    if config is None:
        return False
    return MODE in (config.get("conditions") or [])


# --- 3. the plan's checkpoint bullets must match the control arm's -----------

_base_extract_spl_checkpoints = base.extract_spl_checkpoints


def extract_spl_checkpoints(spl: str, limit: int = 5, max_len: int = 180) -> list[str]:
    tagged = _PROSE_TO_TAGGED.get(str(spl or ""))
    if tagged is None:
        return _base_extract_spl_checkpoints(spl, limit=limit, max_len=max_len)
    # Same extractor, same card, same truncation as the control -- only the
    # notation is removed.  Selecting the bullets from prose would change *which*
    # behavior the plan surfaces, which is a different experiment.
    return [U.strip_checkpoint(item)
            for item in _base_extract_spl_checkpoints(tagged, limit=limit, max_len=max_len)]


# --- 4. the injected character cap becomes a token cap for prose ------------

_base_trim_text = base.trim_text


def trim_text(text: str, max_chars: int) -> str:
    tagged = _PROSE_TO_TAGGED.get(str(text or ""))
    if tagged is None:
        return _base_trim_text(text, max_chars)
    return U.trim_prose_by_tokens(text, tagged, max_chars)


# --- 5. neutralize the labels the frozen builders write --------------------

_base_build_spl_controller_block = base.build_spl_controller_block
_base_render_spl_patch_production_plan = base.render_spl_patch_production_plan
_base_render_source_bound_card_lines = base.render_source_bound_card_lines
_base_build_source_bound_cards_document = base.build_source_bound_cards_document


def build_spl_controller_block(sample_dir: Path, mode: str, config: dict[str, Any]) -> str:
    block = _base_build_spl_controller_block(sample_dir, mode, config)
    if mode != MODE or not block:
        return block
    return _log(
        "build_spl_controller_block",
        U.neutralize(block, "controller"),
        # The plan carries both the cards and the checkpoint bullets taken from
        # them, so a card token that reaches both is legitimately present twice.
        _carried_card_text(with_checkpoints=True),
    )


def render_spl_patch_production_plan(*args: Any, **kwargs: Any) -> list[str]:
    lines = _base_render_spl_patch_production_plan(*args, **kwargs)
    mode = kwargs.get("mode", args[1] if len(args) > 1 else None)
    if mode != MODE or not lines:
        return lines
    return U.neutralize("\n".join(lines), "plan").split("\n")


def render_source_bound_card_lines(*args: Any, **kwargs: Any) -> list[str]:
    lines = _base_render_source_bound_card_lines(*args, **kwargs)
    mode = kwargs.get("mode", args[1] if len(args) > 1 else None)
    if mode != MODE or not lines:
        return lines
    return U.neutralize("\n".join(lines), "card").split("\n")


def build_source_bound_cards_document(sample_dir: Path, mode: str, config: dict[str, Any]) -> str:
    doc = _base_build_source_bound_cards_document(sample_dir, mode, config)
    if mode != MODE or not doc:
        return doc
    return _log(
        "build_source_bound_cards_document",
        U.neutralize(doc, "document"),
        _carried_card_text(with_checkpoints=True),
    )


# --- 6. payload files: in-container tools must serve notes, not tags --------

_base_build_payload_files = base.build_payload_files

# The frozen `spl_search.py` / `spl_show.py` are written for tagged cards: they
# select `[COMMAND ...]` lines and print "SPL CARD".  Neither survives the
# conversion -- the prose renderer emits no such lines, and the printed strings
# would hand the agent the vocabulary the condition is supposed to withhold.
# Each substitution below is asserted to apply exactly once, so a change to the
# frozen scripts fails loudly instead of quietly shipping tagged wording.
_CP_EXTRACTOR = '''def checkpoints(spl: str, limit: int = 4) -> list[str]:
    out = []
    for raw in spl.splitlines():
        line = " ".join(raw.strip().split())
        if not line:
            continue
        if not any(tag in line for tag in ("[COMMAND", "[CONDITION", "[RETURN", "[THROW", "[EXCEPTION_FLOW", "[ALTERNATIVE_FLOW")):
            continue
        out.append(line[:220])
        if len(out) >= limit:
            break
    return out'''

# The checkpoints are precomputed on the host by the frozen extractor acting on
# the tagged card, so the tools show the control arm's exact items, notation
# aside -- an in-container re-derivation could only approximate that.
_CP_PRECOMPUTED = '''def checkpoints(entry: dict, limit: int = 4) -> list[str]:
    return [str(item) for item in (entry.get("checkpoints") or [])][:limit]'''

_SHARED_SUBS: list[tuple[str, str, str]] = [
    (_CP_EXTRACTOR, _CP_PRECOMPUTED, "checkpoint extractor -> precomputed field"),
    ('for item in checkpoints(str(entry.get("spl") or "")):',
     "for item in checkpoints(entry):",
     "checkpoints call site"),
    ('"No SPL index is available at /tmp/spl_tools/spl_index.json"',
     '"No behavior-note index is available at /tmp/spl_tools/spl_index.json"',
     "missing index"),
]

_SEARCH_SUBS: list[tuple[str, str, str]] = [
    ('    spl = str(entry.get("spl") or "")\n'
     '    hay = f"{file_name} {worker} {summary} {spl}".lower()',
     '    notes = str(entry.get("notes") or "")\n'
     '    hay = f"{file_name} {worker} {summary} {notes}".lower()',
     "score_entry field rename (same text, same scoring)"),
    ('print(f"checkpoint: {item}")', 'print(f"note: {item}")', "bullet label"),
    ('"source_check: map at least one checkpoint to real source before editing."',
     '"source_check: map at least one note to real source before editing."',
     "source-check hint"),
    ('"No SPL entries matched. Fall back to source search."',
     '"No behavior notes matched. Fall back to source search."',
     "empty result"),
]

_SHOW_SUBS: list[tuple[str, str, str]] = [
    ('print(entry.get("spl", ""))', 'print(entry.get("notes", ""))', "card field rename"),
    ('print(f"Checkpoint: {item}")', 'print(f"Note: {item}")', "bullet label"),
    ('"Use: source-bound behavior checklist. Map checkpoints to visible source before editing."',
     '"Use: source-bound behavior notes. Map them to visible source before editing."',
     "usage hint"),
    ('"No exact SPL card matched. Try spl_search.py with broader behavior terms."',
     '"No exact behavior note matched. Try spl_search.py with broader behavior terms."',
     "empty result"),
    ('print(f"### SPL CARD {idx}")', 'print(f"### BEHAVIOR NOTE {idx}")', "card heading"),
    ('print("--- END SPL CARD ---")', 'print("--- END BEHAVIOR NOTE ---")', "card footer"),
]


def _neutralize_tool(script: str, name: str, subs: list[tuple[str, str, str]]) -> str:
    for old, new, why in _SHARED_SUBS + subs:
        count = script.count(old)
        if count != 1:
            raise AssertionError(
                f"{name}: substitution {why!r} matched {count} times, expected 1 "
                f"(frozen tool script changed?)"
            )
        script = script.replace(old, new)
    # `/tmp/spl_tools/...` stays: that directory is shared with the frozen
    # free_summary condition and is named in the addendum, so it is baseline
    # vocabulary rather than this condition's notation.
    leftovers = U.residual_spl_mentions(script)
    if leftovers:
        raise AssertionError(f"{name}: agent-visible SPL wording survives: {sorted(set(leftovers))}")
    return script


def _index_for_agent(
    index: str, sample_dir: Path, config: dict[str, Any]
) -> str:
    """Rewrite the delivered index for the unstructured arm.

    Two changes, both required for the condition to be honest:

      * the card field is renamed `spl` -> `notes`, because a JSON key is text
        the agent reads (the in-container tools are repointed to match);
      * a `checkpoints` list is added, computed by the *frozen* extractor from
        the tagged card, so the tools surface the control arm's items.

    The audit is per field rather than over the serialised blob, and each field
    is given the exact text it was derived from.  A blob audit would pool the
    budgets, and the `checkpoints` field is a *copy* of card content the `notes`
    field already carries -- django-16263's card renders the SQL compiler as an
    "SPL compiler" in one note and the frozen extractor turns a nearby line into
    the bullet "Obtain the SPL compiler ...", so the same card token is delivered
    twice.  Pooling excuses that duplicate with the other field's budget, which
    is exactly the slack a real leak would hide in.
    """
    data = json.loads(index)
    source = json.loads(index)  # pristine copy, for the copied-in fields
    note = str(data.get("note") or "")
    if note:
        data["note"] = U.neutralize(note, "index")
    tagged_by_worker = _tagged_by_worker(sample_dir, config)
    source_entries = source.get("entries") or []
    for i, entry in enumerate(data.get("entries") or []):
        notes = entry.pop("spl", None)
        if notes is not None:
            entry["notes"] = notes
        terms = entry.get("matched_terms")
        if isinstance(terms, list):
            entry["matched_terms"] = [U.neutralize_matched_terms(t) for t in terms]
        tagged = tagged_by_worker.get(str(entry.get("worker_name") or ""))
        entry["checkpoints"] = (
            [U.strip_checkpoint(item)
             for item in base.extract_spl_checkpoints(tagged, limit=4)]
            if tagged else []
        )

        where = f"payload:spl_index.json:entries[{i}]"
        src = source_entries[i] if i < len(source_entries) else {}
        # Derived from the tagged card.
        CONVERSION_LOG.append(
            U.assert_clean(str(entry.get("notes") or ""), f"{where}.notes", carried_from=tagged)
        )
        # A copy of what the frozen extractor pulls out of that same card.
        CONVERSION_LOG.append(
            U.assert_clean(
                json.dumps(entry.get("checkpoints") or [], ensure_ascii=False),
                f"{where}.checkpoints",
                carried_from="\n".join(_base_extract_spl_checkpoints(tagged, limit=4))
                if tagged else "",
            )
        )
        # Copied out of the frozen `spl_index.json`, not written here.
        CONVERSION_LOG.append(
            U.assert_clean(
                str(entry.get("summary") or ""),
                f"{where}.summary",
                carried_from=str(src.get("summary") or ""),
            )
        )
        # Scored terms pass through `neutralize_matched_terms`; no card content.
        CONVERSION_LOG.append(
            U.assert_clean(
                json.dumps(entry.get("matched_terms") or [], ensure_ascii=False),
                f"{where}.matched_terms",
            )
        )

    # Builder wording: the index note alone, with nothing to carry it.
    CONVERSION_LOG.append(U.assert_clean(str(data.get("note") or ""), "payload:spl_index.json:note"))
    rendered = json.dumps(data, ensure_ascii=False, indent=2)
    tags = U.tag_hits(rendered)
    if tags:
        raise AssertionError(f"payload:spl_index.json: tags={tags}")
    return rendered


def _tagged_by_worker(sample_dir: Path, config: dict[str, Any]) -> dict[str, str]:
    """Map worker name -> tagged card, from this run's own ranking pass."""
    return {
        str(entry.get("worker_name") or ""): tagged
        for entry, tagged in _RANKED_TAGGED
    }


_RANKED_TAGGED: list[tuple[dict[str, Any], str]] = []


def build_payload_files(sample_dir: Path, mode: str, config: dict[str, Any]) -> dict[str, str]:
    files = _base_build_payload_files(sample_dir, mode, config)
    if mode != MODE:
        return files

    files["/tmp/spl_tools/spl_search.py"] = _neutralize_tool(
        base.SPL_SEARCH_SCRIPT, "spl_search.py", _SEARCH_SUBS
    )
    files["/tmp/spl_tools/spl_show.py"] = _neutralize_tool(
        base.SPL_SHOW_SCRIPT, "spl_show.py", _SHOW_SUBS
    )

    ctx_path = sample_dir / "spl_context.txt"
    if ctx_path.exists():
        limit = int(config.get("mini_spl_entry_limit", 8)) * int(
            config.get("mini_spl_entry_max_chars", 1800)
        )
        text = ctx_path.read_text(encoding="utf-8", errors="replace")
        prose, audit = U.to_unstructured_blocks(text, char_budget=limit)
        audit["source"] = "spl_context.txt"
        CONVERSION_LOG.append(audit)
        files["/tmp/spl_tools/spl_context.txt"] = _log(
            "payload:spl_context.txt", prose
        ).strip() + "\n"

    index = files.get("/tmp/spl_tools/spl_index.json")
    if index:
        # `_index_for_agent` audits itself, field by field, because the index
        # mixes builder wording with two kinds of copied card content.
        files["/tmp/spl_tools/spl_index.json"] = _index_for_agent(index, sample_dir, config)

    return files


# --- 7. the progress rule is appended to every observation ------------------

_base_build_mini_config = base.build_mini_config


def build_mini_config(**kwargs: Any) -> Path:
    path = _base_build_mini_config(**kwargs)
    if kwargs.get("mode") != MODE:
        return path
    text = path.read_text(encoding="utf-8", errors="replace")
    neutral = U.neutralize(text, "config")
    if neutral != text:
        path.write_text(neutral, encoding="utf-8")
    _log("mini_config.yaml", neutral)
    return path


def _install() -> list[str]:
    patched = [
        "spl_controller_budget",
        "source_bound_source_budget",
        "prompt_card_limit",
        "ranked_spl_entries",
        "extract_spl_checkpoints",
        "trim_text",
        "build_spl_controller_block",
        "render_spl_patch_production_plan",
        "render_source_bound_card_lines",
        "build_source_bound_cards_document",
        "build_payload_files",
        "build_mini_config",
    ]
    for name in patched:
        setattr(base, name, globals()[name])
    return patched


def _write_conversion_log(out_dir: Path) -> None:
    if not CONVERSION_LOG:
        return
    out_dir.mkdir(parents=True, exist_ok=True)
    target = out_dir / "unstructured_conversion_log.json"
    payload = {
        "mode": MODE,
        "entries": len(CONVERSION_LOG),
        "render_modes": {},
        "total_tokens_in": 0,
        "total_tokens_out": 0,
    }
    for row in CONVERSION_LOG:
        mode = str(row.get("mode") or row.get("where") or "?")
        payload["render_modes"][mode] = payload["render_modes"].get(mode, 0) + 1
        payload["total_tokens_in"] += int(row.get("tokens_in") or row.get("tokens") or 0)
        payload["total_tokens_out"] += int(row.get("tokens_out") or row.get("tokens") or 0)
    target.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"[unstructured] conversion log -> {target}")
    print(f"[unstructured] render modes: {payload['render_modes']}")
    print(
        f"[unstructured] tokens in/out: {payload['total_tokens_in']:,} / "
        f"{payload['total_tokens_out']:,}"
    )


if __name__ == "__main__":
    patched = _install()
    print(f"[unstructured] patched {len(patched)} run.py functions for mode {MODE}")
    try:
        base.main()
    finally:
        cfg = None
        for i, arg in enumerate(sys.argv):
            if arg == "--config" and i + 1 < len(sys.argv):
                cfg = sys.argv[i + 1]
        if cfg:
            try:
                config = json.loads(Path(cfg).read_text(encoding="utf-8"))
                _write_conversion_log(Path(str(config.get("run_dir") or ".")))
            except Exception as exc:  # pragma: no cover
                print(f"[unstructured] could not write conversion log: {exc}")
