from __future__ import annotations

import re
import shutil
import os
import subprocess
import stat
import time
from pathlib import Path

from .paths import PROJECT_ROOT, ensure_dir, ensure_under_project
from .project_env import prepend_project_env_to_path


FAILING_TEST_PATTERN = re.compile(r"^---\s+([^:]+)(?:::(.+))?$")
_ASCII_DRIVE: str | None = None


def _needs_ascii_drive() -> bool:
    try:
        str(PROJECT_ROOT.resolve()).encode("ascii")
        return False
    except UnicodeEncodeError:
        return True


def _project_ascii_drive() -> str | None:
    """Create a stable ASCII drive alias for Windows tools that corrupt Unicode paths."""
    global _ASCII_DRIVE
    if not _needs_ascii_drive():
        return None
    if _ASCII_DRIVE and Path(_ASCII_DRIVE + "\\").exists():
        return _ASCII_DRIVE

    root = str(PROJECT_ROOT.resolve())
    existing = subprocess.run(["subst"], text=True, encoding="utf-8", errors="replace", capture_output=True)
    for line in existing.stdout.splitlines():
        if ":\\:" in line:
            continue
        match = re.match(r"^([A-Z]:)\\:\s*=>\s*(.+)$", line.strip(), flags=re.IGNORECASE)
        if match and Path(match.group(2)).resolve() == PROJECT_ROOT.resolve():
            _ASCII_DRIVE = match.group(1).upper()
            return _ASCII_DRIVE

    for letter in "ZYXWVUTSRQPONMLKJIHGFED":
        drive = f"{letter}:"
        if Path(drive + "\\").exists():
            continue
        result = subprocess.run(["subst", drive, root], text=True, encoding="utf-8", errors="replace", capture_output=True)
        if result.returncode == 0:
            _ASCII_DRIVE = drive
            return _ASCII_DRIVE
    return None


def _rewrite_project_path(value: str, drive: str | None) -> str:
    if not drive:
        return value
    root = str(PROJECT_ROOT.resolve())
    normalized_root = root.replace("/", "\\").lower()
    normalized_value = value.replace("/", "\\")
    if normalized_value.lower().startswith(normalized_root):
        suffix = normalized_value[len(root) :].lstrip("\\/")
        return drive + "\\" + suffix if suffix else drive + "\\"
    return value


def run_subprocess(args: list[str], cwd: Path | None = None, timeout: int = 600) -> subprocess.CompletedProcess:
    prepend_project_env_to_path()
    drive = _project_ascii_drive() if os.name == "nt" else None
    mapped_args = [_rewrite_project_path(str(arg), drive) for arg in args]
    mapped_cwd = Path(_rewrite_project_path(str(cwd), drive)) if cwd else None
    return subprocess.run(
        mapped_args,
        cwd=str(mapped_cwd) if mapped_cwd else None,
        text=True,
        encoding="utf-8",
        errors="replace",
        capture_output=True,
        timeout=timeout,
    )


def parse_failing_tests_text(text: str) -> dict:
    classes: list[str] = []
    methods: list[str] = []
    asserts: dict[str, int] = {}
    lines = text.splitlines()
    for index, line in enumerate(lines):
        match = FAILING_TEST_PATTERN.match(line.strip())
        if not match:
            continue
        test_class = match.group(1)
        test_method = match.group(2)
        if test_method:
            full = f"{test_class}::{test_method}"
            methods.append(full)
            if index + 1 < len(lines) and "AssertionFailedError" in lines[index + 1]:
                class_tail = test_class.split(".")[-1]
                for trace_line in lines[index + 1 :]:
                    if trace_line.startswith("--- "):
                        break
                    line_match = re.search(rf"{re.escape(class_tail)}\.java:(\d+)", trace_line)
                    if line_match:
                        asserts[full] = int(line_match.group(1))
                        break
        else:
            classes.append(test_class)
    return {"classes": classes, "methods": methods, "asserts": asserts}


def read_lines_if_exists(path: Path) -> list[str]:
    resolved = ensure_under_project(path)
    if not resolved.exists():
        return []
    return [line.strip() for line in resolved.read_text(encoding="utf-8", errors="replace").splitlines() if line.strip()]


def copy_checkout(src: Path, dst: Path) -> Path:
    source = ensure_under_project(src)
    target = ensure_under_project(dst)
    if target.exists():
        remove_tree(target)
    ensure_dir(target.parent)
    shutil.copytree(source, target)
    return target


def remove_tree(path: Path) -> None:
    """Remove a tree on Windows even when Git object files are read-only."""
    target = Path(path)
    if not target.exists():
        return

    def _make_writable(func, victim, _exc_info):
        try:
            if os.path.exists(victim):
                os.chmod(victim, stat.S_IWRITE)
            func(victim)
        except FileNotFoundError:
            return
        except OSError:
            return

    for _attempt in range(3):
        try:
            shutil.rmtree(target, onerror=_make_writable)
            return
        except FileNotFoundError:
            return
        except OSError:
            time.sleep(0.2)
    shutil.rmtree(target, ignore_errors=True)


def repair_windows_build_file_artifacts(work_dir: Path) -> list[str]:
    """Repair Defects4J build files that can be corrupted by Windows Perl tooling.

    Some Defects4J project build files are patched by the framework's dependency
    fixer. On this Windows setup, capture-group replacements may be written back
    literally (for example `${1}"1.6"`), making Ant XML invalid before any model
    patch is applied. When a `.bak` file exists, restoring it is the least
    invasive repair because Defects4J created that backup immediately before
    modifying the file.
    """
    root = Path(work_dir)
    repaired: list[str] = []
    for build_file in root.rglob("maven-build.xml"):
        try:
            text = build_file.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        needs_restore = '${1}"' in text or "source=1.6" in text or "target=1.6" in text
        backup = build_file.with_name(build_file.name + ".bak")
        if needs_restore and backup.exists():
            shutil.copy2(backup, build_file)
            text = build_file.read_text(encoding="utf-8", errors="replace")
            repaired.append(str(build_file.relative_to(root)))
        fixed = re.sub(r'((?:source|target)=)"1\.[1-5]"', r'\1"1.6"', text)
        fixed = re.sub(r'((?:maven\.compiler|maven\.compile)\.(?:source|target)\s*=\s*)1\.[1-5]', r'\g<1>1.6', fixed)
        if fixed != text:
            build_file.write_text(fixed, encoding="utf-8")
            rel = str(build_file.relative_to(root))
            if rel not in repaired:
                repaired.append(rel)
    return repaired
