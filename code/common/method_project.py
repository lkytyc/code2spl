from __future__ import annotations

import argparse
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

from common.paths import PROJECT_ROOT, ensure_dir, read_config, resolve_in_project, write_json, write_text


def parse_phases(value: str) -> list[str]:
    return [part.strip() for part in value.split(",") if part.strip()]


def default_method_run_dir(method: dict[str, Any]) -> str:
    exp_id = str(method.get("experiment_id", "experiment"))
    exp_name = str(method.get("experiment_slug", exp_id))
    name = str(method["method_name"])
    return f"work/by_method/{exp_name}/{name}"


def build_method_config(method_dir: Path, method: dict[str, Any], *, base_config_path: Path | None, run_dir: str | None) -> Path:
    base = read_config(base_config_path or resolve_in_project(method["base_config"]))
    condition = method.get("condition", method["method_name"])
    overrides = method.get("config_overrides") or {}
    if not isinstance(overrides, dict):
        raise TypeError(f"config_overrides for {method['method_name']} must be a mapping")
    base.update(overrides)
    base["conditions"] = [condition]
    base["run_dir"] = run_dir or method.get("run_dir") or default_method_run_dir(method)
    experiment_slug = str(method.get("experiment_slug", "experiment"))
    temp_dir = ensure_dir(
        resolve_in_project(f"work/method_configs/{experiment_slug}")
    )
    temp_path = temp_dir / f"{method['method_name']}.json"
    write_json(temp_path, base)
    write_json(
        method_dir / "last_resolved_config.json",
        {
            "method": method,
            "base_config": str((base_config_path or resolve_in_project(method["base_config"])).relative_to(PROJECT_ROOT)),
            "resolved_config": str(temp_path.relative_to(PROJECT_ROOT)),
            "condition": condition,
            "run_dir": base["run_dir"],
        },
    )
    return temp_path


def main(method_dir: Path) -> None:
    parser = argparse.ArgumentParser(description="Run one SPL experiment method variant as an independent method project.")
    parser.add_argument("--phase", "--phases", default="run,evaluate", help="Comma-separated phases, e.g. run,evaluate.")
    parser.add_argument("--config", help="Override the method's base config.")
    parser.add_argument("--run-dir", help="Override output run_dir for this method.")
    parser.add_argument("--dry-run", action="store_true", help="Print commands without running.")
    parser.add_argument("--continue-on-error", action="store_true", help="Continue if a phase fails.")
    args = parser.parse_args()

    method = read_config(method_dir / "method.yaml")
    phases = parse_phases(args.phase)
    base_config_path = resolve_in_project(args.config) if args.config else None
    resolved_config = build_method_config(method_dir, method, base_config_path=base_config_path, run_dir=args.run_dir)
    engine = method.get("engine", {})
    log_dir = ensure_dir(
        resolve_in_project(f"work/method_logs/{method.get('experiment_slug', 'experiment')}")
        / str(method["method_name"])
        / datetime.now().strftime("%Y%m%d_%H%M%S")
    )

    summary: list[dict[str, Any]] = []
    for phase in phases:
        script_value = engine.get(phase)
        if not script_value:
            summary.append({"phase": phase, "enabled": False, "reason": "phase_not_defined"})
            continue
        script = resolve_in_project(script_value)
        command = [sys.executable, str(script), "--config", str(resolved_config)]
        print(f"[{method['method_name']}:{phase}] {' '.join(command)}")
        row: dict[str, Any] = {
            "method": method["method_name"],
            "phase": phase,
            "script": str(script.relative_to(PROJECT_ROOT)),
            "config": str(resolved_config.relative_to(PROJECT_ROOT)),
            "command": command,
        }
        if args.dry_run:
            row["dry_run"] = True
            row["returncode"] = None
            summary.append(row)
            continue
        started = datetime.now()
        result = subprocess.run(
            command,
            cwd=str(PROJECT_ROOT),
            text=True,
            capture_output=True,
            encoding="utf-8",
            errors="replace",
        )
        row["returncode"] = result.returncode
        row["elapsed_seconds"] = (datetime.now() - started).total_seconds()
        write_text(log_dir / f"{phase}.stdout.txt", result.stdout)
        write_text(log_dir / f"{phase}.stderr.txt", result.stderr)
        summary.append(row)
        write_json(log_dir / "summary.json", summary)
        if result.returncode != 0 and not args.continue_on_error:
            print(f"Stopped at phase '{phase}'. Logs: {log_dir}", file=sys.stderr)
            raise SystemExit(result.returncode)

    write_json(log_dir / "summary.json", summary)
    print(f"Method run finished. Logs: {log_dir}")
