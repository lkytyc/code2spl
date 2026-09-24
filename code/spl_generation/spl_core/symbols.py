from __future__ import annotations

import ast
import fnmatch
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

from .hashing import sha256_text


SUPPORTED_SUFFIXES = {".py": "python", ".java": "java", ".js": "javascript", ".ts": "typescript"}
DEFAULT_EXCLUDES = {
    ".git/**",
    ".spl_index/**",
    "__pycache__/**",
    "node_modules/**",
    "venv/**",
    ".venv/**",
    "dist/**",
    "build/**",
}


@dataclass
class SourceSymbol:
    symbol_id: str
    symbol: str
    file: str
    start_line: int
    end_line: int
    language: str
    code: str
    content_hash: str
    calls: list[str]
    state_changes: list[str]
    summary_hint: str


def detect_language(path: str | Path) -> str:
    return SUPPORTED_SUFFIXES.get(Path(path).suffix.lower(), "text")


def iter_source_files(
    repository_path: str | Path,
    include_patterns: list[str] | None = None,
    exclude_patterns: list[str] | None = None,
) -> Iterable[Path]:
    root = Path(repository_path).resolve()
    includes = include_patterns or ["**/*.py", "**/*.java", "**/*.js", "**/*.ts"]
    excludes = set(DEFAULT_EXCLUDES) | set(exclude_patterns or [])
    seen: set[Path] = set()
    for pattern in includes:
        for path in root.glob(pattern):
            if not path.is_file() or path in seen:
                continue
            rel = path.relative_to(root).as_posix()
            if any(fnmatch.fnmatch(rel, excluded) for excluded in excludes):
                continue
            if detect_language(path) == "text":
                continue
            seen.add(path)
            yield path


def extract_symbols_from_file(file_path: str | Path, repository_path: str | Path) -> tuple[list[SourceSymbol], list[str]]:
    path = Path(file_path).resolve()
    root = Path(repository_path).resolve()
    rel = path.relative_to(root).as_posix()
    language = detect_language(path)
    try:
        text = path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return [], [f"Cannot decode {rel} as utf-8"]
    if language == "python":
        return _extract_python_symbols(text, rel, language), []
    return _extract_brace_symbols(text, rel, language), []


def _extract_python_symbols(text: str, rel: str, language: str) -> list[SourceSymbol]:
    try:
        tree = ast.parse(text)
    except SyntaxError:
        return []
    lines = text.splitlines()
    symbols: list[SourceSymbol] = []

    def add_function(node: ast.FunctionDef | ast.AsyncFunctionDef, owner: str | None = None) -> None:
        start = node.lineno
        end = getattr(node, "end_lineno", node.lineno)
        code = "\n".join(lines[start - 1:end])
        name = f"{owner}.{node.name}" if owner else node.name
        symbol_id = f"{rel}::{name}"
        calls: set[str] = set()
        state_changes: set[str] = set()
        for child in ast.walk(node):
            if isinstance(child, ast.Call):
                call_name = _python_call_name(child.func)
                if call_name:
                    calls.add(call_name)
            elif isinstance(child, (ast.Assign, ast.AnnAssign, ast.AugAssign)):
                targets = []
                if isinstance(child, ast.Assign):
                    targets = list(child.targets)
                else:
                    targets = [child.target]
                for target in targets:
                    target_name = _python_target_name(target)
                    if target_name and (target_name.startswith("self.") or "." in target_name):
                        state_changes.add(target_name)
        doc = ast.get_docstring(node) or ""
        symbols.append(SourceSymbol(
            symbol_id=symbol_id,
            symbol=name,
            file=rel,
            start_line=start,
            end_line=end,
            language=language,
            code=code,
            content_hash=sha256_text(code),
            calls=sorted(calls),
            state_changes=sorted(state_changes),
            summary_hint=doc.splitlines()[0].strip() if doc else _fallback_summary(name, code),
        ))

    for item in tree.body:
        if isinstance(item, ast.ClassDef):
            for child in item.body:
                if isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    add_function(child, item.name)
        elif isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef)):
            add_function(item)
    return symbols


def _python_call_name(node: ast.AST) -> str:
    if isinstance(node, ast.Name):
        return node.id
    if isinstance(node, ast.Attribute):
        prefix = _python_call_name(node.value)
        return f"{prefix}.{node.attr}" if prefix else node.attr
    return ""


def _python_target_name(node: ast.AST) -> str:
    if isinstance(node, ast.Name):
        return node.id
    if isinstance(node, ast.Attribute):
        prefix = _python_target_name(node.value)
        return f"{prefix}.{node.attr}" if prefix else node.attr
    return ""


def _extract_brace_symbols(text: str, rel: str, language: str) -> list[SourceSymbol]:
    pattern = re.compile(
        r"(?P<prefix>(?:public|private|protected|static|final|async|export|\s)+)?"
        r"(?P<name>[A-Za-z_][A-Za-z0-9_]*)\s*\([^;{}]*\)\s*\{",
        re.MULTILINE,
    )
    lines = text.splitlines()
    symbols: list[SourceSymbol] = []
    for match in pattern.finditer(text):
        name = match.group("name")
        start_idx = match.start()
        end_idx = _find_matching_brace(text, match.end() - 1)
        if end_idx <= start_idx:
            continue
        start_line = text.count("\n", 0, start_idx) + 1
        end_line = text.count("\n", 0, end_idx) + 1
        code = "\n".join(lines[start_line - 1:end_line])
        calls = sorted(set(re.findall(r"\b([A-Za-z_][A-Za-z0-9_]*)\s*\(", code)) - {name, "if", "for", "while", "switch"})
        symbol_id = f"{rel}::{name}"
        symbols.append(SourceSymbol(
            symbol_id=symbol_id,
            symbol=name,
            file=rel,
            start_line=start_line,
            end_line=end_line,
            language=language,
            code=code,
            content_hash=sha256_text(code),
            calls=calls,
            state_changes=[],
            summary_hint=_fallback_summary(name, code),
        ))
    return symbols


def _find_matching_brace(text: str, open_idx: int) -> int:
    depth = 0
    for idx in range(open_idx, len(text)):
        if text[idx] == "{":
            depth += 1
        elif text[idx] == "}":
            depth -= 1
            if depth == 0:
                return idx
    return -1


def _fallback_summary(name: str, code: str) -> str:
    tokens = re.findall(r"[A-Za-z_][A-Za-z0-9_]*", name)
    readable = " ".join(tokens) if tokens else name
    returns = "returns a value" if re.search(r"\breturn\b", code) else "performs side effects or control flow"
    return f"Current implementation of {readable} {returns}."

