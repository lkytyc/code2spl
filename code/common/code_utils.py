from __future__ import annotations

import ast
import re
import subprocess
import sys
from pathlib import Path
from typing import Any

from .paths import ensure_dir, ensure_under_project


def extract_code_block(text: str) -> str:
    """Extract the last code-fence block, robust to nested/embedded backticks."""
    opening = re.search(r"```(?:python|java|cpp|c\+\+|diff)?\s*", text, re.IGNORECASE)
    if not opening:
        return text.strip()
    rest = text[opening.end():]
    closing = rest.rfind("```")
    if closing == -1:
        return text.strip()
    return rest[:closing].strip()


def python_syntax_ok(code: str) -> tuple[bool, str]:
    try:
        ast.parse(code)
        return True, ""
    except SyntaxError as exc:
        return False, str(exc)


def run_python_test(generated_code: str, test_code: str, work_dir: Path, timeout: int = 20) -> tuple[bool, str]:
    work_dir = ensure_dir(work_dir)
    test_file = work_dir / "eval_generated.py"
    runner = "\n\nif __name__ == '__main__':\n    import unittest\n    unittest.main(verbosity=2)\n"
    test_file.write_text(generated_code + "\n\n" + test_code + runner, encoding="utf-8")
    result = subprocess.run(
        [sys.executable, str(test_file)],
        cwd=str(work_dir),
        text=True,
        capture_output=True,
        timeout=timeout,
    )
    output = (result.stdout or "") + (result.stderr or "")
    return result.returncode == 0, output[-4000:]


def has_multifunction_signal(code: str) -> bool:
    function_defs = re.findall(
        r"(?m)^\s*(?:def\s+\w+\s*\(|(?:public|private|protected|static|final|inline|virtual|\w|<|>|\*|&|\s)+\s+\w+\s*\([^;{}]*\)\s*\{)",
        code,
    )
    if len(function_defs) >= 2:
        return True
    names = re.findall(r"(?m)^\s*(?:def\s+|(?:public|private|protected|static|final|inline|virtual|\w|<|>|\*|&|\s)+\s+)(\w+)\s*\(", code)
    for name in set(names):
        if len(re.findall(rf"\b{name}\s*\(", code)) >= 2:
            return True
    return False


def load_config(path: str | Path) -> dict[str, Any]:
    import json

    resolved = ensure_under_project(path)
    return json.loads(resolved.read_text(encoding="utf-8"))
