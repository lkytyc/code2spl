"""Load the package's ``.env`` file and expose it as a settings layer.

The harness reads three kinds of setting, in increasing order of precedence:

1. the defaults baked into the shipped config files under ``data/*/settings/``,
2. the process environment, and
3. a ``.env`` file in the package root.

This module is what makes (3) work.  It is deliberately the first thing every
entry point imports, and it is what the provider layer consults when a config
leaves a model, a base URL or a key unset — so a reader can point the whole
package at their own endpoint by copying ``code/.env.example`` to ``.env`` and
filling it in, without touching a single config file.

Nothing here ever prints, logs or returns a secret to a caller that might
serialise it.  :func:`get` returns the value; the callers that need a key take
it straight to the HTTP client.

Environment variables
---------------------
``SPL_PROJECT_ROOT``
    Overrides the package root.  Paths written as ``$PROJECT_ROOT/...`` in the
    shipped configs are expanded against this.  Usually left unset: the root is
    the directory this file's grandparents live in.
``OPENAI_API_KEY`` / ``OPENAI_API_KEYS`` / ``OPENAI_BASE_URL``
    Endpoint credentials shared by every stage, unless a stage overrides them.
``SPL_BUILDER_*``
    The stage that *builds* SPL: one run per repository, whose output is the
    artifact every task then reads.
``SPL_TASK_*``
    The stage that *uses* SPL: one call per task, the thing the experiments
    measure.  See ``code/.env.example`` for the full list and what each one does.
"""

from __future__ import annotations

import os
from pathlib import Path

PACKAGE_ROOT = Path(__file__).resolve().parents[2]

#: The settings file lives next to the code that reads it.  A `.env` at the
#: package root is still honoured if there is one, so an existing checkout keeps
#: working.
ENV_FILE = PACKAGE_ROOT / "code" / ".env"
FALLBACK_ENV_FILE = PACKAGE_ROOT / ".env"

#: Marker used throughout the shipped configs for the package root.
ROOT_MARKER = "$PROJECT_ROOT"

_LOADED = False


def _parse(text: str) -> dict[str, str]:
    """Parse a ``.env`` file.  Blank lines and ``#`` comments are skipped.

    A value may be wrapped in single or double quotes; a double-quoted value
    may carry ``\\n`` and ``\\t`` escapes.  ``export KEY=value`` is accepted so
    the same file can be sourced by a shell.
    """
    values: dict[str, str] = {}
    for line in text.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("export "):
            line = line[len("export "):].lstrip()
        if "=" not in line:
            continue
        name, _, value = line.partition("=")
        name = name.strip()
        value = value.strip()
        if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
            quote = value[0]
            value = value[1:-1]
            if quote == '"':
                value = value.replace("\\n", "\n").replace("\\t", "\t")
        if name:
            values[name] = value
    return values


def load_env(path: str | os.PathLike[str] | None = None, override: bool = False) -> dict[str, str]:
    """Read the ``.env`` file into :data:`os.environ` and return what it held.

    Variables already present in the environment win unless ``override`` is
    set, so a shell can always take precedence over the file.  Calling this
    more than once is cheap and idempotent.
    """
    global _LOADED
    candidates = (Path(path),) if path is not None else (ENV_FILE, FALLBACK_ENV_FILE)
    target = next((candidate for candidate in candidates if candidate.is_file()), None)
    if target is None:
        return {}
    values = _parse(target.read_text(encoding="utf-8", errors="replace"))
    for name, value in values.items():
        if override or name not in os.environ:
            os.environ[name] = value
    _LOADED = True
    return values


def loaded() -> bool:
    """Whether a ``.env`` file has been read in this process."""
    return _LOADED


def get(name: str, default: str | None = None) -> str | None:
    """Return an environment value, or ``default`` when it is unset or empty."""
    value = os.environ.get(name)
    return default if value is None or value == "" else value


def get_list(name: str) -> list[str]:
    """Return a key-list variable split on commas, semicolons or newlines.

    ``OPENAI_API_KEYS`` uses this shape so several keys can be listed in one
    line, or one per line, without changing the file's format.
    """
    raw = get(name)
    if not raw:
        return []
    parts = raw.replace(";", ",").replace("\n", ",").split(",")
    return [part.strip() for part in parts if part.strip()]


def get_int(name: str, default: int | None = None) -> int | None:
    """Return an integer setting, ignoring a value that is not one."""
    raw = get(name)
    if raw is None:
        return default
    try:
        return int(float(raw))
    except ValueError:
        return default


def get_float(name: str, default: float | None = None) -> float | None:
    """Return a float setting, ignoring a value that is not one."""
    raw = get(name)
    if raw is None:
        return default
    try:
        return float(raw)
    except ValueError:
        return default


def project_root() -> Path:
    """The package root that ``$PROJECT_ROOT`` in the configs stands for."""
    override = get("SPL_PROJECT_ROOT")
    if override:
        return Path(override).expanduser().resolve()
    return PACKAGE_ROOT


def expand(value: object) -> object:
    """Replace the ``$PROJECT_ROOT`` marker in a config value with the root.

    Strings are rewritten; containers are walked so a config can carry the
    marker at any depth.  Anything else is returned unchanged.
    """
    if isinstance(value, str):
        if ROOT_MARKER not in value:
            return value
        return value.replace(ROOT_MARKER, str(project_root()))
    if isinstance(value, dict):
        return {key: expand(item) for key, item in value.items()}
    if isinstance(value, list):
        return [expand(item) for item in value]
    return value
