from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from collections import defaultdict
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from common.paths import ensure_dir, read_config, read_json, resolve_in_project, write_json, write_text
from common.project_env import prepend_project_env_to_path
from common.run_utils import selected_items
from common.statistics import binary_condition_statistics, paired_binary_deltas
from common.usage import UsageTotals, read_metadata, summarize_usage
from common.metrics_enhanced import aggregate_cost_summary, compute_cost_per_metric
from common.statistics import (
    benjamini_hochberg,
    compute_cohens_h_from_rows,
    mcnemar_test,
    paired_bootstrap_ci,
)


def normalize(text: str) -> str:
    return " ".join(text.strip().split()).lower()


def load_parse_dependence_output(repo_root: Path):
    scripts_dir = repo_root / "scripts"
    sys.path.insert(0, str(scripts_dir))
    try:
        from parse_response import parse_dependence_output

        return parse_dependence_output
    finally:
        try:
            sys.path.remove(str(scripts_dir))
        except ValueError:
            pass


def task_family(item: dict[str, Any]) -> str:
    family = str(item.get("task_type") or item.get("_task_type") or "").lower()
    if family:
        return "infoflow" if family.startswith("infoflow") else family
    task_id = str(item.get("task_id") or "")
    prefix = task_id.split("_", 1)[0].lower()
    return "infoflow" if prefix.startswith("infoflow") else prefix


def response_mode(item: dict[str, Any]) -> str:
    mode = str(item.get("mode") or item.get("_mode") or "").lower()
    if mode in {"source", "trace"}:
        return mode
    return "trace"


def write_official_response_files(config: dict, manifest: list[dict], run_dir: Path, artifact_dir: Path) -> Path:
    repo_root = resolve_in_project(config.get("core_repo", "datasets/core/repo"))
    parse_dependence_output = load_parse_dependence_output(repo_root)
    response_dir = ensure_dir(run_dir / "official_responses")
    for old_file in response_dir.glob("*.jsonl"):
        old_file.unlink()

    grouped: dict[tuple[str, str, str], list[dict]] = defaultdict(list)
    for item in manifest:
        sample_dir = resolve_in_project(item["sample_dir"])
        raw_item = read_json(sample_dir / "item.json")
        family = task_family({**raw_item, **item})
        mode = response_mode({**raw_item, **item})
        for condition in config.get("conditions", []):
            output_path = run_dir / item["task_id"] / condition / "output.txt"
            if not output_path.exists():
                continue
            output = output_path.read_text(encoding="utf-8")
            response_item = dict(raw_item)
            response_item.setdefault("task_id", raw_item.get("task_id", item["task_id"]))
            response_item["response"] = {
                "raw": output,
                "parsed": parse_dependence_output(output, task_type=family, trace=(mode == "trace")),
            }
            grouped[(condition, family, mode)].append(response_item)

    for (condition, family, mode), rows in grouped.items():
        path = response_dir / f"{condition}_{family}_{mode}.jsonl"
        write_text(path, "".join(json.dumps(row, ensure_ascii=False) + "\n" for row in rows))
    return response_dir


def run_official_eval(config: dict, response_dir: Path, run_dir: Path) -> tuple[bool, str]:
    prepend_project_env_to_path()
    repo_root = resolve_in_project(config.get("core_repo", "datasets/core/repo"))
    script = resolve_in_project(config.get("official_eval_script") or repo_root / "scripts" / "eval.py")
    label_root = resolve_in_project(config.get("official_label_root") or repo_root / "raw_annotation")
    out_root = ensure_dir(run_dir / "official_eval")
    for old_file in out_root.glob("*_eval.jsonl"):
        old_file.unlink()
    lite_path = resolve_in_project(config.get("dataset_path", "datasets/core/repo/lite.json"))
    csv_path = out_root / "summary.csv"

    cmd = [
        sys.executable,
        str(script),
        "-f",
        str(response_dir),
        "-l",
        str(label_root),
        "-o",
        str(out_root),
        "-c",
        str(csv_path),
        "--reeval",
    ]
    if lite_path.exists():
        cmd.extend(["--lite", str(lite_path)])
    eval_env = dict(os.environ)
    eval_env["PYTHONUTF8"] = "1"
    eval_env["PYTHONIOENCODING"] = "utf-8"
    result = subprocess.run(
        cmd,
        cwd=str(script.parent),
        env=eval_env,
        text=True,
        capture_output=True,
        encoding="utf-8",
        errors="replace",
    )
    combined = (result.stdout or "") + (result.stderr or "")
    write_text(run_dir / "official_eval_stdout.txt", combined)
    return result.returncode == 0, combined


def split_eval_stem(stem: str, conditions: list[str]) -> tuple[str, str, str]:
    for condition in sorted(conditions, key=len, reverse=True):
        prefix = f"{condition}_"
        if stem.startswith(prefix):
            remainder = stem[len(prefix) :]
            parts = remainder.split("_")
            mode = parts[-1] if parts else ""
            family = "_".join(parts[:-1]) if len(parts) > 1 else ""
            return condition, family, mode
    parts = stem.split("_")
    return parts[0], "_".join(parts[1:-1]) if len(parts) > 2 else "", parts[-1] if parts else ""


def collect_official_rows(run_dir: Path, conditions: list[str], manifest: list[dict]) -> tuple[list[dict], dict]:
    official_dir = run_dir / "official_eval"
    rows: list[dict] = []
    summary: dict[str, dict] = {}
    by_task = {item["task_id"]: item for item in manifest}
    by_benchmark_mode = {
        (str(item.get("benchmark_task_id") or item["task_id"]), str(item.get("mode", ""))): item
        for item in manifest
    }
    for eval_file in sorted(official_dir.glob("*_eval.jsonl")):
        condition, family, mode = split_eval_stem(eval_file.name.replace("_eval.jsonl", ""), conditions)
        counts = summary.setdefault(
            condition,
            {
                "outputs": 0,
                "correct": 0,
                "strict_correct": 0,
                "parsed": 0,
                "data_total": 0,
                "data_correct": 0,
                "data_strict_correct": 0,
                "control_total": 0,
                "control_correct": 0,
                "control_strict_correct": 0,
                "infoflow_total": 0,
                "infoflow_correct": 0,
                "infoflow_strict_correct": 0,
            },
        )
        for line in eval_file.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            data = json.loads(line)
            eval_data = data.get("response", {}).get("eval", {})
            correct = bool(eval_data.get("correct", eval_data.get("accuracy", 0) == 1))
            parsed = data.get("response", {}).get("parsed") is not None
            strict_correct = correct and parsed
            task_type = data.get("task_id", "").split("_", 1)[0]
            task_type = "infoflow" if task_type.startswith("infoflow") else task_type
            benchmark_task_id = str(data.get("task_id", ""))
            manifest_item = by_benchmark_mode.get(
                (benchmark_task_id, mode),
                by_task.get(benchmark_task_id, {}),
            )
            sample_dir = resolve_in_project(manifest_item["sample_dir"]) if manifest_item.get("sample_dir") else None
            run_task_id = str(manifest_item.get("task_id") or benchmark_task_id)
            usage_dir = run_dir / run_task_id / condition
            llm_usage = (
                read_metadata(usage_dir / "generation_attempts.json")
                or read_metadata(usage_dir / "call_metadata.json")
            )
            spl_usage = read_metadata(sample_dir / "spl_metadata.json") if sample_dir and condition in {"spl", "spl_only", "raw_spl", "raw_spl_retrieved", "raw_spl_reasoned", "raw_spl_controlled"} else None
            summary_usage = (
                read_metadata(sample_dir / "free_summary_metadata.json")
                if sample_dir and condition in {"nl_summary", "raw_free_summary"}
                else read_metadata(sample_dir / "structured_summary_metadata.json")
                if sample_dir and condition in {"structured_summary", "raw_structured_summary"}
                else None
            )
            row = {
                "task_id": data.get("task_id"),
                "condition": condition,
                "task_type": task_type or family,
                "mode": mode,
                "correct": correct,
                "strict_correct": strict_correct,
                "parsed": parsed,
                "official_eval": eval_data,
                "llm_usage": llm_usage,
                "spl_usage": spl_usage,
                "summary_usage": summary_usage,
            }
            rows.append(row)
            counts["outputs"] += 1
            counts["correct"] += int(correct)
            counts["strict_correct"] += int(strict_correct)
            counts["parsed"] += int(parsed)
            if row["task_type"] in {"data", "control", "infoflow"}:
                counts[f"{row['task_type']}_total"] += 1
                counts[f"{row['task_type']}_correct"] += int(correct)
                counts[f"{row['task_type']}_strict_correct"] += int(strict_correct)
    for stats in summary.values():
        total = stats["outputs"] or 1
        stats["overall_accuracy"] = stats["correct"] / total
        stats["strict_overall_accuracy"] = stats["strict_correct"] / total
        stats["parse_success_rate"] = stats["parsed"] / total
        for task_type in ("data", "control", "infoflow"):
            denom = stats[f"{task_type}_total"]
            stats[f"{task_type}_accuracy"] = (stats[f"{task_type}_correct"] / denom) if denom else None
            stats[f"{task_type}_strict_accuracy"] = (stats[f"{task_type}_strict_correct"] / denom) if denom else None
    return rows, summary


def fallback_eval(config: dict, manifest: list[dict], run_dir: Path) -> tuple[list[dict], dict]:
    rows = []
    summary: dict[str, dict] = {}
    for item in manifest:
        gold = normalize((resolve_in_project(item["sample_dir"]) / "gold.txt").read_text(encoding="utf-8"))
        for condition in config.get("conditions", []):
            output_path = run_dir / item["task_id"] / condition / "output.txt"
            if not output_path.exists():
                continue
            pred = normalize(output_path.read_text(encoding="utf-8"))
            exact = pred == gold
            sample_dir = resolve_in_project(item["sample_dir"])
            summary_control = read_json(sample_dir / "summary_control_metrics.json") if (sample_dir / "summary_control_metrics.json").exists() else None
            rows.append(
                {
                    "task_id": item["task_id"],
                    "index": item.get("index"),
                    "condition": condition,
                    "exact_match": exact,
                    "strict_correct": exact,
                    "parsed": True,
                    "gold": gold,
                    "pred": pred,
                    "official_eval_used": False,
                    "llm_usage": (
                        read_metadata(output_path.parent / "generation_attempts.json")
                        or read_metadata(output_path.parent / "call_metadata.json")
                    ),
                    "spl_usage": read_metadata(sample_dir / "spl_metadata.json") if condition in {"spl", "spl_only", "raw_spl", "raw_spl_retrieved", "raw_spl_reasoned", "raw_spl_controlled"} else None,
                    "summary_usage": (
                        read_metadata(sample_dir / "free_summary_metadata.json")
                        if condition in {"nl_summary", "raw_free_summary"}
                        else read_metadata(sample_dir / "structured_summary_metadata.json")
                        if condition in {"structured_summary", "raw_structured_summary"}
                        else None
                    ),
                    "summary_control_metrics": summary_control,
                }
            )
            stats = summary.setdefault(condition, {"outputs": 0, "correct": 0})
            stats["outputs"] += 1
            stats["correct"] += int(exact)
    for stats in summary.values():
        stats["overall_accuracy"] = stats["correct"] / (stats["outputs"] or 1)
    return rows, summary


def write_summary_control_report(run_dir: Path, manifest: list[dict]) -> None:
    control_rows = []
    for item in manifest:
        sample_dir = resolve_in_project(item["sample_dir"])
        path = sample_dir / "summary_control_metrics.json"
        if path.exists():
            control_rows.append(read_json(path))
    if not control_rows:
        return
    write_json(
        run_dir / "summary_control_metrics.json",
        {
            "samples": len(control_rows),
            "structured_summary_token_control_ok_rate": sum(int(row.get("structured_summary_token_control_ok", False)) for row in control_rows) / len(control_rows),
            "avg_structured_summary_to_spl_token_ratio": sum(float(row.get("structured_summary_to_spl_token_ratio") or 0.0) for row in control_rows) / len(control_rows),
            "avg_free_summary_to_spl_token_ratio": sum(float(row.get("free_summary_to_spl_token_ratio") or 0.0) for row in control_rows) / len(control_rows),
            "avg_compressed_raw_to_spl_token_ratio": sum(float(row.get("compressed_raw_to_spl_token_ratio") or 0.0) for row in control_rows) / len(control_rows),
            "note": "Rough token counts use char_count/4. Use tokenizer-specific counts before reporting final budget-control claims.",
        },
    )


def write_main_and_diagnostic_summaries(config: dict, run_dir: Path, summary: dict) -> None:
    default_main = ["official_raw", "raw_free_summary", "raw_structured_summary", "raw_spl"]
    main_conditions = [str(condition) for condition in config.get("main_table_conditions", default_main)]
    diagnostic_conditions = [
        str(condition)
        for condition in config.get(
            "diagnostic_conditions",
            [condition for condition in config.get("conditions", []) if condition not in main_conditions],
        )
    ]
    write_json(
        run_dir / "main_summary.json",
        {
            condition: summary[condition]
            for condition in main_conditions
            if condition in summary
        },
    )
    write_json(
        run_dir / "diagnostic_summary.json",
        {
            condition: summary[condition]
            for condition in diagnostic_conditions
            if condition in summary
        },
    )
    write_json(
        run_dir / "reporting_policy.json",
        {
            "main_table_conditions": main_conditions,
            "diagnostic_conditions": diagnostic_conditions,
            "primary_spl_method": "raw_spl",
            "note": (
                "CoRe questions often depend on exact raw-code line numbers. "
                "The main table treats raw code as the authoritative line anchor "
                "and evaluates SPL as an auxiliary semantic view. spl_only is a "
                "diagnostic ablation unless SPL is augmented with reliable line anchors."
            ),
        },
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", required=True)
    args = parser.parse_args()

    config = read_config(resolve_in_project(args.config))
    run_dir = ensure_dir(resolve_in_project(config["run_dir"]))
    artifact_dir = resolve_in_project(config["artifact_dir"])
    manifest = selected_items(read_json(artifact_dir / "manifest.json"), config)

    if config.get("use_official_eval", True):
        try:
            response_dir = write_official_response_files(config, manifest, run_dir, artifact_dir)
            ok, _output = run_official_eval(config, response_dir, run_dir)
            rows, summary = collect_official_rows(run_dir, list(config.get("conditions", [])), manifest)
            write_json(run_dir / "evaluation.json", rows)
            write_json(run_dir / "summary.json", summary)
            write_main_and_diagnostic_summaries(config, run_dir, summary)
            write_json(
                run_dir / "statistics.json",
                {
                    "wilson_95ci": binary_condition_statistics(rows, ["correct", "strict_correct", "parsed"]),
                    "paired_deltas": paired_binary_deltas(
                        rows,
                        [("official_raw", "raw_spl"), ("raw_free_summary", "raw_spl"), ("raw_structured_summary", "raw_spl"), ("compressed_raw", "spl_only")],
                        ["correct", "strict_correct", "parsed"],
                    ),
                },
            )
            write_json(run_dir / "usage_summary.json", summarize_usage(rows))
            _write_usage_layers(rows, manifest, run_dir)
            write_summary_control_report(run_dir, manifest)
            write_json(run_dir / "official_eval_status.json", {"ok": ok, "response_dir": str(response_dir)})
            _write_enhanced_stats(rows, summary, run_dir, config)
            print(f"Wrote official CoRe evaluation for {len(rows)} outputs")
            return
        except Exception as exc:
            write_json(run_dir / "official_eval_status.json", {"ok": False, "error": repr(exc)})
            if not config.get("allow_fallback_eval", True):
                raise

    rows, summary = fallback_eval(config, manifest, run_dir)
    write_json(run_dir / "evaluation.json", rows)
    write_json(run_dir / "summary.json", summary)
    write_main_and_diagnostic_summaries(config, run_dir, summary)
    write_json(
        run_dir / "statistics.json",
        {
            "wilson_95ci": binary_condition_statistics(rows, ["exact_match"]),
            "paired_deltas": paired_binary_deltas(rows, [("official_raw", "raw_spl"), ("compressed_raw", "spl_only")], ["exact_match"]),
        },
    )
    write_json(run_dir / "usage_summary.json", summarize_usage(rows))
    _write_usage_layers(rows, manifest, run_dir)
    write_summary_control_report(run_dir, manifest)
    _write_enhanced_stats(rows, summary, run_dir, config)
    print(f"Wrote fallback exact-match evaluation for {len(rows)} CoRe outputs")


def _write_usage_layers(rows: list[dict], manifest: list[dict], run_dir: Path) -> None:
    """Keep per-task inference separate from the one-time SPL construction."""
    inference_rows = [
        {
            "condition": row.get("condition"),
            "llm_usage": row.get("llm_usage"),
        }
        for row in rows
    ]
    spl_build = UsageTotals()
    for item in manifest:
        sample_dir = resolve_in_project(item["sample_dir"])
        spl_build.add(read_metadata(sample_dir / "spl_metadata.json"))
    write_json(run_dir / "usage_layers.json", {
        "inference_by_condition": summarize_usage(inference_rows),
        "one_time_spl_build": spl_build.to_dict(),
        "legacy_combined_by_condition": summarize_usage(rows),
        "note": (
            "The legacy combined view adds a sample's SPL build to its SPL condition. "
            "Use inference_by_condition for fair per-task inference comparison and "
            "one_time_spl_build for separately reported construction cost."
        ),
    })


def _write_enhanced_stats(rows: list[dict], summary: dict, run_dir: Path, config: dict) -> None:
    """Write enhanced statistics (bootstrap, McNemar, BH/FDR, effect size, cost)."""
    present = {str(row.get("condition", "")) for row in rows}
    configured = [str(condition) for condition in config.get("conditions", []) if str(condition) in present]
    candidates = [
        ("official_raw", "raw_spl_controlled"),
        ("official_raw", "raw_spl"),
        ("compressed_raw", "spl_only"),
        ("raw_free_summary", "raw_spl"),
        ("raw_structured_summary", "raw_spl"),
    ]
    if len(configured) == 2:
        candidates.insert(0, (configured[0], configured[1]))
    pairs = []
    for pair in candidates:
        if pair[0] in present and pair[1] in present and pair not in pairs:
            pairs.append(pair)
    metric = "correct" if any("correct" in r for r in rows) else "exact_match"
    bootstrap_results: dict[str, Any] = {}
    mcnemar_results: dict[str, Any] = {}
    effect_sizes: dict[str, Any] = {}

    for baseline, treatment in pairs:
        pk = f"{treatment}_minus_{baseline}"
        bootstrap_results[pk] = paired_bootstrap_ci(rows, baseline, treatment, metric)
        mcnemar_results[pk] = mcnemar_test(rows, baseline, treatment, metric)
        effect_sizes[pk] = compute_cohens_h_from_rows(rows, baseline, treatment, metric)

    mcnemar_pvals = [(pk, mcnemar_results[pk].get("p_value") or 1.0) for pk in mcnemar_results]
    bh_result = benjamini_hochberg([(n, p) for n, p in mcnemar_pvals if p is not None])

    write_json(run_dir / "enhanced_statistics.json", {
        "bootstrap_ci": bootstrap_results,
        "mcnemar_tests": mcnemar_results,
        "bh_fdr_correction": bh_result,
        "effect_sizes_cohens_h": effect_sizes,
        "note": "Bootstrap 10K resamples, seed=42.",
    })

    model_name = config.get("model", "deepseek-v4-pro")
    cost_summary = aggregate_cost_summary(rows, model=model_name)
    cost_per_correct = compute_cost_per_metric(cost_summary, summary, metric_key="correct")
    write_json(run_dir / "cost_summary.json", {"per_condition": cost_summary, "cost_per_correct": cost_per_correct})


if __name__ == "__main__":
    main()
