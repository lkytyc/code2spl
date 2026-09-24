from __future__ import annotations

"""Aggregate + statistical analysis for the random218 x 5-condition V2 (guarded) run.

Follows the metric contract used across these experiments:
  - main metric = resolved / conservative denominator (218), NOT resolved/non-empty
  - secondary = "reportable rate" resolved / evaluated (proportion over samples with output)
  - report patch/N, harness coverage of patches, inference tokens, cost USD
  - Wilson 95% CI on proportions; paired exact McNemar (same-task); Holm correction
    across the family of pre-registered comparisons
  - continuous (tokens) reported as total, mean, median, and per-task paired diffs

Reads the same authoritative artifacts the reference analyzer uses:
  - evaluation.json  -> patch_generated / evaluation_available / resolved / llm_usage.total_tokens
  - cost_summary.json -> per_condition[*].total_cost_usd
"""

import json
import math
from collections import defaultdict
from pathlib import Path

EXP6 = Path(__file__).resolve().parents[1]
UNITS = EXP6 / "data/results/reproduced_runs/random218/units"

CONDITIONS = (
    "miniswe_original",
    "miniswe_free_summary",
    "miniswe_spl_localization",
    "miniswe_spl_repair",
    "miniswe_spl_both",
)
SHORT = {
    "miniswe_original": "original",
    "miniswe_free_summary": "free_summary",
    "miniswe_spl_localization": "spl_localization",
    "miniswe_spl_repair": "spl_repair",
    "miniswe_spl_both": "spl_both",
}


def wilson(successes: int, total: int, z: float = 1.96) -> tuple[float | None, float | None]:
    if total <= 0:
        return (None, None)
    p = successes / total
    d = 1 + z**2 / total
    center = (p + z**2 / (2 * total)) / d
    margin = z * math.sqrt(p * (1 - p) / total + z**2 / (4 * total**2)) / d
    return (max(0.0, center - margin), min(1.0, center + margin))


def exact_mcnemar(gains: int, losses: int) -> float | None:
    discordant = gains + losses
    if discordant == 0:
        return None
    tail = sum(math.comb(discordant, k) for k in range(0, min(gains, losses) + 1)) / (2**discordant)
    return min(1.0, 2 * tail)


def holm(pvalues: list[float]) -> list[float]:
    """Holm-Bonferroni adjusted p-values (same family)."""
    m = len(pvalues)
    order = sorted(range(m), key=lambda i: pvalues[i])
    adjusted = [0.0] * m
    for rank, i in enumerate(order):
        adjusted[i] = min(1.0, pvalues[i] * (m - rank))
        if rank > 0:
            adjusted[i] = max(adjusted[i], adjusted[order[rank - 1]])
    return adjusted


def conservative_result(row: dict) -> bool:
    return bool(row.get("evaluation_available") and row.get("resolved"))


def main() -> int:
    # --- load all rows ---
    rows_by_instance: dict[str, dict[str, dict]] = defaultdict(dict)
    costs_by_unit: list[dict] = []
    missing_eval = []
    missing_cost = []
    unit_names = sorted(p.stem for p in UNITS.glob("unit_*"))
    for unit in unit_names:
        ep = UNITS / unit / "runs" / "evaluation.json"
        cp = UNITS / unit / "runs" / "cost_summary.json"
        if not ep.exists():
            missing_eval.append(unit)
            continue
        rows = json.loads(ep.read_text(encoding="utf-8"))
        for r in rows:
            if isinstance(r, dict):
                rows_by_instance[r["instance_id"]][r["condition"]] = r
        if cp.exists():
            costs_by_unit.append(json.loads(cp.read_text(encoding="utf-8")))
        else:
            missing_cost.append(unit)

    n_instances = len(rows_by_instance)
    expected = len(unit_names)
    print(f"units on disk: {expected}")
    print(f"instances with evaluation rows: {n_instances}")
    print(f"missing evaluation.json: {len(missing_eval)} {missing_eval[:5]}")
    print(f"missing cost_summary.json: {len(missing_cost)} {missing_cost[:5]}")

    # completeness audit
    total_rows = sum(len(m) for m in rows_by_instance.values())
    incomplete = [i for i, m in rows_by_instance.items() if set(m) != set(CONDITIONS)]
    print(f"total rows: {total_rows} (expect {expected * len(CONDITIONS)})")
    print(f"instances missing a condition: {len(incomplete)} {incomplete[:5]}")

    # --- per-condition aggregation ---
    by_condition: dict[str, list[dict]] = defaultdict(list)
    for mapping in rows_by_instance.values():
        for cond in CONDITIONS:
            by_condition[cond].append(mapping[cond])

    # cost sums
    cost_sum: dict[str, float] = defaultdict(float)
    for cs in costs_by_unit:
        for cond, vals in cs.get("per_condition", {}).items():
            if cond in CONDITIONS:
                cost_sum[cond] += float(vals.get("total_cost_usd", 0) or 0)

    stats = {}
    for cond in CONDITIONS:
        rows = by_condition[cond]
        patch = sum(bool(r.get("patch_generated")) for r in rows)
        evaluated = sum(bool(r.get("evaluation_available")) for r in rows)
        resolved = sum(conservative_result(r) for r in rows)
        tokens = [int((r.get("llm_usage") or {}).get("total_tokens", 0) or 0) for r in rows]
        total_tokens = sum(tokens)
        stats[cond] = {
            "patch": patch,
            "evaluated": evaluated,
            "resolved": resolved,
            "coverage": (evaluated / patch if patch else None),
            "total_tokens": total_tokens,
            "mean_tokens": total_tokens / len(rows),
            "median_tokens": sorted(tokens)[len(tokens) // 2],
            "cost_usd": cost_sum.get(cond, 0.0),
            "wilson": wilson(resolved, expected),
            "reportable": resolved / evaluated if evaluated else None,
        }

    # --- paired comparisons (same 7 as the reference analyzer) ---
    comparisons = []
    for cond in CONDITIONS[1:]:
        comparisons.append(("miniswe_original", cond))
    for left, right in (
        ("miniswe_spl_localization", "miniswe_spl_repair"),
        ("miniswe_spl_localization", "miniswe_spl_both"),
        ("miniswe_spl_repair", "miniswe_spl_both"),
    ):
        comparisons.append((left, right))

    pair_results = []
    for left, right in comparisons:
        gains = losses = both = neither = 0
        token_diffs = []
        for instance_id, mapping in rows_by_instance.items():
            ls = conservative_result(mapping[left])
            rs = conservative_result(mapping[right])
            if ls and rs:
                both += 1
            elif not ls and rs:
                gains += 1
            elif ls and not rs:
                losses += 1
            else:
                neither += 1
            lt = int((mapping[left].get("llm_usage") or {}).get("total_tokens", 0) or 0)
            rt = int((mapping[right].get("llm_usage") or {}).get("total_tokens", 0) or 0)
            token_diffs.append(rt - lt)
        token_diffs_sorted = sorted(token_diffs)
        mid = len(token_diffs_sorted) // 2
        median_diff = token_diffs_sorted[mid]
        pair_results.append({
            "left": left,
            "right": right,
            "gains": gains,
            "losses": losses,
            "both": both,
            "neither": neither,
            "net": gains - losses,
            "mcnemar": exact_mcnemar(gains, losses),
            "mean_token_diff": sum(token_diffs) / len(token_diffs),
            "median_token_diff": median_diff,
        })

    # Holm across the family of pre-registered comparisons
    raw_ps = [pr["mcnemar"] if pr["mcnemar"] is not None else 1.0 for pr in pair_results]
    holm_ps = holm(raw_ps)
    for pr, hp in zip(pair_results, holm_ps):
        pr["holm"] = hp

    # --- emit report ---
    out = []
    out.append("## Main metrics (conservative denominator = 218)")
    out.append("")
    out.append("| Condition | resolved/218 | patch/218 | harness coverage | inference tokens | cost USD | secondary metric resolved/evaluated |")
    out.append("|---|---:|---:|---:|---:|---:|---:|")
    for cond in CONDITIONS:
        s = stats[cond]
        lo, hi = s["wilson"]
        out.append(
            f"| `{cond}` | **{s['resolved']}/218** | {s['patch']}/218 | "
            f"{s['evaluated']}/{s['patch']} | {s['total_tokens']:,} | {s['cost_usd']:.6f} | "
            f"{s['reportable']:.1%} |"
        )
    out.append("")
    out.append("Wilson 95% CI (resolved/218):")
    for cond in CONDITIONS:
        s = stats[cond]
        lo, hi = s["wilson"]
        out.append(f"- `{cond}`: {s['resolved']/218:.1%} [{lo:.1%}, {hi:.1%}]")
    out.append("")
    out.append("## Paired comparisons (two-sided exact McNemar; Holm correction within the same family)")
    out.append("")
    out.append("| Comparison | right-only gain | left-only loss | net | McNemar p | Holm p | mean per-task token diff | median token diff |")
    out.append("|---|---:|---:|---:|---:|---:|---:|---:|")
    for pr in pair_results:
        p = pr["mcnemar"]
        out.append(
            f"| {SHORT[pr['left']]} vs {SHORT[pr['right']]} | {pr['gains']} | {pr['losses']} | "
            f"{pr['net']:+d} | {'NA' if p is None else f'{p:.6f}'} | {pr['holm']:.6f} | "
            f"{pr['mean_token_diff']:+,.0f} | {pr['median_token_diff']:+,.0f} |"
        )
    out.append("")

    text = "\n".join(out)
    print(text)
    (EXP6 / "data/results/reproduced_runs/random218/final_analysis.md").write_text(
        text + "\n", encoding="utf-8"
    )
    # also dump JSON
    payload = {
        "n": expected,
        "instances": n_instances,
        "missing_eval": missing_eval,
        "missing_cost": missing_cost,
        "incomplete_instances": incomplete,
        "by_condition": {cond: stats[cond] for cond in CONDITIONS},
        "paired_comparisons": pair_results,
    }
    (EXP6 / "data/results/reproduced_runs/random218/final_analysis.json").write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
