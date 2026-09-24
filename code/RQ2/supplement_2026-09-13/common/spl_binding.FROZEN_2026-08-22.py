from __future__ import annotations

import ast
import hashlib
import re
import warnings
from dataclasses import asdict, dataclass
from typing import Any

from .spl_adapter import select_task_relevant_spl_methods


_NUMBERED_LINE = re.compile(r"^\s*(?P<number>\d+)(?P<gap>\s{2,})(?P<code>.*)$")
_WORKER = re.compile(r'\[DEFINE_WORKER:\s*"[^"]*"\s+([^\]\s]+)\]')


@dataclass(frozen=True)
class SourceOwner:
    qualified_name: str
    bare_name: str
    start_line: int
    end_line: int
    source_start_line: int
    source_end_line: int
    signature: str
    code: str
    content_hash: str
    calls: tuple[str, ...]


def normalize_numbered_source(source: str) -> tuple[str, dict[int, int], bool]:
    """Remove benchmark display line numbers while retaining a line map.

    CoRe source snippets are often stored as ``19   statement``. Feeding that
    display representation to a language parser makes valid Python look
    syntactically invalid. Number stripping is enabled only when most non-empty
    lines follow the benchmark format, so ordinary source is left untouched.
    """
    lines = source.splitlines()
    matches = [_NUMBERED_LINE.match(line) for line in lines]
    nonempty = sum(bool(line.strip()) for line in lines)
    matched = sum(match is not None for match in matches)
    is_numbered = bool(nonempty and matched >= 2 and matched / nonempty >= 0.6)
    normalized: list[str] = []
    line_map: dict[int, int] = {}
    for index, (line, match) in enumerate(zip(lines, matches), start=1):
        if is_numbered and match:
            # CoRe renders a visual separator after the line number: three
            # spaces for one-digit lines and at least two thereafter.  Treat
            # only the remaining gap as source indentation.  Comparing total
            # prefix widths makes every three-digit line one space deeper.
            separator_width = max(2, 4 - len(match.group("number")))
            relative_indent = " " * max(0, len(match.group("gap")) - separator_width)
            normalized.append(relative_indent + match.group("code"))
            line_map[index] = int(match.group("number"))
        else:
            normalized.append(line)
            line_map[index] = index
    return "\n".join(normalized), line_map, is_numbered


def extract_source_owners(source: str, language: str) -> tuple[list[SourceOwner], dict[str, Any]]:
    normalized, line_map, stripped = normalize_numbered_source(source)
    normalized_language = _normalize_language(language)
    if normalized_language == "python":
        owners, errors = _extract_python_owners(normalized, line_map)
    else:
        owners, errors = _extract_brace_owners(normalized, line_map)
    return owners, {
        "language": normalized_language,
        "numbered_source_normalized": stripped,
        "owner_count": len(owners),
        "errors": errors,
    }


def bind_spl_to_source(
    source: str,
    spl_by_method: dict[str, str],
    language: str,
) -> tuple[dict[str, str], dict[str, dict[str, Any]], dict[str, Any]]:
    """Bind SPL cards to unique source owners and reject ambiguous cards."""
    owners, source_audit = extract_source_owners(source, language)
    by_qualified = {owner.qualified_name: owner for owner in owners}
    by_bare: dict[str, list[SourceOwner]] = {}
    for owner in owners:
        by_bare.setdefault(owner.bare_name, []).append(owner)

    bound: dict[str, str] = {}
    provenance: dict[str, dict[str, Any]] = {}
    rejected: list[dict[str, str]] = []
    for raw_key, card in spl_by_method.items():
        key = str(raw_key).split("#", 1)[0]
        bare = key.rsplit(".", 1)[-1]
        owner = by_qualified.get(key)
        match_kind = "qualified_exact"
        if owner is None:
            candidates = by_bare.get(bare, [])
            if len(candidates) == 1:
                owner = candidates[0]
                match_kind = "bare_unique"
            elif len(candidates) > 1:
                rejected.append({"spl_key": str(raw_key), "reason": "ambiguous_bare_name"})
                continue
        if owner is None:
            rejected.append({"spl_key": str(raw_key), "reason": "source_owner_not_found"})
            continue

        worker_match = _WORKER.search(str(card))
        worker = worker_match.group(1).strip() if worker_match else ""
        worker_matches_owner = not worker or worker.rsplit(".", 1)[-1] == owner.bare_name

        bound_key = owner.qualified_name
        if bound_key in bound:
            rejected.append({"spl_key": str(raw_key), "reason": "duplicate_source_owner"})
            continue
        bound[bound_key] = str(card)
        provenance[bound_key] = {
            **asdict(owner),
            "spl_key": str(raw_key),
            "worker_name": worker or None,
            # The map key is produced by the source parser; DEFINE_WORKER is
            # generated prose and may be a semantic role name.  Keep the
            # mismatch visible without allowing it to overrule source truth.
            "worker_name_matches_source_owner": worker_matches_owner,
            "match_kind": match_kind,
        }

    audit = {
        **source_audit,
        "input_spl_cards": len(spl_by_method),
        "bound_spl_cards": len(bound),
        "coverage": len(bound) / len(owners) if owners else 0.0,
        "rejected": rejected,
        "worker_name_mismatches": [
            {
                "source_owner": owner,
                "spl_key": details["spl_key"],
                "worker_name": details["worker_name"],
            }
            for owner, details in provenance.items()
            if not details["worker_name_matches_source_owner"]
        ],
        "status": "complete" if owners and len(bound) == len(owners) else (
            "partial" if bound else "unavailable"
        ),
    }
    return bound, provenance, audit


def select_source_bound_spl_cards(
    source: str,
    spl_by_method: dict[str, str],
    query: str,
    language: str,
    *,
    max_cards: int = 4,
    include_source: bool = False,
    expand_callers: bool = False,
    relation_reserve: int = 0,
) -> tuple[str, dict[str, Any]]:
    """Render task-relevant SPL cards with immutable source provenance."""
    bound, provenance, audit = bind_spl_to_source(source, spl_by_method, language)
    reserved = min(max(0, relation_reserve), max(0, max_cards - 1))
    seed_limit = max(1, max_cards - reserved)
    selected = select_task_relevant_spl_methods(bound, query, max_cards=seed_limit)
    query_selected = list(selected)
    class_forced: list[str] = []

    # A class named with source spelling is a high-confidence semantic anchor.
    # Ensure at least one method card from that class survives a crowded
    # lexical top-k; otherwise relations such as "A beats B" can retrieve only
    # the caller and omit B's actual behavior.
    mentioned_classes: list[str] = []
    for owner_name in bound:
        if "." not in owner_name:
            continue
        class_name = owner_name.split(".", 1)[0]
        if class_name in mentioned_classes:
            continue
        if re.search(rf"(?<![A-Za-z0-9_]){re.escape(class_name)}(?![A-Za-z0-9_])", query or ""):
            mentioned_classes.append(class_name)
    for class_name in mentioned_classes:
        if any(owner.startswith(class_name + ".") for owner in selected):
            continue
        candidate = next(
            (owner for owner in bound if owner.startswith(class_name + ".")),
            "",
        )
        if not candidate:
            continue
        if len(selected) >= max_cards:
            selected.pop(next(reversed(selected)))
        selected[candidate] = bound[candidate]
        class_forced.append(candidate)
    query_selected = list(selected)
    call_expanded: list[str] = []

    # Query retrieval identifies likely entry points. Expand those entry points
    # by one source-verified call edge so state changes delegated to a helper do
    # not disappear from the semantic view. Expansion is bounded and only uses
    # owners that already passed source/SPL binding.
    by_bare: dict[str, list[str]] = {}
    for owner_name in bound:
        by_bare.setdefault(owner_name.rsplit(".", 1)[-1], []).append(owner_name)
    for owner_name in query_selected:
        owner_class = owner_name.rsplit(".", 1)[0] if "." in owner_name else ""
        for callee in provenance.get(owner_name, {}).get("calls") or []:
            class_candidate = f"{owner_class}.{callee}" if owner_class else callee
            if class_candidate in bound:
                target = class_candidate
            else:
                candidates = by_bare.get(callee, [])
                target = candidates[0] if len(candidates) == 1 else ""
            if not target:
                continue
            if target in selected:
                if target != owner_name and target not in call_expanded:
                    call_expanded.append(target)
                continue
            if len(selected) >= max_cards:
                continue
            selected[target] = bound[target]
            call_expanded.append(target)
            if len(selected) >= max_cards:
                break

    caller_expanded: list[str] = []
    if expand_callers and len(selected) < max_cards:
        selected_bare = {
            owner_name.rsplit(".", 1)[-1]
            for owner_name in selected
        }
        for candidate_name in bound:
            if candidate_name in selected:
                continue
            calls = set(provenance.get(candidate_name, {}).get("calls") or [])
            if not calls.intersection(selected_bare):
                continue
            selected[candidate_name] = bound[candidate_name]
            caller_expanded.append(candidate_name)
            if len(selected) >= max_cards:
                break

    rendered = render_bound_spl_cards(
        selected,
        provenance,
        include_source=include_source,
        source_language=language,
    )
    audit["query_selected_owners"] = query_selected
    audit["class_forced_owners"] = class_forced
    audit["call_expanded_owners"] = call_expanded
    audit["caller_expanded_owners"] = caller_expanded
    audit["atomic_source_spl_cards"] = include_source
    audit["relation_reserve"] = reserved
    audit["selected_owners"] = list(selected)
    audit["selected_cards"] = len(selected)
    return rendered, audit


def render_bound_spl_cards(
    selected: dict[str, str],
    provenance: dict[str, dict[str, Any]],
    *,
    include_source: bool = False,
    source_language: str = "text",
) -> str:
    cards: list[str] = []
    for owner_name, card in selected.items():
        anchor = provenance.get(owner_name, {})
        lines = [
                f"### Source-bound owner: `{owner_name}`",
                f"- source lines: {anchor.get('source_start_line', '?')}-{anchor.get('source_end_line', '?')}",
                f"- source signature: `{anchor.get('signature', owner_name)}`",
                f"- source content hash: `{anchor.get('content_hash', 'unavailable')}`",
                "- binding rule: the SPL below is a semantic description bound to the numbered source above; it is evidence but auto-generated and not guaranteed correct, and the source is the ground truth when they disagree",
                "",
        ]
        if include_source:
            start_line = int(anchor.get("source_start_line") or 1)
            numbered_source = "\n".join(
                f"{start_line + offset:>4}  {line}"
                for offset, line in enumerate(str(anchor.get("code") or "").splitlines())
            )
            lines.extend([
                "#### Function source (authoritative)",
                f"```{source_language}",
                numbered_source,
                "```",
                "",
            ])
        lines.extend([
            "#### SPL semantics (bound to the function above)",
            "```spl",
            str(card).strip(),
            "```",
        ])
        cards.append("\n".join(lines))
    return "\n\n---\n\n".join(cards)


def source_for_named_owner(
    source: str,
    language: str,
    owner_name: str,
    *,
    source_start_line: int | None = None,
    source_end_line: int | None = None,
) -> tuple[str, dict[str, Any]]:
    """Return one uniquely named owner for task-local SPL regeneration."""
    owners, audit = extract_source_owners(source, language)
    candidates = [
        owner for owner in owners
        if owner.qualified_name == owner_name or owner.bare_name == owner_name.rsplit(".", 1)[-1]
    ]
    if len(candidates) > 1 and source_start_line is not None:
        anchored = [
            owner for owner in candidates
            if owner.source_start_line == int(source_start_line)
            and (source_end_line is None or owner.source_end_line <= int(source_end_line))
        ]
        if len(anchored) == 1:
            candidates = anchored
    if len(candidates) != 1:
        return "", {**audit, "target_owner": owner_name, "target_matches": len(candidates)}
    owner = candidates[0]
    return owner.code, {
        **audit,
        "target_owner": owner.qualified_name,
        "target_matches": 1,
        "source_start_line": owner.source_start_line,
        "source_end_line": owner.source_end_line,
        "content_hash": owner.content_hash,
    }


def python2_compatibility_source(source: str) -> tuple[str, dict[str, Any]]:
    """Create an analysis-only Python-3 parse view for legacy print syntax."""
    try:
        ast.parse(source)
        return source, {"applied": False, "reason": "python3_parseable"}
    except SyntaxError as exc:
        original_parse_error = str(exc)

    try:
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", DeprecationWarning)
            from lib2to3.refactor import RefactoringTool

            tool = RefactoringTool(["lib2to3.fixes.fix_print"])
            converted = str(tool.refactor_string(source.rstrip() + "\n", "spl_source"))
        ast.parse(converted)
    except Exception as exc:
        return source, {
            "applied": False,
            "reason": "compatibility_conversion_failed",
            "original_parse_error": original_parse_error,
            "conversion_error": str(exc),
        }
    changed_lines = sum(
        before != after
        for before, after in zip(source.splitlines(), converted.splitlines())
    )
    return converted, {
        "applied": True,
        "reason": "python2_print_compatibility_for_spl_builder",
        "changed_lines": changed_lines,
        "original_hash": hashlib.sha256(source.encode("utf-8")).hexdigest(),
        "builder_view_hash": hashlib.sha256(converted.encode("utf-8")).hexdigest(),
        "source_authority_unchanged": True,
    }


def _extract_python_owners(source: str, line_map: dict[int, int]) -> tuple[list[SourceOwner], list[str]]:
    try:
        tree = ast.parse(source)
    except SyntaxError as exc:
        owners = _extract_python_owners_lexical(source, line_map)
        return owners, [
            f"python_parse_error:{exc.msg}:line={exc.lineno}",
            "python_lexical_owner_fallback",
        ]
    lines = source.splitlines()
    owners: list[SourceOwner] = []

    def add(node: ast.FunctionDef | ast.AsyncFunctionDef, class_name: str | None = None) -> None:
        start = int(node.lineno)
        end = int(getattr(node, "end_lineno", node.lineno))
        code = "\n".join(lines[start - 1:end])
        qualified = f"{class_name}.{node.name}" if class_name else node.name
        calls: set[str] = set()
        for child in ast.walk(node):
            if not isinstance(child, ast.Call):
                continue
            if isinstance(child.func, ast.Name):
                calls.add(child.func.id)
            elif (
                isinstance(child.func, ast.Attribute)
                and isinstance(child.func.value, ast.Name)
                and child.func.value.id in {"self", "cls"}
            ):
                calls.add(child.func.attr)
        owners.append(_make_owner(
            qualified, node.name, start, end, line_map, code, tuple(sorted(calls)),
        ))

    for node in tree.body:
        if isinstance(node, ast.ClassDef):
            for child in node.body:
                if isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    add(child, node.name)
        elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            add(node)
    return owners, []


def _extract_python_owners_lexical(
    source: str, line_map: dict[int, int],
) -> list[SourceOwner]:
    """Recover Python/Python-2 function spans when Python-3 AST parsing fails."""
    lines = source.splitlines()
    definitions: list[tuple[int, int, str, str | None]] = []
    class_stack: list[tuple[int, str]] = []
    for index, line in enumerate(lines, start=1):
        if not line.strip():
            continue
        indent = len(line) - len(line.lstrip(" \t"))
        while class_stack and indent <= class_stack[-1][0]:
            class_stack.pop()
        class_match = re.match(r"^\s*class\s+([A-Za-z_][A-Za-z0-9_]*)\b", line)
        if class_match:
            class_stack.append((indent, class_match.group(1)))
            continue
        function_match = re.match(
            r"^\s*(?:async\s+)?def\s+([A-Za-z_][A-Za-z0-9_]*)\s*\(", line,
        )
        if function_match:
            class_name = class_stack[-1][1] if class_stack and class_stack[-1][0] < indent else None
            definitions.append((index, indent, function_match.group(1), class_name))

    owners: list[SourceOwner] = []
    for start, indent, name, class_name in definitions:
        end = len(lines)
        for index in range(start + 1, len(lines) + 1):
            line = lines[index - 1]
            if not line.strip() or line.lstrip().startswith(("#", "@")):
                continue
            current_indent = len(line) - len(line.lstrip(" \t"))
            if current_indent <= indent:
                end = index - 1
                break
        code = "\n".join(lines[start - 1:end])
        qualified = f"{class_name}.{name}" if class_name else name
        calls = tuple(sorted({
            called for called in re.findall(r"\b([A-Za-z_][A-Za-z0-9_]*)\s*\(", code)
            if called != name
        }))
        owners.append(_make_owner(
            qualified, name, start, end, line_map, code, calls,
        ))
    return owners


def _extract_brace_owners(source: str, line_map: dict[int, int]) -> tuple[list[SourceOwner], list[str]]:
    pattern = re.compile(
        r"(?P<prefix>(?:public|private|protected|static|final|synchronized|native|abstract|virtual|inline|explicit|\s)+)?"
        r"(?P<name>[A-Za-z_][A-Za-z0-9_]*)\s*\([^;{}]*\)\s*(?:throws\s+[^{}]+)?\{",
        re.MULTILINE,
    )
    lines = source.splitlines()
    owners: list[SourceOwner] = []
    for match in pattern.finditer(source):
        name = match.group("name")
        if name in {"if", "for", "while", "switch", "catch"}:
            continue
        end_index = _matching_brace(source, match.end() - 1)
        if end_index < 0:
            continue
        start = source.count("\n", 0, match.start()) + 1
        end = source.count("\n", 0, end_index) + 1
        code = "\n".join(lines[start - 1:end])
        calls = tuple(sorted({
            called
            for called in re.findall(
                r"(?:this\.|self\.)?([A-Za-z_][A-Za-z0-9_]*)\s*\(", code,
            )
            if called != name
        }))
        owners.append(_make_owner(name, name, start, end, line_map, code, calls))
    return owners, []


def _make_owner(
    qualified: str,
    bare: str,
    start: int,
    end: int,
    line_map: dict[int, int],
    code: str,
    calls: tuple[str, ...] = (),
) -> SourceOwner:
    signature = next((line.strip() for line in code.splitlines() if line.strip()), bare)
    digest = hashlib.sha256(code.encode("utf-8")).hexdigest()
    return SourceOwner(
        qualified_name=qualified,
        bare_name=bare,
        start_line=start,
        end_line=end,
        source_start_line=line_map.get(start, start),
        source_end_line=line_map.get(end, end),
        signature=signature,
        code=code,
        content_hash=digest,
        calls=calls,
    )


def _matching_brace(source: str, open_index: int) -> int:
    depth = 0
    for index in range(open_index, len(source)):
        if source[index] == "{":
            depth += 1
        elif source[index] == "}":
            depth -= 1
            if depth == 0:
                return index
    return -1


def _normalize_language(language: str) -> str:
    lowered = str(language or "").strip().lower()
    if lowered in {"py", "python"}:
        return "python"
    if lowered in {"java"}:
        return "java"
    if lowered in {"c", "c++", "cpp", "cc"}:
        return "cpp"
    return lowered or "python"
