from __future__ import annotations

import argparse
import csv
import json
import math
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[3]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from common.metrics_enhanced import estimate_cost
EXP_ROOT = ROOT
MODELS = (
    "deepseek-v4-flash",
    "deepseek-v4-pro",
    "gpt-5.4",
    "gpt-5.4-mini",
)
PAPER_CONDITIONS = (
    "skeleton_holistic",
    "free_summary",
    "spl_only",
    "skeleton_spl",
)
EXPECTED_SAMPLES = 100
SIGNIFICANCE_COMPARISONS = (
    ("spl_only", "skeleton_holistic"),
    ("spl_only", "free_summary"),
    ("skeleton_spl", "skeleton_holistic"),
    ("skeleton_spl", "free_summary"),
)


def read(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=True, indent=2) + "\n", encoding="utf-8")


def exact_mcnemar_p(left_only: int, right_only: int) -> float:
    """Two-sided exact McNemar p-value for paired binary outcomes."""
    discordant = left_only + right_only
    if discordant == 0:
        return 1.0
    tail = sum(math.comb(discordant, index) for index in range(min(left_only, right_only) + 1))
    return min(1.0, 2.0 * tail / (2**discordant))


def holm_adjust(p_values: list[float]) -> list[float]:
    """Return Holm family-wise-error adjusted p-values in input order."""
    count = len(p_values)
    adjusted = [1.0] * count
    running = 0.0
    for rank, index in enumerate(sorted(range(count), key=p_values.__getitem__)):
        candidate = min(1.0, (count - rank) * p_values[index])
        running = max(running, candidate)
        adjusted[index] = running
    return adjusted


def build_significance(model: str, run_root: Path) -> list[dict[str, Any]]:
    evaluation = read(run_root / "evaluation.json")
    outcomes: dict[str, dict[str, dict[str, bool]]] = {}
    for row in evaluation:
        condition = str(row.get("condition", ""))
        task_id = str(row.get("task_id", ""))
        outcomes.setdefault(condition, {})[task_id] = {
            "passed": bool(row.get("class_test_ok")),
            "available": bool(row.get("evaluation_available")),
        }
    results: list[dict[str, Any]] = []
    for spl_condition, baseline_condition in SIGNIFICANCE_COMPARISONS:
        spl_rows = outcomes.get(spl_condition, {})
        baseline_rows = outcomes.get(baseline_condition, {})
        shared_task_ids = sorted(set(spl_rows) & set(baseline_rows))
        task_ids = [
            task_id
            for task_id in shared_task_ids
            if spl_rows[task_id]["available"] and baseline_rows[task_id]["available"]
        ]
        both_pass = sum(spl_rows[task_id]["passed"] and baseline_rows[task_id]["passed"] for task_id in task_ids)
        spl_only_pass = sum(spl_rows[task_id]["passed"] and not baseline_rows[task_id]["passed"] for task_id in task_ids)
        baseline_only_pass = sum(not spl_rows[task_id]["passed"] and baseline_rows[task_id]["passed"] for task_id in task_ids)
        both_fail = len(task_ids) - both_pass - spl_only_pass - baseline_only_pass
        raw_p = exact_mcnemar_p(spl_only_pass, baseline_only_pass)
        results.append(
            {
                "model": model,
                "metric": "strict_class_pass",
                "test": "two_sided_exact_mcnemar",
                "spl_condition": spl_condition,
                "baseline_condition": baseline_condition,
                "paired_samples": len(task_ids),
                "excluded_unavailable_pairs": len(shared_task_ids) - len(task_ids),
                "both_pass": both_pass,
                "spl_only_pass": spl_only_pass,
                "baseline_only_pass": baseline_only_pass,
                "both_fail": both_fail,
                "spl_passes": both_pass + spl_only_pass,
                "baseline_passes": both_pass + baseline_only_pass,
                "net_pass_difference_count": spl_only_pass - baseline_only_pass,
                "absolute_difference_percentage_points": (
                    100.0 * (spl_only_pass - baseline_only_pass) / len(task_ids)
                    if task_ids
                    else 0.0
                ),
                "p_value_raw": raw_p,
            }
        )
    adjusted = holm_adjust([float(row["p_value_raw"]) for row in results])
    for row, adjusted_p in zip(results, adjusted):
        row["p_value_holm"] = adjusted_p
        row["significant_raw_0_05"] = float(row["p_value_raw"]) < 0.05
        row["significant_holm_0_05"] = adjusted_p < 0.05
        row["multiplicity_family"] = "four pre-specified SPL-vs-non-SPL comparisons within model"
        row["excluded_condition_note"] = (
            "skeleton_incremental is not an official incremental implementation and exposes methods_info fields including solution_code and test_code"
        )
    return results


def build_empty_output_audit(model: str, run_root: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for condition in PAPER_CONDITIONS:
        metadata_paths = sorted(run_root.glob(f"ClassEval_*/{condition}/call_metadata.json"))
        empty_attempts: list[dict[str, Any]] = []
        affected_outputs = 0
        recovered_outputs = 0
        for path in metadata_paths:
            metadata = read(path)
            attempts = metadata.get("attempts") if isinstance(metadata.get("attempts"), list) else [metadata]
            current_empty = [attempt for attempt in attempts if bool(attempt.get("empty_visible_text"))]
            if current_empty:
                affected_outputs += 1
                empty_attempts.extend(current_empty)
                output_path = path.with_name("output.txt")
                recovered_outputs += int(output_path.exists() and bool(output_path.read_text(encoding="utf-8").strip()))
        rows.append(
            {
                "model": model,
                "condition": condition,
                "outputs": len(metadata_paths),
                "outputs_with_empty_attempt": affected_outputs,
                "empty_attempts": len(empty_attempts),
                "recovered_outputs": recovered_outputs,
                "unrecovered_outputs": affected_outputs - recovered_outputs,
                "empty_attempt_input_tokens": sum(int(row.get("input_tokens", 0) or 0) for row in empty_attempts),
                "empty_attempt_output_tokens": sum(int(row.get("output_tokens", 0) or 0) for row in empty_attempts),
                "empty_attempt_reasoning_tokens": sum(int(row.get("reasoning_tokens", 0) or 0) for row in empty_attempts),
                "empty_attempt_total_tokens": sum(int(row.get("total_tokens", 0) or 0) for row in empty_attempts),
                "future_policy": "generation_thinking=disabled; retry same model with thinking disabled if empty",
            }
        )
    return rows


def sum_metadata(root: Path, name: str) -> dict[str, int | float]:
    totals: dict[str, int | float] = {
        "files": 0,
        "calls": 0,
        "input_tokens": 0,
        "output_tokens": 0,
        "reasoning_tokens": 0,
        "total_tokens": 0,
        "elapsed_seconds": 0.0,
    }
    for path in root.rglob(name):
        row = read(path)
        totals["files"] += 1
        for key in ("calls", "input_tokens", "output_tokens", "reasoning_tokens", "total_tokens"):
            totals[key] += int(row.get(key, 0) or 0)
        totals["elapsed_seconds"] += float(row.get("elapsed_seconds", 0) or 0)
    return totals


def empty_usage() -> dict[str, int | float]:
    return {
        "calls": 0,
        "input_tokens": 0,
        "output_tokens": 0,
        "reasoning_tokens": 0,
        "total_tokens": 0,
        "elapsed_seconds": 0.0,
    }


def add_known_costs(*values: Any) -> float | None:
    """Add cost estimates only when every component has known pricing."""
    if any(value is None for value in values):
        return None
    return sum(float(value) for value in values)


def add_usage(totals: dict[str, int | float], row: dict[str, Any] | None) -> None:
    if not row:
        return
    for key in ("calls", "input_tokens", "output_tokens", "reasoning_tokens", "total_tokens"):
        totals[key] += int(row.get(key, 0) or 0)
    totals["elapsed_seconds"] += float(row.get("elapsed_seconds", 0) or 0)


def measured_recovery_usage(model: str, run_root: Path) -> dict[str, Any]:
    audit_root = run_root.parent / "recovery_audit"
    categories = {"superseded_spl": empty_usage(), "superseded_summary": empty_usage(), "superseded_outputs": empty_usage()}
    superseded_metadata = list(audit_root.rglob("superseded_outputs/**/call_metadata.json")) if audit_root.exists() else []
    superseded_task_ids = {path.parent.parent.name for path in superseded_metadata}
    seen_spl: set[str] = set()
    seen_summary: set[str] = set()
    evaluation_paths = audit_root.rglob("initial_evaluation_*/evaluation.json") if audit_root.exists() else []
    for evaluation_path in evaluation_paths:
        for row in read(evaluation_path):
            task_id = str(row.get("task_id", ""))
            if task_id not in superseded_task_ids:
                continue
            if row.get("condition") == "spl_only" and task_id not in seen_spl:
                add_usage(categories["superseded_spl"], row.get("spl_usage"))
                seen_spl.add(task_id)
            if row.get("condition") == "free_summary" and task_id not in seen_summary:
                add_usage(categories["superseded_summary"], row.get("summary_usage"))
                seen_summary.add(task_id)
    for metadata_path in superseded_metadata:
        add_usage(categories["superseded_outputs"], read(metadata_path))
    total = empty_usage()
    for row in categories.values():
        add_usage(total, row)
    total["cost_usd"] = estimate_cost(
        int(total["input_tokens"]),
        int(total["output_tokens"]),
        int(total["reasoning_tokens"]),
        model,
    )
    result = {
        "scope": "completed superseded artifacts with provider usage records",
        "categories": categories,
        "total": total,
        "unmetered_note": (
            "Force-terminated in-flight API calls and stages that returned no provider usage are not assigned invented tokens."
        ),
    }
    write(run_root / "recovery_usage.json", result)
    return result


def aggregate_resource_attempts(resource_dir: Path) -> dict[str, Any]:
    rows = [read(path) for path in sorted((resource_dir / "attempts").glob("*.json"))]
    return {
        "completed_attempt_count": len(rows),
        "wall_seconds": sum(float(row.get("wall_seconds", 0) or 0) for row in rows),
        "peak_process_tree_rss_mib": max((float(row.get("peak_process_tree_rss_mib", 0) or 0) for row in rows), default=0),
        "peak_system_cpu_percent": max((float(row.get("peak_system_cpu_percent", 0) or 0) for row in rows), default=0),
        "minimum_available_memory_mib": min((float(row.get("minimum_available_memory_mib", 0) or 0) for row in rows), default=0),
        "disk_free_delta_gib": sum(float(row.get("disk_free_delta_gib", 0) or 0) for row in rows),
        "failed_attempt_count": sum(int(row.get("returncode", 0) or 0) != 0 for row in rows),
    }


def validate_complete_model_run(model: str, spl_root: Path, run_root: Path, summary: dict[str, Any]) -> dict[str, Any]:
    spl_metadata = list(spl_root.rglob("spl_metadata.json"))
    summary_metadata = list(spl_root.rglob("free_summary_metadata.json"))
    output_files = [
        path for path in run_root.rglob("output.txt")
        if path.parent.name in PAPER_CONDITIONS
    ]
    nonempty_output_files = [path for path in output_files if path.read_text(encoding="utf-8").strip()]
    call_metadata = [
        path for path in run_root.rglob("call_metadata.json")
        if path.parent.name in PAPER_CONDITIONS
    ]
    generation_errors = [
        path for path in run_root.rglob("generation_error.json")
        if path.parent.name in PAPER_CONDITIONS
    ]
    prepare_errors_path = spl_root / "prepare_errors.json"
    prepare_errors = read(prepare_errors_path) if prepare_errors_path.exists() else []

    wrong_spl_models = [str(path.relative_to(ROOT)) for path in spl_metadata if read(path).get("model") != model]
    wrong_summary_models = [
        str(path.relative_to(ROOT)) for path in summary_metadata if read(path).get("model") != model
    ]
    wrong_output_models = [
        str(path.relative_to(ROOT)) for path in call_metadata if read(path).get("model") != model
    ]
    condition_counts = {condition: int(summary.get(condition, {}).get("outputs", 0) or 0) for condition in PAPER_CONDITIONS}
    problems: list[str] = []
    if len(spl_metadata) != EXPECTED_SAMPLES:
        problems.append(f"SPL metadata: {len(spl_metadata)}/{EXPECTED_SAMPLES}")
    if len(summary_metadata) != EXPECTED_SAMPLES:
        problems.append(f"free-summary metadata: {len(summary_metadata)}/{EXPECTED_SAMPLES}")
    if len(nonempty_output_files) != EXPECTED_SAMPLES * len(PAPER_CONDITIONS):
        problems.append(
            f"nonempty outputs: {len(nonempty_output_files)}/{EXPECTED_SAMPLES * len(PAPER_CONDITIONS)} "
            f"({len(output_files)} files)"
        )
    if len(call_metadata) != EXPECTED_SAMPLES * len(PAPER_CONDITIONS):
        problems.append(f"call metadata: {len(call_metadata)}/{EXPECTED_SAMPLES * len(PAPER_CONDITIONS)}")
    if any(count != EXPECTED_SAMPLES for count in condition_counts.values()):
        problems.append(f"per-condition outputs: {condition_counts}")
    if wrong_spl_models:
        problems.append(f"wrong SPL model metadata: {len(wrong_spl_models)}")
    if wrong_summary_models:
        problems.append(f"wrong summary model metadata: {len(wrong_summary_models)}")
    if wrong_output_models:
        problems.append(f"wrong output model metadata: {len(wrong_output_models)}")
    if generation_errors:
        problems.append(f"generation errors: {len(generation_errors)}")
    if prepare_errors:
        problems.append(f"prepare errors: {len(prepare_errors)}")
    return {
        "complete": not problems,
        "problems": problems,
        "spl_metadata_count": len(spl_metadata),
        "summary_metadata_count": len(summary_metadata),
        "output_count": len(output_files),
        "nonempty_output_count": len(nonempty_output_files),
        "empty_output_count": len(output_files) - len(nonempty_output_files),
        "call_metadata_count": len(call_metadata),
        "condition_counts": condition_counts,
        "wrong_spl_model_count": len(wrong_spl_models),
        "wrong_summary_model_count": len(wrong_summary_models),
        "wrong_output_model_count": len(wrong_output_models),
        "generation_error_count": len(generation_errors),
        "prepare_error_count": len(prepare_errors),
    }


def build_model_result(model: str, allow_partial: bool) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    spl_root = EXP_ROOT / "data/RQ1/spl_assets/model_runs" / model / "full100"
    run_root = EXP_ROOT / "data/raw_results/exp1_classeval/model_runs" / model / "full100"
    required = [run_root / "summary.json", run_root / "usage_summary.json", run_root / "cost_summary.json"]
    if not all(path.exists() for path in required):
        if allow_partial:
            return {"model": model, "status": "incomplete"}, []
        missing = [str(path.relative_to(ROOT)) for path in required if not path.exists()]
        raise FileNotFoundError(f"{model} missing result files: {missing}")
    summary = read(run_root / "summary.json")
    completeness = validate_complete_model_run(model, spl_root, run_root, summary)
    if not completeness["complete"] and not allow_partial:
        raise RuntimeError(f"{model} is not a complete formal run: {completeness['problems']}")
    usage = read(run_root / "usage_summary.json")
    cost = read(run_root / "cost_summary.json")["per_condition"]
    resources = read(run_root / "resource_usage/pipeline.json") if (run_root / "resource_usage/pipeline.json").exists() else {}
    all_resources = aggregate_resource_attempts(run_root / "resource_usage")
    stage_resources = {
        stage: read(run_root / f"resource_usage/latest_{stage}.json")
        for stage in ("prepare", "generate", "evaluate")
        if (run_root / f"resource_usage/latest_{stage}.json").exists()
    }
    spl_build = sum_metadata(spl_root, "spl_metadata.json")
    summary_build = sum_metadata(spl_root, "free_summary_metadata.json")
    spl_build_cost = estimate_cost(
        int(spl_build["input_tokens"]),
        int(spl_build["output_tokens"]),
        int(spl_build["reasoning_tokens"]),
        model,
    )
    summary_build_cost = estimate_cost(
        int(summary_build["input_tokens"]),
        int(summary_build["output_tokens"]),
        int(summary_build["reasoning_tokens"]),
        model,
    )
    recovery_usage = measured_recovery_usage(model, run_root)
    recovery_total = recovery_usage["total"]
    final_inference_calls = sum(int(row.get("inference_calls", 0) or 0) for row in cost.values())
    final_inference_tokens = sum(int(row.get("inference_total_tokens", 0) or 0) for row in cost.values())
    final_inference_cost = add_known_costs(*(row.get("inference_cost_usd") for row in cost.values()))
    final_all_calls = final_inference_calls + int(spl_build["calls"]) + int(summary_build["calls"])
    final_all_tokens = final_inference_tokens + int(spl_build["total_tokens"]) + int(summary_build["total_tokens"])
    final_all_cost = add_known_costs(final_inference_cost, spl_build_cost, summary_build_cost)
    conditions: list[dict[str, Any]] = []
    for condition in PAPER_CONDITIONS:
        metrics = summary.get(condition, {})
        u = usage.get(condition, {})
        c = cost.get(condition, {})
        conditions.append(
            {
                "model": model,
                "condition": condition,
                "samples": metrics.get("outputs", 0),
                "syntax_passes": metrics.get("syntax_passes", 0),
                "syntax_pass_rate": metrics.get("syntax_pass_rate"),
                "class_passes": metrics.get("class_test_passes", 0),
                "class_pass_rate": metrics.get("class_test_pass_rate"),
                "valid_evaluations": metrics.get("valid_evaluations"),
                "valid_class_pass_rate": metrics.get("valid_class_test_pass_rate"),
                "method_tests_passed": metrics.get("method_tests_passed", 0),
                "method_tests_total": metrics.get("method_tests_total", 0),
                "method_test_pass_rate": metrics.get("method_test_pass_rate"),
                "avg_codebleu": metrics.get("avg_codebleu"),
                "avg_codebleu_bleu": metrics.get("avg_codebleu_bleu"),
                "avg_codebleu_weighted_bleu": metrics.get("avg_codebleu_weighted_bleu"),
                "avg_codebleu_syntax_match": metrics.get("avg_codebleu_syntax_match"),
                "avg_codebleu_dataflow_match": metrics.get("avg_codebleu_dataflow_match"),
                "inference_calls": c.get("inference_calls", u.get("calls", 0)),
                "inference_input_tokens": c.get("inference_input_tokens", 0),
                "inference_output_tokens": c.get("inference_output_tokens", 0),
                "inference_reasoning_tokens": c.get("inference_reasoning_tokens", 0),
                "inference_total_tokens": c.get("inference_total_tokens", u.get("total_tokens", 0)),
                "inference_elapsed_seconds": c.get("llm_usage_elapsed_seconds", u.get("elapsed_seconds", 0)),
                "inference_cost_usd": c.get("inference_cost_usd", 0),
                "one_time_spl_build_calls": spl_build["calls"] if condition in {"spl_only", "skeleton_spl"} else 0,
                "one_time_spl_build_tokens": spl_build["total_tokens"] if condition in {"spl_only", "skeleton_spl"} else 0,
                "one_time_spl_build_elapsed_seconds": spl_build["elapsed_seconds"] if condition in {"spl_only", "skeleton_spl"} else 0,
                "one_time_spl_build_cost_usd": spl_build_cost if condition in {"spl_only", "skeleton_spl"} else 0,
                "one_time_summary_build_calls": summary_build["calls"] if condition == "free_summary" else 0,
                "one_time_summary_build_tokens": summary_build["total_tokens"] if condition == "free_summary" else 0,
                "one_time_summary_build_elapsed_seconds": summary_build["elapsed_seconds"] if condition == "free_summary" else 0,
                "one_time_summary_build_cost_usd": summary_build_cost if condition == "free_summary" else 0,
                "total_cost_with_relevant_build_usd": add_known_costs(
                    c.get("inference_cost_usd"),
                    spl_build_cost if condition in {"spl_only", "skeleton_spl"} else 0,
                    summary_build_cost if condition == "free_summary" else 0,
                ),
                "pipeline_wall_seconds": resources.get("total_wall_seconds_this_invocation"),
                "pipeline_wall_seconds_all_attempts": all_resources["wall_seconds"],
                "pipeline_peak_rss_mib": all_resources["peak_process_tree_rss_mib"],
                "pipeline_peak_system_cpu_percent": all_resources["peak_system_cpu_percent"],
                "pipeline_minimum_available_memory_mib": all_resources["minimum_available_memory_mib"],
                "prepare_wall_seconds": stage_resources.get("prepare", {}).get("wall_seconds"),
                "generate_wall_seconds": stage_resources.get("generate", {}).get("wall_seconds"),
                "evaluate_wall_seconds": stage_resources.get("evaluate", {}).get("wall_seconds"),
                "disk_free_delta_gib": all_resources["disk_free_delta_gib"],
                "resource_completed_attempts": all_resources["completed_attempt_count"],
                "resource_failed_attempts": all_resources["failed_attempt_count"],
                "model_final_all_llm_calls": final_all_calls,
                "model_final_all_llm_tokens": final_all_tokens,
                "model_final_all_llm_cost_usd": final_all_cost,
                "model_measured_recovery_calls": recovery_total["calls"],
                "model_measured_recovery_tokens": recovery_total["total_tokens"],
                "model_measured_recovery_cost_usd": recovery_total["cost_usd"],
                "model_actual_measured_all_llm_calls": final_all_calls + int(recovery_total["calls"]),
                "model_actual_measured_all_llm_tokens": final_all_tokens + int(recovery_total["total_tokens"]),
                "model_actual_measured_all_llm_cost_usd": add_known_costs(
                    final_all_cost, recovery_total["cost_usd"]
                ),
            }
        )
    result = {
        "status": "complete" if completeness["complete"] else "incomplete",
        "model": model,
        "sample_count": 100,
        "spl_path": str(spl_root.relative_to(ROOT).as_posix()),
        "result_path": str(run_root.relative_to(ROOT).as_posix()),
        "spl_build": spl_build,
        "spl_build_cost_usd": spl_build_cost,
        "summary_build": summary_build,
        "summary_build_cost_usd": summary_build_cost,
        "resource_usage": resources,
        "all_completed_resource_attempts": all_resources,
        "measured_recovery_usage": recovery_usage,
        "stage_resources": stage_resources,
        "completeness": completeness,
        "conditions": conditions,
    }
    write(run_root / "final_result.json", result)
    return result, conditions


def main() -> int:
    parser = argparse.ArgumentParser(description="Build per-model Exp1 JSON and cross-model CSV.")
    parser.add_argument("--allow-partial", action="store_true")
    args = parser.parse_args()
    output_dir = EXP_ROOT / "data/results/model_comparison"
    model_results: dict[str, Any] = {}
    rows: list[dict[str, Any]] = []
    significance_rows: list[dict[str, Any]] = []
    empty_output_rows: list[dict[str, Any]] = []
    for model in MODELS:
        result, model_rows = build_model_result(model, args.allow_partial)
        model_results[model] = result
        rows.extend(model_rows)
        if result.get("status") == "complete":
            run_root = EXP_ROOT / "data/raw_results/exp1_classeval/model_runs" / model / "full100"
            significance_rows.extend(build_significance(model, run_root))
            empty_output_rows.extend(build_empty_output_audit(model, run_root))
    output_dir.mkdir(parents=True, exist_ok=True)
    write(output_dir / "exp1_full100_results.json", model_results)
    csv_path = output_dir / "exp1_full100_results.csv"
    if rows:
        with csv_path.open("w", newline="", encoding="utf-8-sig") as handle:
            writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
            writer.writeheader()
            writer.writerows(rows)
    write(output_dir / "exp1_full100_significance.json", significance_rows)
    significance_csv = output_dir / "exp1_full100_significance.csv"
    if significance_rows:
        with significance_csv.open("w", newline="", encoding="utf-8-sig") as handle:
            writer = csv.DictWriter(handle, fieldnames=list(significance_rows[0]))
            writer.writeheader()
            writer.writerows(significance_rows)
    write(output_dir / "exp1_empty_output_audit.json", empty_output_rows)
    empty_output_csv = output_dir / "exp1_empty_output_audit.csv"
    if empty_output_rows:
        with empty_output_csv.open("w", newline="", encoding="utf-8-sig") as handle:
            writer = csv.DictWriter(handle, fieldnames=list(empty_output_rows[0]))
            writer.writeheader()
            writer.writerows(empty_output_rows)
    print(f"Wrote {len(rows)} rows to {csv_path.relative_to(ROOT)}")
    print(f"Wrote {len(significance_rows)} rows to {significance_csv.relative_to(ROOT)}")
    print(f"Wrote {len(empty_output_rows)} rows to {empty_output_csv.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
