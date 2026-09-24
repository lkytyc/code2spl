from __future__ import annotations

import os
import shutil
from pathlib import Path

from .paths import PROJECT_ROOT


PROJECT_ENV_ROOT = PROJECT_ROOT / "tools" / "experiment-env"


def project_env_path_entries() -> list[Path]:
    return [
        PROJECT_ROOT / "tools" / "bin",
        PROJECT_ROOT / "datasets" / "defects4j" / "defects4j-master" / "major" / "bin",
        PROJECT_ENV_ROOT,
        PROJECT_ENV_ROOT / "Library" / "bin",
        PROJECT_ENV_ROOT / "Library" / "usr" / "bin",
        PROJECT_ENV_ROOT / "Scripts",
        PROJECT_ENV_ROOT / "bin",
    ]


_PROJECT_ENV_INITIALIZED = False


def _append_env_option(name: str, option: str) -> None:
    current = os.environ.get(name, "")
    parts = current.split()
    if option not in parts:
        os.environ[name] = " ".join([current, option]).strip()


def prepend_project_env_to_path() -> None:
    global _PROJECT_ENV_INITIALIZED
    entries = [str(path) for path in project_env_path_entries() if path.exists()]
    if not entries:
        return
    if not _PROJECT_ENV_INITIALIZED:
        current = os.environ.get("PATH", "")
        os.environ["PATH"] = os.pathsep.join(entries + [current])
        perl_lib = PROJECT_ROOT / "tools" / "perl5" / "lib" / "perl5"
        if perl_lib.exists():
            current_perl5lib = os.environ.get("PERL5LIB", "")
            os.environ["PERL5LIB"] = os.pathsep.join([str(perl_lib), current_perl5lib])
        _PROJECT_ENV_INITIALIZED = True
    os.environ.setdefault("JAVA_HOME", str(PROJECT_ENV_ROOT / "Library"))
    os.environ.setdefault("CONDA_PREFIX", str(PROJECT_ENV_ROOT))
    os.environ.setdefault("ANT_HOME", str(PROJECT_ROOT / "datasets" / "defects4j" / "defects4j-master" / "major"))
    os.environ.setdefault("GIT_CONFIG_GLOBAL", str(PROJECT_ROOT / "tools" / "gitconfig"))
    os.environ.setdefault("PYTHONUTF8", "1")
    os.environ.setdefault("TZ", "America/Los_Angeles")
    if os.name != "nt":
        os.environ.setdefault("LANG", "C.UTF-8")
        os.environ.setdefault("LC_ALL", "C.UTF-8")
    _append_env_option("JAVA_TOOL_OPTIONS", "-Dfile.encoding=UTF-8")
    _append_env_option("ANT_OPTS", "-Dfile.encoding=UTF-8")
    _append_env_option("MAVEN_OPTS", "-Dfile.encoding=UTF-8")


def find_executable(name: str) -> str | None:
    prepend_project_env_to_path()
    found = shutil.which(name)
    if found:
        return found
    candidates = []
    for root in project_env_path_entries():
        candidates.extend([root / name, root / f"{name}.exe", root / f"{name}.bat", root / f"{name}.cmd"])
    for candidate in candidates:
        if candidate.exists():
            return str(candidate)
    return None
