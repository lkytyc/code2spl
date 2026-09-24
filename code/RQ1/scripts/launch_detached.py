from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]


def main() -> int:
    parser = argparse.ArgumentParser(description="Launch an Exp1 runner outside the caller console group.")
    parser.add_argument("--config", required=True)
    parser.add_argument("--skip-prepare", action="store_true")
    parser.add_argument("--skip-run", action="store_true")
    args = parser.parse_args()

    config_path = ROOT / args.config
    config = json.loads(config_path.read_text(encoding="utf-8"))
    run_dir = ROOT / config["run_dir"]
    guardian_dir = run_dir / "guardian"
    guardian_dir.mkdir(parents=True, exist_ok=True)
    stdout_path = guardian_dir / "detached.stdout.txt"
    stderr_path = guardian_dir / "detached.stderr.txt"

    command = [
        sys.executable,
        str(ROOT / "code/RQ1/scripts/run_full100_model.py"),
        "--config",
        args.config,
    ]
    if args.skip_prepare:
        command.append("--skip-prepare")
    if args.skip_run:
        command.append("--skip-run")

    creation_flags = 0
    if os.name == "nt":
        creation_flags = subprocess.DETACHED_PROCESS | subprocess.CREATE_NEW_PROCESS_GROUP

    with stdout_path.open("ab") as stdout, stderr_path.open("ab") as stderr:
        process = subprocess.Popen(
            command,
            cwd=ROOT,
            stdin=subprocess.DEVNULL,
            stdout=stdout,
            stderr=stderr,
            creationflags=creation_flags,
            close_fds=True,
            env=os.environ.copy(),
        )

    launch = {
        "pid": process.pid,
        "started_at": datetime.now(timezone.utc).isoformat(),
        "command": command,
        "config": args.config,
        "stdout": str(stdout_path.relative_to(ROOT).as_posix()),
        "stderr": str(stderr_path.relative_to(ROOT).as_posix()),
        "windows_detached_process": os.name == "nt",
        "windows_new_process_group": os.name == "nt",
    }
    (guardian_dir / "detached_launch.json").write_text(
        json.dumps(launch, ensure_ascii=True, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(launch, ensure_ascii=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
