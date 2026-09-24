from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
EXPERIMENTS_ROOT = ROOT / "code"
if str(EXPERIMENTS_ROOT) not in sys.path:
    sys.path.insert(0, str(EXPERIMENTS_ROOT))

from common.spl_snapshot import (  # noqa: E402
    build_snapshot_manifest,
    sample_snapshot_dir,
    verify_sample_snapshot,
)


DEFAULT_PLAN = (
    ROOT
    / "runs"
    / "deepseek"
    / "exp6_random218_first50_20260729"
    / "plan"
    / "pipeline_plan.json"
)
SPL_CONDITIONS = (
    "miniswe_spl_localization",
    "miniswe_spl_repair",
    "miniswe_spl_both",
)
ALL_CONDITIONS = (
    "miniswe_original",
    "miniswe_free_summary",
    *SPL_CONDITIONS,
)
IMAGE_RE = re.compile(
    r"(?:docker\.io/)?(swebench/sweb\.eval\.[^\s'\"()]+:latest)",
    re.IGNORECASE,
)
MIRROR_PREFIXES = ("", "docker.1ms.run/", "docker.m.daocloud.io/")


def read_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8", errors="replace"))


def write_json(path: Path, data) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(data, ensure_ascii=True, indent=2) + "\n",
        encoding="utf-8",
    )


def resolve(value: str | Path) -> Path:
    path = Path(value)
    return path if path.is_absolute() else ROOT / path


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def disk_free_gb() -> float:
    return shutil.disk_usage(ROOT).free / (1024**3)


def memory_free_gb() -> float:
    command = [
        "powershell",
        "-NoProfile",
        "-Command",
        "(Get-CimInstance Win32_OperatingSystem).FreePhysicalMemory",
    ]
    result = subprocess.run(
        command,
        cwd=ROOT,
        text=True,
        encoding="utf-8",
        errors="replace",
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
        timeout=30,
        check=False,
    )
    try:
        return float(result.stdout.strip()) / (1024**2)
    except (TypeError, ValueError):
        return 0.0


def wait_for_resources(min_disk_gb: float, min_memory_gb: float) -> None:
    while True:
        disk = disk_free_gb()
        memory = memory_free_gb()
        if disk < min_disk_gb:
            raise RuntimeError(
                f"Disk guard triggered: {disk:.1f} GiB free, "
                f"minimum {min_disk_gb:.1f} GiB"
            )
        if memory >= min_memory_gb:
            return
        print(
            f"  memory guard waiting: {memory:.2f} GiB free, "
            f"need {min_memory_gb:.2f} GiB",
            flush=True,
        )
        time.sleep(30)


def run_logged(
    args: list[str],
    *,
    timeout: int,
    log_path: Path,
) -> int:
    started = now()
    timed_out = False
    try:
        result = subprocess.run(
            args,
            cwd=ROOT,
            text=True,
            encoding="utf-8",
            errors="replace",
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            timeout=timeout,
            check=False,
        )
        returncode = result.returncode
        output = result.stdout or ""
    except subprocess.TimeoutExpired as exc:
        timed_out = True
        returncode = 124
        output = exc.stdout or ""
        if isinstance(output, bytes):
            output = output.decode("utf-8", errors="replace")
    log_path.parent.mkdir(parents=True, exist_ok=True)
    log_path.write_text(
        "\n".join(
            [
                f"started={started}",
                f"returncode={returncode}",
                f"timed_out={timed_out}",
                f"command={args!r}",
                "",
                output,
            ]
        ),
        encoding="utf-8",
    )
    return returncode


def sample_dir(config: dict, instance_id: str) -> Path:
    return resolve(config["artifact_dir"]) / instance_id


def valid_spl(config: dict, instance_id: str, snapshot_root: Path) -> bool:
    sample = sample_dir(config, instance_id)
    context = sample / "spl_context.txt"
    index = sample / "spl_index.json"
    metadata = sample / "spl_metadata.json"
    source_files = sample / "source_files"
    if not context.exists() or not context.read_text(
        encoding="utf-8", errors="replace"
    ).strip():
        return False
    if not index.is_file() or not metadata.is_file() or not source_files.is_dir():
        return False
    entry = sample_snapshot_dir(snapshot_root, f"{instance_id}::construction")
    if not entry.exists():
        return False
    verify_sample_snapshot(entry)
    return True


def backup_invalid_outputs(
    config: dict,
    instance_id: str,
    backup_root: Path,
) -> None:
    short_id = hashlib.sha256(instance_id.encode("utf-8")).hexdigest()[:12]
    destination = backup_root / short_id
    manifest_path = destination / "manifest.json"
    if manifest_path.exists():
        return
    if destination.exists():
        shutil.rmtree(destination)
    destination.mkdir(parents=True)
    sample = sample_dir(config, instance_id)
    sample_backup = destination / "artifact_spl_assets"
    sample_backup.mkdir()
    for name in (
        "source_fetch_metadata.json",
        "spl_context.txt",
        "spl_index.json",
        "spl_injection_policy.json",
        "spl_metadata.json",
    ):
        source = sample / name
        if source.exists():
            shutil.copy2(source, sample_backup / name)

    instance_run = resolve(config["run_dir"]) / instance_id
    run_backup = destination / "condition_runs"
    run_backup.mkdir()
    archives = {}
    for position, condition in enumerate(SPL_CONDITIONS, start=1):
        source = instance_run / condition
        if source.exists():
            archive_base = run_backup / f"condition_{position:02d}"
            archive_path = shutil.make_archive(
                str(archive_base),
                "zip",
                root_dir=source,
            )
            archives[condition] = str(Path(archive_path).name)
    write_json(
        manifest_path,
        {
            "instance_id": instance_id,
            "short_id": short_id,
            "condition_archives": archives,
        },
    )


def make_configs(
    base: dict,
    *,
    config_root: Path,
    unit_name: str,
) -> tuple[Path, Path, Path]:
    prepare_config = dict(base)
    prepare_config.update(
        reuse_prebuilt_spl_assets=False,
        fail_on_spl_error=True,
        source_fetch_timeout_seconds=180,
    )
    prepare_path = config_root / f"{unit_name}.prepare.json"
    write_json(prepare_path, prepare_config)

    run_config = dict(base)
    run_config.update(
        conditions=list(SPL_CONDITIONS),
        resume_existing_conditions=False,
        max_workers=2,
        continue_on_error=False,
    )
    run_path = config_root / f"{unit_name}.run.json"
    write_json(run_path, run_config)

    evaluate_config = dict(base)
    original_run_id = str(
        evaluate_config.get(
            "smoke_run_id",
            evaluate_config.get("run_id", "empty-spl-recovery"),
        )
    )
    short_run_id = "h" + hashlib.sha256(
        original_run_id.encode("utf-8")
    ).hexdigest()[:12]
    evaluate_config.update(
        smoke_run_id=short_run_id,
        swebench_harness_run_id_prefix=short_run_id,
        conditions=list(ALL_CONDITIONS),
        resume_existing_evaluations=True,
        rerun_evaluation_conditions=list(SPL_CONDITIONS),
        rerun_unavailable_evaluations=False,
        force_rerun_swebench_harness=True,
        swebench_report_wait_seconds=5,
    )
    evaluate_config["swebench_harness_command"] = str(
        evaluate_config["swebench_harness_command"]
    ).replace("--clean true", "--clean false")
    evaluate_path = config_root / f"{unit_name}.evaluate.json"
    write_json(evaluate_path, evaluate_config)
    return prepare_path, run_path, evaluate_path


def prepare_one(
    job: dict,
    attempts: int,
    timeout_seconds: int,
    logs: Path,
) -> dict:
    instance_id = job["instance_id"]
    for attempt in range(1, attempts + 1):
        rc = run_logged(
            [
                sys.executable,
                str(ROOT / "code/RQ3/prepare.py"),
                "--config",
                str(job["prepare_config"]),
            ],
            timeout=timeout_seconds,
            log_path=logs / job["unit_name"] / f"prepare_attempt_{attempt:02d}.log",
        )
        valid = valid_spl(job["base_config"], instance_id, job["snapshot_root"])
        if rc == 0 and valid:
            return {
                "instance_id": instance_id,
                "returncode": rc,
                "attempt": attempt,
                "valid": True,
                "finished_at": now(),
            }
        if attempt < attempts:
            time.sleep(30 * attempt)
    return {
        "instance_id": instance_id,
        "returncode": rc,
        "attempt": attempts,
        "valid": False,
        "finished_at": now(),
    }


def image_available(image: str) -> bool:
    return (
        subprocess.run(
            ["docker", "image", "inspect", image],
            cwd=ROOT,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            timeout=60,
            check=False,
        ).returncode
        == 0
    )


def extract_image(config: dict, instance_id: str) -> str:
    instance_run = resolve(config["run_dir"]) / instance_id
    for condition in ALL_CONDITIONS:
        for name in (
            "swebench_harness_stderr.txt",
            "swebench_harness_stdout.txt",
            "swebench_harness_command.txt",
            "stderr_00.txt",
            "stdout_00.txt",
        ):
            path = instance_run / condition / name
            if not path.exists():
                continue
            match = IMAGE_RE.search(
                path.read_text(encoding="utf-8", errors="replace")
            )
            if match:
                return match.group(1)
    safe_id = instance_id.replace("/", "__")
    for path in (ROOT / "logs" / "run_evaluation").glob(
        f"*{safe_id}*/**/run_instance.log"
    ):
        match = IMAGE_RE.search(path.read_text(encoding="utf-8", errors="replace"))
        if match:
            return match.group(1)
    raise RuntimeError(f"Cannot determine SWE-bench image for {instance_id}")


def pull_image(image: str, log_dir: Path, attempts: int) -> str | None:
    if image_available(image):
        return image
    for prefix_no, prefix in enumerate(MIRROR_PREFIXES, start=1):
        source = f"{prefix}{image}"
        for attempt in range(1, attempts + 1):
            rc = run_logged(
                ["docker", "pull", source],
                timeout=1800,
                log_path=(
                    log_dir
                    / f"pull_source_{prefix_no:02d}_attempt_{attempt:02d}.log"
                ),
            )
            if rc == 0 and image_available(source):
                if source != image:
                    tag_rc = run_logged(
                        ["docker", "tag", source, image],
                        timeout=120,
                        log_path=log_dir / f"tag_source_{prefix_no:02d}.log",
                    )
                    if tag_rc != 0 or not image_available(image):
                        continue
                return source
            if attempt < attempts:
                time.sleep(15 * attempt)
    return None


def remove_image(image: str, log_path: Path) -> int:
    return run_logged(
        ["docker", "image", "rm", "-f", image],
        timeout=300,
        log_path=log_path,
    )


def generated_patch_coverage(config: dict, instance_id: str) -> dict:
    evaluation_path = resolve(config["run_dir"]) / "evaluation.json"
    rows = read_json(evaluation_path)
    selected = {
        row["condition"]: row
        for row in rows
        if row.get("instance_id") == instance_id
        and row.get("condition") in SPL_CONDITIONS
    }
    return {
        condition: {
            "patch_generated": bool(selected.get(condition, {}).get("patch_generated")),
            "evaluation_available": bool(
                selected.get(condition, {}).get("evaluation_available")
            ),
            "resolved": selected.get(condition, {}).get("resolved"),
        }
        for condition in SPL_CONDITIONS
    }


def save_state(path: Path, state: dict) -> None:
    state["updated_at"] = now()
    write_json(path, state)


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Recover instances whose SPL preparation was empty, preserving the "
            "invalid outputs and rerunning only the three SPL conditions."
        )
    )
    parser.add_argument("--plan", type=Path, default=DEFAULT_PLAN)
    parser.add_argument("--prepare-workers", type=int, default=4)
    parser.add_argument("--prepare-attempts", type=int, default=3)
    parser.add_argument("--prepare-timeout-seconds", type=int, default=21600)
    parser.add_argument("--pull-attempts", type=int, default=3)
    parser.add_argument("--min-free-gb", type=float, default=80.0)
    parser.add_argument("--min-free-memory-gb", type=float, default=3.0)
    args = parser.parse_args()

    plan_path = resolve(args.plan)
    plan = read_json(plan_path)
    snapshot_root = resolve(plan["spl_snapshot_dir"])
    work_root = plan_path.parent / "empty_spl_recovery_20260730"
    config_root = work_root / "configs"
    logs = work_root / "logs"
    state_path = work_root / "state.json"
    work_root.mkdir(parents=True, exist_ok=True)

    if state_path.exists():
        state = read_json(state_path)
        target_names = set(state["target_units"])
    else:
        target_names = set()
        for unit in plan["units"]:
            base = read_json(resolve(unit["config_path"]))
            context = sample_dir(base, unit["instance_id"]) / "spl_context.txt"
            if not context.exists() or not context.read_text(
                encoding="utf-8", errors="replace"
            ).strip():
                target_names.add(unit["unit_name"])
        state = {
            "started_at": now(),
            "plan": str(plan_path),
            "target_units": sorted(target_names),
            "invalid_output_policy": (
                "Preserve old SPL-condition outputs, rebuild SPL only, then "
                "rerun only localization/repair/both and their harness reports."
            ),
            "prepared": {},
            "rerun": {},
            "evaluated": {},
            "complete": False,
        }
        save_state(state_path, state)

    jobs = []
    for unit in plan["units"]:
        if unit["unit_name"] not in target_names:
            continue
        base = read_json(resolve(unit["config_path"]))
        backup_invalid_outputs(
            base,
            unit["instance_id"],
            work_root / "pre_recovery_invalid_empty_spl",
        )
        prepare_config, run_config, evaluate_config = make_configs(
            base,
            config_root=config_root,
            unit_name=unit["unit_name"],
        )
        jobs.append(
            {
                **unit,
                "base_config": base,
                "prepare_config": prepare_config,
                "run_config": run_config,
                "evaluate_config": evaluate_config,
                "snapshot_root": snapshot_root,
            }
        )

    pending_prepare = [
        job
        for job in jobs
        if not valid_spl(job["base_config"], job["instance_id"], snapshot_root)
    ]
    if pending_prepare:
        print(
            f"Preparing SPL for {len(pending_prepare)} instances with "
            f"{args.prepare_workers} workers",
            flush=True,
        )
        failed_prepare = []
        with ThreadPoolExecutor(max_workers=max(1, args.prepare_workers)) as executor:
            futures = {
                executor.submit(
                    prepare_one,
                    job,
                    max(1, args.prepare_attempts),
                    max(1, args.prepare_timeout_seconds),
                    logs,
                ): job
                for job in pending_prepare
            }
            for future in as_completed(futures):
                job = futures[future]
                try:
                    result = future.result()
                except Exception as exc:
                    result = {
                        "instance_id": job["instance_id"],
                        "returncode": 1,
                        "attempt": 0,
                        "valid": False,
                        "error": f"{type(exc).__name__}: {exc}",
                        "finished_at": now(),
                    }
                state["prepared"][job["unit_name"]] = result
                save_state(state_path, state)
                print(
                    f"  {job['instance_id']}: valid={result['valid']} "
                    f"attempt={result['attempt']}",
                    flush=True,
                )
                if not result["valid"]:
                    failed_prepare.append(job["instance_id"])

        if failed_prepare:
            raise RuntimeError(
                "SPL preparation failed for: " + ", ".join(failed_prepare)
            )

    manifest = build_snapshot_manifest(
        snapshot_root,
        metadata={
            "experiment": plan["run_name"],
            "expected_instance_count": plan["expected_instance_count"],
            "refreshed_after": "empty_spl_recovery_prepare",
        },
    )
    if manifest["sample_count"] != int(plan["expected_instance_count"]):
        raise RuntimeError(
            f"SPL snapshot coverage is {manifest['sample_count']}/"
            f"{plan['expected_instance_count']}"
        )

    for position, job in enumerate(jobs, start=1):
        if state["rerun"].get(job["unit_name"], {}).get("complete"):
            continue
        wait_for_resources(args.min_free_gb, args.min_free_memory_gb)
        print(
            f"Rerun {position}/{len(jobs)} {job['instance_id']}: "
            f"{', '.join(SPL_CONDITIONS)}",
            flush=True,
        )
        rc = run_logged(
            [
                sys.executable,
                str(ROOT / "code/RQ3/run.py"),
                "--config",
                str(job["run_config"]),
            ],
            timeout=21600,
            log_path=logs / job["unit_name"] / "rerun_spl_conditions.log",
        )
        complete = rc == 0
        state["rerun"][job["unit_name"]] = {
            "returncode": rc,
            "complete": complete,
            "finished_at": now(),
        }
        save_state(state_path, state)
        if not complete:
            raise RuntimeError(f"SPL condition rerun failed for {job['instance_id']}")

    for position, job in enumerate(jobs, start=1):
        if state["evaluated"].get(job["unit_name"], {}).get("complete"):
            continue
        wait_for_resources(args.min_free_gb, args.min_free_memory_gb)
        image = extract_image(job["base_config"], job["instance_id"])
        unit_logs = logs / job["unit_name"]
        print(
            f"Evaluate {position}/{len(jobs)} {job['instance_id']}",
            flush=True,
        )
        pulled = pull_image(image, unit_logs, max(1, args.pull_attempts))
        if not pulled:
            raise RuntimeError(f"Image pull failed for {job['instance_id']}: {image}")
        rc = run_logged(
            [
                sys.executable,
                str(ROOT / "code/RQ3/evaluate.py"),
                "--config",
                str(job["evaluate_config"]),
            ],
            timeout=21600,
            log_path=unit_logs / "evaluate_spl_conditions.log",
        )
        coverage = generated_patch_coverage(
            job["base_config"],
            job["instance_id"],
        )
        unavailable_generated = [
            condition
            for condition, row in coverage.items()
            if row["patch_generated"] and not row["evaluation_available"]
        ]
        remove_image(image, unit_logs / "cleanup_image.log")
        if pulled != image:
            remove_image(pulled, unit_logs / "cleanup_mirror_image.log")
        complete = rc == 0 and not unavailable_generated
        state["evaluated"][job["unit_name"]] = {
            "returncode": rc,
            "coverage": coverage,
            "unavailable_generated": unavailable_generated,
            "complete": complete,
            "finished_at": now(),
        }
        save_state(state_path, state)
        if not complete:
            raise RuntimeError(
                f"Harness recovery incomplete for {job['instance_id']}: "
                f"{unavailable_generated}"
            )

    aggregate_rc = run_logged(
        [
            sys.executable,
            str(ROOT / "code/RQ3/tests_and_validation/aggregate_complex_pipeline.py"),
            "--plan",
            str(plan_path),
            "--require-complete",
        ],
        timeout=600,
        log_path=logs / "aggregate_final.log",
    )
    state["aggregate_returncode"] = aggregate_rc
    state["snapshot_manifest"] = {
        "sample_count": manifest["sample_count"],
        "file_count": manifest["file_count"],
        "total_bytes": manifest["total_bytes"],
    }
    state["complete"] = aggregate_rc == 0
    state["finished_at"] = now()
    save_state(state_path, state)
    print(
        f"Empty-SPL recovery complete={state['complete']}; "
        f"snapshots={manifest['sample_count']}",
        flush=True,
    )
    return 0 if state["complete"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
