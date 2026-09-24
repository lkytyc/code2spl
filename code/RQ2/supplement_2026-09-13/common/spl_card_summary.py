"""Render an Exp2 SPL atomic card as an unstructured natural-language summary.

Motivation
----------
The Experiment 2 ablation needs a condition whose *semantic content* is the same
as the tagged SPL card but whose *keyword structure* is gone, and which is
delivered through the same prompt framing as `raw_free_summary` (numbered source
plus an auxiliary prose summary).  Nothing here adds SPL keyword usage back:
every `[TAG]`, `[END_TAG]` and `<REF>` marker is removed and the payload is
rewritten as plain English.

Scope
-----
The card grammar, measured over all 341 frozen cards in
`spl/s/f341/instances/*/assets/spl.txt`, is exactly:

    [DEFINE_WORKER: "<description>" <name>]     279
        [INPUTS] ... [END_INPUTS]               279   (may be empty)
        [OUTPUTS] ... [END_OUTPUTS]             279
        [MAIN_FLOW] ... [END_MAIN_FLOW]         279
            [SEQUENTIAL_BLOCK] ... [END_SEQUENTIAL_BLOCK]   447
            [COMMAND <text> RESULT <name>]      3931  (always ends with RESULT)
            [ALTERNATIVE_FLOW: <condition>] ... 168
            [EXCEPTION_FLOW: <condition>] ...    90
                [LOG "..."] / [THROW <Type> "..."]
        [END_WORKER]                            279

`[ALTERNATIVE_FLOW]` and `[EXCEPTION_FLOW]` appear both nested inside
`[MAIN_FLOW]` and after `[END_MAIN_FLOW]` at worker level, so this module does a
linear in-order scan rather than assuming a tree.  `<REF> x </REF>` wraps
contract names (858 occurrences).

65 of the 341 frozen cards carry no structure at all: the SPL generation model
emitted JSON that failed to parse and the pipeline stored the raw text under a
`# JSON_PARSE_ERROR` header.  Those are passed through verbatim and reported as
`passthrough` so the ablation never silently drops content.
"""

from __future__ import annotations

import re
from typing import Any

__all__ = [
    "parse_card",
    "render_card_as_summary",
    "audit_content_preservation",
]

# --- tag vocabulary ---------------------------------------------------------

# Greedy on the description: it may itself contain `]` (e.g. "... returns
# [main data] ..."), and the header always ends with `" <name>]`, so matching to
# the last such occurrence is unambiguous.
_RE_WORKER = re.compile(r'^\[DEFINE_WORKER:\s*"(?P<desc>.*)"\s+(?P<name>[^\]\s]+)\s*\]$')
_RE_REF = re.compile(r"<REF>\s*(?P<name>.*?)\s*</REF>")
# The payload may itself contain `]` (e.g. `RESULT a[i]`), so the body is taken
# greedily up to the final bracket and then split on the LAST ` RESULT `.
_RE_COMMAND = re.compile(r"^\[COMMAND\s+(?P<body>.*)\]$")
_RE_LOG = re.compile(r'^\[LOG\s+"(?P<text>.*)"\]$')
_RE_THROW = re.compile(r'^\[THROW\s+(?P<type>[A-Za-z_][A-Za-z0-9_.]*)\s+"(?P<text>.*)"\]$')
_RE_FLOW = re.compile(r"^\[(?P<kind>ALTERNATIVE_FLOW|EXCEPTION_FLOW):\s*(?P<cond>.*)\]$")
# A contract entry such as:  <REF> sx </REF>: int "Initial x-coordinate."
# Contract names may be dotted or subscripted (`System.in`, `path[target]`).
_RE_CONTRACT = re.compile(
    r"^(?P<name><REF>.*?</REF>|[A-Za-z_][\w.\[\]]*)\s*:\s*(?P<type>[^\"\n]+?)\s*"
    r'(?:"(?P<desc>.*)")?\s*$'
)

# Brackets whose contents are prose, not our tags; used to decide whether a
# physical line is a tag line at all.
_ANY_TAG = re.compile(r"^\[(?:/?[A-Z_]+|COMMAND|LOG|THROW|DEFINE_WORKER)[\s:\]]")

_KNOWN_TAGS = {
    "DEFINE_WORKER", "END_WORKER", "INPUTS", "END_INPUTS", "OUTPUTS", "END_OUTPUTS",
    "MAIN_FLOW", "END_MAIN_FLOW", "SEQUENTIAL_BLOCK", "END_SEQUENTIAL_BLOCK",
    "ALTERNATIVE_FLOW", "END_ALTERNATIVE_FLOW", "EXCEPTION_FLOW", "END_EXCEPTION_FLOW",
}


_TAG_NAMES = (
    "DEFINE_WORKER|INPUTS|OUTPUTS|MAIN_FLOW|SEQUENTIAL_BLOCK|ALTERNATIVE_FLOW|EXCEPTION_FLOW"
)
# Block tags have no quoted payload, so they can be delimited by the first `]`.
_BLOCK_TAGS = (
    "INPUTS|OUTPUTS|MAIN_FLOW|SEQUENTIAL_BLOCK|ALTERNATIVE_FLOW|EXCEPTION_FLOW"
)
# Split *before* each tag start.  Array subscripts such as `a[i]` or
# `boolean[size][size]` do not name a tag, so they never become split points.
_TAG_SPLIT = re.compile(
    rf"(?=\[(?:END_)?(?:{_TAG_NAMES})\b|\[COMMAND\s|\[LOG\s|\[THROW\s)"
)
# One leading tag.  `COMMAND`/`LOG`/`THROW` bodies may contain `]` (e.g.
# `RESULT a[i]`), and a chunk never holds a second tag, so `.*` is safe there.
_LEAD_TAG = re.compile(
    rf'^\[(?:COMMAND\s.*|LOG\s.*|THROW\s.*'
    rf'|DEFINE_WORKER:\s*".*"\s+[^\]\s]+\]'
    rf"|(?:END_)?(?:{_BLOCK_TAGS})\b[^\]]*)\]"
)


def _iter_units(card: str):
    """Yield one tag or one plain text line at a time, in document order.

    Cards are usually one tag per line, but some are emitted minified with many
    tags on a single physical line, so tokens are cut at tag starts rather than
    at newlines.
    """
    for chunk in _TAG_SPLIT.split(card):
        chunk = chunk.strip()
        while chunk:
            m = _LEAD_TAG.match(chunk)
            if m:
                yield m.group(0)
                chunk = chunk[m.end():].strip()
                continue
            line, _, rest = chunk.partition("\n")
            line = line.strip()
            if line:
                yield line
            chunk = rest.strip()


def parse_card(card: str) -> dict[str, Any]:
    """Parse a tagged card into its semantic payload.

    Returns a dict with `structured=False` when the text carries no SPL tags
    (the `# JSON_PARSE_ERROR` cards), in which case the caller must pass it
    through untouched.
    """
    text = str(card or "").strip()
    if "[DEFINE_WORKER" not in text and "[MAIN_FLOW]" not in text:
        return {"structured": False, "raw": text}

    out: dict[str, Any] = {
        "structured": True,
        "worker_name": "",
        "description": "",
        "inputs": [],
        "outputs": [],
        "steps": [],          # in document order
        "alternatives": [],
        "exceptions": [],
        "unknown_tag_lines": [],
    }
    section: str | None = None
    current_flow: dict[str, Any] | None = None

    for line in _iter_units(text):
        if not line:
            continue

        m = _RE_WORKER.match(line)
        if m:
            out["worker_name"] = m.group("name")
            out["description"] = m.group("desc").strip()
            continue

        if line in ("[INPUTS]", "[OUTPUTS]"):
            section = line[1:-1].lower()
            continue
        if line in ("[END_INPUTS]", "[END_OUTPUTS]"):
            section = None
            continue

        if line in ("[MAIN_FLOW]", "[SEQUENTIAL_BLOCK]",
                    "[END_MAIN_FLOW]", "[END_SEQUENTIAL_BLOCK]",
                    "[END_WORKER]", "[END_ALTERNATIVE_FLOW]", "[END_EXCEPTION_FLOW]"):
            if line in ("[END_ALTERNATIVE_FLOW]", "[END_EXCEPTION_FLOW]"):
                current_flow = None
            continue

        m = _RE_FLOW.match(line)
        if m:
            flow = {"condition": m.group("cond").strip(), "steps": [], "logs": []}
            (out["alternatives"] if m.group("kind") == "ALTERNATIVE_FLOW"
             else out["exceptions"]).append(flow)
            current_flow = flow
            continue

        if section in ("inputs", "outputs"):
            m = _RE_CONTRACT.match(_strip_ref(line))
            if m:
                out[section].append({
                    "name": m.group("name").strip(),
                    "type": (m.group("type") or "").strip().rstrip(","),
                    "description": (m.group("desc") or "").strip(),
                })
                continue
            out["unknown_tag_lines"].append(line)
            continue

        m = _RE_COMMAND.match(line)
        if m:
            body = m.group("body").strip()
            idx = body.rfind(" RESULT ")
            text, result = (body[:idx], body[idx + 8:]) if idx >= 0 else (body, "")
            step = {"text": text.strip(), "result": result.strip()}
            (current_flow["steps"] if current_flow else out["steps"]).append(step)
            continue

        m = _RE_LOG.match(line)
        if m:
            payload = {"kind": "log", "text": m.group("text").strip()}
            (current_flow["logs"] if current_flow else out["unknown_tag_lines"]).append(
                payload if current_flow else line
            )
            continue

        m = _RE_THROW.match(line)
        if m:
            payload = {"kind": "throw", "type": m.group("type"), "text": m.group("text").strip()}
            (current_flow["logs"] if current_flow else out["unknown_tag_lines"]).append(
                payload if current_flow else line
            )
            continue

        if _ANY_TAG.match(line):
            out["unknown_tag_lines"].append(line)

    return out


def _strip_ref(text: str) -> str:
    return _RE_REF.sub(lambda m: m.group("name"), text).strip()


def _clean(text: str) -> str:
    """Collapse whitespace and normalise `<REF>` so payloads compare equal."""
    return re.sub(r"\s+", " ", _strip_ref(str(text))).strip()


def _sentence(text: str) -> str:
    t = _clean(text)
    return t if t.endswith((".", "!", "?", ";", ":")) else t + "."


def render_card_as_summary(card: str) -> tuple[str, dict[str, Any]]:
    """Render one tagged card as an unstructured prose summary.

    Returns `(summary_text, audit)`.  When the card carries no SPL structure the
    input is returned unchanged with `audit['mode'] == 'passthrough'`, so the
    condition degrades to "identical to the tagged card" rather than losing
    content.
    """
    parsed = parse_card(card)
    if not parsed["structured"]:
        return str(card or "").strip(), {
            "mode": "passthrough",
            "reason": "card carries no SPL tag structure",
            "chars_in": len(str(card or "").strip()),
            "chars_out": len(str(card or "").strip()),
        }

    lines: list[str] = []

    head = f"Function {parsed['worker_name'] or '<anonymous>'}"
    if parsed["description"]:
        head += f": {_sentence(parsed['description'])}"
    else:
        head += "."
    lines.append(head)

    def _contract_line(lead: str, entries: list[dict[str, str]]) -> str:
        items = [
            f"{p['name']} ({p['type']})" + (f" — {_clean(p['description'])}" if p["description"] else "")
            for p in entries
        ]
        text = lead + "; ".join(items)
        return text if text.endswith((".", "!", "?", ":")) else text + "."

    if parsed["inputs"]:
        lines.append(_contract_line("It takes ", parsed["inputs"]))
    if parsed["outputs"]:
        lines.append(_contract_line("It returns ", parsed["outputs"]))

    if parsed["steps"]:
        lines.append("The behaviour proceeds in this order:")
        for i, step in enumerate(parsed["steps"], 1):
            entry = f"{i}. {_sentence(step['text'])}"
            if step["result"]:
                entry += f" This produces {step['result']}."
            lines.append(entry)

    for flow in parsed["alternatives"]:
        lines.append(f"If {_clean(flow['condition'])}:")
        for step in flow["steps"]:
            entry = f"  - {_sentence(step['text'])}"
            if step["result"]:
                entry += f" This produces {step['result']}."
            lines.append(entry)

    for flow in parsed["exceptions"]:
        actions = []
        for item in flow["logs"]:
            if isinstance(item, dict) and item.get("kind") == "log":
                actions.append(f'logs "{_clean(item["text"])}"')
            elif isinstance(item, dict) and item.get("kind") == "throw":
                actions.append(f'raises {item["type"]}: "{_clean(item["text"])}"')
        cond = _clean(flow["condition"]).rstrip(".")
        tail = (" In this case the code " + " and ".join(actions) + ".") if actions else ""
        lines.append(f"{cond}.{tail}")

    summary = "\n".join(lines).strip()
    audit = {
        "mode": "rendered",
        "worker_name": parsed["worker_name"],
        "steps": len(parsed["steps"]),
        "alternatives": len(parsed["alternatives"]),
        "exceptions": len(parsed["exceptions"]),
        "unknown_tag_lines": parsed["unknown_tag_lines"],
        "chars_in": len(str(card or "").strip()),
        "chars_out": len(summary),
    }
    return summary, audit


def audit_content_preservation(card: str, summary: str) -> dict[str, Any]:
    """Verify every payload of `card` survives into `summary`.

    Compares the *payloads* extracted from the tagged card against the rendered
    prose.  Any miss is reported so the caller can refuse to run the condition
    rather than silently ablate content along with structure.
    """
    parsed = parse_card(card)
    if not parsed["structured"]:
        return {
            "structured": False,
            "ok": str(card or "").strip() == str(summary or "").strip(),
            "missing": [],
            "checked": 0,
        }

    hay = _clean(summary)
    payloads: list[tuple[str, str]] = []
    if parsed["description"]:
        payloads.append(("description", parsed["description"]))
    for p in parsed["inputs"]:
        if p["description"]:
            payloads.append((f"input:{p['name']}", p["description"]))
    for p in parsed["outputs"]:
        if p["description"]:
            payloads.append((f"output:{p['name']}", p["description"]))
    for step in parsed["steps"]:
        payloads.append(("step", step["text"]))
        if step["result"]:
            payloads.append(("result", step["result"]))
    for flow in parsed["alternatives"]:
        payloads.append(("alternative_condition", flow["condition"]))
        for step in flow["steps"]:
            payloads.append(("step", step["text"]))
            if step["result"]:
                payloads.append(("result", step["result"]))
    for flow in parsed["exceptions"]:
        payloads.append(("exception_condition", flow["condition"]))
        for item in flow["logs"]:
            if isinstance(item, dict):
                payloads.append((item["kind"], item["text"]))

    missing = []
    for kind, text in payloads:
        needle = _clean(text)
        if not needle:
            continue
        if needle not in hay:
            missing.append({"kind": kind, "text": needle[:200]})

    return {
        "structured": True,
        "ok": not missing,
        "missing": missing,
        "checked": len(payloads),
    }
