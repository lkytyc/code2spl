from __future__ import annotations

import argparse
import json
import subprocess
import sys
import time
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from common.code_utils import extract_code_block, python_syntax_ok, run_python_test
from common.codebleu import DEFAULT_CODEBLEU_WEIGHTS, compute_codebleu
from common.paths import ensure_dir, read_config, read_json, resolve_in_project, write_json
from common.run_utils import selected_items
from common.metrics_enhanced import aggregate_cost_summary, compute_cost_per_metric, estimate_cost
from common.statistics import (
    binary_condition_statistics,
    cohens_h,
    compute_cohens_h_from_rows,
    mcnemar_test,
    paired_binary_deltas,
    paired_bootstrap_ci,
)
from common.usage import read_metadata, summarize_usage


def test_prelude(test_code: str) -> str:
    """Keep module-level imports/setup needed by method-level test snippets."""
    lines: list[str] = []
    for line in test_code.splitlines():
        stripped = line.strip()
        if stripped.startswith("class "):
            break
        lines.append(line)
    prelude = "\n".join(lines).strip()
    return prelude or "import unittest"


def dependency_buckets(methods_info: list[dict]) -> list[str]:
    buckets: list[str] = []
    for method in methods_info:
        deps = method.get("dependencies", [])
        if isinstance(deps, str):
            deps = [deps]
        for dep in deps:
            if dep:
                buckets.append(str(dep))
    return sorted(set(buckets)) or ["unknown"]


def run_method_tests(code: str, methods_info: list[dict], eval_root: Path, prelude: str = "") -> tuple[int, int, list[dict]]:
    details = []
    passed = 0
    total = 0
    prelude = prelude.strip()
    for index, method in enumerate(methods_info):
        test_code = str(method.get("test_code") or "")
        if not test_code.strip():
            continue
        total += 1
        method_name = str(method.get("method_name") or f"method_{index}")
        runnable_test = f"{prelude}\n\n{test_code}" if prelude else test_code
        try:
            ok, output = run_python_test(code, runnable_test, ensure_dir(eval_root / f"method_{index:03d}"))
        except subprocess.TimeoutExpired:
            ok, output = False, "timeout"
        passed += int(ok)
        details.append(
            {
                "method_name": method_name,
                "ok": ok,
                "output": output,
                "dependencies": method.get("dependencies", []),
            }
        )
    return total, passed, details


def count_method_tests(methods_info: list[dict]) -> int:
    return sum(1 for method in methods_info if str(method.get("test_code") or "").strip())


def codebleu_weights(config: dict) -> dict[str, float]:
    configured = config.get("codebleu_weights")
    if not isinstance(configured, dict):
        return dict(DEFAULT_CODEBLEU_WEIGHTS)
    return {
        "bleu": float(configured.get("bleu", DEFAULT_CODEBLEU_WEIGHTS["bleu"])),
        "weighted_bleu": float(configured.get("weighted_bleu", DEFAULT_CODEBLEU_WEIGHTS["weighted_bleu"])),
        "syntax_match": float(configured.get("syntax_match", DEFAULT_CODEBLEU_WEIGHTS["syntax_match"])),
        "dataflow_match": float(configured.get("dataflow_match", DEFAULT_CODEBLEU_WEIGHTS["dataflow_match"])),
    }


def classify_reference_failure(output: str) -> str | None:
    """Classify invalid benchmark executions before scoring candidates."""
    text = str(output or "")
    if not text:
        return "reference_runtime_failure"
    if "ModuleNotFoundError" in text or "ImportError" in text:
        return "missing_dependency"
    if text.strip() == "timeout" or "TimeoutExpired" in text:
        return "reference_timeout"
    if "AssertionError" in text or "FAILED (failures=" in text:
        return "reference_test_inconsistency"
    if "SyntaxError" in text:
        return "reference_syntax_failure"
    return "reference_runtime_failure"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", required=True)
    args = parser.parse_args()

    config = read_config(resolve_in_project(args.config))
    artifact_dir = resolve_in_project(config["artifact_dir"])
    run_dir = resolve_in_project(config["run_dir"])
    manifest = selected_items(read_json(artifact_dir / "manifest.json"), config)
    cb_weights = codebleu_weights(config)
    results = []
    reference_results = []

    for item in manifest:
        sample_dir = resolve_in_project(item["sample_dir"])
        test_code = (sample_dir / "class_test.py").read_text(encoding="utf-8")
        prelude = test_prelude(test_code)
        task = read_json(sample_dir / "task.json")
        methods_info = task.get("methods_info", []) if isinstance(task, dict) else []
        buckets = dependency_buckets(methods_info)
        summary_control = read_json(sample_dir / "summary_control_metrics.json") if (sample_dir / "summary_control_metrics.json").exists() else None
        reference_code = (sample_dir / "raw_solution.py").read_text(encoding="utf-8")
        reference_syntax_ok, reference_syntax_error = python_syntax_ok(reference_code)
        reference_class_ok, reference_class_output = (False, "reference syntax failed")
        reference_method_total = count_method_tests(methods_info)
        reference_method_passed = 0
        reference_method_details = []
        if reference_syntax_ok and test_code.strip():
            try:
                reference_class_ok, reference_class_output = run_python_test(
                    reference_code,
                    test_code,
                    ensure_dir(run_dir / item["task_id"] / "_reference_eval"),
                )
            except subprocess.TimeoutExpired:
                reference_class_ok, reference_class_output = False, "timeout"
            reference_method_total, reference_method_passed, reference_method_details = run_method_tests(
                reference_code,
                methods_info,
                ensure_dir(run_dir / item["task_id"] / "_reference_method_eval"),
                prelude,
            )
        reference_codebleu = compute_codebleu(reference_code, reference_code, cb_weights)
        reference_row = {
            "task_id": item["task_id"],
            "index": item.get("index"),
            "syntax_ok": reference_syntax_ok,
            "syntax_error": reference_syntax_error,
            "codebleu": reference_codebleu,
            "codebleu_score": reference_codebleu["score"],
            "class_test_ok": reference_class_ok,
            "test_output": reference_class_output,
            "method_tests_total": reference_method_total,
            "method_tests_passed": reference_method_passed,
            "method_test_pass_rate": (reference_method_passed / reference_method_total) if reference_method_total else None,
            "method_test_results": reference_method_details,
            "evaluation_available": reference_class_ok,
            "evaluation_unavailable_reason": None if reference_class_ok else classify_reference_failure(reference_class_output),
        }
        reference_results.append(reference_row)
        for condition in config.get("conditions", []):
            output_path = run_dir / item["task_id"] / condition / "output.txt"
            if not output_path.exists():
                continue
            code = extract_code_block(output_path.read_text(encoding="utf-8"))
            llm_usage = read_metadata(output_path.parent / "call_metadata.json")
            spl_conditions = {
                "spl_only",
                "spl_scaffold",
                "skeleton_spl",
                "spl_only_compact",
                "skeleton_spl_compact",
            }
            spl_usage = read_metadata(sample_dir / "spl_metadata.json") if condition in spl_conditions else None
            summary_usage = (
                read_metadata(sample_dir / "free_summary_metadata.json")
                if condition == "free_summary"
                else read_metadata(sample_dir / "structured_summary_metadata.json")
                if condition == "structured_summary"
                else None
            )
            syntax_ok, syntax_error = python_syntax_ok(code)
            codebleu = compute_codebleu(reference_code, code, cb_weights)
            test_ok, test_output = (False, "syntax failed")
            method_total = count_method_tests(methods_info)
            method_passed = 0
            method_details = []
            if syntax_ok and test_code.strip():
                try:
                    test_ok, test_output = run_python_test(code, test_code, ensure_dir(output_path.parent / "eval"))
                except subprocess.TimeoutExpired:
                    test_ok, test_output = False, "timeout"
                method_total, method_passed, method_details = run_method_tests(
                    code,
                    methods_info,
                    ensure_dir(output_path.parent / "method_eval"),
                    prelude,
                )
            results.append(
                {
                    "task_id": item["task_id"],
                    "index": item.get("index"),
                    "condition": condition,
                    "dependency_buckets": buckets,
                    "syntax_ok": syntax_ok,
                    "syntax_error": syntax_error,
                    "codebleu": codebleu,
                    "codebleu_score": codebleu["score"],
                    "class_test_ok": test_ok,
                    "pass_at_1": test_ok,
                    "reference_class_test_ok": reference_class_ok,
                    "reference_method_test_pass_rate": reference_row["method_test_pass_rate"],
                    "evaluation_available": reference_class_ok,
                    "evaluation_status": "valid" if reference_class_ok else "reference_failed_same_environment",
                    "evaluation_unavailable_reason": None if reference_class_ok else classify_reference_failure(reference_class_output),
                    "test_output": test_output,
                    "method_tests_total": method_total,
                    "method_tests_passed": method_passed,
                    "method_test_pass_rate": (method_passed / method_total) if method_total else None,
                    "method_test_results": method_details,
                    "llm_usage": llm_usage,
                    "spl_usage": spl_usage,
                    "summary_usage": summary_usage,
                    "summary_control_metrics": summary_control,
                }
            )

    write_json(run_dir / "reference_evaluation.json", reference_results)
    write_json(run_dir / "evaluation.json", results)
    by_condition: dict[str, dict] = {}
    for row in results:
        stats = by_condition.setdefault(
            row["condition"],
            {
                "outputs": 0,
                "syntax_passes": 0,
                "class_test_passes": 0,
                "valid_evaluations": 0,
                "valid_class_test_passes": 0,
                "method_tests_total": 0,
                "method_tests_passed": 0,
                "codebleu_score_sum": 0.0,
                "codebleu_bleu_sum": 0.0,
                "codebleu_weighted_bleu_sum": 0.0,
                "codebleu_syntax_match_sum": 0.0,
                "codebleu_dataflow_match_sum": 0.0,
            },
        )
        stats["outputs"] += 1
        stats["syntax_passes"] += int(row["syntax_ok"])
        stats["class_test_passes"] += int(row["class_test_ok"])
        stats["valid_evaluations"] += int(row["evaluation_available"])
        stats["valid_class_test_passes"] += int(row["evaluation_available"] and row["class_test_ok"])
        stats["method_tests_total"] += int(row["method_tests_total"])
        stats["method_tests_passed"] += int(row["method_tests_passed"])
        codebleu = row.get("codebleu") or {}
        stats["codebleu_score_sum"] += float(codebleu.get("score") or 0.0)
        stats["codebleu_bleu_sum"] += float(codebleu.get("bleu") or 0.0)
        stats["codebleu_weighted_bleu_sum"] += float(codebleu.get("weighted_bleu") or 0.0)
        stats["codebleu_syntax_match_sum"] += float(codebleu.get("syntax_match") or 0.0)
        stats["codebleu_dataflow_match_sum"] += float(codebleu.get("dataflow_match") or 0.0)
    for stats in by_condition.values():
        total = stats["outputs"] or 1
        method_total = stats["method_tests_total"]
        stats["syntax_pass_rate"] = stats["syntax_passes"] / total
        stats["class_test_pass_rate"] = stats["class_test_passes"] / total
        valid_total = stats["valid_evaluations"]
        stats["valid_class_test_pass_rate"] = (
            stats["valid_class_test_passes"] / valid_total if valid_total else None
        )
        stats["pass_at_1"] = stats["class_test_pass_rate"]
        stats["method_test_pass_rate"] = (stats["method_tests_passed"] / method_total) if method_total else None
        stats["avg_codebleu"] = stats["codebleu_score_sum"] / total
        stats["avg_codebleu_bleu"] = stats["codebleu_bleu_sum"] / total
        stats["avg_codebleu_weighted_bleu"] = stats["codebleu_weighted_bleu_sum"] / total
        stats["avg_codebleu_syntax_match"] = stats["codebleu_syntax_match_sum"] / total
        stats["avg_codebleu_dataflow_match"] = stats["codebleu_dataflow_match_sum"] / total
        for key in [
            "codebleu_score_sum",
            "codebleu_bleu_sum",
            "codebleu_weighted_bleu_sum",
            "codebleu_syntax_match_sum",
            "codebleu_dataflow_match_sum",
        ]:
            stats.pop(key, None)
    write_json(run_dir / "summary.json", by_condition)
    control_by_task = {
        row["task_id"]: row["summary_control_metrics"]
        for row in results
        if row.get("summary_control_metrics")
    }
    control_rows = list(control_by_task.values())
    if control_rows:
        write_json(
            run_dir / "summary_control_metrics.json",
            {
                "samples": len(control_rows),
                "structured_summary_token_control_ok_rate": sum(int(row.get("structured_summary_token_control_ok", False)) for row in control_rows) / len(control_rows),
                "avg_structured_summary_to_spl_token_ratio": sum(float(row.get("structured_summary_to_spl_token_ratio") or 0.0) for row in control_rows) / len(control_rows),
                "avg_free_summary_to_spl_token_ratio": sum(float(row.get("free_summary_to_spl_token_ratio") or 0.0) for row in control_rows) / len(control_rows),
                "note": "Unique task-level summary/SPL token-budget audit.",
            },
        )
    write_json(
        run_dir / "statistics.json",
        {
            "wilson_95ci": binary_condition_statistics(results, ["syntax_ok", "class_test_ok", "pass_at_1"]),
            "paired_deltas": paired_binary_deltas(
                results,
                [("free_summary", "spl_only"), ("structured_summary", "spl_only"), ("skeleton_holistic", "skeleton_spl")],
                ["syntax_ok", "class_test_ok", "pass_at_1"],
            ),
        },
    )
    write_json(run_dir / "usage_summary.json", summarize_usage(results))

    # ── Enhanced metrics ──────────────────────────────────────
    # Build task_id -> sample_dir mapping from manifest
    task_sample_map = {item["task_id"]: resolve_in_project(item["sample_dir"]) for item in manifest}
    # generated_code_lines & exact_match per sample
    for row in results:
        output_path = run_dir / row["task_id"] / row["condition"] / "output.txt"
        sample_dir = task_sample_map.get(row["task_id"])
        if output_path.exists():
            code = extract_code_block(output_path.read_text(encoding="utf-8"))
            row["generated_code_lines"] = len(code.splitlines())
            ref_path = sample_dir / "raw_solution.py" if sample_dir else None
            row["exact_match"] = code.strip() == ref_path.read_text(encoding="utf-8").strip() if ref_path and ref_path.exists() else False
        else:
            row["generated_code_lines"] = 0
            row["exact_match"] = False

    # Enhanced statistics
    enhanced_stats: dict[str, Any] = {}
    for cond in config.get("conditions", []):
        if cond not in by_condition:
            continue
        enhanced_stats[cond] = dict(by_condition[cond])

    # Per-condition exact_match_rate and avg generated_code_lines
    for cond in enhanced_stats:
        cond_rows = [r for r in results if r["condition"] == cond]
        n = len(cond_rows)
        exact_hits = sum(1 for r in cond_rows if r.get("exact_match"))
        enhanced_stats[cond]["exact_match_rate"] = exact_hits / n if n else 0.0
        enhanced_stats[cond]["avg_generated_code_lines"] = sum(r.get("generated_code_lines", 0) for r in cond_rows) / n if n else 0.0

    # Bootstrap CI & McNemar for key pairs
    bootstrap_results: dict[str, Any] = {}
    mcnemar_results: dict[str, Any] = {}
    effect_sizes: dict[str, Any] = {}
    pairs = [("free_summary", "spl_only"), ("structured_summary", "spl_only"), ("skeleton_holistic", "skeleton_spl")]
    for baseline, treatment in pairs:
        pair_key = f"{treatment}_minus_{baseline}"
        bootstrap_results[pair_key] = paired_bootstrap_ci(results, baseline, treatment, "pass_at_1")
        mcnemar_results[pair_key] = mcnemar_test(results, baseline, treatment, "pass_at_1")
        effect_sizes[pair_key] = compute_cohens_h_from_rows(results, baseline, treatment, "pass_at_1")

    # Cost summary
    model_name = config.get("model", "deepseek-v4-pro")
    cost_summary = aggregate_cost_summary(results, model=model_name)
    cost_per_pass = compute_cost_per_metric(cost_summary, by_condition, metric_key="pass_at_1", hits_field="class_test_passes")

    # Add cost/sample and cost/pass to enhanced_stats
    for cond in enhanced_stats:
        cs = cost_summary.get(cond, {})
        cpp = cost_per_pass.get(cond, {})
        enhanced_stats[cond]["cost_per_sample_usd"] = cs.get("cost_per_sample_usd", 0.0)
        enhanced_stats[cond]["cost_per_pass_usd"] = cpp.get("cost_per_hit_usd")
        enhanced_stats[cond]["tokens_per_sample"] = cs.get("tokens_per_sample", 0)
        enhanced_stats[cond]["total_cost_usd"] = cs.get("total_cost_usd", 0.0)
        enhanced_stats[cond]["inference_total_tokens"] = cs.get("inference_total_tokens", 0)
        enhanced_stats[cond]["token_overhead_spl_ratio"] = cs.get("token_overhead_spl_ratio", 0.0)

    write_json(run_dir / "enhanced_summary.json", enhanced_stats)
    write_json(run_dir / "cost_summary.json", {"per_condition": cost_summary, "cost_per_pass": cost_per_pass})
    write_json(run_dir / "enhanced_statistics.json", {
        "bootstrap_ci": bootstrap_results,
        "mcnemar_tests": mcnemar_results,
        "effect_sizes_cohens_h": effect_sizes,
        "note": "Bootstrap uses 10K resamples with seed=42. McNemar uses exact binomial test.",
    })

    print(f"Wrote evaluation for {len(results)} ClassEval outputs")
    print(f"Enhanced statistics written to {run_dir / 'enhanced_statistics.json'}")


if __name__ == "__main__":
    main()
