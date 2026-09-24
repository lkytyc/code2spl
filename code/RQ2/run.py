from __future__ import annotations

import argparse
import json
import re
import string
import sys
from dataclasses import replace
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from common.paths import ensure_dir, read_config, read_json, resolve_in_project, write_json, write_text
from common.prompt_store import load_prompt as load_prompt_template
from common.providers import GenerationConfig, ModelClient
from common.run_utils import generation_kwargs, run_ordered, selected_items
from common.spl_adapter import (
    format_inline_spl_cards_generic,
    recover_spl_by_worker,
    select_task_relevant_spl_methods,
)
from common.spl_binding import bind_spl_to_source, render_bound_spl_cards
from common.spl_source_index import build_source_index, render_source_index_for_raw_spl
from common.usage import write_generation_result


EXPERIMENT_DIR = Path(__file__).resolve().parent
EXPERIMENT_NAME = EXPERIMENT_DIR.name


def load_prompt(condition: str) -> str:
    return load_prompt_template(EXPERIMENT_DIR, EXPERIMENT_NAME, condition, "prompt.md")


PROMPT_CONDITIONS = (
    "official_raw",
    "compressed_raw",
    "nl_summary",
    "raw_free_summary",
    "structured_summary",
    "raw_structured_summary",
    "spl_only",
    "raw_spl",
    "raw_spl_retrieved",
    "raw_spl_reasoned",
    "raw_spl_controlled",
    "raw_spl_atomic_controlled",
    "raw_spl_atomic_precise",
    "raw_spl_atomic_strict",
)
# Populated from the configured conditions in main(). A paper bundle may
# intentionally omit prompts for historical methods that are not being run.
PROMPTS: dict[str, str] = {}
ALLOWED_PROMPT_FIELDS = {
    "official_raw": {"official_prompt"},
    "compressed_raw": {"task_prompt", "compressed_raw"},
    "nl_summary": {"task_prompt", "summary"},
    "raw_free_summary": {"official_prompt", "summary"},
    "structured_summary": {"task_prompt", "structured_summary"},
    "raw_structured_summary": {"official_prompt", "structured_summary"},
    "spl_only": {"task_prompt", "spl_inline"},
    "raw_spl": {"official_prompt", "spl_inline"},
    "raw_spl_retrieved": {"official_prompt", "spl_index", "spl_inline"},
    "raw_spl_reasoned": {"official_prompt", "spl_inline"},
    "raw_spl_controlled": {"official_prompt", "spl_control", "spl_inline"},
    "raw_spl_atomic_controlled": {"official_prompt", "spl_control", "spl_inline"},
    "raw_spl_atomic_precise": {"official_prompt", "spl_control", "spl_inline"},
    "raw_spl_atomic_strict": {"official_prompt", "spl_control", "spl_inline"},
}


_DISPLAY_LINE = re.compile(r"^\s*(\d+)\s{2,}(.*)$")
_IDENTIFIER = re.compile(r"[A-Za-z_][A-Za-z0-9_]*")
_ANALYSIS_KEYWORDS = {
    "boolean", "break", "case", "catch", "char", "class", "const",
    "continue", "def", "do", "double", "else", "false", "float", "for",
    "if", "import", "in", "int", "long", "math", "max", "min", "new",
    "none", "null", "private", "protected", "public", "return", "static",
    "string", "switch", "true", "try", "void", "while",
}


def _source_analysis_candidates(
    source_text: str,
    task_kind: str,
    target_line: str,
    checkpoint_terms: list[str],
    selected_names: list[str],
    source_provenance: dict[str, dict] | None,
    *,
    limit: int = 18,
) -> list[dict[str, object]]:
    """Build a bounded source ledger; entries are candidates, never answers."""
    numbered: list[tuple[int, str]] = []
    for fallback, raw_line in enumerate(source_text.splitlines(), start=1):
        match = _DISPLAY_LINE.match(raw_line)
        numbered.append(
            (int(match.group(1)), match.group(2)) if match else (fallback, raw_line)
        )

    start, end = 1, numbered[-1][0] if numbered else 0
    provenance = source_provenance or {}
    for owner in selected_names:
        anchor = provenance.get(owner) or {}
        if anchor:
            start = int(anchor.get("source_start_line", start))
            end = int(anchor.get("source_end_line", end))
            break
    owner_lines = [(number, code) for number, code in numbered if start <= number <= end]
    target = int(target_line) if target_line else None

    if task_kind == "control dependence":
        candidates: list[dict[str, object]] = []
        control_head = re.compile(
            r"^\s*(?:else\s+)?(?:if|for|while|switch|case|catch)\b|^\s*else\s*[:{]",
            re.IGNORECASE,
        )
        exit_term = re.compile(r"\b(?:break|continue|return|raise|throw)\b", re.IGNORECASE)
        for number, code in owner_lines:
            if control_head.search(code) or exit_term.search(code):
                relation = "after-target cycle/exit candidate" if target and number > target else "pre-target/enclosing candidate"
                candidates.append({"line": number, "code": code.strip(), "relation": relation})
                if len(candidates) >= limit:
                    break
        return candidates

    if task_kind not in {"data dependence", "information flow"}:
        return []

    if task_kind == "information flow":
        # Information flow combines explicit definitions with implicit flows
        # through guards. Keep a bounded, source-only ledger across the whole
        # owner because updates after the target can reach it on a later loop
        # iteration. These rows are candidates for model disposition, not
        # precomputed answers.
        candidates = []
        definition = re.compile(
            r"(?<![=!<>])=(?!=)|\+=|-=|\*=|/=|%=|\+\+|--|\b(?:add|poll|push|pop|put|remove)\s*\(",
            re.IGNORECASE,
        )
        control = re.compile(
            r"^\s*(?:else\s+)?(?:if|for|while|switch|case|catch)\b|^\s*else\s*[:{]",
            re.IGNORECASE,
        )
        target_terms = set(checkpoint_terms)
        for number, code in owner_lines:
            identifiers = set(_IDENTIFIER.findall(code))
            if not (definition.search(code) or control.search(code)):
                continue
            relation = (
                "post-target loop-carried candidate" if target and number > target
                else "target-chain seed" if identifiers & target_terms
                else "definition/control candidate"
            )
            candidates.append({"line": number, "code": code.strip(), "relation": relation})
            if len(candidates) >= max(limit, 30):
                break
        return candidates

    worklist = list(dict.fromkeys(checkpoint_terms))
    seen_terms: set[str] = set()
    candidates: list[dict[str, object]] = []
    seen_lines: set[int] = set()
    eligible = [row for row in owner_lines if target is None or row[0] <= target]
    while worklist and len(candidates) < limit:
        term = worklist.pop(0)
        if term in seen_terms:
            continue
        seen_terms.add(term)
        term_re = re.compile(rf"\b{re.escape(term)}\b")
        for number, code in eligible:
            if not term_re.search(code) or not _line_defines_identifier(code, term):
                continue
            if number not in seen_lines:
                candidates.append({"line": number, "code": code.strip(), "seed": term})
                seen_lines.add(number)
            for token in _IDENTIFIER.findall(code):
                if token.lower() not in _ANALYSIS_KEYWORDS and token not in seen_terms:
                    worklist.append(token)
            if len(candidates) >= limit:
                break
    return sorted(candidates, key=lambda item: int(item["line"]))


def _line_defines_identifier(code: str, identifier: str) -> bool:
    """Conservatively identify declarations/assignments and loop iterators."""
    escaped = re.escape(identifier)
    if re.search(rf"\bfor\s+{escaped}\s+in\b", code):
        return True
    if re.search(rf"\bfor\s*\([^;]*\b{escaped}\b\s*=", code):
        return True
    return bool(re.search(
        rf"\b{escaped}\b(?:\s*\[[^\]]+\])?\s*(?:=(?!=)|\+=|-=|\*=|/=|%=|\+\+|--)",
        code,
    ))


def _dependency_evidence_ledger(
    candidates: list[dict[str, object]],
    checkpoint_terms: list[str],
    target_line: str,
) -> list[dict[str, object]]:
    """Classify source candidates without promoting any candidate to an answer."""
    target = int(target_line) if target_line else None
    ledger: list[dict[str, object]] = []
    for item in candidates:
        code = str(item.get("code") or "")
        line = int(item.get("line") or 0)
        identifiers = sorted(set(_IDENTIFIER.findall(code)))
        relevant = [
            term for term in checkpoint_terms
            if re.search(rf"\b{re.escape(term)}\b", code)
        ]
        definitions = [term for term in relevant if _line_defines_identifier(code, term)]
        roles: list[str] = []
        if definitions:
            roles.append("definition")
        if any(term not in definitions for term in relevant):
            roles.append("use")
        if re.search(r"^\s*(?:else\s+)?(?:if|for|while|switch|case|catch)\b|^\s*else\s*[:{]", code, re.I):
            roles.append("control")
        if re.search(r"\b(?:break|continue|return|raise|throw)\b", code, re.I):
            roles.append("exit")
        ledger.append({
            "line": line,
            "position": (
                "target" if target == line
                else "after_target" if target is not None and line > target
                else "before_target"
            ),
            "roles": roles or ["candidate"],
            "relevant_identifiers": relevant,
            "definitions": definitions,
            "source_identifiers": identifiers,
            "reason": item.get("relation") or item.get("seed") or "source candidate",
            "disposition": "inspect_against_official_dependence_definition",
        })
    return ledger


def _required_output_anchors(
    task_kind: str,
    target_line: str,
    target_variable: str,
    target_source_line: str,
    source_text: str = "",
    source_variable: str = "",
    source_line: str = "",
) -> list[dict[str, object]]:
    """Derive structural answer obligations from the authoritative target line."""
    if not target_line or not target_source_line:
        return []
    match = _DISPLAY_LINE.match(target_source_line)
    code = (match.group(2) if match else target_source_line).strip()
    line = int(target_line)
    anchors: list[dict[str, object]] = []
    if task_kind == "control dependence" and re.match(
        r"^(?:for|while)\b", code, re.IGNORECASE,
    ):
        anchors.append({
            "kind": "line",
            "line": line,
            "reason": "the target is a loop header whose condition controls its next execution",
        })
    if task_kind == "information flow" and target_variable:
        escaped = re.escape(target_variable)
        if re.search(rf"\b{escaped}\b\s*(?:\+=|-=|\*=|/=|%=|\+\+|--)", code):
            anchors.append({
                "kind": "variable_instance",
                "variable": target_variable,
                "line": line,
                "reason": "the target is a read-modify-write update that reads its prior value",
            })
        if source_line and source_text:
            trace_anchor = _loop_carried_trace_anchor(
                source_text,
                source_variable,
                int(source_line),
                target_line=line,
            )
            if trace_anchor:
                anchors.append(trace_anchor)
    unique: list[dict[str, object]] = []
    seen: set[tuple[object, ...]] = set()
    for anchor in anchors:
        key = (
            anchor.get("kind"), anchor.get("variable"), anchor.get("line"),
            json.dumps(anchor.get("from"), sort_keys=True),
            json.dumps(anchor.get("to"), sort_keys=True), anchor.get("type"),
        )
        if key not in seen:
            unique.append(anchor)
            seen.add(key)
    return unique


def _loop_carried_trace_anchor(
    source_text: str,
    source_variable: str,
    source_line: int,
    *,
    target_line: int,
) -> dict[str, object] | None:
    """Find a source-proven loop-carried update-to-condition edge."""
    numbered: list[tuple[int, str]] = []
    for fallback, raw_line in enumerate(source_text.splitlines(), start=1):
        match = _DISPLAY_LINE.match(raw_line)
        numbered.append(
            (int(match.group(1)), match.group(2)) if match else (fallback, raw_line)
        )
    by_line = dict(numbered)
    update = by_line.get(source_line, "")
    escaped = re.escape(source_variable)
    if not re.search(rf"\b{escaped}\b\s*(?:\+=|-=|\*=|/=|%=|\+\+|--)", update):
        return None
    loop_head = re.compile(r"^\s*(?:for|while)\b", re.IGNORECASE)
    candidates = [
        number
        for number, line_text in numbered
        if number < source_line
        and number <= target_line
        and loop_head.search(line_text)
        and re.search(rf"\b{escaped}\b", line_text)
    ]
    if not candidates:
        return None
    header_line = max(candidates)
    return {
        "kind": "trace_edge",
        "from": [source_variable, source_line],
        "to": [source_variable, header_line, "use"],
        "type": "data",
        "reason": "the source update reaches the enclosing loop condition on a later iteration",
    }


def build_core_spl_control(
    spl_by_method: dict[str, str],
    question: str,
    language: str,
    *,
    max_cards: int = 3,
    source_text: str = "",
    source_provenance: dict[str, dict] | None = None,
    include_source_in_cards: bool = False,
    expand_callers: bool = False,
) -> tuple[str, str, dict]:
    """Build a source-bound CoRe reasoning route without another LLM call."""
    function_match = re.search(r"function\s+[`'\"]?([A-Za-z_][A-Za-z0-9_]*)", question, re.I)
    line_match = re.search(r"line\s+[`'\"]?(\d+)", question, re.I)
    variable_instances = re.findall(
        r"\(\s*[`'\"]?([A-Za-z_][A-Za-z0-9_]*)[`'\"]?\s*,\s*(\d+)\s*\)",
        question,
        re.I,
    )
    variable_tuple = variable_instances[-1] if variable_instances else None
    variable_named = re.search(
        r"variable\s+[`'\"]?([A-Za-z_][A-Za-z0-9_]*)", question, re.I,
    )
    target_function = function_match.group(1) if function_match else ""
    target_line = line_match.group(1) if line_match else (variable_tuple[1] if variable_tuple else "")
    target_variable = (
        variable_tuple[0] if variable_tuple
        else variable_named.group(1) if variable_named
        else ""
    )
    source_variable = variable_instances[0][0] if len(variable_instances) >= 2 else ""
    source_line = variable_instances[0][1] if len(variable_instances) >= 2 else ""

    primary: dict[str, str] = {}
    if target_function:
        for key, value in spl_by_method.items():
            bare = key.split("#", 1)[0].rsplit(".", 1)[-1]
            if bare == target_function:
                primary[key] = value
                break
    selected = primary or select_task_relevant_spl_methods(
        spl_by_method, question, max_cards=max_cards,
    )

    # Add source-visible callees around the primary owner. SPL-only semantic
    # neighbors are deliberately not promoted.
    if selected and len(selected) < max_cards:
        first_card = next(iter(selected.values()))
        for callee in re.findall(r"<SPL>\s*([^<]+?)\s*</SPL>", first_card):
            for key, value in spl_by_method.items():
                bare = key.split("#", 1)[0].rsplit(".", 1)[-1]
                if bare == callee.strip() and key not in selected:
                    selected[key] = value
                    break
            if len(selected) >= min(max_cards, 2):
                break

    if expand_callers and selected and source_provenance and len(selected) < max_cards:
        selected_bare = {
            owner.rsplit(".", 1)[-1]
            for owner in selected
        }
        for owner, details in source_provenance.items():
            if owner in selected or owner not in spl_by_method:
                continue
            calls = set(details.get("calls") or [])
            if not calls.intersection(selected_bare):
                continue
            selected[owner] = spl_by_method[owner]
            if len(selected) >= max_cards:
                break

    lowered = question.lower()
    if "control dependence" in lowered:
        task_kind = "control dependence"
        checkpoint_tags = "CONDITION, loop, branch, and enclosing control region"
    elif "data dependence" in lowered:
        task_kind = "data dependence"
        checkpoint_tags = "definitions, assignments, loop-carried values, and data-flow references"
    elif "information flow" in lowered or "infoflow" in lowered:
        task_kind = "information flow"
        checkpoint_tags = "input, output, state update, call, and reference chains"
    else:
        task_kind = "execution trace"
        checkpoint_tags = "COMMAND, CONDITION, RETURN, call, and state-update checkpoints"

    selected_names = [key.split("#", 1)[0] for key in selected]
    checkpoint_terms: list[str] = []
    target_source_line = ""
    if target_variable:
        checkpoint_terms.append(target_variable)
    if target_line and source_text:
        source_lines = source_text.splitlines()
        if 1 <= int(target_line) <= len(source_lines):
            target_source_line = source_lines[int(target_line) - 1]
            ignored = {
                "boolean", "break", "continue", "double", "else", "false", "float",
                "for", "if", "int", "long", "math", "max", "min", "new", "null",
                "return", "static", "true", "void", "while",
            }
            for token in re.findall(r"[A-Za-z_][A-Za-z0-9_]*", target_source_line):
                if token.lower() not in ignored and token not in checkpoint_terms:
                    checkpoint_terms.append(token)
    required_output_anchors = _required_output_anchors(
        task_kind,
        target_line,
        target_variable,
        target_source_line,
        source_text,
        source_variable,
        source_line,
    )

    checkpoint_hints: list[str] = []
    command_lines = [
        line.strip()
        for card in selected.values()
        for line in card.splitlines()
        if line.strip().startswith("[COMMAND")
    ]
    for term in checkpoint_terms:
        term_pattern = re.compile(rf"\b{re.escape(term)}\b")
        added_for_term = 0
        for line in command_lines:
            if term_pattern.search(line) and line not in checkpoint_hints:
                checkpoint_hints.append(line)
                added_for_term += 1
                if len(checkpoint_hints) >= 6:
                    break
                if added_for_term >= 2:
                    break
        if len(checkpoint_hints) >= 6:
            break

    status = "available" if selected else "unavailable"
    source_candidates = _source_analysis_candidates(
        source_text,
        task_kind,
        target_line,
        checkpoint_terms,
        selected_names,
        source_provenance,
    )
    evidence_ledger = _dependency_evidence_ledger(
        source_candidates, checkpoint_terms, target_line,
    )
    control_lines = [
            f"SPL availability: {status}",
            f"Question kind: {task_kind}",
            f"Primary source owner: {target_function or '<derive from source>'}",
            f"Target source anchor: variable={target_variable or '<none>'}, line={target_line or '<none>'}",
            f"Trace source anchor: variable={source_variable or '<none>'}, line={source_line or '<none>'}",
            f"Attached SPL owners: {', '.join(selected_names) if selected_names else '<none>'}",
            "Role of the SPL cards: an auto-generated semantic description of what the code does — evidence, not ground truth.",
            "They are bound to the source and describe its intended behavior, but they are NOT guaranteed correct: they can be wrong, incomplete, or describe intended behavior where the source actually has a bug.",
            "The numbered source code is the ground truth. When an SPL description and the source disagree, trust the source.",
            "Never treat a dependency as real merely because an SPL COMMAND mentions two variables together",
            "(for example, an SPL line describing a loop as 'for j from 0 to n-1' does NOT make n a data source for j; the source's def-use chain decides).",
            "Required route:",
            "1. Start at the exact target line/variable in the authoritative numbered source.",
            "2. Use the SPL cards to locate the relevant function and understand its intended behavior; then verify every dependency against the numbered source, and where the SPL and the source disagree, trust the source.",
            "3. Use a worklist, not a single backward scan. Add every newly discovered definition/guard and continue until one full pass adds nothing.",
            "4. For data dependence, trace value flow backward from the target: a variable instance is a source only if its value is read, directly or through a chain of reads, to compute the target. Recursively enqueue the identifiers that each reaching definition itself reads.",
            "5. For control dependence inside a loop, inspect the complete loop body, including conditions after the target that can break, return, continue, throw, or gate such an exit and therefore control a later iteration of the target.",
            "6. Map every reported line or variable instance back to the numbered source; SPL text and candidate-ledger entries are never automatically answer items.",
            "7. Stop only at a fixed point: every retained node has been source-verified and no unprocessed predecessor remains.",
            "8. Before answering, disposition every source-derived candidate as included or excluded against the official definition. Do not silently omit a candidate that occurs after the target when it can affect a later loop iteration.",
            "9. If the target line is itself a loop header, explicitly decide whether its condition controls a later execution of that same header; do not exclude the target line merely because source and target line numbers are equal.",
            "10. Reserve enough output budget to emit the exact official JSON. Once the candidate ledger is closed, output the JSON immediately; an empty response is never a valid answer.",
        ]
    if required_output_anchors:
        control_lines.append(
            "Source-derived output obligations (machine-audited; verify them against source):"
        )
        control_lines.extend(
            f"- {item['reason']}: {item}"
            for item in required_output_anchors
        )
    if task_kind == "data dependence":
        control_lines.extend([
            "Data-dependence precision rules (source-anchored; the SPL prose does not override these):",
            "- A variable instance is a source if its value is read, directly or transitively, to compute the target's value. Walk the def-use chain backward from the target line in the numbered source, and report every variable instance on that chain (declarations, parameters, allocations, and later writes alike) exactly as the official definition requires.",
            "- LOOP RULE (syntax-aware): in a C/Java-style counter loop 'for (init; cond; incr)' or 'while (cond)', the condition variables (e.g. n in 'k < n') are read only to decide when to stop, so they are CONTROL dependence, not DATA dependence of the iterator — do NOT report them as the iterator's data sources, even if the SPL prose says the loop goes 'from 0 to n-1'. In contrast, in a Python-style 'for x in expr' / 'for x in iterable', the iterable expression expr is actually evaluated to produce x's values, so expr and every variable in its def-use chain ARE data sources of x.",
            "- A variable updated by an explicit read-modify-write ('k++', 'i += 1', 'i = i + 1') is its own source (loop-carried). A variable freshly bound by 'for x in range(...)' / 'for x in iterable' has no loop-carried self-dependence; its sources are the iterable expression's chain.",
            "- A variable mentioned in an SPL COMMAND near the target is only a source if the numbered source itself reads its value to compute the target. SPL prose never adds a source by itself.",
        ])
    if include_source_in_cards and task_kind == "information flow":
        control_lines.extend([
            "Information-flow precision rules:",
            "- Build the bidirectional flow component around the queried instance: close both predecessors that reach it and successors reached from it until neither direction adds a node.",
            "- Do not include the queried instance merely because it is the query anchor. Include it only when that line defines or updates the variable, such as a read-modify-write operation.",
            "- A library or input-handle variable used only as a method-call receiver is not itself a data source for the returned value. Include the receiver only when program data stored in that variable is explicitly read by the analyzed operation.",
            "- After a queried update, inspect every later use and loop-carried update reachable from it; do not stop after predecessor closure.",
        ])
    if checkpoint_hints:
        control_lines.append("SPL-derived checkpoints (hints only; verify each against source):")
        control_lines.extend(f"- {hint}" for hint in checkpoint_hints)
    if source_candidates:
        control_lines.append("Source-derived closure candidates (inspect for reachability; this is not the answer):")
        control_lines.extend(
            f"- line {item['line']}: {item['code']}"
            for item in source_candidates
        )
    if evidence_ledger:
        control_lines.append("Source/SPL dependency evidence ledger (every row requires include/exclude disposition):")
        control_lines.extend(
            "- " + json.dumps(item, ensure_ascii=False, sort_keys=True)
            for item in evidence_ledger
        )
    control = "\n".join(control_lines)
    cards = (
        render_bound_spl_cards(
            selected,
            source_provenance,
            include_source=include_source_in_cards,
            source_language=language,
        )
        if source_provenance is not None
        else format_inline_spl_cards_generic("", selected, language, include_source=False)
    )
    audit = {
        "status": status,
        "task_kind": task_kind,
        "target_function": target_function or None,
        "target_line": int(target_line) if target_line else None,
        "target_variable": target_variable or None,
        "source_variable": source_variable or None,
        "source_line": int(source_line) if source_line else None,
        "selected_spl_owners": selected_names,
        "checkpoint_terms": checkpoint_terms,
        "checkpoint_hints": checkpoint_hints,
        "source_closure_candidates": source_candidates,
        "dependency_evidence_ledger": evidence_ledger,
        "required_output_anchors": required_output_anchors,
        "available_spl_cards": len(spl_by_method),
        "atomic_source_spl_cards": bool(include_source_in_cards),
        "caller_expansion_enabled": bool(expand_callers),
        "guardrails": [
            "numbered source is authoritative",
            "SPL-only neighbors are not promoted",
            "answers must map to source lines or variable instances",
            "every candidate must be explicitly dispositioned before final JSON",
            "final JSON must be committed before the reasoning budget is exhausted",
        ],
    }
    return control, cards, audit


def strip_target_code_block(official_prompt: str) -> str:
    """Keep task/question text while removing the target program from CoRe prompts."""
    matches = list(re.finditer(r"```[^\n]*\n.*?```", official_prompt, flags=re.DOTALL))
    if not matches:
        return official_prompt
    last = matches[-1]
    return (
        official_prompt[: last.start()]
        + "[PROGRAM REPRESENTATION IS PROVIDED BY THIS EXPERIMENT CONDITION BELOW]\n"
        + official_prompt[last.end() :]
    ).strip()


def render_prompt(condition: str, template: str, fields: dict[str, str]) -> str:
    allowed = ALLOWED_PROMPT_FIELDS[condition]
    used = {name for _, name, _, _ in string.Formatter().parse(template) if name}
    disallowed = sorted(used - allowed)
    if disallowed:
        raise ValueError(
            f"Prompt for condition '{condition}' uses disallowed fields {disallowed}. "
            f"Allowed fields are {sorted(allowed)}."
        )
    return template.format(**{name: fields[name] for name in used})


def render_condition_prompt(condition: str, fields: dict[str, str], *, has_spl: bool) -> str:
    effective_condition = (
        "official_raw"
        if condition in {"raw_spl_controlled", "raw_spl_reasoned"} and not has_spl
        else condition
    )
    return render_prompt(effective_condition, PROMPTS[effective_condition], fields)


def empty_output_retry_prompt(prompt: str) -> str:
    return "\n\n".join([
        "FINAL-SUBMISSION RETRY. The previous call exhausted its reasoning budget without a visible answer. "
        "Perform only the minimum remaining verification, then emit the exact JSON object required by the task. "
        "Do not provide analysis, prose, or markdown. Never return an empty response.",
        prompt,
    ])


def generation_usage_row(result: object) -> dict[str, object]:
    return {
        "input_tokens": int(getattr(result, "input_tokens", 0) or 0),
        "output_tokens": int(getattr(result, "output_tokens", 0) or 0),
        "reasoning_tokens": int(getattr(result, "reasoning_tokens", 0) or 0),
        "total_tokens": int(getattr(result, "total_tokens", 0) or 0),
        "elapsed_seconds": float(getattr(result, "elapsed_seconds", 0) or 0),
        "visible_output": bool(str(getattr(result, "text", "") or "").strip()),
    }


def audit_core_output_contract(output: str, spl_control_audit: dict) -> dict[str, object]:
    required = list(spl_control_audit.get("required_output_anchors") or [])
    result: dict[str, object] = {"required_output_anchors": required, "violations": []}
    if not required:
        return result
    match = re.search(r"\{.*\}", output or "", flags=re.DOTALL)
    try:
        payload = json.loads(match.group(0)) if match else {}
    except (TypeError, ValueError):
        payload = {}
    control_sources = payload.get("ControlDependenceSources") or []
    flow_sources = payload.get("InfomationFlowSources") or payload.get("InformationFlowSources") or []
    normalized_flow = {
        (str(item[0]), int(item[1]))
        for item in flow_sources
        if isinstance(item, list) and len(item) >= 2
    }
    trace = payload.get("Trace") or []
    normalized_trace = {
        (
            tuple(edge.get("from") or []),
            tuple(edge.get("to") or []),
            str(edge.get("type") or ""),
        )
        for edge in trace
        if isinstance(edge, dict)
    }
    violations = []
    for anchor in required:
        if anchor.get("kind") == "line" and int(anchor["line"]) not in control_sources:
            violations.append({"kind": "missing_required_line", "anchor": anchor})
        if anchor.get("kind") == "variable_instance":
            pair = (str(anchor["variable"]), int(anchor["line"]))
            if pair not in normalized_flow:
                violations.append({"kind": "missing_required_variable_instance", "anchor": anchor})
        if anchor.get("kind") == "trace_edge":
            edge = (
                tuple(anchor.get("from") or []),
                tuple(anchor.get("to") or []),
                str(anchor.get("type") or ""),
            )
            if edge not in normalized_trace:
                violations.append({"kind": "missing_required_trace_edge", "anchor": anchor})
    result["violations"] = violations
    return result


def core_contract_retry_prompt(prompt: str, output: str, contract_audit: dict) -> str:
    violations = json.dumps(contract_audit.get("violations") or [], ensure_ascii=False)
    return "\n\n".join([
        prompt,
        "SOURCE-CONTRACT RETRY. The previous answer omitted source-derived structural obligations. "
        "Recheck the numbered source and source-bound SPL card, then revise the complete answer. "
        "Do not blindly append an item if source verification contradicts it.",
        f"Contract violations: {violations}",
        f"Previous answer:\n{output}",
        "Return only the exact JSON object required by the official task, with no prose or markdown.",
    ])


def _receiver_only_variable(source_text: str, variable: str, definition_line: int) -> bool:
    """Identify a root API handle whose value never enters program data flow."""
    pattern = re.compile(rf"\b{re.escape(variable)}\b")
    receiver_uses = 0
    definition_code = ""
    for fallback, raw_line in enumerate(source_text.splitlines(), start=1):
        match = _DISPLAY_LINE.match(raw_line)
        line = int(match.group(1)) if match else fallback
        code = match.group(2) if match else raw_line
        if line == definition_line:
            definition_code = code
            continue
        for occurrence in pattern.finditer(code):
            suffix = code[occurrence.end():].lstrip()
            if re.match(r"^\.\s*[A-Za-z_][A-Za-z0-9_]*\s*\(", suffix):
                receiver_uses += 1
            else:
                return False
    if receiver_uses == 0:
        return False
    # A receiver initialized from another object's call (for example,
    # StringTokenizer(br.readLine())) carries that returned program value.
    # A root input handle such as Scanner(System.in) does not.
    rhs = definition_code.split("=", 1)[1] if "=" in definition_code else definition_code
    data_call = re.search(r"\b([a-z_][A-Za-z0-9_]*)\s*\.\s*[A-Za-z_]\w*\s*\(", rhs)
    return data_call is None


def precision_filter_core_output(
    output: str,
    source_text: str,
    control_audit: dict,
) -> tuple[str, dict[str, object]]:
    """Remove only source-provable information-flow boundary false positives."""
    audit: dict[str, object] = {
        "status": "not_applicable",
        "removed": [],
        "added": [],
        "rules": [
            "non_defining_query_anchor",
            "receiver_only_api_handle",
            "pre_target_in_place_mutator_closure",
        ],
    }
    if control_audit.get("task_kind") != "information flow":
        return output, audit
    match = re.search(r"\{.*\}", output or "", flags=re.DOTALL)
    try:
        payload = json.loads(match.group(0)) if match else None
    except (TypeError, ValueError, json.JSONDecodeError):
        payload = None
    if not isinstance(payload, dict):
        audit["status"] = "unparseable_output"
        return output, audit

    key = (
        "InfomationFlowSources"
        if "InfomationFlowSources" in payload
        else "InformationFlowSources"
    )
    flow_sources = payload.get(key)
    if not isinstance(flow_sources, list):
        audit["status"] = "missing_information_flow_sources"
        return output, audit

    by_line: dict[int, str] = {}
    for fallback, raw_line in enumerate(source_text.splitlines(), start=1):
        line_match = _DISPLAY_LINE.match(raw_line)
        line = int(line_match.group(1)) if line_match else fallback
        by_line[line] = line_match.group(2) if line_match else raw_line

    target_variable = str(control_audit.get("target_variable") or "")
    target_line = int(control_audit.get("target_line") or -1)
    kept: list[object] = []
    removed: list[dict[str, object]] = []
    for item in flow_sources:
        if not isinstance(item, list) or len(item) < 2:
            kept.append(item)
            continue
        variable = str(item[0])
        try:
            line = int(item[1])
        except (TypeError, ValueError):
            kept.append(item)
            continue
        reason = ""
        if (
            variable == target_variable
            and line == target_line
            and not _line_defines_identifier(by_line.get(line, ""), variable)
        ):
            reason = "non_defining_query_anchor"
        elif _receiver_only_variable(source_text, variable, line):
            reason = "receiver_only_api_handle"
        if reason:
            removed.append({"item": item, "reason": reason})
        else:
            kept.append(item)

    payload[key] = kept
    existing_pairs = {
        (str(item[0]), int(item[1]))
        for item in kept
        if isinstance(item, list) and len(item) >= 2
    }
    predicted_variables = {variable for variable, _line in existing_pairs}
    added: list[dict[str, object]] = []
    mutator_names = (
        "sort", "add", "addAll", "append", "clear", "extend", "insert",
        "offer", "poll", "pop", "push", "put", "remove", "removeAll",
        "reverse", "set", "update",
    )
    mutator_pattern = "|".join(re.escape(name) for name in mutator_names)
    for variable in sorted(predicted_variables):
        escaped = re.escape(variable)
        receiver_call = re.compile(rf"\b{escaped}\b\s*\.\s*(?:{mutator_pattern})\s*\(")
        library_sort = re.compile(
            rf"\b(?:Arrays|Collections)\s*\.\s*sort\s*\(\s*{escaped}\b"
        )
        for line, code in sorted(by_line.items()):
            if line >= target_line or (variable, line) in existing_pairs:
                continue
            if receiver_call.search(code) or library_sort.search(code):
                kept.append([variable, line])
                existing_pairs.add((variable, line))
                added.append({
                    "item": [variable, line],
                    "reason": "pre_target_in_place_mutator_closure",
                })

    payload[key] = kept
    audit["status"] = "adjusted" if removed or added else "unchanged"
    audit["removed"] = removed
    audit["added"] = added
    audit["before_count"] = len(flow_sources)
    audit["after_count"] = len(kept)
    return json.dumps(payload, ensure_ascii=False, separators=(",", ":")), audit


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", required=True)
    args = parser.parse_args()

    config = read_config(resolve_in_project(args.config))
    conditions = list(config.get("conditions", PROMPT_CONDITIONS))
    unknown_conditions = sorted(set(conditions) - set(PROMPT_CONDITIONS))
    if unknown_conditions:
        raise ValueError(f"Unknown CoRe conditions: {unknown_conditions}")
    PROMPTS.clear()
    PROMPTS.update({condition: load_prompt(condition) for condition in conditions})
    artifact_dir = resolve_in_project(config["artifact_dir"])
    run_dir = ensure_dir(resolve_in_project(config["run_dir"]))
    manifest = selected_items(read_json(artifact_dir / "manifest.json"), config)
    client = ModelClient(GenerationConfig(**generation_kwargs(config, max_tokens_key="max_output_tokens")))

    def work(item: dict) -> str:
        sample_dir = resolve_in_project(item["sample_dir"])
        raw = (sample_dir / "raw_code.txt").read_text(encoding="utf-8")
        compressed_raw_path = sample_dir / "compressed_raw.txt"
        if compressed_raw_path.exists():
            compressed_raw = compressed_raw_path.read_text(encoding="utf-8")
        else:
            compressed_raw = raw
            print(f"WARNING: compressed_raw.txt missing for {item['task_id']}, falling back to full raw code. Re-run prepare.py.")
        spl = (sample_dir / "spl.txt").read_text(encoding="utf-8")
        # Per-method SPL map for inline-card construction
        spl_by_method_path = sample_dir / "spl_by_method.json"
        spl_by_method = read_json(spl_by_method_path) if spl_by_method_path.exists() else {}
        spl_map_source = "sidecar" if spl_by_method else "unavailable"
        if not spl_by_method and spl.strip():
            spl_by_method = recover_spl_by_worker(spl)
            spl_map_source = "recovered_from_spl_text" if spl_by_method else "unavailable"
            if spl_by_method and not spl_by_method_path.exists():
                write_json(spl_by_method_path, spl_by_method)
        language = str(item.get("language", "python")).lower()
        bound_spl, source_provenance, binding_audit = bind_spl_to_source(
            raw, spl_by_method, language,
        )
        if bound_spl:
            spl_by_method = bound_spl
            spl_map_source = f"{spl_map_source}+source_bound"
        else:
            spl_by_method = {}
            spl_map_source = "unavailable_after_source_binding"
        summary_path = sample_dir / "free_summary.txt"
        summary = summary_path.read_text(encoding="utf-8") if summary_path.exists() else ""
        structured_summary_path = sample_dir / "structured_summary.txt"
        structured_summary = structured_summary_path.read_text(encoding="utf-8") if structured_summary_path.exists() else ""
        question = (sample_dir / "question.txt").read_text(encoding="utf-8")
        official_prompt_path = sample_dir / "official_prompt.txt"
        official_prompt = (
            official_prompt_path.read_text(encoding="utf-8")
            if official_prompt_path.exists()
            else f"Given the program and question, answer using the required CoRe label format only.\n\nPROGRAM:\n{raw}\n\nQUESTION:\n{question}"
        )
        # Build per-method inline SPL cards.
        spl_inline_by_condition: dict[str, str] = {}
        if spl_by_method:
            spl_inline_by_condition["spl_only"] = format_inline_spl_cards_generic(
                "", spl_by_method, language, include_source=False,
            )
            spl_inline_by_condition["raw_spl"] = format_inline_spl_cards_generic(
                raw, spl_by_method, language,
            )
            retrieved = select_task_relevant_spl_methods(
                spl_by_method,
                question,
                max_cards=int(config.get("spl_retrieval_max_cards", 4)),
            )
            spl_inline_by_condition["raw_spl_retrieved"] = render_bound_spl_cards(
                retrieved, source_provenance,
            )
            spl_inline_by_condition["raw_spl_reasoned"] = render_bound_spl_cards(
                retrieved, source_provenance,
            )
            spl_index = render_source_index_for_raw_spl(build_source_index(spl_by_method))
        else:
            spl_index = ""
        spl_control, controlled_cards, spl_control_audit = build_core_spl_control(
            spl_by_method,
            question,
            language,
            max_cards=int(config.get("spl_retrieval_max_cards", 4)),
            source_text=raw,
            source_provenance=source_provenance,
        )
        atomic_spl_control, atomic_controlled_cards, atomic_spl_control_audit = build_core_spl_control(
            spl_by_method,
            question,
            language,
            max_cards=int(config.get("spl_retrieval_max_cards", 4)),
            source_text=raw,
            source_provenance=source_provenance,
            include_source_in_cards=True,
            expand_callers=True,
        )
        spl_control_audit["map_source"] = spl_map_source
        spl_control_audit["source_binding"] = binding_audit
        atomic_spl_control_audit["map_source"] = spl_map_source
        atomic_spl_control_audit["source_binding"] = binding_audit
        spl_inline_by_condition["raw_spl_controlled"] = controlled_cards
        spl_inline_by_condition["raw_spl_atomic_controlled"] = atomic_controlled_cards
        spl_inline_by_condition["raw_spl_atomic_precise"] = atomic_controlled_cards
        spl_inline_by_condition["raw_spl_atomic_strict"] = atomic_controlled_cards
        spl_control_by_condition = {
            "raw_spl_controlled": spl_control,
            "raw_spl_atomic_controlled": atomic_spl_control,
            "raw_spl_atomic_precise": atomic_spl_control,
            "raw_spl_atomic_strict": atomic_spl_control,
        }
        spl_audit_by_condition = {
            "raw_spl_controlled": spl_control_audit,
            "raw_spl_atomic_controlled": atomic_spl_control_audit,
            "raw_spl_atomic_precise": atomic_spl_control_audit,
            "raw_spl_atomic_strict": atomic_spl_control_audit,
        }
        fields = {
            "raw": raw,
            "compressed_raw": compressed_raw,
            "spl": spl,
            "spl_inline": spl,  # fallback; overridden per-condition below
            "summary": summary,
            "structured_summary": structured_summary,
            "question": question,
            "official_prompt": official_prompt,
            "task_prompt": strip_target_code_block(official_prompt),
            "spl_index": spl_index,
            "spl_control": spl_control,
        }
        for condition in conditions:
            out_dir = ensure_dir(run_dir / item["task_id"] / condition)
            existing_output_path = out_dir / "output.txt"
            if (
                config.get("resume_nonempty_outputs", False)
                and existing_output_path.exists()
                and existing_output_path.read_text(encoding="utf-8", errors="replace").strip()
            ):
                continue
            if condition in {"nl_summary", "raw_free_summary"} and not summary.strip():
                raise RuntimeError(
                    f"free_summary.txt is empty or missing for {item['task_id']}. "
                    "The CoRe prepare.py generates summaries during the prepare phase; re-run it."
                )
            if condition in {"structured_summary", "raw_structured_summary"} and not structured_summary.strip():
                raise RuntimeError(
                    f"structured_summary.txt is empty or missing for {item['task_id']}. "
                    "The CoRe prepare.py generates summaries during the prepare phase; re-run it. "
                    "The structured_summary condition must not silently fall back to free_summary."
                )
            # Select the appropriate inline SPL for this condition.
            if condition in spl_inline_by_condition:
                fields["spl_inline"] = spl_inline_by_condition[condition]
            else:
                fields["spl_inline"] = spl
            fields["spl_control"] = spl_control_by_condition.get(condition, spl_control)
            condition_spl_audit = spl_audit_by_condition.get(condition, spl_control_audit)
            if condition == "raw_spl_controlled" and not spl_by_method:
                # Keep empty-SPL samples in the paired population, but do not
                # credit the controller with a prompt-only improvement.
                condition_spl_audit["status"] = "spl_unavailable_baseline_fallback"
            prompt = render_condition_prompt(condition, fields, has_spl=bool(spl_by_method))
            result = client.generate_with_metrics(prompt)
            write_text(out_dir / "prompt.txt", prompt)
            if condition in {
                "raw_spl", "raw_spl_retrieved", "raw_spl_reasoned",
                "raw_spl_controlled", "raw_spl_atomic_controlled", "raw_spl_atomic_precise",
                "raw_spl_atomic_strict", "spl_only",
            }:
                write_json(out_dir / "spl_control_audit.json", condition_spl_audit)
            attempts = [generation_usage_row(result)]
            contract_audit = audit_core_output_contract(
                result.text or "",
                condition_spl_audit if condition in {
                    "raw_spl_controlled", "raw_spl_atomic_controlled",
                    "raw_spl_atomic_precise", "raw_spl_atomic_strict",
                } else {},
            )
            write_json(out_dir / "output_contract_attempt_1.json", contract_audit)
            empty_output = not str(result.text or "").strip()
            contract_retry = (
                condition in {
                    "raw_spl_controlled", "raw_spl_atomic_controlled",
                    "raw_spl_atomic_precise", "raw_spl_atomic_strict",
                }
                and bool(spl_by_method)
                and bool(contract_audit.get("violations"))
                and bool(config.get("spl_contract_retry_on_violation", True))
            )
            if (empty_output and bool(config.get("retry_empty_output", True))) or contract_retry:
                attempt_dir = ensure_dir(out_dir / "generation_attempt_1")
                write_generation_result(
                    attempt_dir, result,
                    role="core_reasoning_attempt", condition=condition,
                )
                retry_prompt = (
                    core_contract_retry_prompt(prompt, result.text or "", contract_audit)
                    if contract_retry
                    else empty_output_retry_prompt(prompt)
                )
                write_text(out_dir / "generation_retry_prompt.txt", retry_prompt)
                result = client.generate_with_metrics(retry_prompt)
                attempts.append(generation_usage_row(result))
                contract_audit = audit_core_output_contract(result.text or "", condition_spl_audit)
                contract_audit["retry_performed"] = True
            else:
                contract_audit["retry_performed"] = False
            if condition == "raw_spl_atomic_strict":
                write_text(out_dir / "output_before_precision_filter.txt", result.text or "")
                filtered_text, precision_audit = precision_filter_core_output(
                    result.text or "", raw, condition_spl_audit,
                )
                write_json(out_dir / "precision_filter_audit.json", precision_audit)
                result = replace(result, text=filtered_text)
                contract_audit = audit_core_output_contract(filtered_text, condition_spl_audit)
                contract_audit["retry_performed"] = len(attempts) > 1
            write_json(out_dir / "output_contract.json", contract_audit)
            write_json(out_dir / "generation_attempts.json", {
                "attempts": attempts,
                "calls": len(attempts),
                "input_tokens": sum(int(row["input_tokens"]) for row in attempts),
                "output_tokens": sum(int(row["output_tokens"]) for row in attempts),
                "reasoning_tokens": sum(int(row["reasoning_tokens"]) for row in attempts),
                "total_tokens": sum(int(row["total_tokens"]) for row in attempts),
                "elapsed_seconds": sum(float(row["elapsed_seconds"]) for row in attempts),
            })
            write_generation_result(out_dir, result, role="core_reasoning", condition=condition)
        return item["task_id"]

    _results, errors = run_ordered(manifest, work, int(config.get("max_workers", 1)), bool(config.get("continue_on_error", True)))
    if errors:
        write_json(run_dir / "run_errors.json", errors)
    print(f"Wrote CoRe runs to {run_dir}")


if __name__ == "__main__":
    main()
