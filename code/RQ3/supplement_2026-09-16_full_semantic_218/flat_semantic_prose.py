"""Build genuinely flat prose from the frozen function-level SPL cards.

This module is the representation layer for the Experiment 3 supplement.  It
does not call an LLM and it does not inspect the issue.  It parses the already
frozen SPL cards, keeps their semantic payload, and removes the SPL vocabulary
and hierarchy.  The caller controls the same per-entry character budget used
by the structured ``miniswe_spl_both`` condition.

The delivered text deliberately contains no card/worker headings, role labels,
lists, indentation, source excerpts, repair plan, patch recommendation, or
keyword-shaped replacements such as ``first``, ``then``, and ``producing``.
Function and file names may occur inside ordinary sentences because they are
semantic facts, not presentation structure.
"""

from __future__ import annotations

import functools
import json
import re
import sys
from pathlib import Path
from typing import Any

_REPO_ROOT = Path(__file__).resolve().parents[2]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from common.spl_card_summary import parse_card


FORBIDDEN_PRESENTATION_PATTERNS: tuple[tuple[str, str], ...] = (
    ("spl_tag", r"\[(?:END_)?(?:DEFINE_WORKER|INPUTS|OUTPUTS|MAIN_FLOW|SEQUENTIAL_BLOCK|ALTERNATIVE_FLOW|EXCEPTION_FLOW|COMMAND|CONDITION|RETURN|THROW|LOG)\b"),
    ("ref_tag", r"</?REF>"),
    ("markdown_heading", r"(?m)^\s*#{1,6}\s"),
    ("list_or_numbering", r"(?m)^\s*(?:[-*+]\s+|\d+[.)]\s+)"),
    ("code_fence", r"```"),
    ("role_label", r"\b(?:PRIMARY_SOURCE_OWNER|SECONDARY_SOURCE_OWNER|SOURCE_BOUND_CONTEXT|WEAK_CONTEXT|controller card|patch production plan)\b"),
    ("representation_label", r"\b(?:SPL|worker card|checkpoint)\b"),
    ("implicit_schema_wording", r"\b(?:behavior notes?|current behavior|likely edit focus|source anchor)\b"),
    ("templated_transition", r"\b(?:the program first|the program then|producing|receives|yields|the value is available as)\b"),
)


@functools.lru_cache(maxsize=1)
def _encoder():
    try:
        import tiktoken

        return tiktoken.get_encoding("cl100k_base")
    except Exception:
        return None


def token_count(text: str) -> int:
    encoder = _encoder()
    if encoder is None:
        return len(re.findall(r"\w+|[^\w\s]", str(text)))
    return len(encoder.encode(str(text)))


def _clean(text: Any) -> str:
    value = re.sub(r"</?REF>", "", str(text or ""))
    # Frozen descriptions occasionally reproduce source markup or use the
    # representation name while referring to the target-language output.  The
    # following are wording-only normalizations: the literal/code meaning is
    # retained, but the delivered condition remains ordinary prose.
    value = value.replace("`", "'")
    value = re.sub(r"\bthe SPL compiler\b", "the compiler", value, flags=re.I)
    value = re.sub(r"\bSPL compiler\b", "compiler", value, flags=re.I)
    value = re.sub(r"\bSPL return statement\b", "return statement", value, flags=re.I)
    # Remove vocabulary that could act as a covert replacement for the SPL
    # notation even when that vocabulary originated inside a frozen sentence.
    # These substitutions are wording-only and do not add, drop, or reorder a
    # semantic fact.
    value = re.sub(r"\bproducing\b", "leaving", value, flags=re.I)
    value = re.sub(r"\breceives\b", "uses", value, flags=re.I)
    value = re.sub(r"\byields\b", "gives", value, flags=re.I)
    value = re.sub(r"\bthe value is available as\b", "this is kept in", value, flags=re.I)
    value = re.sub(r"\bthe program first\b", "the implementation", value, flags=re.I)
    value = re.sub(r"\bthe program then\b", "the implementation also", value, flags=re.I)
    value = re.sub(r"\bcurrent behavior\b", "existing implementation", value, flags=re.I)
    value = re.sub(r"\bbehavior notes?\b", "description", value, flags=re.I)
    value = re.sub(r"\blikely edit focus\b", "relevant area", value, flags=re.I)
    value = re.sub(r"\bsource anchor\b", "source location", value, flags=re.I)
    value = re.sub(r"\s+", " ", value).strip()
    return value.strip(" ;.")


def _finish(text: str) -> str:
    value = _clean(text)
    if not value:
        return ""
    return value if value.endswith((".", "!", "?")) else value + "."


def _lower_lead(text: str) -> str:
    value = _clean(text)
    if not value:
        return value
    return value[0].lower() + value[1:]


def _context_cards(text: str) -> list[tuple[str, dict[str, Any]]]:
    """Return ``(file, parsed card)`` pairs in frozen source order."""
    file_name = "the supplied source"
    chunks: list[tuple[str, str]] = []
    current: list[str] = []
    for line in str(text or "").splitlines():
        match = re.match(r"^#\s*FILE:\s*(.+?)\s*$", line)
        if match:
            if current:
                chunks.append((file_name, "\n".join(current)))
                current = []
            file_name = match.group(1).strip()
            continue
        current.append(line)
    if current:
        chunks.append((file_name, "\n".join(current)))

    cards: list[tuple[str, dict[str, Any]]] = []
    for source_file, body in chunks:
        matches = re.findall(r"\[DEFINE_WORKER:.*?\[END_WORKER\]", body, flags=re.S)
        for raw_card in matches:
            parsed = parse_card(raw_card)
            if parsed.get("structured"):
                cards.append((source_file, parsed))
    return cards


def _card_sentences(source_file: str, card: dict[str, Any]) -> list[str]:
    """Render semantic facts as ordinary sentences without schema-like cues."""
    function = _clean(card.get("worker_name")) or "the function"
    prefix = f"In {source_file}, {function}"
    sentences: list[str] = []

    description = _clean(card.get("description"))
    if description:
        short_name = function.rsplit(".", 1)[-1]
        if description.lower().startswith(short_name.lower() + " "):
            sentences.append(_finish(f"In {source_file}, {_lower_lead(description)}"))
        else:
            sentences.append(_finish(f"{prefix} {_lower_lead(description)}"))
    else:
        sentences.append(_finish(f"{prefix} implements the described source behavior"))

    inputs = list(card.get("inputs") or [])
    if inputs:
        pieces = []
        for item in inputs:
            name = _clean(item.get("name"))
            desc = _clean(item.get("description"))
            lead = desc.split(" ", 1)[0].lower() if desc else ""
            if lead in {
                "determines", "controls", "specifies", "provides", "contains",
                "selects", "indicates", "identifies", "sets", "allows",
            }:
                pieces.append(f"{name} {_lower_lead(desc)}")
            elif lead == "if":
                pieces.append(f"{name}, {_lower_lead(desc)}")
            else:
                pieces.append(f"{name} refers to {_lower_lead(desc)}" if desc else f"{name} is used here")
        sentences.append(_finish(f"In {function}, " + "; ".join(pieces)))

    outputs = list(card.get("outputs") or [])
    if outputs:
        for item in outputs:
            name = _clean(item.get("name"))
            desc = _clean(item.get("description"))
            if desc:
                sentences.append(_finish(
                    f"{function} returns {_lower_lead(desc)}, stored as {name}"
                ))
            else:
                sentences.append(_finish(f"{function} returns a value named {name}"))

    for step in card.get("steps") or []:
        action = _clean(step.get("text"))
        result = _clean(step.get("result"))
        sentence = f"While {function} runs, it will {_lower_lead(action)}"
        if result:
            sentence += f"; that value is stored as {result}"
        sentences.append(_finish(sentence))

    for flow in card.get("alternatives") or []:
        condition = _clean(flow.get("condition"))
        actions = []
        for step in flow.get("steps") or []:
            action = _clean(step.get("text"))
            result = _clean(step.get("result"))
            actions.append(action + (f", producing {result}" if result else ""))
        tail = "; ".join(actions) or "the alternative behavior is followed"
        sentences.append(_finish(f"When {condition}, {function} will {_lower_lead(tail)}"))

    for flow in card.get("exceptions") or []:
        condition = _clean(flow.get("condition"))
        actions = []
        for item in flow.get("logs") or []:
            if item.get("kind") == "throw":
                actions.append(f"raises {item.get('type')} with {_clean(item.get('text'))}")
            elif item.get("kind") == "log":
                actions.append(f"records {_clean(item.get('text'))}")
        tail = " and ".join(actions) or "takes the exceptional path"
        sentences.append(_finish(f"When {condition}, {function} {tail}"))

    return [sentence for sentence in sentences if sentence]


def _round_robin(groups: list[list[str]]) -> list[str]:
    """Interleave functions so the output cannot preserve card blocks."""
    out: list[str] = []
    width = max((len(group) for group in groups), default=0)
    for index in range(width):
        for group in groups:
            if index < len(group):
                out.append(group[index])
    return out


def _paragraph_budgets(reference: str) -> list[int]:
    paragraphs = [p.strip() for p in re.split(r"\n\s*\n", str(reference or "")) if p.strip()]
    budgets = [token_count(p) for p in paragraphs]
    return budgets or [max(1, token_count(reference))]


def _pack(sentences: list[str], budgets: list[int]) -> tuple[str, int]:
    paragraphs: list[str] = []
    remaining = list(sentences)
    delivered = 0
    for budget in budgets:
        chosen: list[str] = []
        while remaining:
            picked = None
            for index, sentence in enumerate(remaining):
                candidate = " ".join([*chosen, sentence])
                if token_count(candidate) <= budget:
                    picked = index
                    break
            if picked is None:
                break
            chosen.append(remaining.pop(picked))
            delivered += 1
        if chosen:
            paragraphs.append(" ".join(chosen))
    return "\n\n".join(paragraphs).strip(), delivered


def forbidden_hits(text: str) -> list[str]:
    # SPL tags are deliberately uppercase.  Case-insensitive matching would
    # incorrectly reject legitimate source expressions such as
    # ``WhereNode([condition], ...)``.  Other presentation checks remain
    # case-insensitive.
    return [
        name
        for name, pattern in FORBIDDEN_PRESENTATION_PATTERNS
        if re.search(pattern, text, flags=0 if name == "spl_tag" else re.I)
    ]


def build_flat_semantic_prose(
    spl_context: str,
    free_summary_reference: str,
) -> tuple[str, dict[str, Any]]:
    cards = _context_cards(spl_context)
    groups = [_card_sentences(source_file, card) for source_file, card in cards]
    sentences = _round_robin(groups)
    budgets = _paragraph_budgets(free_summary_reference)
    prose, consumed = _pack(sentences, budgets)
    hits = forbidden_hits(prose)
    if hits:
        raise AssertionError(f"flat semantic prose still contains presentation structure: {hits}")
    if not prose:
        raise AssertionError("flat semantic prose is empty")
    audit = {
        "cards_parsed": len(cards),
        "semantic_sentences_available": len(sentences),
        "semantic_sentences_delivered": consumed,
        "paragraphs_reference": len(budgets),
        "paragraphs_delivered": len([p for p in prose.split("\n\n") if p.strip()]),
        "reference_tokens": token_count(free_summary_reference),
        "delivered_tokens": token_count(prose),
        "token_ratio": token_count(prose) / max(1, token_count(free_summary_reference)),
        "forbidden_hits": hits,
        "issue_used_for_conversion": False,
        "model_called_for_conversion": False,
        "visible_card_or_worker_grouping": False,
    }
    return prose.rstrip() + "\n", audit


def _fit_card_sentences(sentences: list[str], token_budget: int) -> list[str]:
    selected: list[str] = []
    for sentence in sentences:
        candidate = " ".join([*selected, sentence])
        if token_count(candidate) <= token_budget:
            selected.append(sentence)
    return selected


def flatten_entry(
    entry: dict[str, Any],
    *,
    max_chars: int,
) -> tuple[str, dict[str, Any]]:
    """Render one frozen card as ordinary prose under a character budget.

    Selection/ranking happens outside this function.  Consequently this
    conversion cannot use the issue to add, delete, reorder, or reinterpret
    facts.  ``max_chars`` is deliberately the structured arm's card budget.
    """
    raw = str(entry.get("spl") or "")
    parsed = parse_card(raw)
    if not parsed.get("structured"):
        raise ValueError(f"could not parse frozen card for {entry.get('worker_name')}")
    sentences = _card_sentences(str(entry.get("file") or "the supplied source"), parsed)
    kept: list[str] = []
    for sentence in sentences:
        candidate = " ".join([*kept, sentence])
        if len(candidate) <= max(200, int(max_chars)):
            kept.append(sentence)
    prose = " ".join(kept).strip()
    if not prose and sentences:
        prose = sentences[0][: max(200, int(max_chars))].rstrip()
        if prose and not prose.endswith((".", "!", "?")):
            prose += "."
    hits = forbidden_hits(prose)
    if hits:
        raise AssertionError(f"flat entry still contains presentation structure: {hits}")
    if not prose:
        raise AssertionError("flat entry is empty")
    return prose, {
        "file": entry.get("file"),
        "function": entry.get("worker_name"),
        "character_budget": int(max_chars),
        "structured_characters": len(raw),
        "flat_characters": len(prose),
        "structured_tokens": token_count(raw[: int(max_chars)]),
        "flat_tokens": token_count(prose),
        "sentences_available": len(sentences),
        "sentences_delivered": len(kept),
        "forbidden_hits": hits,
    }


def build_flat_semantic_corpus(
    spl_index: dict[str, Any],
    *,
    entry_limit: int = 80,
    entry_max_chars: int = 1800,
) -> tuple[str, dict[str, Any]]:
    """Flatten the same frozen searchable entries exposed by ``run.py``.

    ``run.py:load_trimmed_spl_index`` exposes at most 80 entries and trims each
    frozen card to 1800 characters.  We apply those limits before parsing, then
    cap each prose fragment by the trimmed card's token count.  The output is a
    single paragraph and preserves neither card boundaries nor entry labels.
    """
    entries = list(spl_index.get("entries") or [])[: max(1, int(entry_limit))]
    delivered: list[str] = []
    structured_tokens = 0
    parsed_count = 0
    available_sentences = 0
    delivered_sentences = 0
    for entry in entries:
        if not isinstance(entry, dict):
            continue
        raw = str(entry.get("spl") or "")[: max(200, int(entry_max_chars))]
        if not raw.strip():
            continue
        structured_tokens += token_count(raw)
        parsed = parse_card(raw)
        if not parsed.get("structured"):
            continue
        parsed_count += 1
        sentences = _card_sentences(str(entry.get("file") or "the supplied source"), parsed)
        available_sentences += len(sentences)
        selected = _fit_card_sentences(sentences, token_count(raw))
        delivered_sentences += len(selected)
        delivered.extend(selected)

    prose = " ".join(delivered).strip()
    hits = forbidden_hits(prose)
    if hits:
        raise AssertionError(f"flat semantic corpus still contains presentation structure: {hits}")
    if not prose:
        raise AssertionError("flat semantic corpus is empty")
    audit = {
        "source": "frozen spl_index.json",
        "entries_available": len(spl_index.get("entries") or []),
        "entries_exposed": len(entries),
        "entries_parsed": parsed_count,
        "entry_limit": int(entry_limit),
        "entry_max_chars": int(entry_max_chars),
        "semantic_sentences_available": available_sentences,
        "semantic_sentences_delivered": delivered_sentences,
        "structured_reference_tokens": structured_tokens,
        "delivered_tokens": token_count(prose),
        "token_ratio": token_count(prose) / max(1, structured_tokens),
        "paragraphs_delivered": 1,
        "forbidden_hits": hits,
        "issue_used_for_conversion": False,
        "model_called_for_conversion": False,
        "visible_card_or_worker_grouping": False,
    }
    return prose + "\n", audit


def build_from_directory(
    sample_dir: Path,
    *,
    entry_limit: int = 80,
    entry_max_chars: int = 1800,
) -> tuple[str, dict[str, Any]]:
    index_path = sample_dir / "spl_index.json"
    if not index_path.is_file():
        raise FileNotFoundError(index_path)
    data = json.loads(index_path.read_text(encoding="utf-8", errors="replace"))
    return build_flat_semantic_corpus(
        data,
        entry_limit=entry_limit,
        entry_max_chars=entry_max_chars,
    )
