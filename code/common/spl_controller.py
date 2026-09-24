from __future__ import annotations

import re
from dataclasses import asdict, dataclass, field
from typing import Any


DEFAULT_GENERIC_TERMS = {
    "actual",
    "also",
    "array",
    "before",
    "build",
    "case",
    "class",
    "code",
    "collection",
    "correct",
    "data",
    "different",
    "does",
    "error",
    "expected",
    "field",
    "file",
    "first",
    "format",
    "function",
    "handle",
    "incorrect",
    "input",
    "into",
    "issue",
    "last",
    "line",
    "map",
    "method",
    "object",
    "only",
    "output",
    "parse",
    "process",
    "result",
    "return",
    "same",
    "second",
    "split",
    "string",
    "than",
    "then",
    "type",
    "value",
}

ACTION_TERMS = {
    "add": {"add", "append", "insert", "create", "new"},
    "remove": {"remove", "delete", "drop", "clear"},
    "alter": {"alter", "change", "update", "replace", "modify", "convert", "migrate"},
    "parse_format": {
        "parse",
        "format",
        "split",
        "join",
        "quote",
        "escape",
        "unescape",
        "encode",
        "decode",
        "serialize",
        "deserialize",
        "string",
    },
    "exception": {"exception", "error", "throw", "raise", "warning", "message"},
    "data_flow": {
        "value",
        "result",
        "field",
        "state",
        "type",
        "dtype",
        "shape",
        "dimension",
        "coord",
        "concat",
        "combine",
        "dependency",
        "foreign",
        "key",
    },
}


@dataclass
class IssueProfile:
    terms: list[str]
    action_kinds: list[str]
    raw_text: str = ""


@dataclass
class SourceBoundCard:
    owner_id: str
    file_path: str
    source_anchor: str
    spl_summary: str
    selected_spl: str
    label: str
    score: int
    reasons: list[str] = field(default_factory=list)


@dataclass
class OwnerRanking:
    selected_owners: list[str]
    ranked_owners: list[str]
    cards: list[SourceBoundCard]
    audit: dict[str, Any]

    def to_dict(self) -> dict[str, Any]:
        return {
            "selected_owners": self.selected_owners,
            "ranked_owners": self.ranked_owners,
            "cards": [asdict(card) for card in self.cards],
            "audit": self.audit,
        }


def _split_identifier(text: str) -> set[str]:
    tokens: set[str] = set()
    for token in re.findall(r"[A-Za-z_][A-Za-z0-9_]*", str(text or "")):
        parts = re.findall(r"[A-Z][a-z]+|[a-z]+|[A-Z]+(?=[A-Z]|$)|[0-9]+", token)
        tokens.update(part.lower() for part in parts if len(part) > 1)
    return tokens


def _terms(text: str, generic_terms: set[str]) -> set[str]:
    out = {
        token.lower()
        for token in re.findall(r"\b[A-Za-z_][A-Za-z0-9_]*\b", str(text or ""))
        if len(token) > 2
    }
    expanded = set(out)
    for token in out:
        expanded |= _split_identifier(token)
        if len(token) > 4 and token.endswith("s"):
            expanded.add(token[:-1])
    return {term for term in expanded if term not in generic_terms}


def _action_kinds(text: str) -> set[str]:
    toks = _split_identifier(text)
    return {kind for kind, values in ACTION_TERMS.items() if toks & values}


def _method_name(owner_id: str) -> str:
    signature = str(owner_id or "").split("::", 1)[1] if "::" in str(owner_id or "") else str(owner_id or "")
    before_args = signature.split("(", 1)[0].strip()
    return before_args.split()[-1] if before_args else signature


def _summary_from_spl(spl_text: str) -> str:
    for line in str(spl_text or "").splitlines():
        stripped = line.strip()
        match = re.match(r'\[DEFINE_WORKER:\s*"(?P<summary>.*?)"', stripped)
        if match:
            return match.group("summary").strip()
    return ""


def _selected_spl_slice(spl_text: str, profile_terms: set[str], max_lines: int = 8) -> str:
    selected: list[str] = []
    concrete_tags = (
        "[COMMAND",
        "[CONDITION",
        "[RETURN",
        "[THROW",
        "[ALTERNATIVE_FLOW",
        "[EXCEPTION_FLOW",
    )
    for line in str(spl_text or "").splitlines():
        stripped = line.strip()
        lower = stripped.lower()
        if not stripped.startswith(concrete_tags):
            continue
        if profile_terms and not any(re.search(rf"\b{re.escape(term)}\b", lower) for term in profile_terms):
            continue
        selected.append(stripped)
        if len(selected) >= max_lines:
            break
    if not selected:
        for line in str(spl_text or "").splitlines():
            stripped = line.strip()
            if stripped.startswith(concrete_tags):
                selected.append(stripped)
                if len(selected) >= min(3, max_lines):
                    break
    return "\n".join(selected)


class SPLController:
    """Program-side SPL workflow for source-bound localization support.

    The controller converts noisy SPL pools into a small owner ranking and
    source-bound behavior cards. It is deliberately not an oracle: the original
    localization result remains the primary repair owner, while SPL can add
    high-confidence owners inside the current task boundary.
    """

    def __init__(self, *, generic_terms: set[str] | None = None, top_k: int = 3):
        self.generic_terms = set(generic_terms or DEFAULT_GENERIC_TERMS)
        self.top_k = max(1, int(top_k))

    def classify_issue(self, *texts: str) -> IssueProfile:
        raw = "\n".join(str(text or "") for text in texts)
        issue_terms = sorted(_terms(raw, self.generic_terms))
        return IssueProfile(
            terms=issue_terms,
            action_kinds=sorted(_action_kinds(raw)),
            raw_text=raw,
        )

    def rank_method_owners(
        self,
        *,
        methods: list[dict[str, Any]],
        spl_by_owner: dict[str, str],
        raw_owners: list[str],
        issue_profile: IssueProfile,
    ) -> OwnerRanking:
        method_by_id = {str(method.get("method_id") or ""): method for method in methods}
        raw_rank = {owner: idx for idx, owner in enumerate(raw_owners) if owner in method_by_id}
        profile_terms = set(issue_profile.terms)
        issue_kinds = set(issue_profile.action_kinds)
        scored: list[SourceBoundCard] = []

        for method in methods:
            owner_id = str(method.get("method_id") or "")
            if not owner_id:
                continue
            source = str(method.get("code") or "")
            spl_text = str(spl_by_owner.get(owner_id, ""))
            file_path = str(method.get("relative_path") or method.get("file_path") or "")
            source_terms = _terms(owner_id + "\n" + source, self.generic_terms)
            spl_terms = _terms(spl_text, self.generic_terms)
            owner_kinds = _action_kinds(owner_id + "\n" + source + "\n" + spl_text)

            source_hits = sorted(profile_terms & source_terms)
            spl_hits = sorted((profile_terms & spl_terms) - set(source_hits))
            is_raw = owner_id in raw_rank

            score = 0
            reasons: list[str] = []
            if is_raw:
                score += 1000 - raw_rank[owner_id] * 120
                reasons.append(f"raw_owner_rank={raw_rank[owner_id] + 1}")
            if source_hits:
                score += 70 * min(3, len(source_hits))
                reasons.append("source_terms=" + ",".join(source_hits[:6]))
            if spl_hits:
                score += 16 * min(3, len(spl_hits))
                reasons.append("spl_terms=" + ",".join(spl_hits[:6]))

            overlap = issue_kinds & owner_kinds
            if overlap:
                score += 45
                reasons.append("action_match=" + ",".join(sorted(overlap)))
            elif issue_kinds and owner_kinds and not is_raw:
                if "alter" in issue_kinds and "add" in owner_kinds:
                    score -= 90
                    reasons.append("penalty=add_helper_for_alter_issue")
                elif "remove" in issue_kinds and "add" in owner_kinds:
                    score -= 70
                    reasons.append("penalty=opposite_action")

            if is_raw:
                label = "PRIMARY_LOCALIZED_OWNER" if raw_rank[owner_id] == 0 else "LOCALIZED_OWNER"
            elif source_hits and overlap:
                label = "SOURCE_SPL_SUPPORTED_OWNER"
            elif source_hits:
                label = "SOURCE_ISSUE_MATCH"
            elif spl_hits:
                label = "SPL_RECALL_ONLY"
            else:
                label = "CONTEXT_ONLY"

            scored.append(
                SourceBoundCard(
                    owner_id=owner_id,
                    file_path=file_path,
                    source_anchor=_method_name(owner_id),
                    spl_summary=_summary_from_spl(spl_text),
                    selected_spl=_selected_spl_slice(spl_text, profile_terms),
                    label=label,
                    score=score,
                    reasons=reasons,
                )
            )

        scored.sort(key=lambda card: (-card.score, card.owner_id))
        selected: list[str] = []
        if raw_owners and raw_owners[0] in method_by_id:
            selected.append(raw_owners[0])

        promotable = {
            "PRIMARY_LOCALIZED_OWNER",
            "LOCALIZED_OWNER",
            "SOURCE_SPL_SUPPORTED_OWNER",
            "SOURCE_ISSUE_MATCH",
        }
        for card in scored:
            if len(selected) >= self.top_k:
                break
            if card.owner_id in selected:
                continue
            if card.label not in promotable:
                continue
            selected.append(card.owner_id)

        for owner in raw_owners:
            if len(selected) >= self.top_k:
                break
            if owner in method_by_id and owner not in selected:
                selected.append(owner)

        ranked = selected + [
            card.owner_id
            for card in scored
            if card.owner_id not in selected and card.label in promotable
        ]
        for owner in raw_owners:
            if owner not in ranked:
                ranked.append(owner)

        return OwnerRanking(
            selected_owners=selected,
            ranked_owners=ranked[:10],
            cards=[card for card in scored if card.owner_id in selected],
            audit={
                "issue_profile": asdict(issue_profile),
                "raw_owners": raw_owners,
                "top_k": self.top_k,
                "scored_candidates": [asdict(card) for card in scored[:20]],
                "guardrails": [
                    "raw top-1 owner is kept as primary when valid",
                    "SPL-only generic hits are not promoted",
                    "SPL cards remain bound to their source owner",
                ],
            },
        )
