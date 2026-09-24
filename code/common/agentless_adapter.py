from __future__ import annotations

import json
import shlex
import subprocess
from pathlib import Path
from typing import Any

from .paths import ensure_dir, ensure_under_project


def write_agentless_handoff(
    output_dir: Path,
    *,
    bug_id: str,
    track: str,
    condition: str,
    raw_bundle: str,
    spl_bundle: str,
    allowed_methods: list[str],
) -> Path:
    output_dir = ensure_dir(output_dir)
    handoff = {
        "bug_id": bug_id,
        "track": track,
        "condition": condition,
        "input_granularity": "function_bundle",
        "agentless_stage": "repair_and_patch_validation_only",
        "skip_agentless_repo_level_localization": True,
        "allowed_methods": allowed_methods,
        "raw_bundle": raw_bundle,
        "spl_bundle": spl_bundle,
        "output_format": "unified_diff_patch",
    }
    handoff_path = output_dir / "agentless_handoff.json"
    handoff_path.write_text(json.dumps(handoff, ensure_ascii=False, indent=2), encoding="utf-8")
    return handoff_path


def run_agentless_command(command_template: str, agentless_repo: Path, handoff_path: Path, output_dir: Path) -> subprocess.CompletedProcess:
    repo = ensure_under_project(agentless_repo)
    handoff = ensure_under_project(handoff_path)
    out_dir = ensure_dir(output_dir)
    if not repo.exists():
        raise FileNotFoundError(f"Agentless repository not found: {repo}")

    command = command_template.format(
        agentless_repo=str(repo),
        handoff=str(handoff),
        handoff_path=str(handoff),
        output_dir=str(out_dir),
        out_dir=str(out_dir),
    )
    args = shlex.split(command, posix=False)
    result = subprocess.run(args, cwd=str(repo), text=True, capture_output=True, timeout=3600)
    (out_dir / "agentless_stdout.txt").write_text(result.stdout, encoding="utf-8")
    (out_dir / "agentless_stderr.txt").write_text(result.stderr, encoding="utf-8")
    return result


def find_agentless_patch(output_dir: Path) -> str | None:
    output_dir = ensure_under_project(output_dir)
    candidates = list(output_dir.rglob("*.diff")) + list(output_dir.rglob("*.patch"))
    for path in candidates:
        text = path.read_text(encoding="utf-8", errors="ignore")
        if "--- " in text and "+++ " in text and "@@" in text:
            return text
    jsonl_candidates = list(output_dir.rglob("*.jsonl"))
    for path in jsonl_candidates:
        for line in path.read_text(encoding="utf-8", errors="ignore").splitlines():
            if not line.strip():
                continue
            try:
                obj: dict[str, Any] = json.loads(line)
            except json.JSONDecodeError:
                continue
            for key in ("patch", "model_patch", "diff"):
                value = obj.get(key)
                if isinstance(value, str) and "--- " in value and "+++ " in value:
                    return value
    return None
