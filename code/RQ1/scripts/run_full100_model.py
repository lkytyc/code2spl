from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import threading
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import psutil


ROOT = Path(__file__).resolve().parents[3]


def read(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=True, indent=2) + "\n", encoding="utf-8")


def relative(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def process_tree_rss(root_process: psutil.Process) -> int:
    total = 0
    for process in [root_process, *root_process.children(recursive=True)]:
        try:
            total += process.memory_info().rss
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass
    return total


def run_stage(stage: str, command: list[str], resource_dir: Path) -> dict[str, Any]:
    started_wall = datetime.now(timezone.utc)
    attempt_id = started_wall.strftime("%Y%m%dT%H%M%S_%fZ")
    started = time.perf_counter()
    disk_start = psutil.disk_usage(str(ROOT))
    process = subprocess.Popen(
        command,
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding="utf-8",
        errors="replace",
        env=os.environ.copy(),
    )
    root_process = psutil.Process(process.pid)
    peak_rss = 0
    peak_system_cpu_percent = 0.0
    minimum_available_memory = psutil.virtual_memory().available
    samples = 0
    stop = threading.Event()

    def monitor() -> None:
        nonlocal peak_rss, peak_system_cpu_percent, minimum_available_memory, samples
        while not stop.wait(1.0):
            try:
                peak_rss = max(peak_rss, process_tree_rss(root_process))
                peak_system_cpu_percent = max(peak_system_cpu_percent, psutil.cpu_percent(interval=None))
                minimum_available_memory = min(minimum_available_memory, psutil.virtual_memory().available)
                samples += 1
            except psutil.NoSuchProcess:
                break

    thread = threading.Thread(target=monitor, daemon=True)
    thread.start()
    stdout, stderr = process.communicate()
    stop.set()
    thread.join(timeout=2)
    elapsed = time.perf_counter() - started
    ended_wall = datetime.now(timezone.utc)
    disk_end = psutil.disk_usage(str(ROOT))
    resource_dir.mkdir(parents=True, exist_ok=True)
    attempt_dir = resource_dir / "attempts"
    attempt_dir.mkdir(parents=True, exist_ok=True)
    stdout_path = attempt_dir / f"{attempt_id}_{stage}.stdout.txt"
    stderr_path = attempt_dir / f"{attempt_id}_{stage}.stderr.txt"
    stdout_path.write_text(stdout, encoding="utf-8")
    stderr_path.write_text(stderr, encoding="utf-8")
    row = {
        "stage": stage,
        "command": command,
        "started_at": started_wall.isoformat(),
        "ended_at": ended_wall.isoformat(),
        "wall_seconds": elapsed,
        "peak_process_tree_rss_bytes": peak_rss,
        "peak_process_tree_rss_mib": peak_rss / (1024 * 1024),
        "peak_system_cpu_percent": peak_system_cpu_percent,
        "minimum_available_memory_mib": minimum_available_memory / (1024 * 1024),
        "disk_free_start_gib": disk_start.free / (1024**3),
        "disk_free_end_gib": disk_end.free / (1024**3),
        "disk_free_delta_gib": (disk_end.free - disk_start.free) / (1024**3),
        "resource_samples": samples,
        "returncode": process.returncode,
        "stdout_path": relative(stdout_path),
        "stderr_path": relative(stderr_path),
    }
    write(attempt_dir / f"{attempt_id}_{stage}.json", row)
    write(resource_dir / f"latest_{stage}.json", row)
    if process.returncode:
        raise RuntimeError(f"{stage} failed with exit code {process.returncode}; see {row['stderr_path']}")
    return row


def validate_config(config: dict[str, Any]) -> None:
    model = str(config["model"])
    if config.get("spl_model") != model or config.get("summary_model") != model:
        raise ValueError("model, spl_model, and summary_model must be identical")
    if config.get("indices") or config.get("limit") or config.get("random_sample"):
        raise ValueError("Full100 config must not contain index/range/sample limits")
    sample = read(ROOT / config["sample_ids_file"])
    if len(sample.get("sample_ids", [])) != 100:
        raise ValueError("Exp1 full run requires exactly 100 frozen sample IDs")
    artifact = Path(config["artifact_dir"]).as_posix()
    run_dir = Path(config["run_dir"]).as_posix()
    if model not in artifact or model not in run_dir:
        raise ValueError("Model name must appear in both SPL and result paths")


def main() -> int:
    parser = argparse.ArgumentParser(description="Run one isolated Exp1 full100 model pipeline.")
    parser.add_argument("--config", required=True)
    parser.add_argument("--skip-prepare", action="store_true")
    parser.add_argument("--skip-run", action="store_true")
    args = parser.parse_args()

    config_path = ROOT / args.config
    config = read(config_path)
    validate_config(config)
    run_dir = ROOT / config["run_dir"]
    resource_dir = run_dir / "resource_usage"
    stages: list[dict[str, Any]] = []
    python = sys.executable
    if not args.skip_prepare:
        stages.append(
            run_stage(
                "prepare",
                [python, str(ROOT / "code/RQ1/prepare.py"), "--config", args.config],
                resource_dir,
            )
        )
    if not args.skip_run:
        stages.append(
            run_stage(
                "generate",
                [python, str(ROOT / "code/RQ1/run.py"), "--config", args.config],
                resource_dir,
            )
        )
    stages.append(
        run_stage(
            "evaluate",
            [python, str(ROOT / "code/RQ1/evaluate.py"), "--config", args.config],
            resource_dir,
        )
    )
    summary = {
        "model": config["model"],
        "spl_model": config["spl_model"],
        "summary_model": config["summary_model"],
        "config": relative(config_path),
        "sample_count": 100,
        "stages": stages,
        "total_wall_seconds_this_invocation": sum(float(row["wall_seconds"]) for row in stages),
        "peak_process_tree_rss_mib": max(float(row["peak_process_tree_rss_mib"]) for row in stages),
        "peak_system_cpu_percent": max(float(row["peak_system_cpu_percent"]) for row in stages),
        "minimum_available_memory_mib": min(float(row["minimum_available_memory_mib"]) for row in stages),
    }
    prior_attempts = sorted((resource_dir / "attempts").glob("*.json"))
    all_attempt_rows = [read(path) for path in prior_attempts]
    summary["all_attempt_count"] = len(all_attempt_rows)
    summary["total_wall_seconds_all_attempts"] = sum(float(row.get("wall_seconds", 0)) for row in all_attempt_rows)
    write(resource_dir / "pipeline.json", summary)
    print(f"Completed {config['model']} Exp1 full100 pipeline: {relative(run_dir)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
