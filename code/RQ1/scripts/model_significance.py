"""Exp1 paired significance on one shared, fixed evaluation subset.

The reference solution is re-executed inside each model run, and a few ClassEval
tasks are not reliably evaluable in this environment (missing dependencies,
NumPy 2.0 removals, timeouts, one unseeded-random task). Those tasks can flip
between runs, so the per-run valid set differs slightly across arms and the
paired denominators would not be comparable.

This script fixes the exclusion set once — every task whose gold solution failed
in any arm of the original pass — and applies it to all arms, so all four
pre-specified SPL-vs-non-SPL comparisons use the same 100-minus-N tasks. The
set is deliberately *not* recomputed for the five models reported here: it was
fixed before the comparisons were made, and recomputing it over a smaller set of
arms would move every denominator and change the reported figures.

Writes `data/results/model_comparison/exp1_model_significance.json`.
"""

from __future__ import annotations

import json
import math
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
BASE = ROOT / "data/raw_results/exp1_classeval/model_runs"

MODELS = {
    "deepseek-v4-flash": "deepseek-v4-flash/full100",
    "deepseek-v4-pro": "deepseek-v4-pro/full100",
    "gpt-5.4": "gpt-5.4/full100",
    "gpt-5.4-mini": "gpt-5.4-mini/full100",
    "claude-opus-5": "claude-opus-5/full100",
}
CONDITIONS = ("skeleton_holistic", "free_summary", "spl_only", "skeleton_spl")
COMPARISONS = (
    ("spl_only", "skeleton_holistic"),
    ("spl_only", "free_summary"),
    ("skeleton_spl", "skeleton_holistic"),
    ("skeleton_spl", "free_summary"),
)


def read(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def mcnemar_exact(b: int, c: int) -> float:
    n = b + c
    if n == 0:
        return 1.0
    tail = sum(math.comb(n, i) for i in range(min(b, c) + 1)) / (2 ** n)
    return min(1.0, 2.0 * tail)


def holm(p_values: list[float]) -> list[float]:
    order = sorted(range(len(p_values)), key=lambda i: p_values[i])
    adjusted = [1.0] * len(p_values)
    running = 0.0
    for rank, index in enumerate(order):
        value = min(1.0, (len(p_values) - rank) * p_values[index])
        running = max(running, value)
        adjusted[index] = running
    return adjusted


def main() -> int:
    runs = {model: BASE / rel for model, rel in MODELS.items()}

    # ── fixed shared exclusion set ──────────────────────────────────────
    reference_fail: dict[str, set[str]] = {}
    for model, run in runs.items():
        ref = read(run / "reference_evaluation.json")
        reference_fail[model] = {r["task_id"] for r in ref if not r.get("class_test_ok")}
    excluded = sorted(set().union(*reference_fail.values()), key=lambda s: int(s.split("_")[1]))
    n_valid = 100 - len(excluded)

    rows = []
    for model, run in runs.items():
        ev = read(run / "evaluation.json")
        by_condition: dict[str, dict[str, dict]] = {}
        for row in ev:
            by_condition.setdefault(row["condition"], {})[row["task_id"]] = row

        passes = {c: sum(int(bool(r["class_test_ok"])) for r in by_condition[c].values())
                  for c in CONDITIONS if c in by_condition}

        p_raw = []
        entries = []
        for treatment, baseline in COMPARISONS:
            b = c = t_ok = base_ok = 0
            for task in sorted(set(by_condition[treatment]) & set(by_condition[baseline])):
                if task in excluded:
                    continue
                t = bool(by_condition[treatment][task]["class_test_ok"])
                bl = bool(by_condition[baseline][task]["class_test_ok"])
                t_ok += int(t)
                base_ok += int(bl)
                b += int(t and not bl)
                c += int(bl and not t)
            p = mcnemar_exact(b, c)
            p_raw.append(p)
            entries.append({
                "treatment": treatment,
                "baseline": baseline,
                "treatment_passes": t_ok,
                "baseline_passes": base_ok,
                "treatment_rate": t_ok / n_valid,
                "baseline_rate": base_ok / n_valid,
                "delta_percentage_points": (t_ok - base_ok) / n_valid * 100,
                "treatment_only": b,
                "baseline_only": c,
                "p_value_raw": p,
            })
        for entry, p_holm in zip(entries, holm(p_raw)):
            entry["p_value_holm"] = p_holm
            entry["significant_holm_0_05"] = p_holm < 0.05

        rows.append({
            "model": model,
            "run_dir": runs[model].relative_to(ROOT).as_posix(),
            "reference_invalid_in_this_run": sorted(reference_fail[model], key=lambda s: int(s.split("_")[1])),
            "strict_passes_per_100": passes,
            "comparisons": entries,
        })

    out = {
        "experiment": "Exp1 ClassEval reconstruction — five-model paired significance",
        "n_raw": 100,
        "n_valid": n_valid,
        "excluded_tasks": excluded,
        "exclusion_rule": "task excluded if the gold solution failed to pass its own tests in ANY of the model runs",
        "test": "two-sided exact McNemar on paired task outcomes; Holm correction within each model over the four pre-specified comparisons",
        "models": rows,
    }
    path = ROOT / "data/results/exp1_classeval/model_comparison/exp1_model_significance.json"
    path.write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(f"shared exclusion set ({len(excluded)}): {excluded}\n")
    for row in rows:
        print(f"{row['model']}")
        for e in row["comparisons"]:
            print(f"   {e['treatment']:13s} vs {e['baseline']:18s} {e['baseline_passes']:>3} -> {e['treatment_passes']:>3} "
                  f"({e['delta_percentage_points']:+5.1f}pp)  b={e['treatment_only']:>2} c={e['baseline_only']:>2}  "
                  f"p_holm={e['p_value_holm']:.3e} {'*' if e['significant_holm_0_05'] else 'n.s.'}")
        print()
    print("wrote", path.relative_to(ROOT))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
