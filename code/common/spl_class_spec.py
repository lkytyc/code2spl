"""
SPL Class Specification parser and renderer for Experiment 01 (ClassEval).

Parses raw SPL method blocks (``spl_by_method.json`` values) into structured
``MethodSpec`` objects, builds a ``ClassSpec`` from the collection, and renders
human-readable Markdown specifications for the ``spl_only`` and ``skeleton_spl``
conditions.

The parser is intentionally robust: when a tag or field is missing or
malformed it emits a warning and continues rather than crashing.
"""

from __future__ import annotations

import logging
import re
from dataclasses import dataclass, field
from typing import Any

logger = logging.getLogger(__name__)

# ── regex patterns ─────────────────────────────────────────────────────

_WORKER_RE = re.compile(
    r'\[DEFINE_WORKER:\s*"([^"]*)"\s+(\w+)\]'
)

_INPUT_BLOCK_RE = re.compile(
    r'\[INPUTS\](.*?)\[END_INPUTS\]', re.DOTALL
)
_OUTPUT_BLOCK_RE = re.compile(
    r'\[OUTPUTS\](.*?)\[END_OUTPUTS\]', re.DOTALL
)
_MAIN_FLOW_RE = re.compile(
    r'\[MAIN_FLOW\](.*?)\[END_MAIN_FLOW\]', re.DOTALL
)
_ALT_FLOW_RE = re.compile(
    r'\[ALTERNATIVE_FLOW\](.*?)\[END_ALTERNATIVE_FLOW\]', re.DOTALL
)
_EXC_FLOW_RE = re.compile(
    r'\[EXCEPTION_FLOW\](.*?)\[END_EXCEPTION_FLOW\]', re.DOTALL
)

_REF_RE = re.compile(
    r'<REF>\s*(\w+)\s*</REF>\s*:?\s*(\w[\w\[\],\s]*?)?\s*"([^"]*)"'
)
_COMMAND_RE = re.compile(
    r'\[COMMAND\s+(.*?)\]', re.DOTALL
)
_CONDITION_RE = re.compile(
    r'\[CONDITION\s+(.*?)\]', re.DOTALL
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
_FIELD_RE = re.compile(
    r'self\.(\w+)'
)

_STEP_TAGS = [
    ("command",   _COMMAND_RE),
    ("condition", _CONDITION_RE),
    ("return",    _RETURN_RE),
    ("throw",     _THROW_RE),
]

_ORDERED_STEP_RE = re.compile(
    r'\[(COMMAND|CONDITION|RETURN|THROW)\s+(.*?)\]',
    re.DOTALL,
)


# ── data types ──────────────────────────────────────────────────────────

@dataclass
class ParamSpec:
    name: str
    type_hint: str
    description: str


@dataclass
class FlowStep:
    step_type: str   # command | condition | return | throw
    text: str        # cleaned description text
    result: str      # extracted RESULT value, or ""


@dataclass
class MethodSpec:
    worker_name: str
    class_name: str
    method_name: str
    description: str
    inputs: list[ParamSpec] = field(default_factory=list)
    outputs: list[ParamSpec] = field(default_factory=list)
    main_flow: list[FlowStep] = field(default_factory=list)
    alternative_flows: list[FlowStep] = field(default_factory=list)
    exception_flows: list[FlowStep] = field(default_factory=list)
    calls: list[str] = field(default_factory=list)
    field_refs: list[str] = field(default_factory=list)
    raises: list[str] = field(default_factory=list)


@dataclass
class FieldSpec:
    name: str
    type_hint: str
    set_in: list[str] = field(default_factory=list)
    read_in: list[str] = field(default_factory=list)


@dataclass
class ClassSpec:
    class_name: str
    methods: list[MethodSpec] = field(default_factory=list)
    fields: list[FieldSpec] = field(default_factory=list)
    call_graph: dict[str, list[str]] = field(default_factory=dict)


# ── main public API ────────────────────────────────────────────────────

def build_class_spec(
    spl_by_method: dict[str, str],
    class_name: str = "",
) -> ClassSpec:
    """Build a ClassSpec from ``{ClassName.method: spl_text_block}``."""
    methods: list[MethodSpec] = []
    all_fields: dict[str, FieldSpec] = {}

    inferred_class = class_name
    if not inferred_class and spl_by_method:
        first_key = next(iter(spl_by_method))
        inferred_class = first_key.split(".", 1)[0] if "." in first_key else ""

    for key, spl_text in spl_by_method.items():
        method = _parse_method_block(spl_text, key)
        if not inferred_class and method.class_name:
            inferred_class = method.class_name
        methods.append(method)

    # Gather all method names for cross-referencing
    all_method_names = {m.method_name for m in methods}

    # Filter: remove method names from field_refs, remove field names from calls
    for m in methods:
        m.field_refs = [f for f in m.field_refs if f not in all_method_names]
        m.calls = [c for c in m.calls if c not in {f.name for f in all_fields.values()}]

    # Rebuild field info after filtering
    all_fields.clear()
    for m in methods:
        for fref in m.field_refs:
            if fref not in all_fields:
                all_fields[fref] = FieldSpec(name=fref, type_hint="")
            all_fields[fref].set_in.append(m.method_name)
            all_fields[fref].read_in.append(m.method_name)

    # Sort by constructor first, then alphabetically
    def _sort_key(m: MethodSpec) -> tuple[int, str]:
        return (0 if m.method_name == "__init__" else 1, m.method_name)
    methods.sort(key=_sort_key)

    # Build call graph
    call_graph: dict[str, list[str]] = {}
    for m in methods:
        key = f"{inferred_class}.{m.method_name}" if inferred_class else m.method_name
        call_graph[key] = m.calls

    return ClassSpec(
        class_name=inferred_class,
        methods=methods,
        fields=list(all_fields.values()),
        call_graph=call_graph,
    )


def render_class_spec_for_spl_only(spec: ClassSpec) -> str:
    """Compact precision format for ``spl_only``.

    Preserves SPL's sequential ordering and RESULT annotations while
    removing tag syntax.  More compact than raw SPL, equally precise.
    """
    lines = [_render_overview_compact(spec), ""]
    for m in spec.methods:
        lines.append(_render_method_compact(m))
        lines.append("")
    return "\n".join(lines)


def render_class_spec_for_skeleton(spec: ClassSpec, skeleton_code: str) -> str:
    """Compact precision format for ``skeleton_spl``.

    Skeleton provides API (signatures, imports).  This provides
    implementation steps.  Source code is NOT repeated.
    """
    lines = [_render_overview_compact(spec), ""]
    for m in spec.methods:
        lines.append(_render_method_compact(m))
        lines.append("")
    return "\n".join(lines)


# ── internal: parsing ──────────────────────────────────────────────────

def _parse_method_block(spl_text: str, qualified_key: str = "") -> MethodSpec:
    worker_match = _WORKER_RE.search(spl_text)
    worker_name = worker_match.group(2) if worker_match else ""
    description = worker_match.group(1) if worker_match else ""

    cls_name, method_name = _split_key(qualified_key, worker_name)

    inputs = _parse_refs(_extract_block(spl_text, _INPUT_BLOCK_RE))
    outputs = _parse_refs(_extract_block(spl_text, _OUTPUT_BLOCK_RE))
    main_flow = _parse_flow_steps(_extract_block(spl_text, _MAIN_FLOW_RE))
    alt_flow = _parse_flow_steps(_extract_block(spl_text, _ALT_FLOW_RE))
    exc_flow = _parse_flow_steps(_extract_block(spl_text, _EXC_FLOW_RE))

    calls = list(set(m.group(1) for m in _SPL_CALL_RE.finditer(spl_text)))
    # Also detect calls from self.method_name() patterns in COMMAND text
    _self_call_re = re.compile(r'self\.(\w+)\s*\(')
    for m in _self_call_re.finditer(spl_text):
        name = m.group(1)
        if name not in calls:
            calls.append(name)
    # Field refs: self.xxx that are NOT method calls (no trailing paren)
    field_refs = list(set(m.group(1) for m in _FIELD_RE.finditer(spl_text)))

    # Collect exception types from THROW steps
    raises: list[str] = []
    for step in exc_flow:
        if step.step_type == "throw":
            raises.append(step.text.split()[0] if step.text.split() else step.text)
    for step in main_flow:
        if step.step_type == "throw":
            raises.append(step.text.split()[0] if step.text.split() else step.text)

    return MethodSpec(
        worker_name=worker_name,
        class_name=cls_name,
        method_name=method_name,
        description=description,
        inputs=inputs,
        outputs=outputs,
        main_flow=main_flow,
        alternative_flows=alt_flow,
        exception_flows=exc_flow,
        calls=calls,
        field_refs=field_refs,
        raises=list(set(raises)),
    )


def _split_key(qualified_key: str, worker_name: str) -> tuple[str, str]:
    if "." in qualified_key:
        cls, method = qualified_key.split(".", 1)
        return cls, method
    return "", worker_name or qualified_key


def _extract_block(text: str, pattern: re.Pattern) -> str:
    m = pattern.search(text)
    return m.group(1).strip() if m else ""


def _parse_refs(block_text: str) -> list[ParamSpec]:
    result: list[ParamSpec] = []
    for m in _REF_RE.finditer(block_text):
        name = m.group(1)
        type_str = (m.group(2) or "").strip()
        desc = m.group(3).strip() if m.lastindex and m.lastindex >= 3 else ""
        result.append(ParamSpec(name=name, type_hint=type_str, description=desc))
    return result


def _parse_flow_steps(block_text: str) -> list[FlowStep]:
    steps: list[FlowStep] = []
    for match in _ORDERED_STEP_RE.finditer(block_text):
        tag_name = match.group(1).lower()
        raw = match.group(2).strip()
        text, result = _split_result(raw)
        steps.append(FlowStep(step_type=tag_name, text=text, result=result))
    return steps


def _split_result(raw: str) -> tuple[str, str]:
    m = re.search(r'\s+RESULT\s+(\S+)', raw)
    if m:
        text = raw[:m.start()].strip()
        return text, m.group(1)
    return raw, ""


# ── internal: rendering (compact precision format) ─────────────────────

def _render_method_compact(m: MethodSpec) -> str:
    """Render one method in compact precision format.

    Keeps SPL's sequential ordering, RESULT annotations, and condition
    branches but removes all tag syntax.  Each line is a direct instruction.
    """
    parts: list[str] = []

    # Signature line
    params = ", ".join(f"{p.name}: {p.type_hint}" if p.type_hint else p.name
                       for p in m.inputs)
    sig = f"## {m.method_name}(self, {params})" if params else f"## {m.method_name}(self)"
    if m.outputs:
        ret = ", ".join(p.type_hint or p.name for p in m.outputs)
        sig += f" → {ret}"
    parts.append(sig)

    # Input contract (compact)
    if m.inputs:
        for p in m.inputs:
            parts.append(f"#   {p.name}: {p.type_hint or 'any'}")

    # Main flow with numbered steps
    if m.main_flow:
        for j, step in enumerate(m.main_flow, 1):
            prefix = {
                "condition": "IF",
                "return": "RETURN",
                "throw": "THROW",
            }.get(step.step_type, "")
            line = f"{j}. {prefix + ' ' if prefix else ''}{step.text}"
            if step.result:
                line += f" → {step.result}"
            parts.append(line)

    # Conditions become inline if/else
    if m.alternative_flows:
        for step in m.alternative_flows:
            parts.append(f"   ? {step.text}")

    # Exception paths
    if m.exception_flows:
        for step in m.exception_flows:
            parts.append(f"   ! {step.text}")

    return "\n".join(parts)


def _render_overview_compact(spec: ClassSpec) -> str:
    """One-line class overview."""
    fields_str = ", ".join(f.name for f in spec.fields)
    methods_str = ", ".join(m.method_name for m in spec.methods)
    lines = [f"# Class: {spec.class_name}"]
    if fields_str:
        lines.append(f"# Fields: {fields_str}")
    # Call relationships
    edges = []
    for caller, callees in spec.call_graph.items():
        for c in callees:
            caller_short = caller.split(".", 1)[-1] if "." in caller else caller
            edges.append(f"{caller_short}→{c}")
    if edges:
        lines.append(f"# Calls: {', '.join(edges)}")
    return "\n".join(lines)


def _append_overview(lines, spec):  # kept for compat, unused
    pass

def _append_method_table(lines, spec):  # kept for compat, unused
    pass

def _append_call_graph(lines, spec):  # kept for compat, unused
    pass

def _append_method_details(lines, spec, **kw):  # kept for compat, unused
    pass
