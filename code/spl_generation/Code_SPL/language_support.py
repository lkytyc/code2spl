import ast
import json
import re
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple


PYTHON_EXTENSIONS = {".py"}
JAVA_EXTENSIONS = {".java"}
CPP_EXTENSIONS = {".c", ".cc", ".cpp", ".cxx", ".h", ".hh", ".hpp", ".hxx"}
SUPPORTED_SOURCE_PATTERNS = (
    "*.py",
    "*.java",
    "*.c",
    "*.cc",
    "*.cpp",
    "*.cxx",
    "*.h",
    "*.hh",
    "*.hpp",
    "*.hxx",
)


def detect_language(path_like: Any) -> str:
    suffix = Path(str(path_like)).suffix.lower()
    if suffix in PYTHON_EXTENSIONS:
        return "python"
    if suffix in JAVA_EXTENSIONS:
        return "java"
    if suffix in CPP_EXTENSIONS:
        return "cpp"
    return "text"


def iter_source_files(code_dir: Path) -> List[Path]:
    files: List[Path] = []
    seen = set()
    for pattern in SUPPORTED_SOURCE_PATTERNS:
        for file_path in code_dir.glob(pattern):
            key = str(file_path.resolve())
            if key in seen:
                continue
            seen.add(key)
            files.append(file_path)
    return sorted(files, key=lambda item: item.name.lower())


def extract_source_members(file_path: Path) -> Tuple[Dict[str, List[Dict[str, Any]]], List[Dict[str, Any]]]:
    language = detect_language(file_path)
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    if language == "python":
        return _extract_python_members(content)
    if language in {"java", "cpp"}:
        return _extract_brace_members(content, language)
    return {}, []


def analyze_source_file(file_path: Path) -> Dict[str, Any]:
    language = detect_language(file_path)
    if language == "python":
        return _analyze_python_file(file_path)

    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    classes, global_methods = _extract_brace_members(content, language)
    class_map: Dict[str, Dict[str, Any]] = {}
    for class_name, methods in classes.items():
        class_map[class_name] = {
            "name": class_name,
            "lineno": methods[0]["lineno"] if methods else 1,
            "bases": [],
            "methods": [analyze_specific_method_ast(method["code"], method["name"], language, class_name)["ast_analysis"] for method in methods],
            "class_variables": [],
            "decorators": [],
            "language": language,
        }

    analyzed_globals = [
        analyze_specific_method_ast(method["code"], method["name"], language).get("ast_analysis", {})
        for method in global_methods
    ]

    return {
        "file_name": file_path.name,
        "file_path": str(file_path),
        "content_length": len(content),
        "language": language,
        "classes": class_map,
        "global_functions": analyzed_globals,
        "imports": _extract_imports(content, language),
        "global_variables": [],
        "ast_structure": _build_file_structure(class_map, analyzed_globals, language),
    }


def analyze_specific_method_ast(
    method_code: str,
    method_name: str = "unknown_method",
    language: str = "python",
    class_name: Optional[str] = None,
) -> Dict[str, Any]:
    if language == "python":
        info = _analyze_python_method(method_code, method_name)
        return {
            "method_name": method_name,
            "language": language,
            "code": method_code,
            "ast_analysis": info,
            "raw_ast": info.get("ast_structure", {}),
        }

    info = _analyze_brace_method(method_code, method_name, language, class_name)
    return {
        "method_name": method_name,
        "language": language,
        "code": method_code,
        "ast_analysis": info,
        "raw_ast": info.get("ast_structure", {}),
    }


def analyze_code_structure(code: str, language: str) -> Dict[str, Any]:
    if language == "python":
        return _analyze_python_code_structure(code)
    if language in {"java", "cpp"}:
        return _analyze_brace_code_structure(code, language)
    return {
        "control_structures": [],
        "loops": [],
        "assignments": [],
        "function_calls": [],
        "returns": [],
        "switch_cases": [],
    }


def safe_json_serialize(obj: Any) -> Any:
    if isinstance(obj, (str, int, float, bool, type(None))):
        return obj
    if isinstance(obj, (list, tuple)):
        return [safe_json_serialize(item) for item in obj]
    if isinstance(obj, dict):
        return {str(key): safe_json_serialize(value) for key, value in obj.items()}
    return str(obj)


def _extract_python_members(content: str) -> Tuple[Dict[str, List[Dict[str, Any]]], List[Dict[str, Any]]]:
    try:
        tree = ast.parse(content)
    except SyntaxError:
        return {}, []

    classes: Dict[str, List[Dict[str, Any]]] = {}
    global_methods: List[Dict[str, Any]] = []

    for node in tree.body:
        if isinstance(node, ast.ClassDef):
            class_name = node.name
            classes[class_name] = []
            for item in node.body:
                if isinstance(item, ast.FunctionDef):
                    method_name = item.name
                    if not method_name.startswith("__") or method_name == "__init__":
                        classes[class_name].append(
                            {
                                "name": method_name,
                                "code": ast.get_source_segment(content, item),
                                "lineno": item.lineno,
                                "language": "python",
                            }
                        )
        elif isinstance(node, ast.FunctionDef):
            if not node.name.startswith("__"):
                global_methods.append(
                    {
                        "name": node.name,
                        "code": ast.get_source_segment(content, node),
                        "lineno": node.lineno,
                        "language": "python",
                    }
                )

    return classes, global_methods


def _analyze_python_file(file_path: Path) -> Dict[str, Any]:
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    try:
        tree = ast.parse(content)
    except SyntaxError as e:
        return {"error": str(e), "file_name": file_path.name, "file_path": str(file_path), "language": "python"}

    classes, global_methods = _extract_python_members(content)
    class_map: Dict[str, Dict[str, Any]] = {}
    for class_name, methods in classes.items():
        class_map[class_name] = {
            "name": class_name,
            "lineno": methods[0]["lineno"] if methods else 1,
            "bases": [],
            "methods": [analyze_specific_method_ast(method["code"], method["name"], "python")["ast_analysis"] for method in methods],
            "class_variables": [],
            "decorators": [],
            "language": "python",
        }

    return {
        "file_name": file_path.name,
        "file_path": str(file_path),
        "content_length": len(content),
        "language": "python",
        "classes": class_map,
        "global_functions": [
            analyze_specific_method_ast(method["code"], method["name"], "python")["ast_analysis"]
            for method in global_methods
        ],
        "imports": _extract_python_imports(tree),
        "global_variables": _extract_python_globals(tree, content),
        "ast_structure": {"type": "Module", "language": "python", "body_length": len(tree.body)},
    }


def _extract_python_imports(tree: ast.AST) -> List[Dict[str, Any]]:
    imports: List[Dict[str, Any]] = []
    for node in getattr(tree, "body", []):
        if isinstance(node, ast.Import):
            for alias in node.names:
                imports.append(
                    {
                        "type": "import",
                        "module": alias.name,
                        "alias": alias.asname,
                        "lineno": node.lineno,
                    }
                )
        elif isinstance(node, ast.ImportFrom):
            for alias in node.names:
                imports.append(
                    {
                        "type": "from_import",
                        "module": node.module,
                        "name": alias.name,
                        "alias": alias.asname,
                        "level": node.level,
                        "lineno": node.lineno,
                    }
                )
    return imports


def _extract_python_globals(tree: ast.AST, content: str) -> List[Dict[str, Any]]:
    global_vars: List[Dict[str, Any]] = []
    for node in getattr(tree, "body", []):
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name):
                    global_vars.append(
                        {
                            "name": target.id,
                            "code": ast.get_source_segment(content, node),
                            "lineno": node.lineno,
                            "type": "assignment",
                        }
                    )
    return global_vars


def _analyze_python_method(method_code: str, method_name: str) -> Dict[str, Any]:
    tree = ast.parse(method_code)
    if not tree.body or not isinstance(tree.body[0], ast.FunctionDef):
        raise ValueError("Python method code does not contain a top-level function definition")

    func_node = tree.body[0]
    return {
        "name": method_name,
        "language": "python",
        "code": method_code,
        "lineno": getattr(func_node, "lineno", 1),
        "args": {
            "args": [arg.arg for arg in func_node.args.args],
            "defaults": len(func_node.args.defaults),
            "vararg": func_node.args.vararg.arg if func_node.args.vararg else None,
            "kwarg": func_node.args.kwarg.arg if func_node.args.kwarg else None,
            "kwonlyargs": [arg.arg for arg in func_node.args.kwonlyargs],
        },
        "decorators": [],
        "returns": _python_annotation_name(getattr(func_node, "returns", None)),
        "body_analysis": _analyze_python_function_body(func_node.body, method_code),
        "ast_structure": {
            "type": "FunctionDef",
            "name": func_node.name,
            "lineno": getattr(func_node, "lineno", 1),
            "args_count": len(func_node.args.args),
            "language": "python",
        },
    }


def _python_annotation_name(annotation: Any) -> Optional[str]:
    if annotation is None:
        return None
    try:
        return ast.unparse(annotation)
    except Exception:
        return str(type(annotation).__name__)


def _analyze_python_function_body(body: List[ast.AST], content: str) -> Dict[str, Any]:
    analysis = {
        "statements_count": len(body),
        "control_structures": [],
        "loops": [],
        "assignments": [],
        "function_calls": [],
        "returns": [],
        "switch_cases": [],
    }

    for node in body:
        if isinstance(node, ast.If):
            analysis["control_structures"].append(
                {"type": "if", "lineno": node.lineno, "code": ast.get_source_segment(content, node)}
            )
        elif isinstance(node, ast.For):
            analysis["loops"].append({"type": "for", "lineno": node.lineno, "code": ast.get_source_segment(content, node)})
        elif isinstance(node, ast.While):
            analysis["loops"].append({"type": "while", "lineno": node.lineno, "code": ast.get_source_segment(content, node)})
        elif isinstance(node, ast.Assign):
            analysis["assignments"].append(
                {"type": "assignment", "lineno": node.lineno, "code": ast.get_source_segment(content, node)}
            )
        elif isinstance(node, ast.Expr) and isinstance(node.value, ast.Call):
            analysis["function_calls"].append(
                {"type": "function_call", "lineno": node.lineno, "code": ast.get_source_segment(content, node)}
            )
        elif isinstance(node, ast.Return):
            analysis["returns"].append({"type": "return", "lineno": node.lineno, "code": ast.get_source_segment(content, node)})
        elif hasattr(ast, "Match") and isinstance(node, ast.Match):
            analysis["switch_cases"].append(
                {"type": "match", "lineno": node.lineno, "code": ast.get_source_segment(content, node)}
            )

    return analysis


def _analyze_python_code_structure(code: str) -> Dict[str, Any]:
    try:
        tree = ast.parse(code)
    except Exception:
        return {
            "control_structures": [],
            "loops": [],
            "assignments": [],
            "function_calls": [],
            "returns": [],
            "switch_cases": [],
        }

    analysis = {
        "control_structures": [],
        "loops": [],
        "assignments": [],
        "function_calls": [],
        "returns": [],
        "switch_cases": [],
    }

    for node in ast.walk(tree):
        if isinstance(node, ast.If):
            analysis["control_structures"].append(
                {"type": "if", "code": ast.get_source_segment(code, node), "lineno": getattr(node, "lineno", 0)}
            )
        elif isinstance(node, ast.For):
            analysis["loops"].append(
                {"type": "for", "code": ast.get_source_segment(code, node), "lineno": getattr(node, "lineno", 0)}
            )
        elif isinstance(node, ast.While):
            analysis["loops"].append(
                {"type": "while", "code": ast.get_source_segment(code, node), "lineno": getattr(node, "lineno", 0)}
            )
        elif isinstance(node, ast.Assign):
            analysis["assignments"].append(
                {"type": "assignment", "code": ast.get_source_segment(code, node), "lineno": getattr(node, "lineno", 0)}
            )
        elif isinstance(node, ast.Expr) and isinstance(node.value, ast.Call):
            analysis["function_calls"].append(
                {"type": "function_call", "code": ast.get_source_segment(code, node), "lineno": getattr(node, "lineno", 0)}
            )
        elif isinstance(node, ast.Return):
            analysis["returns"].append(
                {"type": "return", "code": ast.get_source_segment(code, node), "lineno": getattr(node, "lineno", 0)}
            )
        elif hasattr(ast, "Match") and isinstance(node, ast.Match):
            analysis["switch_cases"].append(
                {"type": "match", "code": ast.get_source_segment(code, node), "lineno": getattr(node, "lineno", 0)}
            )

    return analysis


def _extract_brace_members(content: str, language: str) -> Tuple[Dict[str, List[Dict[str, Any]]], List[Dict[str, Any]]]:
    masked = _mask_c_like_content(content)
    class_entries = _extract_class_entries(content, masked, language)
    function_entries = _extract_function_entries(content, masked)

    classes: Dict[str, List[Dict[str, Any]]] = {entry["name"]: [] for entry in class_entries}
    global_methods: List[Dict[str, Any]] = []

    for function in function_entries:
        owning_class = _resolve_function_class(function, class_entries)
        record = {
            "name": function["name"],
            "code": function["code"],
            "lineno": function["lineno"],
            "signature": function["signature"],
            "language": language,
        }
        if owning_class:
            classes.setdefault(owning_class, []).append(record)
        else:
            global_methods.append(record)

    return classes, global_methods


def _extract_imports(content: str, language: str) -> List[Dict[str, Any]]:
    imports: List[Dict[str, Any]] = []
    for lineno, line in enumerate(content.splitlines(), start=1):
        stripped = line.strip()
        if language == "java":
            if stripped.startswith("package "):
                imports.append({"type": "package", "module": stripped[8:].rstrip(";"), "lineno": lineno})
            elif stripped.startswith("import "):
                imports.append({"type": "import", "module": stripped[7:].rstrip(";"), "lineno": lineno})
        elif language == "cpp":
            if stripped.startswith("#include"):
                imports.append({"type": "include", "module": stripped[8:].strip(), "lineno": lineno})
            elif stripped.startswith("using "):
                imports.append({"type": "using", "module": stripped.rstrip(";"), "lineno": lineno})
    return imports


def _build_file_structure(
    classes: Dict[str, Dict[str, Any]],
    global_functions: List[Dict[str, Any]],
    language: str,
) -> Dict[str, Any]:
    return {
        "type": "SourceFile",
        "language": language,
        "classes": [
            {"name": class_name, "methods_count": len(info.get("methods", []))}
            for class_name, info in classes.items()
        ],
        "global_functions": [func.get("name") for func in global_functions],
    }


def _analyze_brace_method(
    method_code: str,
    method_name: str,
    language: str,
    class_name: Optional[str] = None,
) -> Dict[str, Any]:
    masked = _mask_c_like_content(method_code)
    entries = _extract_function_entries(method_code, masked)
    entry = entries[0] if entries else None

    if entry is None:
        signature = method_name
        args = {"args": [], "defaults": 0, "vararg": None, "kwarg": None, "kwonlyargs": []}
        body_analysis = _analyze_brace_code_structure(method_code, language)
        lineno = 1
    else:
        signature = entry["signature"]
        args = _parse_brace_arguments(signature)
        body_analysis = _analyze_brace_code_structure(entry["code"], language)
        lineno = entry["lineno"]
        class_name = class_name or entry.get("class_name")

    return {
        "name": method_name,
        "language": language,
        "code": method_code,
        "lineno": lineno,
        "signature": signature,
        "args": args,
        "decorators": [],
        "returns": _extract_return_type(signature, method_name, class_name),
        "body_analysis": body_analysis,
        "ast_structure": {
            "type": "MethodDeclaration" if class_name else "FunctionDeclaration",
            "name": method_name,
            "class_name": class_name,
            "signature": signature,
            "lineno": lineno,
            "language": language,
        },
    }


def _parse_brace_arguments(signature: str) -> Dict[str, Any]:
    open_paren = signature.find("(")
    close_paren = signature.rfind(")")
    if open_paren == -1 or close_paren == -1 or close_paren < open_paren:
        return {"args": [], "defaults": 0, "vararg": None, "kwarg": None, "kwonlyargs": []}

    raw_args = signature[open_paren + 1 : close_paren].strip()
    if not raw_args or raw_args == "void":
        return {"args": [], "defaults": 0, "vararg": None, "kwarg": None, "kwonlyargs": []}

    args: List[str] = []
    defaults = 0
    vararg = None

    for part in _split_arguments(raw_args):
        clean = part.strip()
        if not clean:
            continue
        if "=" in clean:
            defaults += 1
            clean = clean.split("=", 1)[0].strip()
        name = _extract_argument_name(clean)
        if "..." in clean:
            vararg = name
        args.append(name)

    return {"args": args, "defaults": defaults, "vararg": vararg, "kwarg": None, "kwonlyargs": []}


def _split_arguments(raw_args: str) -> List[str]:
    parts: List[str] = []
    start = 0
    angle = 0
    paren = 0
    bracket = 0
    for idx, char in enumerate(raw_args):
        if char == "<":
            angle += 1
        elif char == ">":
            angle = max(0, angle - 1)
        elif char == "(":
            paren += 1
        elif char == ")":
            paren = max(0, paren - 1)
        elif char == "[":
            bracket += 1
        elif char == "]":
            bracket = max(0, bracket - 1)
        elif char == "," and angle == 0 and paren == 0 and bracket == 0:
            parts.append(raw_args[start:idx])
            start = idx + 1
    parts.append(raw_args[start:])
    return parts


def _extract_argument_name(argument: str) -> str:
    candidate = argument.replace("&", " ").replace("*", " ").replace("...", " ")
    tokens = [token for token in re.split(r"\s+", candidate.strip()) if token]
    if not tokens:
        return "arg"
    last = tokens[-1]
    last = last.split("[", 1)[0]
    return last or "arg"


def _extract_return_type(signature: str, method_name: str, class_name: Optional[str]) -> Optional[str]:
    prefix = signature[: signature.find("(")].strip()
    if not prefix:
        return None

    token_match = re.search(r"([~A-Za-z_][\w:]*)\s*$", prefix)
    if not token_match:
        return None

    token = token_match.group(1)
    scoped_name = token.split("::")[-1]
    if scoped_name == method_name and class_name and method_name in {class_name, f"~{class_name}"}:
        return None

    return _clean_return_type(prefix[: token_match.start()].strip()) or None


def _clean_return_type(return_type: str) -> str:
    modifiers = {
        "public",
        "protected",
        "private",
        "static",
        "final",
        "abstract",
        "synchronized",
        "native",
        "strictfp",
        "inline",
        "virtual",
        "constexpr",
        "consteval",
        "constinit",
        "extern",
        "friend",
        "explicit",
        "typename",
    }
    tokens = [token for token in return_type.split() if token not in modifiers]
    return " ".join(tokens)


def _analyze_brace_code_structure(code: str, language: str) -> Dict[str, Any]:
    body_text, base_lineno = _extract_body_text(code)
    if body_text is None:
        body_text = code
        base_lineno = 1

    analysis = {
        "statements_count": 0,
        "control_structures": [],
        "loops": [],
        "assignments": [],
        "function_calls": [],
        "returns": [],
        "switch_cases": [],
    }

    masked = _mask_c_like_content(body_text)
    pos = 0
    while pos < len(masked):
        pos = _skip_whitespace(masked, pos)
        if pos >= len(masked):
            break

        statement, next_pos = _consume_brace_statement(body_text, masked, pos)
        if not statement.strip():
            pos = max(next_pos, pos + 1)
            continue

        lineno = base_lineno + body_text.count("\n", 0, pos)
        stripped = statement.strip()
        lowered = stripped.lower()
        analysis["statements_count"] += 1

        if lowered.startswith("if ") or lowered.startswith("if(") or lowered.startswith("else if"):
            analysis["control_structures"].append({"type": "if", "lineno": lineno, "code": stripped})
        elif lowered.startswith("for ") or lowered.startswith("for("):
            analysis["loops"].append({"type": "for", "lineno": lineno, "code": stripped})
        elif lowered.startswith("while ") or lowered.startswith("while("):
            analysis["loops"].append({"type": "while", "lineno": lineno, "code": stripped})
        elif lowered.startswith("do"):
            analysis["loops"].append({"type": "do", "lineno": lineno, "code": stripped})
        elif lowered.startswith("switch ") or lowered.startswith("switch("):
            analysis["switch_cases"].append({"type": "switch", "lineno": lineno, "code": stripped})
        elif lowered.startswith("return"):
            analysis["returns"].append({"type": "return", "lineno": lineno, "code": stripped})
        elif _looks_like_assignment(stripped):
            analysis["assignments"].append({"type": "assignment", "lineno": lineno, "code": stripped})
        elif _looks_like_function_call(stripped, language):
            analysis["function_calls"].append({"type": "function_call", "lineno": lineno, "code": stripped})

        pos = max(next_pos, pos + 1)

    return analysis


def _looks_like_assignment(statement: str) -> bool:
    if statement.endswith(":"):
        return False
    compact = statement.replace("==", "").replace("!=", "").replace(">=", "").replace("<=", "")
    compact = compact.replace("=>", "")
    return "=" in compact


def _looks_like_function_call(statement: str, language: str) -> bool:
    stripped = statement.strip().rstrip(";")
    if not stripped or stripped.startswith(("if", "for", "while", "switch", "catch", "return", "delete", "new ")):
        return False
    if "=" in stripped and not re.search(r"\w+\s*\([^)]*\)\s*$", stripped):
        return False
    return bool(re.search(r"[A-Za-z_~][\w:<>]*\s*(?:\.|->|::)?\s*[A-Za-z_~]?[\w<>]*\s*\([^;]*\)$", stripped))


def _extract_body_text(code: str) -> Tuple[Optional[str], int]:
    masked = _mask_c_like_content(code)
    open_brace = masked.find("{")
    if open_brace == -1:
        return None, 1
    close_brace = _find_matching_brace(masked, open_brace)
    if close_brace == -1:
        return None, 1
    return code[open_brace + 1 : close_brace], code.count("\n", 0, open_brace) + 2


def _consume_brace_statement(body_text: str, masked: str, start: int) -> Tuple[str, int]:
    depth = 0
    idx = start
    while idx < len(masked):
        char = masked[idx]
        if char == "{":
            if depth == 0:
                end = _find_matching_brace(masked, idx)
                if end == -1:
                    return body_text[start:], len(masked)
                idx = end + 1
                while idx < len(masked) and masked[idx].isspace():
                    idx += 1
                if body_text[start:idx].strip().startswith("if") and body_text[idx: idx + 4].strip().startswith("else"):
                    continue
                if body_text[start:idx].strip().startswith("do"):
                    while idx < len(masked) and masked[idx].isspace():
                        idx += 1
                    if masked[idx: idx + 5].startswith("while"):
                        while idx < len(masked) and masked[idx] != ";":
                            idx += 1
                        if idx < len(masked):
                            idx += 1
                return body_text[start:idx], idx
            depth += 1
        elif char == "}":
            depth = max(0, depth - 1)
        elif char == ";" and depth == 0:
            return body_text[start : idx + 1], idx + 1
        idx += 1
    return body_text[start:], len(masked)


def _skip_whitespace(text: str, start: int) -> int:
    idx = start
    while idx < len(text) and text[idx].isspace():
        idx += 1
    return idx


def _mask_c_like_content(content: str) -> str:
    chars: List[str] = []
    idx = 0
    state = "code"
    quote = ""

    while idx < len(content):
        char = content[idx]
        nxt = content[idx + 1] if idx + 1 < len(content) else ""

        if state == "code":
            if char == "/" and nxt == "/":
                chars.extend([" ", " "])
                idx += 2
                state = "line_comment"
                continue
            if char == "/" and nxt == "*":
                chars.extend([" ", " "])
                idx += 2
                state = "block_comment"
                continue
            if char in {'"', "'"}:
                quote = char
                chars.append(char)
                idx += 1
                state = "string"
                continue
            chars.append(char)
            idx += 1
            continue

        if state == "line_comment":
            chars.append("\n" if char == "\n" else " ")
            idx += 1
            if char == "\n":
                state = "code"
            continue

        if state == "block_comment":
            if char == "*" and nxt == "/":
                chars.extend([" ", " "])
                idx += 2
                state = "code"
            else:
                chars.append("\n" if char == "\n" else " ")
                idx += 1
            continue

        if state == "string":
            if char == "\\":
                chars.append(" ")
                if idx + 1 < len(content):
                    chars.append(" " if content[idx + 1] != "\n" else "\n")
                    idx += 2
                else:
                    idx += 1
            elif char == quote:
                chars.append(char)
                idx += 1
                state = "code"
            else:
                chars.append("\n" if char == "\n" else " ")
                idx += 1

    return "".join(chars)


def _extract_class_entries(content: str, masked: str, language: str) -> List[Dict[str, Any]]:
    if language == "java":
        pattern = re.compile(
            r"\b(?:public|protected|private|abstract|final|static\s+)*"
            r"(?:class|interface|enum)\s+([A-Za-z_]\w*)[^{;]*\{"
        )
    else:
        pattern = re.compile(
            r"\b(?:template\s*<[^;{]+>\s*)?(?:class|struct)\s+([A-Za-z_]\w*)[^;{]*\{"
        )

    classes: List[Dict[str, Any]] = []
    for match in pattern.finditer(masked):
        open_brace = masked.find("{", match.start(), match.end())
        if open_brace == -1:
            continue
        close_brace = _find_matching_brace(masked, open_brace)
        if close_brace == -1:
            continue
        code_end = close_brace + 1
        if language == "cpp":
            temp = code_end
            while temp < len(masked) and masked[temp].isspace():
                temp += 1
            if temp < len(masked) and masked[temp] == ";":
                code_end = temp + 1
        classes.append(
            {
                "name": match.group(1),
                "start": match.start(),
                "body_start": open_brace + 1,
                "body_end": close_brace,
                "end": code_end,
                "lineno": content.count("\n", 0, match.start()) + 1,
                "code": content[match.start() : code_end],
            }
        )
    return classes


def _extract_function_entries(content: str, masked: str) -> List[Dict[str, Any]]:
    functions: List[Dict[str, Any]] = []
    idx = 0

    while idx < len(masked):
        if masked[idx] != "{":
            idx += 1
            continue

        header_start = max(masked.rfind(";", 0, idx), masked.rfind("}", 0, idx), masked.rfind("{", 0, idx)) + 1
        header_start = _skip_access_label(content, header_start, idx)
        header = content[header_start:idx]
        signature_info = _parse_function_header(header)
        if signature_info is None:
            idx += 1
            continue

        close_brace = _find_matching_brace(masked, idx)
        if close_brace == -1:
            idx += 1
            continue

        code_start = _expand_function_start(content, header_start)
        code = content[code_start : close_brace + 1]
        functions.append(
            {
                "name": signature_info["name"],
                "class_name": signature_info.get("class_name"),
                "signature": signature_info["signature"],
                "lineno": content.count("\n", 0, code_start) + 1,
                "start": code_start,
                "end": close_brace + 1,
                "code": code,
            }
        )
        idx = close_brace + 1

    return functions


def _skip_access_label(content: str, start: int, end: int) -> int:
    prefix = content[start:end]
    match = re.match(r"\s*(?:public|private|protected)\s*:\s*", prefix)
    if not match:
        return start
    return start + match.end()


def _parse_function_header(header: str) -> Optional[Dict[str, Any]]:
    signature = " ".join(header.replace("\n", " ").split())
    if not signature or "(" not in signature or ")" not in signature:
        return None

    prefix = signature[: signature.rfind("(")].strip()
    if not prefix:
        return None

    first_word_match = re.match(r"[A-Za-z_~]+", prefix)
    first_word = first_word_match.group(0).lower() if first_word_match else ""
    if first_word in {"if", "for", "while", "switch", "catch", "else", "do", "try", "synchronized"}:
        return None

    token_match = re.search(r"([~A-Za-z_][\w:]*)\s*$", prefix)
    if not token_match:
        return None

    token = token_match.group(1)
    parts = token.split("::")
    method_name = parts[-1]
    if method_name.lower() in {"if", "for", "while", "switch", "catch", "else", "return", "new", "delete"}:
        return None

    class_name = parts[-2] if len(parts) > 1 else None
    return {"name": method_name, "class_name": class_name, "signature": signature}


def _expand_function_start(content: str, start: int) -> int:
    current = start
    while current > 0:
        previous_break = content.rfind("\n", 0, current - 1)
        if previous_break == -1:
            break
        previous_line = content[previous_break + 1 : current].strip()
        if previous_line.startswith("@"):
            current = previous_break + 1
            continue
        break
    return current


def _resolve_function_class(function: Dict[str, Any], class_entries: List[Dict[str, Any]]) -> Optional[str]:
    if function.get("class_name"):
        return function["class_name"]

    for entry in class_entries:
        if entry["body_start"] <= function["start"] <= entry["body_end"]:
            return entry["name"]
    return None


def _find_matching_brace(masked: str, open_brace: int) -> int:
    depth = 0
    for idx in range(open_brace, len(masked)):
        if masked[idx] == "{":
            depth += 1
        elif masked[idx] == "}":
            depth -= 1
            if depth == 0:
                return idx
    return -1
