from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any, Iterable

try:  # imported as part of `common`
    from . import env as _env
except ImportError:  # imported as a bare module
    import env as _env  # type: ignore[no-redef]


#: The package root.  Every path in this package is written relative to it, and
#: the shipped configs say so explicitly with the marker ``$PROJECT_ROOT``;
#: `env.py` expands that marker and `resolve_in_project` applies the same rule.
PROJECT_ROOT = Path(__file__).resolve().parents[2]

#: Where the kinds of content live here.  The authoring tree had one experiment
#: root per experiment holding all of them side by side; this package splits
#: that by kind, so each of these names a directory of the package.
DATASETS_ROOT = PROJECT_ROOT / "data" / "datasets"
TOOLS_ROOT = PROJECT_ROOT / "code" / "tools"

#: Scratch the harness writes to while a run builds SPL: the temporary source
#: files handed to the AST layer, one subdirectory per generator instance.
#: Created on demand and excluded from the package (see `.gitignore`); no
#: result is read from under it.
ARTIFACTS_ROOT = PROJECT_ROOT / "work" / "artifacts"

#: The directory that has to be importable for the Code-SPL modules the SPL
#: builder calls (`language_support`, `method_analyzer`, `AST`).  The upstream
#: checkout is vendored inside the SPL construction system, at
#: `code/spl_generation/Code_SPL/`, so that is the import root.
CODE_SPL_ROOT = PROJECT_ROOT / "code" / "spl_generation" / "Code_SPL"


def resolve_in_project(*parts: str | Path) -> Path:
    """``parts`` joined under the package root, with the marker expanded.

    A config value may still carry ``$PROJECT_ROOT``; expanding it here means
    a caller can pass a config value straight through without knowing whether
    it was written as a marker path or as a relative one.
    """
    joined = _env.expand(os.path.join(*(str(part) for part in parts)))
    path = Path(joined)
    if not path.is_absolute():
        path = PROJECT_ROOT / path
    path = path.resolve()
    ensure_under_project(path)
    return path


def _normalize_path(p: Path) -> Path:
    """Strip Windows \\\\?\\ extended-length prefix so parent checks work."""
    s = str(p)
    if s.startswith("\\\\?\\"):
        return Path(s[4:])
    return p


def _open_path(p: Path) -> str:
    """Return an ``open()``-compatible path string for ``p``.

    On Windows, prefixes the extended-length ``\\\\?\\`` marker so file paths at
    or beyond the legacy ``MAX_PATH`` (260 char) limit can still be opened.
    ``resolve()`` and the parent checks above already work on these paths; only
    the underlying ``CreateFile`` call needs the prefix.
    """
    s = str(p)
    if os.name == "nt" and not s.startswith("\\\\?\\"):
        s = "\\\\?\\" + s.replace("/", "\\")
    return s


def _read_text(p: Path) -> str:
    with open(_open_path(p), "r", encoding="utf-8") as fh:
        return fh.read()


def _write_text(p: Path, text: str) -> None:
    with open(_open_path(p), "w", encoding="utf-8") as fh:
        fh.write(text)


def ensure_under_project(path: str | Path) -> Path:
    resolved = Path(path).resolve()
    resolved = _normalize_path(resolved)
    root = _normalize_path(PROJECT_ROOT.resolve())
    if resolved != root and root not in resolved.parents:
        raise ValueError(f"Refusing to access path outside project: {resolved}")
    return resolved


def ensure_dir(path: str | Path) -> Path:
    resolved = ensure_under_project(path)
    resolved.mkdir(parents=True, exist_ok=True)
    return resolved


def read_json(path: str | Path) -> Any:
    """Parse a JSON file, with any ``$PROJECT_ROOT`` inside it expanded."""
    resolved = ensure_under_project(path)
    return _env.expand(json.loads(_read_text(resolved)))


def read_config(path: str | Path) -> dict[str, Any]:
    """Parse a JSON or YAML config, expanding every ``$PROJECT_ROOT``.

    The shipped configs write their paths as ``$PROJECT_ROOT/...`` so the
    package can be unpacked anywhere.  Expanding here is the single place that
    turns those into real paths for every reader of a config.
    """
    resolved = ensure_under_project(path)
    text = _read_text(resolved)
    if resolved.suffix.lower() in {".yaml", ".yml"}:
        try:
            import yaml
        except ImportError as exc:
            raise RuntimeError("PyYAML is required to read YAML config files. Install pyyaml or use JSON config.") from exc
        data = yaml.safe_load(text) or {}
    else:
        data = json.loads(text)
    if not isinstance(data, dict):
        raise ValueError(f"Config must be a mapping/object: {resolved}")
    return _env.expand(data)


def write_json(path: str | Path, data: Any) -> None:
    resolved = ensure_under_project(path)
    ensure_dir(resolved.parent)
    _write_text(resolved, json.dumps(data, ensure_ascii=False, indent=2))


def write_text(path: str | Path, text: str) -> None:
    resolved = ensure_under_project(path)
    ensure_dir(resolved.parent)
    _write_text(resolved, text)


def write_text_new(path: str | Path, text: str) -> None:
    resolved = ensure_under_project(path)
    ensure_dir(resolved.parent)
    if os.path.exists(_open_path(resolved)):
        raise FileExistsError(f"Refusing to overwrite existing file: {resolved}")
    _write_text(resolved, text)


def iter_json_or_jsonl(path: str | Path) -> Iterable[dict[str, Any]]:
    resolved = ensure_under_project(path)
    if resolved.suffix.lower() == ".jsonl":
        for line in _read_text(resolved).splitlines():
            if line.strip():
                yield json.loads(line)
        return
    data = read_json(resolved)
    if isinstance(data, list):
        yield from data
    elif isinstance(data, dict):
        for value in data.values():
            if isinstance(value, list):
                for item in value:
                    if isinstance(item, dict):
                        yield item
            elif isinstance(value, dict):
                yield value
