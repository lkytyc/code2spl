from __future__ import annotations

import ast
import io
import keyword
import math
import re
import tokenize
from collections import Counter
from typing import Iterable


DEFAULT_CODEBLEU_WEIGHTS = {
    "bleu": 0.25,
    "weighted_bleu": 0.25,
    "syntax_match": 0.25,
    "dataflow_match": 0.25,
}


def compute_codebleu(reference_code: str, candidate_code: str, weights: dict[str, float] | None = None) -> dict:
    """Compute a lightweight Python CodeBLEU-compatible score.

    The official CodeBLEU implementation relies on tree-sitter language binaries,
    which are fragile across platforms. This implementation keeps the same four
    components while using Python's built-in tokenizer and AST.
    """
    resolved_weights = _normalize_weights(weights or DEFAULT_CODEBLEU_WEIGHTS)
    bleu = _bleu_score(_python_tokens(reference_code), _python_tokens(candidate_code))
    weighted_bleu = _weighted_bleu_score(
        _python_tokens(reference_code),
        _python_tokens(candidate_code),
        set(keyword.kwlist),
    )
    syntax_match = _syntax_match(reference_code, candidate_code)
    dataflow_match = _dataflow_match(reference_code, candidate_code)
    score = (
        resolved_weights["bleu"] * bleu
        + resolved_weights["weighted_bleu"] * weighted_bleu
        + resolved_weights["syntax_match"] * syntax_match
        + resolved_weights["dataflow_match"] * dataflow_match
    )
    return {
        "score": score,
        "bleu": bleu,
        "weighted_bleu": weighted_bleu,
        "syntax_match": syntax_match,
        "dataflow_match": dataflow_match,
        "weights": resolved_weights,
        "implementation": "python_ast_compatible",
        "note": "CodeBLEU-compatible metric: BLEU and weighted BLEU use Python tokens; syntax/dataflow use Python AST.",
    }


def _normalize_weights(weights: dict[str, float]) -> dict[str, float]:
    normalized = {key: float(weights.get(key, DEFAULT_CODEBLEU_WEIGHTS[key])) for key in DEFAULT_CODEBLEU_WEIGHTS}
    total = sum(normalized.values())
    if total <= 0:
        return dict(DEFAULT_CODEBLEU_WEIGHTS)
    return {key: value / total for key, value in normalized.items()}


def _python_tokens(code: str) -> list[str]:
    try:
        tokens: list[str] = []
        reader = io.StringIO(code).readline
        ignored = {
            tokenize.ENCODING,
            tokenize.ENDMARKER,
            tokenize.NL,
            tokenize.NEWLINE,
            tokenize.INDENT,
            tokenize.DEDENT,
            tokenize.COMMENT,
        }
        for token in tokenize.generate_tokens(reader):
            if token.type not in ignored and token.string.strip():
                tokens.append(token.string)
        return tokens
    except (tokenize.TokenError, SyntaxError):
        return re.findall(r"\w+|[^\s\w]", code)


def _ngram_counts(tokens: list[str], n: int) -> Counter[tuple[str, ...]]:
    return Counter(tuple(tokens[index : index + n]) for index in range(max(len(tokens) - n + 1, 0)))


def _bleu_score(reference_tokens: list[str], candidate_tokens: list[str], max_order: int = 4) -> float:
    if not reference_tokens or not candidate_tokens:
        return 0.0

    precisions: list[float] = []
    for order in range(1, max_order + 1):
        ref_counts = _ngram_counts(reference_tokens, order)
        cand_counts = _ngram_counts(candidate_tokens, order)
        possible = sum(cand_counts.values())
        if possible == 0:
            precisions.append(1.0)
            continue
        matches = sum(min(count, ref_counts[ngram]) for ngram, count in cand_counts.items())
        precisions.append((matches + 1.0) / (possible + 1.0))

    brevity_penalty = 1.0
    if len(candidate_tokens) < len(reference_tokens):
        brevity_penalty = math.exp(1.0 - len(reference_tokens) / max(len(candidate_tokens), 1))
    return brevity_penalty * math.exp(sum(math.log(precision) for precision in precisions) / max_order)


def _weighted_bleu_score(reference_tokens: list[str], candidate_tokens: list[str], keywords: set[str], max_order: int = 4) -> float:
    if not reference_tokens or not candidate_tokens:
        return 0.0

    precisions: list[float] = []
    for order in range(1, max_order + 1):
        ref_counts = _ngram_counts(reference_tokens, order)
        cand_counts = _ngram_counts(candidate_tokens, order)
        possible = 0.0
        matches = 0.0
        for ngram, count in cand_counts.items():
            weight = _ngram_weight(ngram, keywords)
            possible += count * weight
            matches += min(count, ref_counts[ngram]) * weight
        if possible == 0:
            precisions.append(1.0)
        else:
            precisions.append((matches + 1.0) / (possible + 1.0))

    brevity_penalty = 1.0
    if len(candidate_tokens) < len(reference_tokens):
        brevity_penalty = math.exp(1.0 - len(reference_tokens) / max(len(candidate_tokens), 1))
    return brevity_penalty * math.exp(sum(math.log(precision) for precision in precisions) / max_order)


def _ngram_weight(ngram: tuple[str, ...], keywords: set[str]) -> float:
    token_weights = [1.0 if token in keywords else 0.2 for token in ngram]
    return sum(token_weights) / len(token_weights)


def _parse_python(code: str) -> ast.AST | None:
    try:
        return ast.parse(code)
    except SyntaxError:
        return None


def _syntax_match(reference_code: str, candidate_code: str) -> float:
    reference_tree = _parse_python(reference_code)
    candidate_tree = _parse_python(candidate_code)
    if reference_tree is None or candidate_tree is None:
        return 0.0
    reference_subtrees = Counter(_subtree_signature(node) for node in ast.walk(reference_tree))
    candidate_subtrees = Counter(_subtree_signature(node) for node in ast.walk(candidate_tree))
    total = sum(reference_subtrees.values())
    if total == 0:
        return 0.0
    matches = sum(min(count, candidate_subtrees[signature]) for signature, count in reference_subtrees.items())
    return matches / total


def _subtree_signature(node: ast.AST) -> str:
    children = " ".join(_subtree_signature(child) for child in ast.iter_child_nodes(node))
    return f"({type(node).__name__} {children})" if children else f"({type(node).__name__})"


def _dataflow_match(reference_code: str, candidate_code: str) -> float:
    reference_flows = Counter(_normalized_dataflow(reference_code))
    candidate_flows = Counter(_normalized_dataflow(candidate_code))
    total = sum(reference_flows.values())
    if total == 0:
        return 0.0
    matches = sum(min(count, candidate_flows[flow]) for flow, count in reference_flows.items())
    return matches / total


def _normalized_dataflow(code: str) -> list[tuple[str, str, tuple[str, ...]]]:
    tree = _parse_python(code)
    if tree is None:
        return []
    flows = _raw_dataflow(tree)
    names: dict[str, str] = {}

    def normalize_name(name: str) -> str:
        if name.startswith("<") and name.endswith(">"):
            return name
        if name not in names:
            names[name] = f"var_{len(names)}"
        return names[name]

    normalized: list[tuple[str, str, tuple[str, ...]]] = []
    for relation, target, sources in flows:
        normalized.append(
            (
                relation,
                normalize_name(target),
                tuple(sorted(normalize_name(source) for source in sources)),
            )
        )
    return normalized


def _raw_dataflow(tree: ast.AST) -> list[tuple[str, str, tuple[str, ...]]]:
    flows: list[tuple[str, str, tuple[str, ...]]] = []
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            for arg in list(node.args.posonlyargs) + list(node.args.args) + list(node.args.kwonlyargs):
                flows.append(("param", arg.arg, tuple()))
            if node.args.vararg:
                flows.append(("param", node.args.vararg.arg, tuple()))
            if node.args.kwarg:
                flows.append(("param", node.args.kwarg.arg, tuple()))
        elif isinstance(node, ast.Assign):
            sources = tuple(sorted(_read_names(node.value)))
            for target in _target_names(node.targets):
                flows.append(("assign", target, sources))
        elif isinstance(node, ast.AnnAssign):
            sources = tuple(sorted(_read_names(node.value) if node.value else []))
            for target in _target_names([node.target]):
                flows.append(("assign", target, sources))
        elif isinstance(node, ast.AugAssign):
            sources = tuple(sorted(set(_read_names(node.target) + _read_names(node.value))))
            for target in _target_names([node.target]):
                flows.append(("update", target, sources))
        elif isinstance(node, (ast.For, ast.AsyncFor)):
            sources = tuple(sorted(_read_names(node.iter)))
            for target in _target_names([node.target]):
                flows.append(("iterate", target, sources))
        elif isinstance(node, (ast.With, ast.AsyncWith)):
            for item in node.items:
                sources = tuple(sorted(_read_names(item.context_expr)))
                if item.optional_vars:
                    for target in _target_names([item.optional_vars]):
                        flows.append(("with", target, sources))
        elif isinstance(node, ast.Return):
            flows.append(("return", "<return>", tuple(sorted(_read_names(node.value) if node.value else []))))
        elif isinstance(node, ast.If):
            flows.append(("control", "<condition>", tuple(sorted(_read_names(node.test)))))
        elif isinstance(node, ast.While):
            flows.append(("control", "<condition>", tuple(sorted(_read_names(node.test)))))
    return flows


def _read_names(node: ast.AST | None) -> list[str]:
    if node is None:
        return []
    names: list[str] = []
    for child in ast.walk(node):
        if isinstance(child, ast.Name) and isinstance(child.ctx, ast.Load):
            names.append(child.id)
        elif isinstance(child, ast.Attribute) and isinstance(child.ctx, ast.Load):
            names.append(_attribute_name(child))
    return names


def _target_names(nodes: Iterable[ast.AST]) -> list[str]:
    targets: list[str] = []
    for node in nodes:
        for child in ast.walk(node):
            if isinstance(child, ast.Name) and isinstance(child.ctx, (ast.Store, ast.Del)):
                targets.append(child.id)
            elif isinstance(child, ast.Attribute) and isinstance(child.ctx, (ast.Store, ast.Del)):
                targets.append(_attribute_name(child))
    return targets


def _attribute_name(node: ast.Attribute) -> str:
    parts = [node.attr]
    value = node.value
    while isinstance(value, ast.Attribute):
        parts.append(value.attr)
        value = value.value
    if isinstance(value, ast.Name):
        parts.append(value.id)
    return ".".join(reversed(parts))
