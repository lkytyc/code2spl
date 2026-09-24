from __future__ import annotations

import ast
import json
from dataclasses import dataclass, field
from typing import Any

from .spl_binding import bind_spl_to_source


@dataclass
class OwnerImpact:
    owner: str
    parameters: dict[str, str] = field(default_factory=dict)
    calls: list[str] = field(default_factory=list)
    reads: list[str] = field(default_factory=list)
    mutates: list[str] = field(default_factory=list)
    assertions: list[str] = field(default_factory=list)
    state_relations: list[str] = field(default_factory=list)


def build_semantic_impact_ledger(
    source: str,
    instruction: str,
    spl_by_method: dict[str, str],
    selected_owners: list[str],
    language: str = "python",
) -> tuple[str, dict[str, Any]]:
    """Build a source-verified dependency ledger for semantic clarification.

    SPL contributes current-behavior meaning. The source AST contributes exact
    calls, state accesses, assertions, and type links. The result deliberately
    contains questions and evidence, not a guessed future implementation.
    """
    bound, provenance, binding_audit = bind_spl_to_source(
        source, spl_by_method, language,
    )
    if language.lower() != "python":
        audit = {
            "status": "unsupported_language",
            "selected_owners": selected_owners,
            "valid_owner_names": list(provenance),
            "binding": binding_audit,
        }
        return "", audit

    facts, parse_errors = _python_owner_impacts(source)
    valid_owners = set(facts) & set(bound)
    seeds = [owner for owner in selected_owners if owner in valid_owners]
    impact_owners, reasons = _impact_closure(seeds, facts, valid_owners)

    owner_rows: list[dict[str, Any]] = []
    for owner in impact_owners:
        fact = facts[owner]
        owner_rows.append({
            "owner": owner,
            "reason": reasons.get(owner, ["source-bound SPL selection"]),
            "source_lines": [
                provenance[owner].get("source_start_line"),
                provenance[owner].get("source_end_line"),
            ],
            "parameters": fact.parameters,
            "calls": fact.calls,
            "reads": fact.reads,
            "mutates": fact.mutates,
            "assertions": fact.assertions,
            "state_relations": fact.state_relations,
            "spl_current_behavior": _card_summary(bound[owner]),
        })

    shared_state = _shared_state_edges(impact_owners, facts)
    questions = [
        "Which current owner or state relation should be authoritative for the requested behavior?",
        "Which dependency owners must be composed, rather than reimplemented, to realize the instruction?",
        "Do current constructor assertions or validation boundaries reject values that the requested semantic domain must support?",
        "For every numeric assertion, what happens at negative, zero, and positive boundaries, and what is the weakest constraint required by the requested operation?",
        "For every object parameter accepted by an aggregate owner, must it belong to one of the aggregate's source-verified collections before the operation is meaningful?",
        "If the same relationship is represented in more than one object or collection, which mutation boundary must keep those views coherent?",
        "Which boundary cases follow from the instruction itself, and which details remain genuinely unspecified?",
    ]
    audit = {
        "status": "available" if owner_rows else "unavailable",
        "instruction": instruction,
        "selected_owners": seeds,
        "impact_owners": impact_owners,
        "valid_owner_names": sorted(valid_owners),
        "owners": owner_rows,
        "shared_state_edges": shared_state,
        "clarification_questions": questions,
        "parse_errors": parse_errors,
        "binding": binding_audit,
    }
    lines = [
        "Semantic Impact Ledger",
        "- authority: source facts are exact; SPL describes current behavior; neither specifies a hidden future patch.",
        "- purpose: clarify the instruction by tracing dependencies, invariants, and shared state before editing.",
        "",
        "Impact owners:",
    ]
    for row in owner_rows:
        lines.append(f"- `{row['owner']}` ({'; '.join(row['reason'])})")
        if row["parameters"]:
            lines.append("  parameters: " + json.dumps(row["parameters"], ensure_ascii=False))
        if row["calls"]:
            lines.append("  calls: " + ", ".join(row["calls"]))
        if row["reads"]:
            lines.append("  reads: " + ", ".join(row["reads"]))
        if row["mutates"]:
            lines.append("  mutates: " + ", ".join(row["mutates"]))
        if row["assertions"]:
            lines.append("  current assertions: " + "; ".join(row["assertions"]))
        if row["state_relations"]:
            lines.append("  state relations: " + "; ".join(row["state_relations"]))
        if row["spl_current_behavior"]:
            lines.append("  SPL meaning: " + row["spl_current_behavior"])
    if shared_state:
        lines.extend(["", "Shared-state evidence:"])
        lines.extend(
            f"- `{edge['left_owner']}` and `{edge['right_owner']}` touch `{edge['state']}`"
            for edge in shared_state
        )
    lines.extend(["", "Questions the clarification planner must resolve:"])
    lines.extend(f"- {question}" for question in questions)
    return "\n".join(lines), audit


def _python_owner_impacts(source: str) -> tuple[dict[str, OwnerImpact], list[str]]:
    try:
        tree = ast.parse(source)
    except SyntaxError as exc:
        return {}, [f"python_parse_error:{exc.msg}:line={exc.lineno}"]

    facts: dict[str, OwnerImpact] = {}
    for node in tree.body:
        if isinstance(node, ast.ClassDef):
            for child in node.body:
                if isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    owner = f"{node.name}.{child.name}"
                    facts[owner] = _method_impact(node.name, child)
        elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            facts[node.name] = _method_impact("", node)
    return facts, []


def _method_impact(
    class_name: str,
    node: ast.FunctionDef | ast.AsyncFunctionDef,
) -> OwnerImpact:
    owner = f"{class_name}.{node.name}" if class_name else node.name
    parameters: dict[str, str] = {}
    for arg in [*node.args.posonlyargs, *node.args.args, *node.args.kwonlyargs]:
        if arg.arg in {"self", "cls"}:
            continue
        parameters[arg.arg] = ast.unparse(arg.annotation) if arg.annotation else "unknown"

    reads: set[str] = set()
    mutates: set[str] = set()
    calls: set[str] = set()
    assertions: list[str] = []
    relations: set[str] = set()

    for child in ast.walk(node):
        if isinstance(child, ast.Assert):
            assertions.append(ast.unparse(child.test))
        if isinstance(child, ast.Attribute):
            path = _attribute_path(child)
            if path:
                reads.add(_typed_path(path, class_name, parameters))
        if isinstance(child, (ast.Assign, ast.AnnAssign, ast.AugAssign)):
            targets = child.targets if isinstance(child, ast.Assign) else [child.target]
            value = getattr(child, "value", None)
            for target in targets:
                path = _attribute_path(target)
                if not path:
                    continue
                typed_target = _typed_path(path, class_name, parameters)
                mutates.add(typed_target)
                relation = _assignment_relation(typed_target, value, parameters)
                if relation:
                    relations.add(relation)
        if not isinstance(child, ast.Call):
            continue
        call_name = _call_name(child.func, class_name, parameters)
        if call_name:
            calls.add(call_name)
        if isinstance(child.func, ast.Attribute) and child.func.attr in {
            "append", "add", "extend", "insert", "update", "remove", "discard", "pop", "clear",
        }:
            receiver = _attribute_path(child.func.value)
            if receiver:
                typed_receiver = _typed_path(receiver, class_name, parameters)
                mutates.add(typed_receiver)
                if child.args:
                    relation = _collection_relation(
                        typed_receiver, child.args[0], parameters,
                    )
                    if relation:
                        relations.add(relation)

    reads.difference_update(mutates)
    return OwnerImpact(
        owner=owner,
        parameters=parameters,
        calls=sorted(calls),
        reads=sorted(reads),
        mutates=sorted(mutates),
        assertions=assertions,
        state_relations=sorted(relations),
    )


def _impact_closure(
    seeds: list[str],
    facts: dict[str, OwnerImpact],
    valid_owners: set[str],
) -> tuple[list[str], dict[str, list[str]]]:
    ordered = list(seeds)
    reasons: dict[str, list[str]] = {
        owner: ["source-bound SPL selection"] for owner in seeds
    }
    by_bare: dict[str, list[str]] = {}
    for owner in valid_owners:
        by_bare.setdefault(owner.rsplit(".", 1)[-1], []).append(owner)

    changed = True
    while changed and len(ordered) < 8:
        changed = False
        snapshot = list(ordered)
        touched = {
            state
            for owner in snapshot
            for state in [*facts[owner].reads, *facts[owner].mutates]
        }
        for candidate in sorted(valid_owners):
            candidate_reasons: list[str] = []
            if candidate in ordered:
                continue
            if set(facts[candidate].reads + facts[candidate].mutates) & touched:
                candidate_reasons.append("shares source state with an impact owner")
            for owner in snapshot:
                for called in facts[owner].calls:
                    if candidate in by_bare.get(called.rsplit(".", 1)[-1], []):
                        candidate_reasons.append(f"called by {owner}")
            if candidate_reasons:
                ordered.append(candidate)
                reasons[candidate] = list(dict.fromkeys(candidate_reasons))
                changed = True
                if len(ordered) >= 8:
                    break
    return ordered, reasons


def _shared_state_edges(
    owners: list[str], facts: dict[str, OwnerImpact],
) -> list[dict[str, str]]:
    edges: list[dict[str, str]] = []
    for index, left in enumerate(owners):
        left_state = set(facts[left].reads + facts[left].mutates)
        for right in owners[index + 1:]:
            for state in sorted(left_state & set(facts[right].reads + facts[right].mutates)):
                edges.append({
                    "left_owner": left,
                    "right_owner": right,
                    "state": state,
                })
    return edges


def _attribute_path(node: ast.AST | None) -> str:
    parts: list[str] = []
    current = node
    while isinstance(current, ast.Attribute):
        parts.append(current.attr)
        current = current.value
    if isinstance(current, ast.Name):
        parts.append(current.id)
        return ".".join(reversed(parts))
    return ""


def _typed_path(path: str, class_name: str, parameters: dict[str, str]) -> str:
    root, *rest = path.split(".")
    if root in {"self", "cls"} and class_name:
        root = class_name
    elif root in parameters and parameters[root] != "unknown":
        root = parameters[root]
    return ".".join([root, *rest])


def _call_name(func: ast.AST, class_name: str, parameters: dict[str, str]) -> str:
    if isinstance(func, ast.Name):
        return func.id
    path = _attribute_path(func)
    return _typed_path(path, class_name, parameters) if path else ""


def _assignment_relation(
    target: str, value: ast.AST | None, parameters: dict[str, str],
) -> str:
    if isinstance(value, ast.Name) and value.id in parameters:
        return f"{target} references {parameters[value.id]} from parameter `{value.id}`"
    return ""


def _collection_relation(
    target: str, value: ast.AST, parameters: dict[str, str],
) -> str:
    if isinstance(value, ast.Name) and value.id in parameters:
        return f"{target} contains {parameters[value.id]} values from parameter `{value.id}`"
    return ""


def _card_summary(card: str, limit: int = 280) -> str:
    compact = " ".join(str(card).split())
    marker = '[DEFINE_WORKER: "'
    if marker in compact:
        compact = compact.split(marker, 1)[1].split('"', 1)[0]
    return compact[:limit]
