"""Aggregate + statistical analysis for the Exp3 supplement arm.

The supplement is one extra condition, `miniswe_spl_unstructured_both`, run over
the same 218 SWE-bench Verified instances as the five published arms.  The five
frozen arms are read from the published tree rather than re-derived, so the
comparison is against the recorded run and not against a re-run.

Metric contract is the frozen one, imported rather than re-implemented so the
supplement cannot drift from it by accident:
  - main metric = resolved / conservative denominator (218)
  - secondary   = resolved / evaluated ("reportable")
  - Wilson 95% CI; paired exact McNemar on the same instance; Holm over the
    family of comparisons the supplement needs

The comparison family here is the supplement against each of the five frozen
arms -- five comparisons, pre-registered as one family for the Holm correction.
The seven frozen-vs-frozen comparisons are re-derived too, purely to confirm the
frozen numbers still reproduce from the frozen files.

Read-only with respect to every frozen artifact.
Usage: python $PROJECT_ROOT/code/RQ3/supplement_2026-09-13/untagged_arm/scripts/analyze_unstructured_both_results.py
"""

from __future__ import annotations

import json
import sys
from collections import defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
EXP6 = HERE.parents[4]
sys.path.insert(0, str(HERE))
# Reuse the frozen analyzer's statistics verbatim; re-deriving McNemar or the
# Wilson interval here would let the two reports disagree on the same numbers.
from analyze_random218_results import (  # noqa: E402
    CONDITIONS as FROZEN_CONDITIONS,
    SHORT,
    conservative_result,
    exact_mcnemar,
    holm,
    wilson,
)

FROZEN_UNITS = EXP6 / "data/raw_results/exp3_swebench/random218_compact/units"
SUPP_UNITS = EXP6 / "data/raw_results/exp3_swebench/random218_untagged_both/units"
OUT_MD = EXP6 / "data/results/exp3_swebench/random218_untagged_both/final_analysis_unstructured_both.json"
OUT_JSON = EXP6 / "data/results/exp3_swebench/random218_untagged_both/final_analysis_unstructured_both.json"

SUPPLEMENT = "miniswe_spl_unstructured_both"
SHORT[SUPPLEMENT] = "spl_unstructured_both"
CONDITIONS = tuple(FROZEN_CONDITIONS) + (SUPPLEMENT,)
DENOM = 218


def load() -> tuple[dict[str, dict[str, dict]], dict[str, dict], list[str], list[str]]:
    """Return per-instance condition rows plus per-unit cost payloads."""
    rows: dict[str, dict[str, dict]] = defaultdict(dict)
    costs: dict[str, dict] = {}
    missing_frozen: list[str] = []
    missing_supp: list[str] = []

    for unit_dir in sorted(FROZEN_UNITS.glob("unit_*")):
        unit = unit_dir.name
        ev = unit_dir / "runs" / "evaluation.json"
        if not ev.is_file():
            missing_frozen.append(unit)
            continue
        for row in json.loads(ev.read_text(encoding="utf-8")):
            if isinstance(row, dict):
                rows[row["instance_id"]][row["condition"]] = row
        cp = unit_dir / "runs" / "cost_summary.json"
        if cp.is_file():
            costs[unit] = json.loads(cp.read_text(encoding="utf-8"))

    for unit_dir in sorted(SUPP_UNITS.glob("unit_*")):
        unit = unit_dir.name
        ev = unit_dir / "evaluation.json"
        if not ev.is_file():
            missing_supp.append(unit)
            continue
        for row in json.loads(ev.read_text(encoding="utf-8")):
            if isinstance(row, dict):
                rows[row["instance_id"]][row["condition"]] = row
        cp = unit_dir / "cost_summary.json"
        if cp.is_file():
            # Separate trees, so key collisions are impossible by construction.
            costs[f"{unit}::{SUPPLEMENT}"] = json.loads(cp.read_text(encoding="utf-8"))

    return rows, costs, missing_frozen, missing_supp


def aggregate(rows: dict[str, dict[str, dict]], costs: dict[str, dict]) -> dict:
    cost_sum: dict[str, float] = defaultdict(float)
    for payload in costs.values():
        for cond, vals in (payload.get("per_condition") or {}).items():
            if cond in CONDITIONS:
                cost_sum[cond] += float(vals.get("total_cost_usd", 0) or 0)

    stats: dict[str, dict] = {}
    for cond in CONDITIONS:
        present = [m[cond] for m in rows.values() if cond in m]
        patch = sum(bool(r.get("patch_generated")) for r in present)
        evaluated = sum(bool(r.get("evaluation_available")) for r in present)
        resolved = sum(conservative_result(r) for r in present)
        tokens = [int((r.get("llm_usage") or {}).get("total_tokens", 0) or 0) for r in present]
        total_tokens = sum(tokens)
        stats[cond] = {
            "rows": len(present),
            "patch": patch,
            "evaluated": evaluated,
            "resolved": resolved,
            "coverage": (evaluated / patch if patch else None),
            "total_tokens": total_tokens,
            "mean_tokens": total_tokens / len(present) if present else None,
            "median_tokens": sorted(tokens)[len(tokens) // 2] if tokens else None,
            "cost_usd": cost_sum.get(cond, 0.0),
            "wilson": wilson(resolved, DENOM),
            "reportable": resolved / evaluated if evaluated else None,
        }
    return stats


def paired(rows: dict[str, dict[str, dict]], comparisons: list[tuple[str, str]]) -> list[dict]:
    out = []
    for left, right in comparisons:
        gains = losses = both = neither = 0
        token_diffs: list[int] = []
        for mapping in rows.values():
            if left not in mapping or right not in mapping:
                continue
            ls = conservative_result(mapping[left])
            rs = conservative_result(mapping[right])
            if ls and rs:
                both += 1
            elif rs:
                gains += 1
            elif ls:
                losses += 1
            else:
                neither += 1
            lt = int((mapping[left].get("llm_usage") or {}).get("total_tokens", 0) or 0)
            rt = int((mapping[right].get("llm_usage") or {}).get("total_tokens", 0) or 0)
            token_diffs.append(rt - lt)
        s = sorted(token_diffs)
        out.append({
            "left": left,
            "right": right,
            "gains": gains,
            "losses": losses,
            "both": both,
            "neither": neither,
            "net": gains - losses,
            "mcnemar": exact_mcnemar(gains, losses),
            "mean_token_diff": (sum(token_diffs) / len(token_diffs)) if token_diffs else None,
            "median_token_diff": s[len(s) // 2] if s else None,
        })
    return out


def report(stats: dict, supp_pairs: list[dict], frozen_pairs: list[dict]) -> str:
    out: list[str] = []
    out.append("## Main metrics (conservative denominator = 218)")
    out.append("")
    out.append(
        "| Condition | resolved/218 | patch/218 | harness coverage | inference tokens | "
        "cost USD | secondary metric resolved/evaluated |"
    )
    out.append("|---|---:|---:|---:|---:|---:|---:|")
    for cond in CONDITIONS:
        s = stats[cond]
        cov = f"{s['evaluated']}/{s['patch']}" if s["patch"] else "NA"
        cost = f"{s['cost_usd']:.6f}" if s["cost_usd"] else "NA"
        rep = f"{s['reportable']:.1%}" if s["reportable"] is not None else "NA"
        star = "**" if cond == SUPPLEMENT else ""
        out.append(
            f"| {star}`{cond}`{star} | {star}{s['resolved']}/218{star} | {s['patch']}/218 | "
            f"{cov} | {s['total_tokens']:,} | {cost} | {rep} |"
        )
    out.append("")
    out.append("Wilson 95% CI (resolved/218):")
    for cond in CONDITIONS:
        s = stats[cond]
        lo, hi = s["wilson"]
        out.append(f"- `{cond}`: {s['resolved']/DENOM:.1%} [{lo:.1%}, {hi:.1%}]")
    out.append("")
    out.append("## Paired comparisons: supplement arm vs the five frozen arms (two-sided exact McNemar; Holm correction within the same family)")
    out.append("")
    out.append(
        "| Comparison | supplement only | control only | both | neither | net | "
        "McNemar p | Holm p | mean per-task token diff | median token diff |"
    )
    out.append("|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|")
    for pr in supp_pairs:
        p = pr["mcnemar"]
        mt = f"{pr['mean_token_diff']:+,.0f}" if pr["mean_token_diff"] is not None else "NA"
        md = f"{pr['median_token_diff']:+,.0f}" if pr["median_token_diff"] is not None else "NA"
        out.append(
            f"| {SHORT[pr['right']]} vs {SHORT[pr['left']]} | {pr['gains']} | {pr['losses']} | "
            f"{pr['both']} | {pr['neither']} | {pr['net']:+d} | "
            f"{'NA' if p is None else f'{p:.6f}'} | {pr['holm']:.6f} | {mt} | {md} |"
        )
    out.append("")
    out.append("## Control recomputation: the seven comparisons among the frozen arms (should match `final_analysis.md`)")
    out.append("")
    out.append("| Comparison | right-only gain | left-only loss | net | McNemar p | Holm p |")
    out.append("|---|---:|---:|---:|---:|---:|")
    for pr in frozen_pairs:
        p = pr["mcnemar"]
        out.append(
            f"| {SHORT[pr['left']]} vs {SHORT[pr['right']]} | {pr['gains']} | {pr['losses']} | "
            f"{pr['net']:+d} | {'NA' if p is None else f'{p:.6f}'} | {pr['holm']:.6f} |"
        )
    out.append("")
    return "\n".join(out)


def main() -> int:
    rows, costs, missing_frozen, missing_supp = load()
    print(f"instances with rows      : {len(rows)}")
    print(f"frozen units missing eval: {len(missing_frozen)} {missing_frozen[:5]}")
    print(f"supplement units unevaluated: {len(missing_supp)} {missing_supp[:5]}")
    if missing_supp:
        print("NOTE: supplement is incomplete; numbers below cover evaluated units only")

    stats = aggregate(rows, costs)
    supp_pairs = paired(rows, [(c, SUPPLEMENT) for c in FROZEN_CONDITIONS])
    supp_holm = holm([p["mcnemar"] if p["mcnemar"] is not None else 1.0 for p in supp_pairs])
    for pr, hp in zip(supp_pairs, supp_holm):
        pr["holm"] = hp

    frozen_pairs = paired(rows, [
        ("miniswe_original", "miniswe_free_summary"),
        ("miniswe_original", "miniswe_spl_localization"),
        ("miniswe_original", "miniswe_spl_repair"),
        ("miniswe_original", "miniswe_spl_both"),
        ("miniswe_spl_localization", "miniswe_spl_repair"),
        ("miniswe_spl_localization", "miniswe_spl_both"),
        ("miniswe_spl_repair", "miniswe_spl_both"),
    ])
    frozen_holm = holm([p["mcnemar"] if p["mcnemar"] is not None else 1.0 for p in frozen_pairs])
    for pr, hp in zip(frozen_pairs, frozen_holm):
        pr["holm"] = hp

    text = report(stats, supp_pairs, frozen_pairs)
    print()
    print(text)
    OUT_MD.write_text(text + "\n", encoding="utf-8")
    OUT_JSON.write_text(
        json.dumps(
            {
                "n": DENOM,
                "instances": len(rows),
                "missing_frozen": missing_frozen,
                "missing_supplement": missing_supp,
                "by_condition": stats,
                "supplement_vs_frozen": supp_pairs,
                "frozen_recomputed": frozen_pairs,
            },
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    print(f"wrote {OUT_MD.name} and {OUT_JSON.name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
