"""Build the package's headline result tables from the frozen run records.

The tables under ``data/results_tables/`` are derived, never hand-written: each row is
summed from the per-run ``usage_summary.json`` and ``metrics_by_mode.json`` that
the harness wrote, so a reader can trace any figure back to the run that
produced it.  Re-running this script regenerates every table.

Two counting conventions exist in the frozen records and they disagree on the
call count:

* ``usage_summary.json`` -> ``calls`` counts every LLM request the run made,
  including retries and auxiliary traffic.
* ``cost_summary.json`` -> ``llm_usage_calls`` counts only the requests the
  cost model could attribute to a priced model.

The tables report the ``usage_summary`` figure, because that is the one the
experiment reports quote; the cost columns come from ``cost_summary``.

A unit whose baseline was unavailable still counts as a sampled task, so the
denominator is ``resolved_total + unavailable_outputs`` rather than the number
of units the evaluator managed to score.

Usage:
    build_tables.py [--package DIR]
"""

from __future__ import annotations

import argparse
import csv
import json
import os
import sys
from pathlib import Path

DEFAULT_PACKAGE = Path(__file__).resolve().parents[2]

EXP3_CONDITIONS = [
    # (label in the table, path under data/raw_results/exp3_swebench)
    ("random218_compact", "random218_compact"),
    ("random218_budget_aligned", "random218_budget_aligned"),
    ("random218_untagged_both", "random218_untagged_both"),
    ("budget_relaxation_80step_stratified30",
     "budget_relaxation_80step_stratified30"),
    ("random218_full_semantic_summary", "random218_full_semantic_summary"),
]


def extended(path) -> str:
    """The path carrying the Windows extended-length prefix.

    SWE-bench instance ids push recorded paths past the Win32 limit, where the
    plain API silently fails to open them.
    """
    text = str(path)
    if os.name != "nt" or text.startswith("\\\\?\\"):
        return text
    return "\\\\?\\" + str(Path(text).absolute())



def load(path: Path):
    with open(extended(str(path)), "rb") as handle:
        return json.loads(handle.read().decode("utf-8"))


def number(text: str, cast):
    """Cast a CSV cell, leaving blanks and unparsable text as written."""
    text = (text or "").strip()
    if not text:
        return ""
    try:
        return cast(text)
    except ValueError:
        return text


def write_csv(path: Path, fieldnames: list[str], rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    print(f"  wrote {path.name}: {len(rows)} rows")


# --------------------------------------------------------------------------- #
# Experiment 1 -- ClassEval reconstruction, five models x four conditions
# --------------------------------------------------------------------------- #

def exp1(package: Path, out: Path) -> None:
    source = (package / "data/results/exp1_classeval/model_comparison"
              / "exp1_full100_results.csv")
    with open(extended(str(source)), "r", encoding="utf-8-sig") as handle:
        rows = list(csv.DictReader(handle))

    columns = [
        ("model", "model", str),
        ("condition", "condition", str),
        ("samples", "samples", int),
        ("syntax_passes", "syntax_passes", int),
        ("syntax_pass_rate", "syntax_pass_rate", float),
        ("class_passes", "class_passes", int),
        ("valid_evaluations", "valid_evaluations", int),
        ("valid_class_pass_rate", "valid_class_pass_rate", float),
        ("method_tests_passed", "method_tests_passed", int),
        ("method_tests_total", "method_tests_total", int),
        ("method_test_pass_rate", "method_test_pass_rate", float),
        ("avg_codebleu", "avg_codebleu", float),
    ]
    table = []
    for row in rows:
        table.append({out_name: number(row[src_name], cast)
                      for out_name, src_name, cast in columns})
    table.sort(key=lambda r: (r["model"], r["condition"]))
    write_csv(out / "table1_rq1_classeval_main.csv",
              [name for name, _, _ in columns], table)

    # Calls, tokens and cost are recorded once per model run, not per condition,
    # so they belong in their own table rather than repeated down every row.
    totals = {}
    for row in rows:
        totals.setdefault(row["model"], {
            "model": row["model"],
            "samples": number(row["samples"], int),
            "llm_calls": number(row["model_final_all_llm_calls"], int),
            "total_tokens": number(row["model_final_all_llm_tokens"], int),
            "llm_cost_usd": number(row["model_final_all_llm_cost_usd"], float),
            "pipeline_wall_seconds":
                number(row["pipeline_wall_seconds"], float),
        })
    total_rows = [totals[k] for k in sorted(totals)]
    write_csv(out / "exp1_classeval_run_totals.csv",
              list(total_rows[0].keys()), total_rows)

    significance = (package / "data/results/exp1_classeval/model_comparison"
                    / "exp1_full100_significance.csv")
    with open(extended(str(significance)), "r", encoding="utf-8-sig") as handle:
        sig_rows = list(csv.DictReader(handle))
    keep = ["model", "test", "spl_condition", "baseline_condition",
            "paired_samples", "both_pass", "spl_only_pass",
            "baseline_only_pass", "both_fail", "spl_passes", "baseline_passes",
            "absolute_difference_percentage_points", "p_value_raw",
            "p_value_holm", "significant_holm_0_05"]
    write_csv(out / "exp1_classeval_significance.csv", keep,
              [{k: r[k] for k in keep} for r in sig_rows])


def exp1_ablation(package: Path, out: Path) -> None:
    """Tagged versus compact SPL, per model, on the ClassEval sample."""
    root = package / "data/raw_results/exp1_classeval/model_runs"
    table = []
    for model_dir in sorted(p for p in root.iterdir() if p.is_dir()):
        source = (model_dir / "full100_spl_structure_ablation"
                  / "structure_ablation_comparison.json")
        if not source.exists():
            continue
        record = load(source)
        for name, block in record.get("conditions", {}).items():
            raw = block.get("raw_n100", {})
            valid = block.get("valid_only", {})
            table.append({
                "model": model_dir.name,
                "condition": name,
                "tagged_condition": block.get("tagged_condition"),
                "compact_condition": block.get("compact_condition"),
                "n_raw": raw.get("n"),
                "tagged_passes_raw": raw.get("tagged_passes"),
                "compact_passes_raw": raw.get("compact_passes"),
                "delta_raw": raw.get("delta_tagged_minus_compact"),
                "mcnemar_p_raw": (raw.get("mcnemar") or {}).get("p_value"),
                "n_valid": valid.get("n"),
                "tagged_passes_valid": valid.get("tagged_passes"),
                "compact_passes_valid": valid.get("compact_passes"),
                "delta_valid": valid.get("delta_tagged_minus_compact"),
                "mcnemar_p_valid": (valid.get("mcnemar") or {}).get("p_value"),
            })
    if not table:
        print("  !! no structure-ablation records found")
        return
    table.sort(key=lambda r: (r["model"], r["condition"]))
    write_csv(out / "tableC1_rq1_structure_ablation.csv",
              list(table[0].keys()), table)


# --------------------------------------------------------------------------- #
# Experiment 2 -- core reasoning, DeepSeek-V4-Pro across four conditions
# --------------------------------------------------------------------------- #

def exp2(package: Path, out: Path) -> None:
    root = package / "data/results/exp2_core"
    table = []
    for run in sorted(p for p in root.iterdir() if p.is_dir()):
        summary = load(run / "summary.json")
        usage = load(run / "usage_summary.json")
        cost = load(run / "cost_summary.json")
        for condition in summary:
            metrics = summary[condition]
            used = usage.get(condition, {})
            spent = cost.get("per_condition", {}).get(condition, {})
            per_hit = cost.get("cost_per_resolved", {}).get(condition, {})
            table.append({
                "run": run.name,
                "condition": condition,
                "outputs": metrics.get("outputs"),
                "parsed": metrics.get("parsed"),
                "parse_success_rate": metrics.get("parse_success_rate"),
                "correct": metrics.get("correct"),
                "strict_correct": metrics.get("strict_correct"),
                "strict_overall_accuracy": metrics.get("strict_overall_accuracy"),
                "data_correct": metrics.get("data_correct"),
                "data_total": metrics.get("data_total"),
                "data_strict_accuracy": metrics.get("data_strict_accuracy"),
                "control_correct": metrics.get("control_correct"),
                "control_total": metrics.get("control_total"),
                "infoflow_correct": metrics.get("infoflow_correct"),
                "infoflow_total": metrics.get("infoflow_total"),
                "infoflow_strict_accuracy": metrics.get("infoflow_strict_accuracy"),
                "llm_calls": used.get("calls"),
                "input_tokens": used.get("input_tokens"),
                "output_tokens": used.get("output_tokens"),
                "reasoning_tokens": used.get("reasoning_tokens"),
                "total_tokens": used.get("total_tokens"),
                "elapsed_seconds": used.get("elapsed_seconds"),
                "total_cost_usd": spent.get("total_cost_usd"),
                "cost_per_correct_usd": per_hit.get("cost_per_hit_usd"),
            })
    table.sort(key=lambda r: (r["run"], r["condition"]))
    write_csv(out / "table2_rq2_core_main.csv", list(table[0].keys()), table)


# --------------------------------------------------------------------------- #
# Experiment 3 -- SWE-bench Lite under mini-swe-agent
# --------------------------------------------------------------------------- #

def exp3_collect(runs_dir: Path) -> dict[str, dict]:
    """Sum one run directory's per-condition usage and outcomes.

    A run tree either keeps its aggregates beside itself (the single-run
    supplements) or one level down, under each sampled unit.
    """
    if (runs_dir / "usage_summary.json").exists():
        entries = [runs_dir]
    else:
        entries = sorted(p for p in runs_dir.iterdir() if p.is_dir())

    totals: dict[str, dict] = {}
    for entry in entries:
        if not entry.is_dir():
            continue
        usage_file = entry / "usage_summary.json"
        metrics_file = entry / "metrics_by_mode.json"
        cost_file = entry / "cost_summary.json"
        if not usage_file.exists():
            continue
        usage = load(usage_file)
        metrics = load(metrics_file) if metrics_file.exists() else {}
        cost = load(cost_file).get("per_condition", {}) \
            if cost_file.exists() else {}
        for condition, used in usage.items():
            bucket = totals.setdefault(condition, {
                "calls": 0, "input_tokens": 0, "output_tokens": 0,
                "reasoning_tokens": 0, "total_tokens": 0,
                "elapsed_seconds": 0.0, "total_cost_usd": None,
                "outputs": 0, "unavailable_outputs": 0,
                "patch_generated_hits": 0,
                "resolved_total": 0, "resolved_hits": 0,
            })
            for key in ("calls", "input_tokens", "output_tokens",
                        "reasoning_tokens", "total_tokens"):
                bucket[key] += used.get(key, 0) or 0
            bucket["elapsed_seconds"] += used.get("elapsed_seconds", 0) or 0
            # A run whose model had no price attached records a null cost; that
            # is "not measured", which must not read as "free".
            spent = (cost.get(condition) or {}).get("total_cost_usd")
            if spent is not None:
                bucket["total_cost_usd"] = (bucket["total_cost_usd"] or 0) + spent
            seen = metrics.get(condition, {})
            for key in ("outputs", "unavailable_outputs",
                        "patch_generated_hits", "resolved_total",
                        "resolved_hits"):
                bucket[key] += seen.get(key, 0) or 0
    return totals


def exp3(package: Path, out: Path) -> None:
    root = package / "data/raw_results/exp3_swebench"
    table = []
    for label, relative in EXP3_CONDITIONS:
        base = root / relative
        # Two layouts: one tree per sampled unit, or a single run tree.
        units = base / "units"
        if units.is_dir():
            totals: dict[str, dict] = {}
            for unit in sorted(p for p in units.iterdir() if p.is_dir()):
                # The unit aggregates sit either beside the unit or in runs/.
                for candidate in (unit, unit / "runs"):
                    if (candidate / "usage_summary.json").exists():
                        runs = candidate
                        break
                else:
                    continue
                for condition, bucket in exp3_collect(runs).items():
                    if condition not in totals:
                        totals[condition] = dict(bucket)
                    else:
                        for key, value in bucket.items():
                            totals[condition][key] += value
        else:
            totals = exp3_collect(base / "runs")

        for condition in sorted(totals):
            bucket = totals[condition]
            # A unit whose baseline was unavailable still belongs to the sample:
            # it is an unresolved task, not a missing one.
            tasks = bucket["resolved_total"] + bucket["unavailable_outputs"]
            table.append({
                "arm": label,
                "condition": condition,
                "tasks_sampled": tasks,
                "patches_generated": bucket["patch_generated_hits"],
                "evaluated": bucket["resolved_total"],
                "unavailable": bucket["unavailable_outputs"],
                "resolved": bucket["resolved_hits"],
                "resolved_rate_of_sampled":
                    round(bucket["resolved_hits"] / tasks, 6) if tasks else "",
                "resolved_rate_of_evaluated":
                    round(bucket["resolved_hits"] / bucket["resolved_total"], 6)
                    if bucket["resolved_total"] else "",
                "llm_calls": bucket["calls"],
                "input_tokens": bucket["input_tokens"],
                "output_tokens": bucket["output_tokens"],
                "reasoning_tokens": bucket["reasoning_tokens"],
                "total_tokens": bucket["total_tokens"],
                "elapsed_hours": round(bucket["elapsed_seconds"] / 3600, 2),
                "total_cost_usd": (round(bucket["total_cost_usd"], 4)
                                   if bucket["total_cost_usd"] is not None else ""),
            })
    write_csv(out / "table3_rq3_swebench_main.csv", list(table[0].keys()), table)

    # The frozen analyses that shipped with the runs are the reference for the
    # figures above; compare against them so a silent counting drift shows up.
    exp3_verify(package)


def exp3_verify(package: Path) -> None:
    reference = {
        ("random218_compact", "miniswe_original"): (114, 76390942),
        ("random218_compact", "miniswe_free_summary"): (118, 78098072),
        ("random218_compact", "miniswe_spl_localization"): (141, 42852228),
        ("random218_compact", "miniswe_spl_repair"): (143, 46051675),
        ("random218_compact", "miniswe_spl_both"): (138, 43637276),
        ("random218_untagged_both", "miniswe_spl_unstructured_both"):
            (139, 41541787),
    }
    table = out_path = package / "data/results_tables/table3_rq3_swebench_main.csv"
    with open(extended(str(out_path)), "r", encoding="utf-8") as handle:
        rows = {(r["arm"], r["condition"]): r for r in csv.DictReader(handle)}
    mismatches = 0
    for key, (resolved, tokens) in reference.items():
        row = rows.get(key)
        if row is None:
            print(f"  !! missing row {key}")
            mismatches += 1
            continue
        if int(row["resolved"]) != resolved or int(row["total_tokens"]) != tokens:
            print(f"  !! {key}: got {row['resolved']}/{row['total_tokens']}, "
                  f"frozen analysis says {resolved}/{tokens}")
            mismatches += 1
    print(f"  cross-checked {len(reference)} frozen rows, "
          f"{mismatches} mismatch(es)")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--package", default=str(DEFAULT_PACKAGE))
    args = parser.parse_args()

    package = Path(args.package)
    if not package.is_dir():
        sys.exit(f"not a directory: {package}")
    out = package / "data/results_tables"

    print("building headline tables")
    exp1(package, out)
    exp1_ablation(package, out)
    exp2(package, out)
    exp3(package, out)
    print("done")


if __name__ == "__main__":
    main()
