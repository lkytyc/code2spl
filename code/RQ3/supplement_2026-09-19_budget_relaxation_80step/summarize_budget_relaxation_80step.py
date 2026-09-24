from __future__ import annotations

import csv
import json
import math
from collections import defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
EXP = ROOT
RUN = EXP / "data/raw_results/exp3_swebench/budget_relaxation_80step_stratified30"
EVAL80 = RUN / "runs/evaluation.json"
AUDIT = RUN / "selection_audit.json"
BASE36 = EXP / "data/raw_results/exp3_swebench/random218_compact/units"
SEM36 = EXP / "data/raw_results/exp3_swebench/random218_full_semantic_summary/runs/evaluation.json"

METHODS = [
    ("miniswe_original", "Original"),
    ("miniswe_free_summary", "Free Summary"),
    ("miniswe_spl_localization", "SPL Localization"),
    ("miniswe_spl_repair", "SPL Repair"),
    ("miniswe_spl_both", "SPL Both"),
    ("miniswe_full_semantic_summary", "Full Semantic Summary"),
]


def read_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload) -> None:
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def status(row: dict) -> str:
    if not row["patch_generated"]:
        return "No Patch"
    return "Patch Pass" if row["resolved"] else "Patch Fail"


def exact_mcnemar(gains: int, losses: int) -> float:
    n = gains + losses
    if not n:
        return 1.0
    tail = sum(math.comb(n, k) for k in range(0, min(gains, losses) + 1)) / (2**n)
    return min(1.0, 2 * tail)


def main() -> None:
    rows80 = read_json(EVAL80)
    assert len(rows80) == 180
    assert all(row.get("evaluation_available") or not row.get("patch_generated") for row in rows80)
    audit = read_json(AUDIT)
    strata = {row["instance_id"]: row["stratum"] for row in audit["instances"]}
    selected = set(strata)

    rows36: list[dict] = []
    for path in sorted(BASE36.glob("unit_*/runs/evaluation.json")):
        rows36.extend(row for row in read_json(path) if row["instance_id"] in selected)
    rows36.extend(row for row in read_json(SEM36) if row["instance_id"] in selected)
    by36 = {(row["instance_id"], row["condition"]): row for row in rows36}
    by80 = {(row["instance_id"], row["condition"]): row for row in rows80}
    assert len(by80) == 180
    assert all((instance, mode) in by36 for instance in selected for mode, _ in METHODS)

    per_task = []
    for instance in sorted(selected):
        for mode, display in METHODS:
            old = by36[(instance, mode)]
            new = by80[(instance, mode)]
            usage = new.get("llm_usage") or {}
            per_task.append(
                {
                    "task_id": instance,
                    "selection_stratum_36step": strata[instance],
                    "method": display,
                    "condition": mode,
                    "resolved_36step": int(bool(old.get("resolved"))),
                    "resolved_80step": int(bool(new.get("resolved"))),
                    "patch_generated_80step": int(bool(new.get("patch_generated"))),
                    "patch_status_80step": status(new),
                    "llm_calls_80step": int(usage.get("calls") or 0),
                    "input_tokens_80step": int(usage.get("input_tokens") or 0),
                    "output_tokens_80step": int(usage.get("output_tokens") or 0),
                    "total_tokens_80step": int(usage.get("total_tokens") or 0),
                    "elapsed_seconds_80step": float(usage.get("elapsed_seconds") or 0),
                }
            )
    csv_path = RUN / "per_task_budget80_results.csv"
    with csv_path.open("w", encoding="utf-8-sig", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(per_task[0]))
        writer.writeheader()
        writer.writerows(per_task)

    summaries = []
    transitions = []
    paired80 = []
    for mode, display in METHODS:
        current = [row for row in per_task if row["condition"] == mode]
        passed = sum(row["resolved_80step"] for row in current)
        patch_fail = sum(row["patch_status_80step"] == "Patch Fail" for row in current)
        no_patch = sum(row["patch_status_80step"] == "No Patch" for row in current)
        total_tokens = sum(row["total_tokens_80step"] for row in current)
        total_calls = sum(row["llm_calls_80step"] for row in current)
        input_tokens = sum(row["input_tokens_80step"] for row in current)
        output_tokens = sum(row["output_tokens_80step"] for row in current)
        summaries.append(
            {
                "method": display,
                "condition": mode,
                "tasks": 30,
                "patch_pass": passed,
                "patch_fail": patch_fail,
                "no_patch": no_patch,
                "resolved_rate": passed / 30,
                "total_llm_calls": total_calls,
                "mean_llm_calls_per_task": total_calls / 30,
                "input_tokens": input_tokens,
                "output_tokens": output_tokens,
                "total_tokens": total_tokens,
                "mean_tokens_per_task": total_tokens / 30,
                "mean_tokens_per_resolved_task": total_tokens / passed if passed else None,
            }
        )
        gains = sum(not row["resolved_36step"] and row["resolved_80step"] for row in current)
        losses = sum(row["resolved_36step"] and not row["resolved_80step"] for row in current)
        both = sum(row["resolved_36step"] and row["resolved_80step"] for row in current)
        neither = 30 - gains - losses - both
        transitions.append(
            {
                "method": display,
                "resolved_36step": sum(row["resolved_36step"] for row in current),
                "resolved_80step": passed,
                "gain_0_to_1": gains,
                "loss_1_to_0": losses,
                "both_resolved": both,
                "neither_resolved": neither,
                "exact_mcnemar_p": exact_mcnemar(gains, losses),
            }
        )

    original80 = {row["task_id"]: row["resolved_80step"] for row in per_task if row["condition"] == "miniswe_original"}
    for mode, display in METHODS[1:]:
        current = {row["task_id"]: row["resolved_80step"] for row in per_task if row["condition"] == mode}
        gains = sum(not original80[x] and current[x] for x in selected)
        losses = sum(original80[x] and not current[x] for x in selected)
        both = sum(original80[x] and current[x] for x in selected)
        paired80.append(
            {
                "comparison": f"{display} vs Original",
                "method_only": gains,
                "original_only": losses,
                "both_resolved": both,
                "neither_resolved": 30 - gains - losses - both,
                "net_resolved": gains - losses,
                "exact_mcnemar_p": exact_mcnemar(gains, losses),
            }
        )

    strata_summary = []
    for stratum in ("original_only", "spl_only", "neither"):
        ids = {instance for instance, value in strata.items() if value == stratum}
        for mode, display in (METHODS[0], METHODS[3]):
            current = [row for row in per_task if row["condition"] == mode and row["task_id"] in ids]
            strata_summary.append(
                {
                    "stratum": stratum,
                    "method": display,
                    "n": len(current),
                    "resolved_36step": sum(row["resolved_36step"] for row in current),
                    "resolved_80step": sum(row["resolved_80step"] for row in current),
                }
            )

    payload = {
        "study": "budget_relaxation_80step_stratified30",
        "sample_design": audit["selected_strata"],
        "complete_task_method_rows": len(per_task),
        "evaluation_missing": 0,
        "summary_80step": summaries,
        "budget_transitions_36_to_80": transitions,
        "paired_comparisons_at_80step": paired80,
        "original_vs_spl_repair_by_selection_stratum": strata_summary,
        "interaction_step_definition": "one recorded model call in llm_usage.calls",
    }
    write_json(RUN / "budget80_summary.json", payload)

    summary_by = {row["method"]: row for row in summaries}
    trans_by = {row["method"]: row for row in transitions}
    lines = [
        "# Experiment 3 Supplementary Experiment: 80-Step Interaction Budget Relaxation Study",
        "",
        "## 1. Purpose",
        "",
        "This supplementary experiment tests whether the SPL advantage still holds once the Mini-SWE-agent interaction limit is relaxed from 36 steps to 80 steps. This study is not a new overall leaderboard; the 30 samples were deliberately stratified, so the results can only support budget-sensitivity and method-behavior analysis, and cannot be extrapolated to the 218-case overall pass rate.",
        "",
        "## 2. Samples and fairness",
        "",
        "All samples come from the 218 cases of the formal RQ3 and were stratified strictly by the final evaluator results of Original and SPL Repair at 36 steps. Following the pre-registered design, samples solved by both are not selected:",
        "",
        "| 36-step stratum | Total available | Selected here |",
        "|---|---:|---:|",
        "| SPL Repair pass, Original fail | 36 | 12 |",
        "| Original pass, SPL Repair fail | 7 | 7 (all) |",
        "| Both fail | 68 | 11 |",
        "| Both pass | 107 | 0 |",
        "",
        "The SPL-only and both-fail strata were sampled with the fixed random seed 12680; Original-only had only 7 cases, so all were included. All six methods used exactly the same 30 tasks.",
        "",
        "## 3. Fixed setup",
        "",
        "- Model: DeepSeek-V4-Pro; temperature = 0; max output 8192 tokens.",
        "- The only algorithmic budget change: `mini_step_limit` raised from 36 to 80.",
        "- Concurrency kept at 4 as in the formal configuration; all other Mini-SWE-agent, SWE-bench harness, and prompting-strategy parameters unchanged.",
        "- Reused the source code, SPL cards, Free Summary, and full natural-language semantics frozen by the formal experiment; no semantic asset was rebuilt.",
        "- All six methods generated patches first, then the official SWE-bench harness was run uniformly afterwards.",
        "- Patch Pass, Patch Fail, and No Patch are mutually exclusive and sum to 30 for each method.",
        "",
        "## 4. Final 80-step results",
        "",
        "| Method | Patch Pass | Patch Fail | No Patch | Pass rate |",
        "|---|---:|---:|---:|---:|",
    ]
    for _, display in METHODS:
        row = summary_by[display]
        lines.append(f"| {display} | {row['patch_pass']} | {row['patch_fail']} | {row['no_patch']} | {row['resolved_rate']:.1%} |")
    lines += [
        "",
        "At 80 steps SPL Localization achieved the best result (19/30), SPL Both was 18/30, SPL Repair and Free Summary were both 17/30, Original was 13/30, and Full Semantic Summary was 12/30. SPL Localization net-gained 6 solved tasks over Original; SPL Repair net-gained 4.",
        "",
        "## 5. Change from 36 to 80 steps",
        "",
        "| Method | 36-step pass | 80-step pass | New gains | Pass-to-fail | Net change |",
        "|---|---:|---:|---:|---:|---:|",
    ]
    for _, display in METHODS:
        row = trans_by[display]
        lines.append(
            f"| {display} | {row['resolved_36step']} | {row['resolved_80step']} | {row['gain_0_to_1']} | {row['loss_1_to_0']} | {row['resolved_80step'] - row['resolved_36step']:+d} |"
        )
    lines += [
        "",
        "Relaxing the budget does not monotonically preserve every 36-step success: model calls are stochastic, and even at temperature=0 server-side inference and tool trajectories can still differ. The table therefore reports new gains and pass-to-fail together, rather than comparing only the two totals.",
        "",
        "Original improved from 7/30 to 13/30 and SPL Repair from 12/30 to 17/30; both benefited from more exploration, but SPL Repair still led Original by 4 tasks at 80 steps. Meanwhile SPL Localization reached 19/30, showing that under a wider budget the lighter localization aid is more robust than the stronger repair-control strategy.",
        "",
        "## 6. Resource consumption",
        "",
        "Interaction steps here are counted as one model call in the evaluation records.",
        "",
        "| Method | Model calls | Mean calls/task | Input tokens | Output tokens | Total tokens | Mean tokens/task |",
        "|---|---:|---:|---:|---:|---:|---:|",
    ]
    for _, display in METHODS:
        row = summary_by[display]
        lines.append(
            f"| {display} | {row['total_llm_calls']:,} | {row['mean_llm_calls_per_task']:.1f} | {row['input_tokens']:,} | {row['output_tokens']:,} | {row['total_tokens']:,} | {row['mean_tokens_per_task']:,.0f} |"
        )
    lines += [
        "",
        "The three structured SPL strategies consumed markedly less than Original and Free Summary: SPL Localization used only about 6.71M tokens, whereas Original used about 24.96M tokens. Even with 80 steps allowed, SPL conditions usually formed and submitted edits earlier, while Original/Free Summary more often kept exploring to higher call counts. Full Semantic Summary added all semantics at once to an ordinary natural-language context, reaching 12/30 while using about 27.34M tokens — it gained neither the pass rate nor the efficiency of the structured methods, showing that \"supplying more semantic text\" is by itself not enough to replace function binding, selection, and execution strategy.",
        "",
        "## 7. Stratified observations",
        "",
        "| Original 36-step stratum | n | Original 80-step | SPL Repair 80-step |",
        "|---|---:|---:|---:|",
    ]
    for stratum, label in (("original_only", "Original-only"), ("spl_only", "SPL-only"), ("neither", "Both fail")):
        o = next(x for x in strata_summary if x["stratum"] == stratum and x["method"] == "Original")
        s = next(x for x in strata_summary if x["stratum"] == stratum and x["method"] == "SPL Repair")
        lines.append(f"| {label} | {o['n']} | {o['resolved_80step']} | {s['resolved_80step']} |")
    lines += [
        "",
        "The stratified results explain where the budget change took effect: whether Original recovered the original SPL-only cases, whether SPL Repair recovered the Original-only cases, and whether either method could crack the previously both-fail tasks. Per-task results are saved in a CSV in the same directory, so every transition can be checked directly.",
        "",
        "## 8. Completeness and exception handling",
        "",
        "- All 30 × 6 = 180 agent conditions completed, with trajectory, patch, call statistics, and completion flags saved.",
        "- In the initial uniform evaluation, two already-generated patches lacked a verdict because GitHub test-dependency downloads hit a temporary SSL disconnect; afterwards only the harness for those two existing patches was re-run, without calling the model again or modifying the patch.",
        "- After re-evaluation all 180 rows fall uniquely into Patch Pass, Patch Fail, or No Patch, with 0 missing evaluations.",
        "- The API key was not written into configs, run results, or the reproducibility package.",
        "",
        "## 9. Conclusion",
        "",
        "After the budget increased from 36 to 80, Original did solve more tasks through extra exploration, but the SPL advantage did not disappear: the best SPL condition solved 6/30 more than Original, SPL Repair solved 4/30 more, and the three structured SPL methods consumed far fewer tokens than Original. The results support \"structured semantics improve search direction and convergence efficiency\" more than \"SPL merely compensates for insufficient steps\". However, because this subset deliberately excludes the 36-step both-pass tasks and over-weights inconsistent/failed cases, subset pass rates such as 63.3% cannot be compared directly with the 218-case overall pass rate.",
        "",
        "## 10. Data file notes",
        "",
        "- `per_task_budget80_results.csv`: per-task status, 36/80-step correctness, call counts, and tokens for 30 tasks × 6 methods. The CSV uses a UTF-8 BOM to avoid mojibake when opened by Chinese-language software.",
        "- `budget80_summary.json`: the summary, budget transitions, 80-step paired comparisons, and stratified statistics needed for paper tables.",
        "- `selection_audit.json`: sampling source, fixed seed, stratum sizes, and the list of 30 tasks.",
        "- `runs/evaluation.json`: the raw per-condition results from the final official evaluator.",
    ]
    (RUN / "exp3_budget_relaxation_80step_supplement.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote summary for {len(per_task)} task-method rows")


if __name__ == "__main__":
    main()
