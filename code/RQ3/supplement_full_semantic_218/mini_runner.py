from __future__ import annotations

import argparse
import faulthandler
import json
import os
import subprocess
import sys
import traceback
from datetime import datetime, timezone
from pathlib import Path

import yaml


def load_jsonl_first(path: Path) -> dict:
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        if line.strip():
            return json.loads(line)
    raise ValueError(f"No JSONL records found in {path}")


def write_progress(path: Path, message: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now(timezone.utc).isoformat()
    with path.open("a", encoding="utf-8") as f:
        f.write(f"{timestamp} {message}\n")
    print(f"[mini_runner] {message}", flush=True)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mini-src", required=True)
    parser.add_argument("--mini-config", required=True)
    parser.add_argument("--instance-jsonl", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--tool-dir", default="")
    args = parser.parse_args()

    sys.path.insert(0, str(Path(args.mini_src).resolve()))

    from minisweagent.agents import get_agent
    from minisweagent.models import get_model
    from minisweagent.run.benchmarks.swebench import get_sb_environment

    config_path = Path(args.mini_config)
    instance_path = Path(args.instance_jsonl)
    output_path = Path(args.output)
    progress_path = output_path.with_suffix(".progress.log")
    faulthandler.dump_traceback_later(120, repeat=True, file=sys.stderr)
    write_progress(progress_path, "load_config_start")
    config = yaml.safe_load(config_path.read_text(encoding="utf-8"))
    config.setdefault("agent", {})["output_path"] = str(output_path)
    write_progress(progress_path, "load_instance_start")
    instance = load_jsonl_first(instance_path)
    write_progress(progress_path, f"instance_loaded {instance.get('instance_id')}")

    agent = None
    env = None
    exit_status = ""
    result = ""
    extra_info: dict = {}
    try:
        write_progress(progress_path, "environment_start")
        env = get_sb_environment(config, instance)
        write_progress(progress_path, "environment_ready")
        tool_dir = Path(args.tool_dir).resolve() if args.tool_dir else None
        if tool_dir and tool_dir.exists():
            container_id = getattr(env, "container_id", "")
            docker_executable = getattr(getattr(env, "config", None), "executable", "docker")
            if not container_id:
                raise RuntimeError("Cannot copy mini auxiliary tools: Docker container id is unavailable")
            write_progress(progress_path, f"copy_tool_dir_start {tool_dir}")
            subprocess.run([docker_executable, "exec", container_id, "mkdir", "-p", "/tmp/spl_tools"], check=True)
            subprocess.run([docker_executable, "cp", str(tool_dir) + "/.", f"{container_id}:/tmp/spl_tools"], check=True)
            env.execute({"command": "chmod -R a+r /tmp/spl_tools && chmod +x /tmp/spl_tools/*.py 2>/dev/null || true"})
            write_progress(progress_path, "copy_tool_dir_done")
        write_progress(progress_path, "agent_start")
        agent = get_agent(
            get_model(config=config.get("model", {})),
            env,
            config.get("agent", {}),
            default_type="default",
        )
        write_progress(progress_path, "agent_ready")
        write_progress(progress_path, "agent_run_start")
        info = agent.run(instance["problem_statement"])
        write_progress(progress_path, "agent_run_done")
        exit_status = str(info.get("exit_status") or "")
        result = str(info.get("submission") or "")
    except Exception as exc:
        exit_status = type(exc).__name__
        extra_info = {
            "traceback": traceback.format_exc(),
            "exception_str": str(exc),
        }
        write_progress(progress_path, f"exception {type(exc).__name__}: {exc}")
        raise
    finally:
        faulthandler.cancel_dump_traceback_later()
        output_path.parent.mkdir(parents=True, exist_ok=True)
        if agent is not None:
            write_progress(progress_path, "save_trajectory_start")
            agent.save(
                output_path,
                {
                    "info": {
                        "exit_status": exit_status,
                        "submission": result,
                        **extra_info,
                    },
                    "instance_id": instance.get("instance_id"),
                },
            )
            write_progress(progress_path, "save_trajectory_done")
        if env is not None:
            write_progress(progress_path, "environment_cleanup_start")
            env.cleanup()
            write_progress(progress_path, "environment_cleanup_done")
            if os.name == "nt":
                write_progress(progress_path, "docker_wsl_cache_reclaim_start")
                try:
                    subprocess.run(
                        [
                            "wsl",
                            "-d",
                            "docker-desktop",
                            "-u",
                            "root",
                            "--",
                            "sh",
                            "-lc",
                            "sync; echo 3 > /proc/sys/vm/drop_caches",
                        ],
                        stdout=subprocess.DEVNULL,
                        stderr=subprocess.DEVNULL,
                        timeout=30,
                        check=False,
                    )
                except (OSError, subprocess.TimeoutExpired):
                    write_progress(progress_path, "docker_wsl_cache_reclaim_failed")
                write_progress(progress_path, "docker_wsl_cache_reclaim_done")


if __name__ == "__main__":
    main()
