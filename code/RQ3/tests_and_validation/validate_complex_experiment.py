import argparse
import hashlib
import importlib.util
import json
import os
import shutil
from datetime import datetime, timezone
from pathlib import Path

from datasets import Dataset


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_PLAN = ROOT / "runs" / "exp6_complex_top20_swebench_verified_20260721" / "optimized_plan" / "pipeline_plan.json"
DEFAULT_REPORT = DEFAULT_PLAN.parent / "preparation_readiness.json"
STORAGE_GUARD = ROOT / "code" / "RQ3" / "swebench_storage_guard.py"
REQUIRED_CONDITIONS = [
    "miniswe_original",
    "miniswe_free_summary",
    "miniswe_spl_localization",
    "miniswe_spl_repair",
    "miniswe_spl_both",
]


def read_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8", errors="replace"))


def write_json(path: Path, data) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=True, indent=2) + "\n", encoding="utf-8")


def resolve_path(value: str | Path) -> Path:
    path = Path(value)
    return path if path.is_absolute() else ROOT / path


def sample_ids_sha256(ids: list[str]) -> str:
    payload = ("\n".join(ids) + "\n").encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def add_check(checks: list[dict], name: str, ok: bool, details, severity: str = "error") -> None:
    checks.append({"name": name, "ok": bool(ok), "severity": severity, "details": details})


def load_storage_guard():
    spec = importlib.util.spec_from_file_location("exp6_storage_guard", STORAGE_GUARD)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot load storage guard: {STORAGE_GUARD}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def directory_is_nonempty(path: Path) -> bool:
    return path.exists() and any(path.iterdir())


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate the optimized Exp6 pipeline without starting any work.")
    parser.add_argument("--plan", type=Path, default=DEFAULT_PLAN)
    parser.add_argument("--out", type=Path)
    parser.add_argument("--min-free-gb", type=float, default=80.0)
    parser.add_argument("--require-api-key", action="store_true")
    parser.add_argument("--require-clean-outputs", action="store_true")
    args = parser.parse_args()

    checks: list[dict] = []
    plan_path = resolve_path(args.plan).resolve()
    report_path = resolve_path(args.out) if args.out else plan_path.parent / "preparation_readiness.json"
    add_check(checks, "plan_exists", plan_path.exists(), str(plan_path))
    if not plan_path.exists():
        report = {"ready": False, "ready_for_execution": False, "checks": checks}
        write_json(report_path, report)
        return 2

    plan = read_json(plan_path)
    add_check(checks, "optimized_schema", plan.get("schema_version") == 2, plan.get("schema_version"))
    locked_hashes = plan.get("execution_input_hashes", {})
    hash_failures = []
    for value, expected_hash in locked_hashes.items():
        input_path = resolve_path(value)
        if not input_path.exists():
            hash_failures.append({"path": value, "reason": "missing"})
            continue
        actual_hash = file_sha256(input_path)
        if actual_hash != expected_hash:
            hash_failures.append(
                {
                    "path": value,
                    "reason": "sha256_mismatch",
                    "expected": expected_hash,
                    "actual": actual_hash,
                }
            )
    add_check(
        checks,
        "immutable_execution_inputs",
        bool(locked_hashes) and not hash_failures,
        {
            "algorithm": plan.get("execution_input_hash_algorithm"),
            "locked_file_count": len(locked_hashes),
            "failures": hash_failures,
        },
    )
    selection_path = resolve_path(plan["selection_path"])
    base_config_path = resolve_path(plan["base_config_path"])
    add_check(checks, "selection_exists", selection_path.exists(), str(selection_path))
    add_check(checks, "base_config_exists", base_config_path.exists(), str(base_config_path))

    required_paths = [
        ROOT / "tools" / "mini-swe-agent" / "repo" / "src" / "minisweagent",
        ROOT / "code" / "RQ3" / "swebench_windows_resource_shim",
        STORAGE_GUARD,
        ROOT / "code" / "RQ3" / "prepare.py",
        ROOT / "code" / "RQ3" / "run.py",
        ROOT / "code" / "RQ3" / "evaluate.py",
        ROOT / "code" / "RQ3" / "run_complex_batches.py",
    ]
    missing_paths = [str(path) for path in required_paths if not path.exists()]
    add_check(checks, "required_local_paths", not missing_paths, {"missing": missing_paths})

    available_gb = round(shutil.disk_usage(ROOT).free / 1024**3, 2)
    add_check(
        checks,
        "workspace_free_space",
        available_gb >= args.min_free_gb,
        {"free_gb": available_gb, "minimum_gb": args.min_free_gb},
    )
    storage_guard = load_storage_guard()
    docker_inventory = storage_guard.inventory()
    add_check(checks, "docker_available", docker_inventory["docker_available"], docker_inventory.get("docker_errors", []))
    add_check(
        checks,
        "old_swebench_resources_absent",
        not docker_inventory["swebench_containers"] and not docker_inventory["swebench_images"],
        {
            "containers": len(docker_inventory["swebench_containers"]),
            "images": len(docker_inventory["swebench_images"]),
        },
        severity="warning",
    )

    selection = read_json(selection_path) if selection_path.exists() else []
    selection_ids = [row.get("instance_id") for row in selection]
    expected_count = int(plan.get("expected_instance_count") or len(selection_ids))
    add_check(
        checks,
        "selection_has_expected_unique_instances",
        len(selection_ids) == expected_count and len(set(selection_ids)) == expected_count,
        {"expected": expected_count, "actual": len(selection_ids), "ids": selection_ids},
    )
    add_check(
        checks,
        "selection_versions_present",
        all(row.get("version") for row in selection),
        {"missing": [row.get("instance_id") for row in selection if not row.get("version")]},
    )

    units = plan.get("units", [])
    waves = plan.get("waves", [])
    unit_ids = [unit.get("instance_id") for unit in units]
    unit_nos = [int(unit.get("unit_no", -1)) for unit in units]
    add_check(
        checks,
        "plan_covers_selection_once",
        len(unit_ids) == expected_count
        and len(set(unit_ids)) == expected_count
        and set(unit_ids) == set(selection_ids),
        unit_ids,
    )
    add_check(checks, "unit_numbers_contiguous", unit_nos == list(range(1, len(units) + 1)), unit_nos)
    wave_size = max(1, int(plan.get("wave_size", 0)))
    wave_unit_nos = [int(no) for wave in waves for no in wave.get("unit_nos", [])]
    add_check(
        checks,
        "waves_cover_units_once",
        sorted(wave_unit_nos) == unit_nos
        and len(wave_unit_nos) == len(set(wave_unit_nos))
        and all(1 <= len(wave.get("unit_nos", [])) <= wave_size for wave in waves),
        {"wave_size": wave_size, "sizes": [len(wave.get("unit_nos", [])) for wave in waves]},
    )

    prepare_instance_workers = int(plan.get("prepare_instance_workers", 0))
    patch_instance_workers = int(plan.get("patch_instance_workers", 0))
    condition_workers = int(plan.get("condition_workers", 0))
    harness_workers = int(plan.get("harness_instance_workers", 0))
    add_check(
        checks,
        "bounded_patch_parallelism",
        1 <= prepare_instance_workers <= 8
        and 1 <= patch_instance_workers <= 4
        and 1 <= condition_workers <= 3,
        {
            "prepare_instance_workers": prepare_instance_workers,
            "patch_instance_workers": patch_instance_workers,
            "condition_workers": condition_workers,
            "maximum_simultaneous_conditions": patch_instance_workers * condition_workers,
        },
    )
    add_check(checks, "serialized_harness", harness_workers == 1, {"harness_instance_workers": harness_workers})

    config_issues = []
    artifact_dirs = []
    run_dirs = []
    missing_credentials = []
    pool_paths = set()
    pool_counts = set()
    dataset_arrow = None
    selected_by_id = {row.get("instance_id"): row for row in selection}
    expected_model = plan.get("model")
    expected_spl_builder_model = plan.get("spl_builder_model")
    expected_summary_model = plan.get("summary_model")
    expected_step_limit = plan.get("mini_step_limit")
    expected_wall_time_limit = plan.get("mini_wall_time_limit_seconds")
    expected_command_timeout = plan.get("mini_command_timeout_seconds")
    expected_spl_protocol = plan.get("mini_spl_protocol")
    expected_snapshot_dir = plan.get("spl_snapshot_dir")
    expected_controller_budget = {
        "mini_spl_controller_cards": 4,
        "mini_spl_controller_spl_chars": 750,
        "mini_spl_prompt_cards": 2,
        "mini_source_bound_source_chars": 1400,
        "mini_spl_both_controller_cards": 3,
        "mini_spl_both_controller_spl_chars": 600,
        "mini_spl_both_prompt_cards": 1,
        "mini_spl_both_source_bound_source_chars": 1200,
    }
    for unit in units:
        config_path = resolve_path(unit["config_path"])
        if not config_path.exists():
            config_issues.append(f"missing config: {config_path}")
            continue
        config = read_json(config_path)
        selected = selected_by_id.get(unit["instance_id"], {})
        if config.get("indices") != [int(unit["dataset_index"])]:
            config_issues.append(f"{config_path.name}: config must contain exactly one instance index")
        if int(unit["dataset_index"]) != int(selected.get("dataset_index", -1)):
            config_issues.append(f"{config_path.name}: dataset index differs from selection")
        if config.get("conditions") != REQUIRED_CONDITIONS:
            config_issues.append(f"{config_path.name}: condition family differs from Exp6")
        if expected_model and config.get("model") != expected_model:
            config_issues.append(f"{config_path.name}: model differs from plan")
        if expected_spl_builder_model and config.get("spl_model") != expected_spl_builder_model:
            config_issues.append(f"{config_path.name}: SPL builder model differs from plan")
        if expected_summary_model and config.get("summary_model") != expected_summary_model:
            config_issues.append(f"{config_path.name}: summary model differs from plan")
        if expected_step_limit is not None and int(config.get("mini_step_limit", -1)) != int(expected_step_limit):
            config_issues.append(f"{config_path.name}: mini_step_limit differs from plan")
        if (
            expected_wall_time_limit is not None
            and int(config.get("mini_wall_time_limit_seconds", -1)) != int(expected_wall_time_limit)
        ):
            config_issues.append(f"{config_path.name}: wall-time limit differs from plan")
        if (
            expected_command_timeout is not None
            and int(config.get("mini_command_timeout_seconds", -1)) != int(expected_command_timeout)
        ):
            config_issues.append(f"{config_path.name}: command timeout differs from plan")
        if expected_spl_protocol and config.get("mini_spl_protocol") != expected_spl_protocol:
            config_issues.append(f"{config_path.name}: SPL protocol differs from plan")
        if expected_spl_protocol == "spl_guarded_protocol":
            for key, expected_value in expected_controller_budget.items():
                if int(config.get(key, -1)) != expected_value:
                    config_issues.append(
                        f"{config_path.name}: {key} differs from successful Experiment 6"
                    )
        if plan.get("require_legacy_gold_patch_scope") and config.get("spl_source_scope") != "legacy_gold_patch_scope":
            config_issues.append(f"{config_path.name}: legacy gold-patch SPL scope is required")
        if expected_snapshot_dir and config.get("spl_snapshot_dir") != expected_snapshot_dir:
            config_issues.append(f"{config_path.name}: SPL snapshot destination differs from plan")
        if expected_snapshot_dir and not config.get("reuse_prebuilt_spl_assets"):
            config_issues.append(f"{config_path.name}: prebuilt SPL reuse must be enabled")
        if expected_snapshot_dir and not config.get("save_spl_snapshot"):
            config_issues.append(f"{config_path.name}: SPL snapshot saving must be enabled")
        if plan.get("require_deepseek_paths"):
            normalized_paths = (
                str(config.get("artifact_dir") or "").replace("\\", "/"),
                str(config.get("run_dir") or "").replace("\\", "/"),
            )
            if any("/deepseek/" not in f"/{value.strip('/')}/" for value in normalized_paths):
                config_issues.append(f"{config_path.name}: outputs must live below a deepseek directory")
        if config.get("max_workers") != condition_workers:
            config_issues.append(f"{config_path.name}: condition worker count differs from plan")
        if not config.get("resume_existing_conditions"):
            config_issues.append(f"{config_path.name}: condition-level resume must be enabled")
        if not config.get("resume_existing_evaluations"):
            config_issues.append(f"{config_path.name}: evaluation checkpointing must be enabled")
        if config.get("swebench_harness_max_workers") != 1:
            config_issues.append(f"{config_path.name}: harness worker count must equal 1")
        if not config.get("hf_offline"):
            config_issues.append(f"{config_path.name}: hf_offline must be true")
        if not config.get("run_swebench_harness"):
            config_issues.append(f"{config_path.name}: harness must be enabled")
        command = str(config.get("swebench_harness_command") or "")
        if "--cache_level env" not in command or "--clean true" not in command:
            config_issues.append(f"{config_path.name}: harness storage flags missing")
        artifact_dirs.append(str(config.get("artifact_dir") or ""))
        run_dirs.append(str(config.get("run_dir") or ""))

        pool_ok = False
        pool_file = config.get("api_key_pool_file")
        if pool_file:
            pool_path = resolve_path(pool_file)
            if pool_path.exists():
                keys = {str(key).strip() for key in read_json(pool_path).get("keys", []) if str(key).strip()}
                pool_ok = bool(keys)
                pool_paths.add(str(pool_path))
                pool_counts.add(len(keys))
        key_env = str(config.get("api_key_env") or "OPENAI_API_KEY")
        if not pool_ok and not config.get("api_key") and not os.environ.get(key_env):
            missing_credentials.append(f"{config_path.name}:{key_env}")

        if dataset_arrow is None:
            cache_root = resolve_path(str(config.get("hf_datasets_cache") or "artifacts/hf_cache/datasets"))
            matches = list(cache_root.rglob("swe-bench_verified-test.arrow")) if cache_root.exists() else []
            dataset_arrow = matches[0] if matches else None

    if len(set(artifact_dirs)) != len(artifact_dirs) or len(set(run_dirs)) != len(run_dirs):
        config_issues.append("artifact_dir or run_dir is reused across instance units")
    add_check(checks, "unit_configs", not config_issues, {"issues": config_issues})
    add_check(
        checks,
        "shared_api_key_pool",
        len(pool_paths) == 1 and len(pool_counts) == 1 and next(iter(pool_counts), 0) > 0,
        {"pool_file_count": len(pool_paths), "unique_key_counts": sorted(pool_counts)},
    )
    key_capacity = next(iter(pool_counts), 0) * max(1, int(plan.get("max_per_key", 1)))
    add_check(
        checks,
        "api_capacity_covers_scheduler",
        key_capacity >= max(prepare_instance_workers, patch_instance_workers * condition_workers),
        {
            "key_capacity": key_capacity,
            "scheduled_prepare_capacity": prepare_instance_workers,
            "scheduled_condition_capacity": patch_instance_workers * condition_workers,
        },
        severity="warning",
    )

    existing_outputs = []
    for relative in artifact_dirs + run_dirs:
        if relative and directory_is_nonempty(resolve_path(relative)):
            existing_outputs.append(str(resolve_path(relative)))
    add_check(
        checks,
        "output_state",
        not existing_outputs,
        {"nonempty": existing_outputs, "resume_supported": True},
        severity="error" if args.require_clean_outputs else "warning",
    )
    stop_file = plan_path.parent / "execution" / "STOP_REQUESTED"
    add_check(checks, "stop_file_absent", not stop_file.exists(), str(stop_file))

    add_check(checks, "dataset_arrow_cached", dataset_arrow is not None, str(dataset_arrow) if dataset_arrow else None)
    dataset_mismatches = []
    if dataset_arrow is not None:
        dataset = Dataset.from_file(str(dataset_arrow))
        for selected in selection:
            index = int(selected["dataset_index"])
            if index < 0 or index >= len(dataset):
                dataset_mismatches.append(f"{selected['instance_id']}: index {index} out of range")
                continue
            row = dataset[index]
            if row.get("instance_id") != selected["instance_id"]:
                dataset_mismatches.append(f"{selected['instance_id']}: index points to {row.get('instance_id')}")
            if selected.get("version") and row.get("version") != selected.get("version"):
                dataset_mismatches.append(f"{selected['instance_id']}: version mismatch")
    add_check(checks, "selection_matches_cached_dataset", not dataset_mismatches, {"mismatches": dataset_mismatches})

    parent_sample_path = plan.get("parent_sample_file")
    if parent_sample_path:
        parent_path = resolve_path(parent_sample_path)
        add_check(checks, "parent_sample_exists", parent_path.exists(), str(parent_path))
        if parent_path.exists():
            parent = read_json(parent_path)
            parent_ids = [str(value) for value in parent.get("sample_ids", [])]
            selection_order_field = str(plan.get("selection_order_field") or "sample_ids")
            ordered_parent_ids = [
                str(value)
                for value in parent.get(selection_order_field, [])
            ]
            prefix_count = int(plan.get("selection_prefix_count", expected_count))
            parent_sha = str(parent.get("sample_ids_sha256") or "")
            add_check(
                checks,
                "parent_sample_hash",
                parent_sha == plan.get("parent_sample_sha256") and parent_sha == sample_ids_sha256(parent_ids),
                {
                    "manifest": parent_sha,
                    "plan": plan.get("parent_sample_sha256"),
                    "computed": sample_ids_sha256(parent_ids),
                },
            )
            add_check(
                checks,
                "selection_is_frozen_parent_execution_prefix",
                (
                    len(ordered_parent_ids) == len(parent_ids)
                    and set(ordered_parent_ids) == set(parent_ids)
                    and selection_ids == ordered_parent_ids[:prefix_count]
                    and prefix_count == expected_count
                ),
                {
                    "order_field": selection_order_field,
                    "prefix_count": prefix_count,
                    "selection_count": len(selection_ids),
                },
            )

    historical_sources = [resolve_path(value) for value in plan.get("spl_snapshot_source_dirs", [])]
    historical_reuse = plan.get("historical_spl_reuse", {})
    missing_historical_snapshots = []
    missing_migrated_snapshots = []
    if historical_reuse:
        experiments_root = ROOT / "code"
        if str(experiments_root) not in os.sys.path:
            os.sys.path.insert(0, str(experiments_root))
        from common.spl_snapshot import sample_snapshot_dir, verify_sample_snapshot

        for instance_id, source_value in historical_reuse.items():
            source_root = resolve_path(source_value)
            entry = sample_snapshot_dir(source_root, f"{instance_id}::construction")
            try:
                verify_sample_snapshot(entry)
            except (FileNotFoundError, ValueError, OSError) as exc:
                missing_historical_snapshots.append({"instance_id": instance_id, "error": str(exc)})
            if expected_snapshot_dir:
                migrated_entry = sample_snapshot_dir(
                    resolve_path(expected_snapshot_dir), f"{instance_id}::construction"
                )
                try:
                    verify_sample_snapshot(migrated_entry)
                except (FileNotFoundError, ValueError, OSError) as exc:
                    missing_migrated_snapshots.append({"instance_id": instance_id, "error": str(exc)})
    add_check(
        checks,
        "historical_spl_snapshots_verified",
        not missing_historical_snapshots,
        {
            "expected_reuse_count": len(historical_reuse),
            "source_dirs": [str(path) for path in historical_sources],
            "failures": missing_historical_snapshots,
        },
    )
    add_check(
        checks,
        "historical_spl_migrated_to_experiment",
        not missing_migrated_snapshots,
        {
            "target": str(resolve_path(expected_snapshot_dir)) if expected_snapshot_dir else None,
            "expected_count": len(historical_reuse),
            "failures": missing_migrated_snapshots,
        },
    )

    credential_severity = "error" if args.require_api_key else "warning"
    add_check(checks, "api_credentials", not missing_credentials, {"missing": missing_credentials}, credential_severity)
    errors = [check for check in checks if not check["ok"] and check["severity"] == "error"]
    warnings = [check for check in checks if not check["ok"] and check["severity"] == "warning"]
    report = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "ready": not errors,
        "ready_for_execution": not errors and not missing_credentials,
        "formal_experiment_started": bool(existing_outputs),
        "checks": checks,
        "error_count": len(errors),
        "warning_count": len(warnings),
    }
    write_json(report_path, report)
    print(json.dumps({key: report[key] for key in ["ready", "ready_for_execution", "error_count", "warning_count"]}, indent=2))
    print(f"Readiness report: {report_path}")
    return 0 if not errors else 3


if __name__ == "__main__":
    raise SystemExit(main())
