from __future__ import annotations

import re
from dataclasses import dataclass, asdict
from pathlib import Path

from .paths import ensure_under_project


CONTROL_KEYWORDS = {"if", "for", "while", "switch", "catch", "do", "try", "else", "synchronized"}
TYPE_KEYWORDS = {"class", "interface", "enum", "record"}


@dataclass
class JavaMethod:
    class_name: str
    signature: str
    name: str
    start_line: int
    end_line: int
    code: str
    file_path: str

    @property
    def method_id(self) -> str:
        return f"{self.class_name}::{self.signature}"

    def to_dict(self) -> dict:
        data = asdict(self)
        data["method_id"] = self.method_id
        return data


def extract_java_methods(path: str | Path) -> list[JavaMethod]:
    resolved = ensure_under_project(path)
    code = resolved.read_text(encoding="utf-8", errors="replace")
    clean = _strip_comments_and_strings(code)
    lines = code.splitlines()
    class_name = _find_class_name(clean) or resolved.stem
    methods: list[JavaMethod] = []

    brace_depth = 0
    buffer = ""
    buffer_start_line = 1
    line_number = 1

    index = 0
    while index < len(clean):
        char = clean[index]
        if char == "\n":
            line_number += 1

        if char == "{":
            candidate = buffer.strip()
            if brace_depth == 1:
                header = _extract_method_header(candidate)
                if header:
                    end_index = _find_matching_brace(clean, index)
                    if end_index != -1:
                        end_line = code[: end_index + 1].count("\n") + 1
                        method_code = "\n".join(lines[buffer_start_line - 1 : end_line])
                        signature = _normalize_signature(header)
                        name = _extract_method_name(signature)
                        if name:
                            methods.append(
                                JavaMethod(
                                    class_name=class_name,
                                    signature=signature,
                                    name=name,
                                    start_line=buffer_start_line,
                                    end_line=end_line,
                                    code=method_code,
                                    file_path=str(resolved),
                                )
                            )
            brace_depth += 1
            buffer = ""
        elif char == "}":
            brace_depth = max(0, brace_depth - 1)
            buffer = ""
        elif char == ";":
            buffer = ""
        else:
            if brace_depth <= 1:
                if not buffer.strip() and not char.isspace():
                    buffer_start_line = line_number
                buffer += char
        index += 1
    return methods


def methods_covering_lines(path: str | Path, changed_lines: set[int]) -> list[JavaMethod]:
    methods = extract_java_methods(path)
    return [method for method in methods if any(method.start_line <= line <= method.end_line for line in changed_lines)]


def _find_class_name(code: str) -> str | None:
    match = re.search(r"\bclass\s+(\w+)", code)
    return match.group(1) if match else None


def _strip_comments_and_strings(code: str) -> str:
    result: list[str] = []
    index = 0
    while index < len(code):
        chunk = code[index : index + 2]
        if chunk == "//":
            while index < len(code) and code[index] != "\n":
                result.append(" ")
                index += 1
        elif chunk == "/*":
            result.extend("  ")
            index += 2
            while index < len(code) - 1 and code[index : index + 2] != "*/":
                result.append("\n" if code[index] == "\n" else " ")
                index += 1
            if index < len(code) - 1:
                result.extend("  ")
                index += 2
        elif code[index] in {'"', "'"}:
            quote = code[index]
            result.append(" ")
            index += 1
            while index < len(code):
                char = code[index]
                if char == "\\":
                    result.extend("  ")
                    index += 2
                    continue
                result.append("\n" if char == "\n" else " ")
                index += 1
                if char == quote:
                    break
        else:
            result.append(code[index])
            index += 1
    return "".join(result)


def _extract_method_header(candidate: str) -> str | None:
    lines = [line.strip() for line in candidate.splitlines() if line.strip() and not line.strip().startswith("@")]
    if not lines:
        return None
    header = " ".join(lines)
    if "(" not in header or ")" not in header:
        return None
    if re.search(r"\b(?:class|interface|enum|record)\b", header):
        return None
    prefix = header.split("(", 1)[0].strip()
    if "=" in prefix:
        return None
    name = _extract_method_name(header)
    if not name or name in CONTROL_KEYWORDS:
        return None
    if re.search(rf"\b(?:{'|'.join(sorted(CONTROL_KEYWORDS))})\s+{re.escape(name)}$", prefix):
        return None
    return header


def _extract_method_name(header: str) -> str | None:
    match = re.search(r"([A-Za-z_]\w*)\s*\([^()]*\)\s*(?:throws\b.*)?$", header)
    return match.group(1) if match else None


def _normalize_signature(header: str) -> str:
    header = re.sub(r"\s+", " ", header.strip())
    header = re.sub(r"\s+\)", ")", header)
    header = re.sub(r"\(\s+", "(", header)
    header = re.sub(r"\s+,", ",", header)
    return header


def _find_matching_brace(code: str, open_index: int) -> int:
    depth = 0
    for index in range(open_index, len(code)):
        if code[index] == "{":
            depth += 1
        elif code[index] == "}":
            depth -= 1
            if depth == 0:
                return index
    return -1
