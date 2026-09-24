"""
SPL Source Navigation Index for Experiment 02 (CoRe).

Extracts structured navigation information from SPL method blocks:
decision points, cross-function calls, field modifications, pure/leaf
functions, and exception paths.  Designed to supplement (not repeat)
the source code that is already present in the CoRe prompt.

The output is a compact Markdown index that helps the model quickly
locate control-flow decision points and cross-function relationships
without having to parse raw SPL tags.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field


# ── regex ──────────────────────────────────────────────────────────────

_WORKER_RE = re.compile(
    r'\[DEFINE_WORKER:\s*"([^"]*)"\s+(\w+)\]'
)
_CONDITION_RE = re.compile(
    r'\[CONDITION\s+(.*?)\]', re.DOTALL
)
_COMMAND_RE = re.compile(
    r'\[COMMAND\s+(.*?)\]', re.DOTALL
)
_RETURN_RE = re.compile(
    r'\[RETURN\s+(.*?)\]', re.DOTALL
)
_THROW_RE = re.compile(
    r'\[THROW\s+(.*?)\]', re.DOTALL
)
_SPL_CALL_RE = re.compile(
    r'<SPL>\s*(\w+)\s*</SPL>'
)
_SELF_CALL_RE = re.compile(
    r'self\.(\w+)\s*\('
)
_FIELD_WRITE_RE = re.compile(
    r'(?:self\.(\w+)\s*=|assign\s+(?:to\s+)?self\.(\w+)|set\s+(?:this\.)?(\w+)\s*(?:to|=))',
    re.IGNORECASE
)
_ALT_FLOW_RE = re.compile(
    r'\[ALTERNATIVE_FLOW\](.*?)\[END_ALTERNATIVE_FLOW\]', re.DOTALL
)
_EXC_FLOW_RE = re.compile(
    r'\[EXCEPTION_FLOW\](.*?)\[END_EXCEPTION_FLOW\]', re.DOTALL
)
_MAIN_FLOW_RE = re.compile(
    r'\[MAIN_FLOW\](.*?)\[END_MAIN_FLOW\]', re.DOTALL
)
_INPUT_BLOCK_RE = re.compile(
    r'\[INPUTS\](.*?)\[END_INPUTS\]', re.DOTALL
)
_OUTPUT_BLOCK_RE = re.compile(
    r'\[OUTPUTS\](.*?)\[END_OUTPUTS\]', re.DOTALL
)
_REF_RE = re.compile(
    r'<REF>\s*(\w+)\s*</REF>'
)


# ── data types ─────────────────────────────────────────────────────────

@dataclass
class DecisionPoint:
    function: str
    condition_text: str
    is_loop: bool = False


@dataclass
class CallInfo:
    callee: str
    caller: str
    conditional: bool = False


@dataclass
class FieldAccess:
    field: str
    function: str
    is_write: bool = False


@dataclass
class SourceIndex:
    functions: list[str] = field(default_factory=list)
    decision_points: dict[str, list[DecisionPoint]] = field(default_factory=dict)
    calls: dict[str, list[CallInfo]] = field(default_factory=dict)
    field_accesses: dict[str, list[FieldAccess]] = field(default_factory=dict)
    exceptions: dict[str, list[str]] = field(default_factory=dict)
    pure_functions: list[str] = field(default_factory=list)
    leaf_functions: list[str] = field(default_factory=list)


# ── public API ─────────────────────────────────────────────────────────

def build_source_index(
    spl_by_method: dict[str, str],
) -> SourceIndex:
    """Build a SourceIndex from ``{ClassName.method: spl_text_block}``."""
    index = SourceIndex()
    method_map: dict[str, str] = {}  # bare_name -> qualified_key

    for key, spl_text in spl_by_method.items():
        bare = key.split(".")[-1] if "." in key else key
        index.functions.append(bare)
        method_map[bare] = key

        # Decision points: from CONDITION tags AND from COMMAND text
        for m in _CONDITION_RE.finditer(spl_text):
            cond_text = _clean_text(m.group(1))
            is_loop = any(w in cond_text.lower() for w in ['while', 'loop', 'for each', 'iterate'])
            index.decision_points.setdefault(bare, []).append(
                DecisionPoint(function=bare, condition_text=cond_text, is_loop=is_loop)
            )
        # Also detect decision points from COMMAND text
        _decision_keywords = ['if ', 'else ', 'while ', 'for ', 'check ', 'decide', 'branch',
                              'condition', 'validate', 'determine']
        for m in _COMMAND_RE.finditer(spl_text):
            cmd_text = _clean_text(m.group(1))
            if any(kw in cmd_text.lower()[:30] for kw in _decision_keywords):
                # Avoid duplicates with CONDITION tags
                if not any(dp.condition_text in cmd_text for dp in index.decision_points.get(bare, [])):
                    index.decision_points.setdefault(bare, []).append(
                        DecisionPoint(function=bare, condition_text=cmd_text[:120])
                    )

        # Calls: SPL refs, self.method(), AND description patterns
        for m in _SPL_CALL_RE.finditer(spl_text):
            callee = m.group(1)
            if callee != bare:
                index.calls.setdefault(bare, []).append(
                    CallInfo(callee=callee, caller=bare))
        for m in _SELF_CALL_RE.finditer(spl_text):
            callee = m.group(1)
            if callee != bare and not any(c.callee == callee for c in index.calls.get(bare, [])):
                index.calls.setdefault(bare, []).append(
                    CallInfo(callee=callee, caller=bare))
        # Calls from description or COMMAND text
        _call_patterns = [r'calls?\s+(\w+)', r'invokes?\s+(\w+)', r'delegates?\s+to\s+(\w+)']
        for pat in _call_patterns:
            for m in re.finditer(pat, spl_text, re.IGNORECASE):
                callee = m.group(1)
                if (callee != bare and
                    not any(c.callee == callee for c in index.calls.get(bare, []))):
                    index.calls.setdefault(bare, []).append(
                        CallInfo(callee=callee, caller=bare))

        # Field accesses
        fields_seen = set()
        for m in _FIELD_WRITE_RE.finditer(spl_text):
            fname = m.group(1) or m.group(2) or m.group(3)
            if fname and fname not in fields_seen:
                fields_seen.add(fname)
                index.field_accesses.setdefault(fname, []).append(
                    FieldAccess(field=fname, function=bare, is_write=True)
                )

        # Exceptions
        for m in _THROW_RE.finditer(spl_text):
            exc_text = _clean_text(m.group(1))
            exc_type = exc_text.split()[0] if exc_text.split() else exc_text
            index.exceptions.setdefault(bare, []).append(exc_type)

    # Pure functions: no field writes, no calls
    all_callers = set()
    for calls in index.calls.values():
        for c in calls:
            all_callers.add(c.callee)
    for fname in index.functions:
        has_writes = any(
            fa.is_write for fas in index.field_accesses.values()
            for fa in fas if fa.function == fname
        )
        has_calls = fname in index.calls
        if not has_writes and not has_calls:
            index.pure_functions.append(fname)
        if fname not in index.calls or not index.calls.get(fname):
            index.leaf_functions.append(fname)

    return index


def render_source_index_for_raw_spl(index: SourceIndex) -> str:
    """Render a SourceIndex as a compact navigation supplement.

    When SPL data is sparse, falls back to a brief function summary.
    """
    lines: list[str] = []
    lines.append("## Source Navigation Index")
    lines.append("")
    lines.append("Auxiliary view — source code above is authoritative.")

    has_dp = any(v for v in index.decision_points.values())
    has_calls = any(v for v in index.calls.values())
    has_fields = any(v for v in index.field_accesses.values())
    has_exc = any(v for v in index.exceptions.values())

    # When SPL provides no structured data, show compact function list
    if not (has_dp or has_calls or has_fields or has_exc):
        lines.append("")
        lines.append("Functions: " + ", ".join(index.functions))
        if index.pure_functions:
            lines.append(f"Pure (no side effects): {', '.join(sorted(index.pure_functions))}")
        lines.append("")
        return "\n".join(lines)

    # Decision points
    if has_dp:
        lines.append("")
        lines.append("### Control Flow")
        for fname in index.functions:
            dps = index.decision_points.get(fname, [])
            if not dps:
                continue
            lines.append(f"**{fname}**:")
            for dp in dps:
                tag = "loop" if dp.is_loop else "branch"
                lines.append(f"  - [{tag}] {dp.condition_text[:150]}")

    # Cross-function calls
    if has_calls:
        lines.append("")
        lines.append("### Calls")
        for caller in sorted(index.calls):
            callees = index.calls[caller]
            unique = list(dict.fromkeys(c.callee for c in callees))
            lines.append(f"  - `{caller}` → {', '.join('`' + c + '`' for c in unique)}")

    # Fields
    if has_fields:
        lines.append("")
        lines.append("### State")
        for fname in sorted(index.field_accesses):
            fas = index.field_accesses[fname]
            writers = [fa.function for fa in fas if fa.is_write]
            if writers:
                lines.append(f"  - `{fname}` written by: {', '.join(writers)}")

    # Exceptions
    if has_exc:
        lines.append("")
        lines.append("### Exceptions")
        for fname in sorted(index.exceptions):
            excs = index.exceptions[fname]
            lines.append(f"  - `{fname}`: {', '.join(excs)}")

    # Summary
    if index.pure_functions:
        lines.append("")
        lines.append(f"Pure functions: {', '.join(sorted(index.pure_functions))}")

    lines.append("")
    return "\n".join(lines)


# ── internal ──────────────────────────────────────────────────────────

def _clean_text(text: str) -> str:
    """Collapse whitespace and strip."""
    return " ".join(text.split()).strip()
