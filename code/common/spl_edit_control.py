from __future__ import annotations

import re
from typing import Any

from .spl_binding import extract_source_owners, select_source_bound_spl_cards


def build_semantic_edit_control(
    source: str,
    instruction: str,
    spl_by_method: dict[str, str],
    language: str = "python",
    *,
    max_cards: int = 4,
) -> tuple[str, str, dict[str, Any]]:
    """Turn current-behavior SPL into a source-bound semantic edit contract.

    The contract deliberately does not guess hidden benchmark requirements.
    Its job is to make a lazy request safer and clearer by spelling out the
    current owner behavior and the observable properties that must not change.
    """
    cards, binding_audit = select_source_bound_spl_cards(
        source, spl_by_method, instruction, language, max_cards=max_cards,
    )
    selected_owners = list(binding_audit.get("selected_owners") or [])
    selected_owner_cards = _selected_owner_cards(spl_by_method, selected_owners)
    selected_cards = list(selected_owner_cards.values())
    intent = _classify_edit_intent(instruction)
    reliability = _spl_semantic_reliability(
        source, language, intent, selected_owners,
        _instruction_symbols(instruction, selected_owners),
    )
    checkpoints = _behavior_checkpoints(selected_cards)
    owner_capabilities = _owner_capabilities(selected_owner_cards)
    identity_risks = _identity_domain_risks(selected_owner_cards)
    explicit_symbols = _instruction_symbols(instruction, selected_owners)
    requested_symbols = _requested_symbols(instruction)
    requested_parameter_contract = _requested_parameter_contract(
        instruction,
        requested_symbols,
    )
    owner_reuse_obligations = _owner_reuse_obligations(
        instruction,
        requested_symbols,
        owner_capabilities,
    )
    call_expanded = list(binding_audit.get("call_expanded_owners") or [])
    source_owners, _source_owner_audit = extract_source_owners(source, language)
    callable_surface = [
        owner.qualified_name
        for owner in source_owners
        if not owner.bare_name.startswith("_")
    ]
    rollback_obligations = _rollback_obligations(source, instruction, language)

    preservation = [
        "Keep public names, signatures, return types, and external dependencies unless the instruction explicitly changes them.",
        "Keep output shape, ordering, numeric representation/rounding, and deterministic behavior unless explicitly targeted.",
        "Keep behavior of source owners not named by the instruction; SPL cards for them are preservation evidence, not edit requests.",
        "Keep every existing source-defined callable available unless the instruction explicitly requests its removal or rename. Rewriting one caller does not authorize deleting a helper that other callers or tests may invoke directly.",
    ]
    if intent == "optimization":
        preservation.extend([
            "Optimization must be observationally equivalent: preserve move/order iteration and tie-breaking unless the instruction explicitly permits a behavior change.",
            "Change the execution strategy or pruning only; do not add heuristics that can select a different valid output.",
        ])
    elif intent == "corrective":
        preservation.extend([
            "Change the smallest expression, condition, or state update that produces the named wrong behavior; preserve adjacent successful paths.",
            "Preserve non-target operators, calls, control-flow order, and output formatting. Do not replace an operator or data representation unless the instruction targets that aspect.",
        ])
        if _is_stateful_change(instruction):
            preservation.append(
                "When adding visited/seen/cache state, use it only to suppress repeated work after the original state transition. A guard must not skip an existing label, assignment, enqueue/dequeue effect, or first processing of a seed."
            )
            if call_expanded:
                preservation.append(
                    "The state spans a source call boundary: initialize it once in the outer operation owner and pass the same state to each participating helper. Do not recreate per-helper or per-iteration state that is meant to suppress work across the whole operation."
                )
    elif intent == "addition":
        preservation.extend([
            "Add only the requested owner or API; treat existing source owners as read-only unless the instruction explicitly asks to change them.",
            "If the requested value is a subset, projection, or presentation of behavior already exposed by a selected owner, delegate to or compose that owner. Do not duplicate its parsing/traversal logic or invent a new empty-input/error policy.",
            "When a selected owner already implements a required parse, traversal, search, conversion, or state query, call that owner. A new duplicate loop is not a minimal addition unless the existing owner's contract cannot supply the required value.",
            "Before writing a new loop, make an owner-composition decision: list which selected owner supplies each needed intermediate value, then implement the requested API around those calls.",
        ])
        if identity_risks:
            preservation.append(
                "Keep object-reference domains consistent when composing owners that allocate or return fresh objects. Do not use adjacency, keys, visited state, or lookup tables from one object domain with nodes from another; bridge domains only through a stable source-verified key."
            )

    lines = [
        "SPL semantic edit contract",
        f"- availability: {'source-bound' if cards else 'unavailable'}",
        f"- inferred edit class: {intent}",
        f"- source-bound owner candidates: {', '.join(selected_owners) if selected_owners else '<none>'}",
        f"- instruction-named owners: {', '.join(explicit_symbols) if explicit_symbols else '<none>'}",
        f"- requested identifiers: {', '.join(requested_symbols) if requested_symbols else '<none>'}",
        "- requested input contract: " + (
            "; ".join(
                f"{symbol}={details}"
                for symbol, details in requested_parameter_contract.items()
            )
            if requested_parameter_contract else "<none>"
        ),
        f"- source-call expansion: {', '.join(call_expanded) if call_expanded else '<none>'}",
        "- authority: Code Before and Instruction define the requested change; SPL defines current behavior and preservation checkpoints only.",
        "",
        "Current-behavior checkpoints to verify in Code Before:",
    ]
    lines.extend(f"- {checkpoint}" for checkpoint in checkpoints)
    if not checkpoints:
        lines.append("- No reliable SPL checkpoint is available; use the baseline source-only edit path.")
    if owner_capabilities:
        lines.extend(["", "Source-bound owner composition table:"])
        lines.extend(
            f"- {owner}: {capability}"
            for owner, capability in owner_capabilities.items()
        )
    if owner_reuse_obligations:
        lines.extend(["", "Machine-checkable owner-reuse obligations:"])
        lines.extend(
            f"- The requested implementation must call `{owner}` instead of reproducing its current behavior."
            for owner in owner_reuse_obligations
        )
        lines.append(
            "- Forward shared context parameters to those owners unchanged unless the Instruction explicitly requests filtering, augmentation, or conversion. Changing the receiver is allowed; silently rebuilding the owner's input collection is not."
        )
    if rollback_obligations:
        lines.extend(["", "Machine-checkable rollback obligations:"])
        lines.extend(
            f"- In {item['owner']}, every unsuccessful backtrack must remove values journaled by "
            f"`{item['journal']}` from `{item['collection']}`."
            for item in rollback_obligations
        )
    if identity_risks:
        lines.extend(["", "Reference-domain risks to verify in source:"])
        lines.extend(f"- {risk}" for risk in identity_risks)
    if callable_surface:
        lines.extend(["", "Existing callable surface to preserve:"])
        lines.extend(f"- {owner}" for owner in callable_surface)
    lines.extend(["", "Required semantic-delta procedure:"])
    lines.extend([
        "1. State internally which observable behavior the instruction asks to change and which source-bound owner currently produces it.",
        "2. Verify that owner and every used SPL checkpoint against Code Before.",
        "3. Make the smallest edit that realizes only that semantic delta.",
        "4. Re-check the edited code against every preservation obligation below before answering.",
        "5. If the lazy instruction omits a detail, prefer the smallest source-consistent interpretation; do not invent a new policy, ordering, dependency, or output convention.",
        "",
        "Preservation obligations:",
    ])
    lines.extend(f"- {item}" for item in preservation)
    audit = {
        "status": (
            "spl_nonsemantic_baseline_fallback"
            if cards and reliability["fallback"]
            else "available" if cards
            else "spl_unavailable_baseline_fallback"
        ),
        "instruction": instruction,
        "edit_intent": intent,
        "spl_semantic_reliability": reliability,
        "selected_owners": selected_owners,
        "instruction_named_owners": explicit_symbols,
        "requested_identifiers": requested_symbols,
        "requested_parameter_contract": requested_parameter_contract,
        "source_call_expanded_owners": call_expanded,
        "behavior_checkpoints": checkpoints,
        "owner_capabilities": owner_capabilities,
        "owner_reuse_obligations": owner_reuse_obligations,
        "rollback_obligations": rollback_obligations,
        "identity_domain_risks": identity_risks,
        "callable_surface": callable_surface,
        "preservation_obligations": preservation,
        "source_binding": binding_audit,
    }
    if cards and reliability["fallback"]:
        return "", "", audit
    return "\n".join(lines), cards, audit


def _python_hierarchy_targets(
    source: str,
    instruction: str,
    selected_owners: list[str],
    owner_names: list[str],
    language: str,
) -> tuple[list[str], set[str]]:
    """Propagate selected methods across an explicitly named class hierarchy."""
    if language.lower() != "python" or not re.search(
        r"\b(?:subclasses?|derived\s+classes?|implementations?|child\s+classes?)\b",
        instruction,
        re.IGNORECASE,
    ):
        return [], set()

    import ast

    try:
        tree = ast.parse(source)
    except SyntaxError:
        return [], set()

    bases: dict[str, set[str]] = {}
    for node in tree.body:
        if not isinstance(node, ast.ClassDef):
            continue
        node_bases: set[str] = set()
        for base in node.bases:
            if isinstance(base, ast.Name):
                node_bases.add(base.id)
            elif isinstance(base, ast.Attribute):
                node_bases.add(base.attr)
        bases[node.name] = node_bases

    roots = {
        class_name
        for class_name in bases
        if re.search(rf"\b{re.escape(class_name)}\b", instruction)
    }
    if not roots:
        return [], set()

    family = set(roots)
    changed = True
    while changed:
        changed = False
        for class_name, class_bases in bases.items():
            if class_name not in family and class_bases & family:
                family.add(class_name)
                changed = True

    selected_methods = {
        owner.rsplit(".", 1)[-1]
        for owner in selected_owners
        if "." in owner and not owner.rsplit(".", 1)[-1].startswith("_")
    }
    selected_methods.update(
        owner.rsplit(".", 1)[-1]
        for owner in owner_names
        if "." in owner
        and re.search(
            rf"\b{re.escape(owner.rsplit('.', 1)[-1])}\b",
            instruction,
        )
    )
    propagated = [
        owner
        for owner in owner_names
        if "." in owner
        and owner.split(".", 1)[0] in family
        and owner.rsplit(".", 1)[-1] in selected_methods
    ]
    return propagated, roots


def _python_noop_callable_owners(source: str) -> set[str]:
    """Return class methods whose source body is only a no-op/abstract marker."""
    import ast

    try:
        tree = ast.parse(source)
    except SyntaxError:
        return set()

    owners: set[str] = set()
    for node in tree.body:
        if not isinstance(node, ast.ClassDef):
            continue
        for child in node.body:
            if not isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef)):
                continue
            body = list(child.body)
            if body and isinstance(body[0], ast.Expr) and isinstance(
                getattr(body[0], "value", None), ast.Constant
            ) and isinstance(body[0].value.value, str):
                body = body[1:]
            no_op = len(body) == 1 and (
                isinstance(body[0], ast.Pass)
                or (
                    isinstance(body[0], ast.Expr)
                    and isinstance(body[0].value, ast.Constant)
                    and body[0].value.value is Ellipsis
                )
                or (
                    isinstance(body[0], ast.Raise)
                    and isinstance(body[0].exc, (ast.Name, ast.Call))
                    and (
                        getattr(body[0].exc, "id", "") == "NotImplementedError"
                        or getattr(getattr(body[0].exc, "func", None), "id", "")
                        == "NotImplementedError"
                    )
                )
            )
            if no_op:
                owners.add(f"{node.name}.{child.name}")
    return owners


def build_task_delta_contract(
    source: str,
    instruction: str,
    semantic_audit: dict[str, Any],
    language: str = "python",
) -> tuple[str, dict[str, Any]]:
    """Separate requested future behavior from SPL's current-behavior facts."""
    source_owners, _ = extract_source_owners(source, language)
    owner_names = [owner.qualified_name for owner in source_owners]
    bare_to_qualified: dict[str, list[str]] = {}
    for owner in owner_names:
        bare_to_qualified.setdefault(owner.rsplit(".", 1)[-1], []).append(owner)

    selected = list(semantic_audit.get("selected_owners") or [])
    named = list(semantic_audit.get("instruction_named_owners") or [])
    requested = list(semantic_audit.get("requested_identifiers") or [])
    explicit_targets: list[str] = []
    for symbol in [*named, *requested]:
        candidates = [symbol] if symbol in owner_names else bare_to_qualified.get(symbol, [])
        for candidate in candidates:
            if candidate not in explicit_targets:
                explicit_targets.append(candidate)

    hierarchy_targets, hierarchy_roots = _python_hierarchy_targets(
        source,
        instruction,
        selected,
        owner_names,
        language,
    )
    for owner in hierarchy_targets:
        if owner not in explicit_targets:
            explicit_targets.append(owner)

    lowered = instruction.lower()
    intent = str(semantic_audit.get("edit_intent") or _classify_edit_intent(instruction))
    must_add = [
        symbol
        for symbol in requested
        if symbol not in bare_to_qualified and symbol not in owner_names
    ]
    if not explicit_targets and selected and not (intent == "addition" and must_add):
        explicit_targets.append(selected[0])
    # Replacing an operation or call path does not by itself authorize deleting
    # the old public callable. Preserve compatibility unless removal/rename is
    # explicit; source-bound SPL makes that existing API surface observable.
    removal_verbs = r"(?:remove|delete|drop|eliminate|rename)"
    must_remove: list[str] = []
    for bare, qualified in bare_to_qualified.items():
        if re.search(rf"\b{removal_verbs}\b[^.\n]{{0,60}}\b{re.escape(bare)}\b", lowered):
            must_remove.extend(owner for owner in qualified if owner not in must_remove)
    replacement_compatibility_anchors: set[str] = set()
    for bare, qualified in bare_to_qualified.items():
        if re.search(
            rf"\breplace\b[^.\n]{{0,100}}\b{re.escape(bare)}\b[^.\n]{{0,100}}\bwith\b",
            lowered,
        ):
            replacement_compatibility_anchors.update(qualified)

    if intent == "addition":
        editable_targets = [
            owner
            for owner in explicit_targets
            if _addition_allows_existing_owner_change(instruction, owner)
        ]
    else:
        editable_targets = list(explicit_targets)
        for owner in selected:
            if owner not in editable_targets:
                editable_targets.append(owner)
    noop_owners = _python_noop_callable_owners(source) if language.lower() == "python" else set()
    hierarchy_scope_anchors = {
        owner
        for owner in hierarchy_targets
        if owner.split(".", 1)[0] in hierarchy_roots and owner in noop_owners
    }
    required_change_owners = [
        owner for owner in explicit_targets
        if owner not in hierarchy_scope_anchors
        and owner not in replacement_compatibility_anchors
    ]
    target_set = set(editable_targets) | set(must_remove)
    must_preserve = [
        owner
        for owner in owner_names
        if owner not in target_set and not owner.rsplit(".", 1)[-1].startswith("_")
    ]
    current_behavior = list(semantic_audit.get("behavior_checkpoints") or [])

    lines = [
        "Task Delta Contract",
        "- authority: the Instruction defines future behavior; SPL describes current behavior only.",
        f"- edit class: {intent}",
        "",
        "MUST_CHANGE:",
        f"- Implement this instruction literally: {instruction.strip()}",
    ]
    if explicit_targets:
        lines.append(f"- Primary instruction-named owners: {', '.join(explicit_targets)}")
    else:
        lines.append("- No target owner is certain; make the narrowest source-supported change.")
    if editable_targets:
        lines.append(
            "- Source-bound semantic neighborhood that may change when required: "
            + ", ".join(editable_targets)
        )
    if hierarchy_targets:
        lines.append(
            "- Class-hierarchy propagation: the selected method obligations apply to matching "
            "implementations in " + ", ".join(hierarchy_targets)
        )
    if hierarchy_scope_anchors:
        lines.append(
            "- Abstract/no-op hierarchy anchors define scope but need not change when concrete "
            "implementations realize the requested behavior: "
            + ", ".join(sorted(hierarchy_scope_anchors))
        )
    if replacement_compatibility_anchors:
        lines.append(
            "- Replacement compatibility anchors remain callable; replace the requested call path, "
            "not the existing declaration: "
            + ", ".join(sorted(replacement_compatibility_anchors))
        )
    lines.extend(["", "MUST_ADD:"])
    lines.extend(f"- Add `{symbol}` as requested." for symbol in must_add)
    if not must_add:
        lines.append("- No source-absent requested identifier was detected.")
    lines.extend(["", "MUST_REMOVE:"])
    lines.extend(f"- Remove or replace `{owner}` only as explicitly requested." for owner in must_remove)
    if not must_remove:
        lines.append("- No explicit removal obligation was detected.")
    lines.extend(["", "MUST_PRESERVE:"])
    if must_preserve:
        lines.append(f"- Preserve unrelated source owners: {', '.join(must_preserve)}")
    else:
        lines.append("- Preserve all behavior outside the requested semantic delta.")
    lines.extend([
        "- Preserve dependencies, exceptions, ordering, output representation, and state transitions unless the Instruction targets them.",
        "",
        "CURRENT SPL FACT DISPOSITION:",
        "- Facts about target owners are MAY_CHANGE evidence. Never restore a target behavior that conflicts with MUST_CHANGE.",
        "- Facts about unrelated owners are MUST_PRESERVE evidence after verification against Code Before.",
    ])
    lines.extend(f"- Current checkpoint (classify before use): {fact}" for fact in current_behavior[:10])
    lines.extend([
        "",
        "FINAL CHECK:",
        "1. Confirm every MUST_CHANGE and MUST_ADD item is realized in code.",
        "2. Confirm no MUST_REMOVE item remains unless the Instruction permits compatibility retention.",
        "3. Confirm unrelated owners and observable behavior remain unchanged.",
        "4. When MUST_CHANGE conflicts with a current SPL fact, MUST_CHANGE wins.",
    ])
    audit = {
        "status": semantic_audit.get("status"),
        "instruction": instruction,
        "edit_intent": intent,
        "must_change": [instruction.strip()],
        "primary_target_owners": editable_targets
        if intent == "addition"
        else required_change_owners,
        "target_owners": editable_targets,
        "required_change_owners": required_change_owners,
        "hierarchy_propagated_owners": hierarchy_targets,
        "hierarchy_scope_anchors": sorted(hierarchy_scope_anchors),
        "replacement_compatibility_anchors": sorted(replacement_compatibility_anchors),
        "must_add": must_add,
        "must_remove": must_remove,
        "must_preserve": must_preserve,
        "current_behavior_checkpoints": current_behavior,
        "source_bound_spl_owners": selected,
    }
    return "\n".join(lines), audit


def _python_unresolved_global_names(source: str) -> tuple[set[str], bool]:
    """Return statically unresolved global reads and whether star imports exist.

    Comparing candidate findings with the original source avoids treating
    pre-existing framework globals as edit regressions. Star imports make
    global resolution unknowable, so callers can record but must not enforce
    the result in that case.
    """
    import ast
    import builtins
    import symtable

    tree = ast.parse(source)
    has_star_import = any(
        isinstance(node, ast.ImportFrom)
        and any(alias.name == "*" for alias in node.names)
        for node in ast.walk(tree)
    )
    table = symtable.symtable(source, "<candidate>", "exec")
    module_bound = {
        symbol.get_name()
        for symbol in table.get_symbols()
        if (
            symbol.is_assigned()
            or symbol.is_imported()
            or symbol.is_namespace()
            or symbol.is_parameter()
        )
    }
    builtin_names = set(dir(builtins))
    unresolved: set[str] = set()

    def visit(current: symtable.SymbolTable) -> None:
        for symbol in current.get_symbols():
            name = symbol.get_name()
            if (
                symbol.is_referenced()
                and symbol.is_global()
                and name not in module_bound
                and name not in builtin_names
            ):
                unresolved.add(name)
        for child in current.get_children():
            visit(child)

    visit(table)
    return unresolved, has_star_import


def audit_python_semantic_edit(
    before_source: str,
    after_source: str,
    semantic_audit: dict[str, Any],
) -> dict[str, Any]:
    """Check source-derived edit obligations without benchmark knowledge.

    This audit is deliberately structural. It verifies that an edited Python
    module still exposes the original callable surface and that a newly
    requested API actually composes owners identified by the source-bound SPL
    contract. It does not attempt to predict hidden test behavior.
    """
    import ast

    violations: list[dict[str, Any]] = []
    try:
        before_tree = ast.parse(before_source)
        after_tree = ast.parse(after_source)
    except SyntaxError as exc:
        return {
            "status": "invalid_python",
            "violations": [{
                "kind": "syntax_error",
                "message": str(exc),
            }],
        }

    before_callables = _python_callable_nodes(before_tree)
    after_callables = _python_callable_nodes(after_tree)

    before_unresolved, before_has_star_import = _python_unresolved_global_names(before_source)
    after_unresolved, after_has_star_import = _python_unresolved_global_names(after_source)
    introduced_unresolved = sorted(after_unresolved - before_unresolved)
    if introduced_unresolved and not after_has_star_import:
        for name in introduced_unresolved:
            violations.append({
                "kind": "introduced_unresolved_name",
                "name": name,
                "message": (
                    f"The candidate newly references global `{name}` without declaring or importing it."
                ),
            })
    expected_surface = set(semantic_audit.get("callable_surface") or before_callables)
    missing = sorted(expected_surface - set(after_callables))
    if missing:
        violations.append({
            "kind": "missing_callable_surface",
            "owners": missing,
            "message": "Keep every original callable unless removal or rename is explicit.",
        })

    before_value_returns = {
        owner
        for owner in (
            _python_value_return_surface(before_callables)
            | _python_declared_value_return_surface(before_callables)
        )
        if not _python_callable_is_stub(before_callables.get(owner))
    }
    after_value_returns = _python_value_return_surface(after_callables)
    instruction = str(semantic_audit.get("instruction") or "")
    named_return_owners = {
        owner
        for owner in semantic_audit.get("instruction_named_owners") or []
        if owner in before_callables
    }
    for owner in sorted(before_value_returns):
        if (
            owner in named_return_owners
            and owner in after_callables
            and owner not in after_value_returns
            and not _instruction_allows_value_return_change(instruction, owner)
        ):
            violations.append({
                "kind": "value_return_removed",
                "owner": owner,
                "message": "Preserve the callable's value-return behavior unless the instruction explicitly changes it.",
            })

    requested = list(semantic_audit.get("requested_identifiers") or [])
    required_owners = list(semantic_audit.get("owner_reuse_obligations") or [])
    requested_nodes = [
        after_callables[name]
        for name in requested
        if name in after_callables
    ]
    requested_nodes.extend(
        node
        for name, node in after_callables.items()
        if name.rsplit(".", 1)[-1] in requested and node not in requested_nodes
    )
    parameter_contract = semantic_audit.get("requested_parameter_contract") or {}
    for symbol, contract in parameter_contract.items():
        matching_nodes = [
            node for name, node in after_callables.items()
            if name.rsplit(".", 1)[-1] == symbol
        ]
        for node in matching_nodes:
            positional = [*getattr(node.args, "posonlyargs", []), *node.args.args]
            actual_names = [
                arg.arg for arg in [*positional, *node.args.kwonlyargs]
                if arg.arg not in {"self", "cls"}
            ]
            expected_names = list(contract.get("names") or [])
            expected_arity = contract.get("arity")
            mismatch = bool(
                expected_names and actual_names != expected_names
            ) or bool(
                not expected_names
                and expected_arity is not None
                and len(actual_names) != int(expected_arity)
            )
            if mismatch:
                violations.append({
                    "kind": "requested_signature_mismatch",
                    "owner": symbol,
                    "expected_names": expected_names,
                    "expected_arity": expected_arity,
                    "actual_names": actual_names,
                    "evidence_class": contract.get("evidence_class"),
                    "message": (
                        f"The candidate signature for `{symbol}` has inputs {actual_names}, "
                        f"which do not match the instruction-derived input contract."
                    ),
                })
    if required_owners and requested_nodes:
        calls = {
            _python_call_name(call)
            for node in requested_nodes
            for call in ast.walk(node)
            if isinstance(call, ast.Call)
        }
        calls.discard("")
        for owner in required_owners:
            bare = owner.rsplit(".", 1)[-1]
            if bare not in calls and owner not in calls:
                violations.append({
                    "kind": "owner_not_reused",
                    "owner": owner,
                    "requested_identifiers": requested,
                    "message": (
                        f"Call {owner} from the requested implementation; do not copy its formula, "
                        "traversal, parsing, or policy."
                    ),
                })
                continue

            owner_calls = [
                call
                for node in requested_nodes
                for call in ast.walk(node)
                if isinstance(call, ast.Call)
                and _python_call_name(call).rsplit(".", 1)[-1] == bare
            ]
            request_parameters = {
                arg.arg
                for node in requested_nodes
                for arg in node.args.args
                if arg.arg not in {"self", "cls"}
            }
            rewritten = []
            for call in owner_calls:
                for argument in call.args:
                    if isinstance(argument, ast.Name) and argument.id in request_parameters:
                        continue
                    if isinstance(argument, ast.Constant):
                        continue
                    rewritten.append(ast.unparse(argument))
            if rewritten and request_parameters:
                violations.append({
                    "kind": "owner_context_rewritten",
                    "owner": owner,
                    "arguments": rewritten,
                    "available_context_parameters": sorted(request_parameters),
                    "message": (
                        f"Pass the requested API's existing context parameter directly to {owner}. "
                        "Do not filter, augment, or rebuild that context unless the instruction explicitly requires it."
                    ),
                })

    rollback_obligations = list(semantic_audit.get("rollback_obligations") or [])
    for obligation in rollback_obligations:
        owner = str(obligation.get("owner") or "")
        node = after_callables.get(owner)
        if node is None:
            continue
        if not _has_journal_cleanup(
            node,
            str(obligation.get("journal") or ""),
            str(obligation.get("collection") or ""),
        ):
            violations.append({
                "kind": "missing_paired_rollback",
                "owner": owner,
                "journal": obligation.get("journal"),
                "collection": obligation.get("collection"),
                "message": "Undo every source-journaled state mutation on unsuccessful backtracking paths.",
            })
    for owner in sorted({str(item.get("owner") or "") for item in rollback_obligations}):
        node = after_callables.get(owner)
        owner_obligations = [item for item in rollback_obligations if item.get("owner") == owner]
        if node is None or len(owner_obligations) < 2:
            continue
        for cleaned in _rollback_cleanup_sets_before_false_returns(node, owner_obligations):
            if not cleaned:
                continue
            for obligation in owner_obligations:
                journal = str(obligation.get("journal") or "")
                marker = (journal, str(obligation.get("collection") or ""))
                if marker in cleaned:
                    continue
                violation = {
                    "kind": "missing_paired_rollback",
                    "owner": owner,
                    "journal": journal,
                    "collection": obligation.get("collection"),
                    "message": "A failure return cleans part of a source-derived state journal but not its paired mutations.",
                }
                duplicate = any(
                    item.get("kind") == violation["kind"]
                    and item.get("owner") == violation["owner"]
                    and item.get("journal") == violation["journal"]
                    and item.get("collection") == violation["collection"]
                    for item in violations
                )
                if not duplicate:
                    violations.append(violation)

    return {
        "status": "pass" if not violations else "violations",
        "before_callable_surface": sorted(before_callables),
        "after_callable_surface": sorted(after_callables),
        "checked_requested_identifiers": requested,
        "checked_requested_parameter_contract": parameter_contract,
        "checked_owner_reuse": required_owners,
        "checked_value_return_surface": sorted(before_value_returns),
        "checked_rollback_obligations": list(semantic_audit.get("rollback_obligations") or []),
        "before_unresolved_global_names": sorted(before_unresolved),
        "after_unresolved_global_names": sorted(after_unresolved),
        "introduced_unresolved_global_names": introduced_unresolved,
        "unresolved_name_check_skipped_for_star_import": bool(after_has_star_import),
        "violations": violations,
    }


def audit_task_delta_edit(
    before_source: str,
    candidate_source: str,
    delta_audit: dict[str, Any],
) -> dict[str, Any]:
    """Audit only structural task-delta obligations derivable without tests."""
    import ast

    try:
        before_tree = ast.parse(before_source)
        candidate_tree = ast.parse(candidate_source)
    except SyntaxError as exc:
        return {
            "status": "invalid_python",
            "violations": [{"kind": "syntax_error", "message": str(exc)}],
        }

    before_callables = _python_callable_nodes(before_tree)
    candidate_callables = _python_callable_nodes(candidate_tree)
    candidate_symbols = _python_declared_symbols(candidate_tree, candidate_callables)
    violations: list[dict[str, Any]] = []

    for symbol in delta_audit.get("must_add") or []:
        if symbol not in candidate_symbols:
            violations.append({
                "kind": "missing_must_add",
                "symbol": symbol,
                "message": f"The instruction requires adding `{symbol}`, but the candidate does not declare it.",
            })

    for owner in delta_audit.get("must_remove") or []:
        bare = str(owner).rsplit(".", 1)[-1]
        if owner in candidate_callables or bare in candidate_symbols:
            violations.append({
                "kind": "must_remove_still_present",
                "owner": owner,
                "message": f"The instruction explicitly removes or replaces `{owner}`, but it remains declared.",
            })

    if str(delta_audit.get("edit_intent") or "") != "addition":
        required_change_owners = delta_audit.get("required_change_owners")
        if required_change_owners is None:
            required_change_owners = (
                delta_audit.get("primary_target_owners")
                or delta_audit.get("target_owners")
                or []
            )
        for owner in required_change_owners:
            before_node = before_callables.get(owner)
            after_node = candidate_callables.get(owner)
            if before_node is None or after_node is None:
                continue
            if ast.dump(before_node, include_attributes=False) == ast.dump(after_node, include_attributes=False):
                violations.append({
                    "kind": "target_owner_unchanged",
                    "owner": owner,
                    "message": f"The instruction targets `{owner}`, but its implementation is structurally unchanged.",
                })

    return {
        "status": "pass" if not violations else "violations",
        "candidate_symbols": sorted(candidate_symbols),
        "checked_must_add": list(delta_audit.get("must_add") or []),
        "checked_must_remove": list(delta_audit.get("must_remove") or []),
        "checked_target_owners": list(delta_audit.get("target_owners") or []),
        "checked_required_change_owners": list(
            delta_audit.get("required_change_owners")
            if delta_audit.get("required_change_owners") is not None
            else delta_audit.get("primary_target_owners") or []
        ),
        "violations": violations,
    }


def audit_candidate_repair_scope(
    baseline_source: str,
    repaired_source: str,
    delta_audit: dict[str, Any],
) -> dict[str, Any]:
    """Reject a repair that rewrites existing owners outside the task delta."""
    import ast

    try:
        baseline_tree = ast.parse(baseline_source)
        repaired_tree = ast.parse(repaired_source)
    except SyntaxError as exc:
        return {
            "status": "invalid_python",
            "violations": [{"kind": "syntax_error", "message": str(exc)}],
        }

    baseline_callables = _python_callable_nodes(baseline_tree)
    repaired_callables = _python_callable_nodes(repaired_tree)
    allowed = set(delta_audit.get("target_owners") or [])
    allowed_bare = {str(item).rsplit(".", 1)[-1] for item in allowed}
    allowed_added = {str(item) for item in delta_audit.get("must_add") or []}
    allowed_bare.update(allowed_added)
    changed_unrelated: list[str] = []
    for owner, before_node in baseline_callables.items():
        after_node = repaired_callables.get(owner)
        if after_node is None:
            continue
        if owner in allowed or owner.rsplit(".", 1)[-1] in allowed_bare:
            continue
        if owner.split(".", 1)[0] in allowed_added:
            continue
        if ast.dump(before_node, include_attributes=False) != ast.dump(
            after_node, include_attributes=False,
        ):
            changed_unrelated.append(owner)

    violations: list[dict[str, Any]] = []
    if changed_unrelated:
        violations.append({
            "kind": "unrelated_owner_changed",
            "owners": sorted(changed_unrelated),
            "message": "The SPL repair changed existing owners outside the source-bound task delta.",
        })
    return {
        "status": "pass" if not violations else "violations",
        "allowed_target_owners": sorted(allowed),
        "allowed_added_symbols": sorted(
            str(item) for item in delta_audit.get("must_add") or []
        ),
        "violations": violations,
    }


def _python_declared_symbols(tree: Any, callables: dict[str, Any]) -> set[str]:
    import ast

    symbols = {name.rsplit(".", 1)[-1] for name in callables}
    symbols.update(node.name for node in ast.walk(tree) if isinstance(node, ast.ClassDef))
    for node in ast.walk(tree):
        targets: list[Any] = []
        if isinstance(node, (ast.Assign, ast.AnnAssign, ast.AugAssign)):
            targets = list(node.targets) if isinstance(node, ast.Assign) else [node.target]
        for target in targets:
            if isinstance(target, ast.Name):
                symbols.add(target.id)
            elif isinstance(target, ast.Attribute):
                symbols.add(target.attr)
    return symbols


def _python_value_return_surface(callables: dict[str, Any]) -> set[str]:
    import ast

    return {
        owner
        for owner, node in callables.items()
        if any(isinstance(child, ast.Return) and child.value is not None for child in ast.walk(node))
    }


def _python_declared_value_return_surface(callables: dict[str, Any]) -> set[str]:
    import ast

    declared: set[str] = set()
    for owner, node in callables.items():
        annotation = getattr(node, "returns", None)
        if annotation is None:
            continue
        rendered = ast.unparse(annotation).replace(" ", "")
        if rendered not in {"None", "NoneType", "type(None)"}:
            declared.add(owner)
    return declared


def _spl_semantic_reliability(
    source: str,
    language: str,
    intent: str,
    selected_owners: list[str],
    instruction_named_owners: list[str],
) -> dict[str, Any]:
    """Route away from SPL when selected cards describe only source stubs."""
    result: dict[str, Any] = {
        "fallback": False,
        "reason": None,
        "instruction_named_owners": instruction_named_owners,
        "nonsemantic_owners": [],
    }
    if language.lower() not in {"python", "py"} or intent != "addition":
        return result
    import ast

    try:
        callables = _python_callable_nodes(ast.parse(source))
    except SyntaxError:
        return result
    relevant = instruction_named_owners or selected_owners
    nonsemantic = [owner for owner in relevant if _python_callable_is_stub(callables.get(owner))]
    result["nonsemantic_owners"] = nonsemantic
    if relevant and len(nonsemantic) == len(relevant):
        result["fallback"] = True
        result["reason"] = "all instruction-relevant SPL owners are abstract or stub-only"
    return result


def _python_callable_is_stub(node: Any) -> bool:
    import ast

    if node is None:
        return False
    body = [stmt for stmt in node.body if not (
        isinstance(stmt, ast.Expr)
        and isinstance(stmt.value, ast.Constant)
        and isinstance(stmt.value.value, str)
    )]
    if not body or all(isinstance(stmt, ast.Pass) for stmt in body):
        return True
    if len(body) == 1 and isinstance(body[0], ast.Raise):
        call = body[0].exc
        return (
            isinstance(call, ast.Call)
            and isinstance(call.func, ast.Name)
            and call.func.id == "NotImplementedError"
        )
    return False


def _rollback_obligations(source: str, instruction: str, language: str) -> list[dict[str, str]]:
    """Derive paired state-journal cleanup obligations from current source."""
    if language.lower() not in {"python", "py"} or not re.search(
        r"\b(backtrack|rollback|roll back|undo|revert|contradiction|empty clauses?)\b",
        instruction,
        re.IGNORECASE,
    ):
        return []
    import ast

    try:
        callables = _python_callable_nodes(ast.parse(source))
    except SyntaxError:
        return []
    obligations: list[dict[str, str]] = []
    for owner, node in callables.items():
        state_adds: dict[str, list[tuple[int, str]]] = {}
        journal_appends: dict[str, list[tuple[int, str]]] = {}
        for call in (child for child in ast.walk(node) if isinstance(child, ast.Call)):
            if len(call.args) != 1 or not isinstance(call.func, ast.Attribute):
                continue
            value_key = ast.dump(call.args[0], include_attributes=False)
            receiver = call.func.value
            if (
                call.func.attr == "add"
                and isinstance(receiver, ast.Attribute)
                and isinstance(receiver.value, ast.Name)
                and receiver.value.id == "self"
            ):
                state_adds.setdefault(value_key, []).append(
                    (int(getattr(call, "lineno", 0)), f"self.{receiver.attr}")
                )
            elif call.func.attr == "append" and isinstance(receiver, ast.Name):
                journal_appends.setdefault(value_key, []).append(
                    (int(getattr(call, "lineno", 0)), receiver.id)
                )
        for value_key in sorted(set(state_adds) & set(journal_appends)):
            additions = sorted(state_adds[value_key])
            journals = sorted(journal_appends[value_key])
            unused = list(additions)
            for journal_line, journal in journals:
                if not unused:
                    break
                preceding = [entry for entry in unused if entry[0] <= journal_line]
                chosen = max(preceding or unused, key=lambda entry: entry[0])
                unused.remove(chosen)
                obligations.append({
                    "owner": owner,
                    "journal": journal,
                    "collection": chosen[1],
                })
    return obligations


def _has_journal_cleanup(node: Any, journal: str, collection: str) -> bool:
    import ast

    collection_attr = collection.removeprefix("self.")
    for loop in (child for child in ast.walk(node) if isinstance(child, ast.For)):
        if not isinstance(loop.iter, ast.Name) or loop.iter.id != journal:
            continue
        loop_name = loop.target.id if isinstance(loop.target, ast.Name) else ""
        for call in (child for child in ast.walk(loop) if isinstance(child, ast.Call)):
            if not isinstance(call.func, ast.Attribute) or call.func.attr not in {"remove", "discard"}:
                continue
            receiver = call.func.value
            if not (
                isinstance(receiver, ast.Attribute)
                and isinstance(receiver.value, ast.Name)
                and receiver.value.id == "self"
                and receiver.attr == collection_attr
            ):
                continue
            if call.args and isinstance(call.args[0], ast.Name) and call.args[0].id == loop_name:
                return True
    return False


def _rollback_cleanup_sets_before_false_returns(
    node: Any,
    obligations: list[dict[str, str]],
) -> list[set[tuple[str, str]]]:
    """Collect journal cleanups adjacent to each explicit unsuccessful return."""
    import ast

    results: list[set[tuple[str, str]]] = []

    def visit_block(statements: list[Any]) -> None:
        preceding: list[Any] = []
        for statement in statements:
            if (
                isinstance(statement, ast.Return)
                and isinstance(statement.value, ast.Constant)
                and statement.value.value is False
            ):
                cleaned: set[tuple[str, str]] = set()
                for obligation in obligations:
                    if any(
                        _has_journal_cleanup(previous, obligation["journal"], obligation["collection"])
                        for previous in preceding
                    ):
                        cleaned.add((obligation["journal"], obligation["collection"]))
                results.append(cleaned)
            for child_block in _python_statement_blocks(statement):
                visit_block(child_block)
            preceding.append(statement)

    visit_block(list(getattr(node, "body", [])))
    return results


def _python_statement_blocks(statement: Any) -> list[list[Any]]:
    import ast

    blocks: list[list[Any]] = []
    for attribute in ("body", "orelse", "finalbody"):
        value = getattr(statement, attribute, None)
        if isinstance(value, list) and value:
            blocks.append(value)
    if isinstance(statement, ast.Try):
        blocks.extend(handler.body for handler in statement.handlers if handler.body)
    return blocks


def _classify_edit_intent(instruction: str) -> str:
    action = _instruction_action_clause(instruction)
    declaration_noun = r"(?:functions?|methods?|classes?|properties|attributes|fields|variables|parameters|apis?)"
    if re.search(
        rf"\b(?:add|introduce|create|implement|define|include|write)\b[^.\n]{{0,120}}\b{declaration_noun}\b",
        action,
    ) or re.search(
        r"\b(?:add|introduce|create|implement|define)\s+[`'\"][A-Za-z_][A-Za-z0-9_]*[`'\"]",
        action,
    ) or re.search(
        r"\b(?:add|introduce|create|implement|define)\s+(?:(?:a|an|the)\s+)?[a-z_][a-z0-9_]*\s+[`'\"][a-z_][a-z0-9_]*[`'\"]",
        action,
    ):
        return "addition"
    if re.search(r"\b(optimi[sz]e|faster|performance|less steps|prun|refactor)\b", action):
        return "optimization"
    if re.search(r"\b(fix|bug|wrong|correct|prevent|avoid)\b", action):
        return "corrective"
    return "behavioral_change"


def _instruction_action_clause(instruction: str) -> str:
    """Return the leading requested action, excluding examples and notes."""
    first_paragraph = re.split(r"\n\s*\n", instruction.strip(), maxsplit=1)[0]
    return first_paragraph[:1000].lower()


def _semantic_terms(text: str) -> set[str]:
    stop = {
        "add", "and", "are", "for", "from", "into", "method", "new", "of",
        "return", "returns", "that", "the", "this", "to", "using", "with",
    }
    terms: set[str] = set()
    for raw in re.findall(r"[A-Za-z_][A-Za-z0-9_]*", text.lower()):
        for part in raw.split("_"):
            if len(part) < 3 or part in stop:
                continue
            # A small lexical stem is enough to align estimate/estimated and
            # parse/parsed without introducing another semantic model call.
            stem = re.sub(r"(?:ing|ed|es|s)$", "", part)
            terms.add(stem or part)
    return terms


def _owner_reuse_obligations(
    instruction: str,
    requested_symbols: list[str],
    owner_capabilities: dict[str, str],
) -> list[str]:
    """Select high-confidence existing capabilities that a new API must reuse."""
    if _classify_edit_intent(instruction) != "addition":
        return []
    if not re.search(
        r"\b(?:based\s+on|derived\s+from|delegate(?:s|d|ing)?\s+to|compose(?:s|d|ing)?\s+with)\b",
        instruction,
        re.IGNORECASE,
    ):
        return []
    if (
        re.search(r"\breturn(?:s|ing)?\b", instruction, re.IGNORECASE)
        and re.search(r"[+*/%]|\b(?:difference|product|quotient|formula)\b", instruction, re.IGNORECASE)
    ):
        return []
    query_terms = _semantic_terms(instruction)
    requested_bare = {symbol.rsplit(".", 1)[-1] for symbol in requested_symbols}
    scored: list[tuple[int, str]] = []
    for owner, capability in owner_capabilities.items():
        bare = owner.rsplit(".", 1)[-1]
        if bare in requested_bare or bare.startswith("__"):
            continue
        overlap = len(query_terms & _semantic_terms(f"{bare} {capability}"))
        if overlap >= 2:
            scored.append((overlap, owner))
    if not scored:
        return []
    best = max(score for score, _owner in scored)
    return [owner for score, owner in scored if score == best][:2]


def _python_callable_nodes(tree: Any) -> dict[str, Any]:
    import ast

    callables: dict[str, Any] = {}
    for node in tree.body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            callables[node.name] = node
        elif isinstance(node, ast.ClassDef):
            for child in node.body:
                if isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    callables[f"{node.name}.{child.name}"] = child
    return callables


def _python_call_name(call: Any) -> str:
    import ast

    target = call.func
    if isinstance(target, ast.Name):
        return target.id
    if isinstance(target, ast.Attribute):
        parts = [target.attr]
        value = target.value
        while isinstance(value, ast.Attribute):
            parts.append(value.attr)
            value = value.value
        if isinstance(value, ast.Name) and value.id not in {"self", "cls"}:
            parts.append(value.id)
        return ".".join(reversed(parts))
    return ""


def _selected_owner_cards(
    spl_by_method: dict[str, str], selected_owners: list[str],
) -> dict[str, str]:
    cards: dict[str, str] = {}
    for owner in selected_owners:
        bare = owner.rsplit(".", 1)[-1]
        for key, card in spl_by_method.items():
            normalized = str(key).split("#", 1)[0]
            if normalized == owner or normalized.rsplit(".", 1)[-1] == bare:
                cards[owner] = str(card)
                break
    return cards


def _owner_capabilities(cards: dict[str, str]) -> dict[str, str]:
    """Extract compact current-behavior capabilities without inventing APIs."""
    capabilities: dict[str, str] = {}
    for owner, card in cards.items():
        worker = re.search(r'\[DEFINE_WORKER:\s*"([^"]+)"', card)
        if worker:
            capability = re.sub(r"\s+", " ", worker.group(1)).strip().rstrip(".")
        else:
            command = next(
                (line.strip() for line in card.splitlines() if line.strip().startswith("[COMMAND")),
                "current behavior described by its source-bound SPL card",
            )
            capability = re.sub(r"\s+", " ", command).strip("[]")
        capabilities[owner] = capability
    return capabilities


def _identity_domain_risks(cards: dict[str, str]) -> list[str]:
    """Flag generic fresh-object/reference mixing hazards found in SPL cards."""
    risks: list[str] = []
    allocation = re.compile(
        r"\b(fresh|newly created|new\s+(?:object|instance|node|graph)|allocate[sd]?)\b",
        re.IGNORECASE,
    )
    reference = re.compile(
        r"\b(reference|adjacen|edge|mapping|lookup|visited|key|identity|identities)\w*\b",
        re.IGNORECASE,
    )
    for owner, card in cards.items():
        compact = re.sub(r"\s+", " ", card)
        if allocation.search(compact) and reference.search(compact):
            risks.append(
                f"{owner} appears to create fresh objects while carrying reference-based relationships; verify that consumers stay within the returned object's identity domain."
            )
    return risks


def _behavior_checkpoints(cards: list[str], limit: int = 10) -> list[str]:
    checkpoints: list[str] = []
    for card in cards:
        worker = re.search(r'\[DEFINE_WORKER:\s*"([^"]+)"\s+([^\]\s]+)\]', card)
        if worker:
            checkpoints.append(f"{worker.group(2)} currently {worker.group(1).rstrip('.')}.")
        commands_added = 0
        for raw_line in card.splitlines():
            line = raw_line.strip()
            if line.startswith(("[COMMAND", "[CONDITION", "[RETURN")):
                compact = re.sub(r"\s+", " ", line)
                if compact not in checkpoints:
                    checkpoints.append(compact)
                    commands_added += 1
            if commands_added >= 2:
                break
            if len(checkpoints) >= limit:
                return checkpoints
        if len(checkpoints) >= limit:
            return checkpoints
    return checkpoints


def _instruction_symbols(instruction: str, owners: list[str]) -> list[str]:
    lowered = instruction.lower()
    return [
        owner for owner in owners
        if owner.rsplit(".", 1)[-1].lower() in lowered
    ]


def _requested_symbols(instruction: str) -> list[str]:
    """Extract identifiers explicitly requested as new declarations.

    Quoted examples, parameter names, literals, and type annotations are not
    declaration requests. Restrict extraction to the leading action clause
    and require a declaration noun or an explicit naming construction.
    """
    action = re.split(r"\n\s*\n", instruction.strip(), maxsplit=1)[0][:1000]
    symbols: list[str] = []
    declaration_noun = r"(?:functions?|methods?|classes?|properties|attributes|fields|variables|parameters|apis?)"
    patterns = [
        rf"\breplace\b[^.\n]{{0,100}}\bwith\s+(?:(?:a|an|the)\s+)?(?:new\s+)?{declaration_noun}\s*[`'\"]?([A-Za-z_][A-Za-z0-9_]*)",
        r"\brename\b[^.\n]{0,100}\bto\s*[`'\"]?([A-Za-z_][A-Za-z0-9_]*)",
        rf"\b(?:add|introduce|create|implement|define|include|write)\s+(?:(?:a|an|the)\s+)?[`'\"]([A-Za-z_][A-Za-z0-9_]*)[`'\"]\s+{declaration_noun}\b",
        r"\b(?:add|introduce|create|implement|define)\s+(?:(?:a|an|the)\s+)?[A-Za-z_][A-Za-z0-9_]*\s+[`'\"]([A-Za-z_][A-Za-z0-9_]*)[`'\"]",
        rf"\b{declaration_noun}\b[^.\n]{{0,100}}\b(?:with\s+(?:the\s+)?signature|called|named)\s*[`'\"]?([A-Za-z_][A-Za-z0-9_]*)",
        rf"\b(?:add|introduce|create|implement|define|include|write)\s+(?:(?:a|an|the|two|three)\s+)?(?:new\s+)?{declaration_noun}\s+(?:called|named)?\s*[`'\"]?([A-Za-z_][A-Za-z0-9_]*)",
        rf"\b(?:add|introduce|create|implement|define|include|write)\s+[`'\"]([A-Za-z_][A-Za-z0-9_]*)[`'\"]\s+(?:as\s+)?(?:a|an)?\s*{declaration_noun}\b",
        r"\b(?:add|introduce|create|implement|define)\s+[`'\"]([A-Za-z_][A-Za-z0-9_]*)[`'\"]",
        rf"\b{declaration_noun}\s+[`'\"]([A-Za-z_][A-Za-z0-9_]*)[`'\"]\s+(?:should|must|that\s+will)\b",
    ]
    stopwords = {
        "a", "an", "as", "at", "by", "for", "from", "in", "into", "of",
        "on", "that", "the", "to", "using", "with", "node", "int", "str",
        "float", "bool", "dict", "list", "set", "tuple",
    }
    for pattern in patterns:
        for symbol in re.findall(pattern, action, re.IGNORECASE):
            if symbol.lower() not in stopwords and symbol not in symbols:
                symbols.append(symbol)
    return symbols


def _requested_parameter_contract(
    instruction: str,
    requested_symbols: list[str],
) -> dict[str, dict[str, Any]]:
    """Extract only explicit or single-concept inputs for a requested API."""
    contracts: dict[str, dict[str, Any]] = {}
    for symbol in requested_symbols:
        escaped = re.escape(symbol)
        signature = re.search(
            rf"[`'\"]?{escaped}[`'\"]?\s*\(([^)]*)\)",
            instruction,
            re.IGNORECASE,
        )
        if signature:
            names = []
            for raw in signature.group(1).split(","):
                name_match = re.match(r"\s*([A-Za-z_][A-Za-z0-9_]*)", raw)
                if name_match and name_match.group(1) not in {"self", "cls"}:
                    names.append(name_match.group(1))
            contracts[symbol] = {
                "names": names,
                "arity": len(names),
                "evidence_class": "explicit_signature",
            }
            continue

        argument = re.search(
            rf"\b{escaped}\b[^.\n]{{0,120}}\btakes(?:\s+in)?\s+"
            r"(?:(?:a|an|the)\s+)?argument\s+[`'\"]?([A-Za-z_][A-Za-z0-9_]*)",
            instruction,
            re.IGNORECASE,
        )
        if argument:
            contracts[symbol] = {
                "names": [argument.group(1)],
                "arity": 1,
                "evidence_class": "explicit_argument",
            }
            continue

        if len(requested_symbols) == 1 and re.search(
            r"\b(?:by|using|from)\s+(?:(?:a|an|the)\s+)?given\s+"
            r"(?:[A-Za-z_][A-Za-z0-9_]*\s+)?(?:amount|value|number|count|index|key)\b",
            instruction,
            re.IGNORECASE,
        ):
            contracts[symbol] = {
                "names": [],
                "arity": 1,
                "evidence_class": "single_given_input_concept",
            }
    return contracts


def _addition_allows_existing_owner_change(instruction: str, owner: str) -> bool:
    """Identify existing owners that an additive request explicitly rewires."""
    bare = owner.rsplit(".", 1)[-1]
    escaped = re.escape(bare)
    return bool(
        re.search(
            rf"\b(?:modify|update|change|rewrite)\b[^.\n]{{0,100}}\b{escaped}\b",
            instruction,
            re.IGNORECASE,
        )
        or re.search(
            rf"\bensure\b[^.\n]{{0,160}}\b{escaped}\b[^.\n]{{0,120}}\b(?:use|call|invoke|delegate)\b",
            instruction,
            re.IGNORECASE,
        )
        or re.search(
            rf"\b{escaped}\b\s+(?:must|should|will)\s+(?:use|call|invoke|delegate)\b",
            instruction,
            re.IGNORECASE,
        )
    )


def _is_stateful_change(instruction: str) -> bool:
    return bool(re.search(
        r"\b(visit(?:ed)?|seen|cache|state|track|mark|label|queue|cluster)\w*\b",
        instruction,
        re.IGNORECASE,
    ))


def _instruction_allows_value_return_change(instruction: str, owner: str) -> bool:
    bare = owner.rsplit(".", 1)[-1]
    if not re.search(rf"\b{re.escape(bare)}\b", instruction, re.IGNORECASE):
        return False
    return bool(re.search(
        r"\b(?:in[ -]?place|no return|return(?:s|ing)?\s+none|void)\b",
        instruction,
        re.IGNORECASE,
    ))
