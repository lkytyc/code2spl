from __future__ import annotations

"""Full aggregate for the budget-aligned experiment.

Builds a single consistent results table over 6 conditions:
  - 5 original-run conditions (miniswe_original, free_summary,
    localization, repair, both_orig) from random218
  - 1 budget-aligned probe (both_probe) from random218_budget_aligned

Per-instance: resolved / patch_generated from evaluation.json;
tokens from evaluation.json llm_usage.total_tokens; cost from
cost_summary.json per_condition[cond].total_cost_usd.

Outputs:
  - aggregate table (resolved/patch/tokens/mean/median/cost/wilson/reportable)
  - paired exact McNemar + Holm over the comparison family (probe_both vs
    each original condition, plus the intra-original SPL pairs)
  - per-task token diff mean/median for each paired comparison
  - failure-mode (empty-patch) counts per condition
"""

import json
from collections import defaultdict
from math import comb, sqrt
from pathlib import Path

EXP6 = Path(__file__).resolve().parents[1]
ORIG = EXP6 / "data/results/reproduced_runs/random218/units"
PROBE = EXP6 / "data/results/reproduced_runs/random218_budget_aligned/units"

CONDS = ["miniswe_original", "miniswe_free_summary",
         "miniswe_spl_localization", "miniswe_spl_repair"]
ORIG_BOTH = "miniswe_spl_both"
PROBE_BOTH = "miniswe_spl_both"  # same condition key, different dir


def load_eval(run_units: Path) -> dict[str, dict]:
    out = {}
    for ep in sorted(run_units.glob("unit_*/runs/evaluation.json")):
        rows = json.loads(ep.read_text(encoding="utf-8"))
        for r in rows:
            if isinstance(r, dict):
                iid = r.get("instance_id")
                out[(iid, r.get("condition"))] = r
    return out


def load_cost(run_units: Path) -> dict[str, dict]:
    out = {}
    for cp in sorted(run_units.glob("unit_*/runs/cost_summary.json")):
        data = json.loads(cp.read_text(encoding="utf-8"))
        iid = cp.parts[-3]
        pc = data.get("per_condition", {})
        for cond, v in pc.items():
            out[(iid, cond)] = v
    return out


def wilson(k: int, n: int, z: float = 1.96) -> tuple[float, float]:
    if n == 0:
        return (0.0, 0.0)
    p = k / n
    d = 1 + z * z / n
    c = p + z * z / (2 * n)
    h = z * sqrt(p * (1 - p) / n + z * z / (4 * n * n))
    return ((c - h) / d, (c + h) / d)


def mcnemar_p(b: int, c: int) -> float:
    if b + c == 0:
        return 1.0
    n = b + c
    lo, hi = min(b, c), max(b, c)
    tail = sum(comb(n, i) for i in range(0, lo + 1)) * 0.5 ** n
    tail += sum(comb(n, i) for i in range(hi, n + 1)) * 0.5 ** n
    return min(1.0, tail)


def holm(ps: list[float]) -> list[float]:
    idx = sorted(range(len(ps)), key=lambda i: ps[i])
    m = len(ps)
    adj = [0.0] * m
    prev = 0.0
    for rank, i in enumerate(idx):
        adj[i] = min(1.0, max(prev, ps[i] * (m - rank)))
        prev = adj[i]
    return adj


def main() -> None:
    oe = load_eval(ORIG)
    pe = load_eval(PROBE)
    oc = load_cost(ORIG)
    pc = load_cost(PROBE)

    iids = sorted({k[0] for k in oe} | {k[0] for k in pe})
    N = len(iids)
    print(f"N instances = {N}")

    # per-condition resolved/patch/tokens/cost
    def agg(iids, cond, eval_map, cost_map):
        resolved = patch = evaluated = 0
        tokens = []
        cost = 0.0
        for iid in iids:
            r = eval_map.get((iid, cond))
            c = cost_map.get((iid, cond))
            if r is None:
                continue
            if r.get("patch_generated"):
                patch += 1
                evaluated += 1
            if r.get("resolved"):
                resolved += 1
            lu = r.get("llm_usage") or {}
            t = lu.get("total_tokens")
            if t is not None:
                tokens.append(t)
            if c is not None:
                cost += c.get("total_cost_usd", 0.0)
        tot = sum(tokens)
        return {
            "resolved": resolved, "patch": patch, "evaluated": evaluated,
            "total_tokens": tot,
            "mean_tokens": tot / len(tokens) if tokens else 0.0,
            "median_tokens": sorted(tokens)[len(tokens) // 2] if tokens else 0,
            "cost_usd": cost,
        }

    result = {}
    for cond in CONDS:
        result[cond] = agg(iids, cond, oe, oc)
    result["miniswe_spl_both_orig"] = agg(iids, ORIG_BOTH, oe, oc)
    result["miniswe_spl_both_probe"] = agg(iids, PROBE_BOTH, pe, pc)

    print("\n=== aggregate (denominator 218) ===")
    print(f"{'condition':26s} {'res':>4} {'patch':>5} {'eval':>5} {'tokens':>12} {'mean':>9} {'median':>8} {'cost_usd':>12} {'wilson':>20}")
    for cond, r in result.items():
        lo, hi = wilson(r["resolved"], N)
        print(f"{cond:26s} {r['resolved']:4d} {r['patch']:5d} {r['evaluated']:5d} "
              f"{r['total_tokens']:12d} {r['mean_tokens']:9.0f} {r['median_tokens']:8.0f} "
              f"{r['cost_usd']:12.6f} [{lo*100:.1f}%,{hi*100:.1f}%]")

    # per-instance resolved + token dicts for paired comparisons
    def per(iids, cond, eval_map):
        res = {}
        tok = {}
        for iid in iids:
            r = eval_map.get((iid, cond))
            if r is None:
                continue
            res[iid] = bool(r.get("resolved"))
            lu = r.get("llm_usage") or {}
            tok[iid] = lu.get("total_tokens") or 0
        return res, tok

    R = {}
    T = {}
    for cond in CONDS:
        R[cond], T[cond] = per(iids, cond, oe)
    R["both_orig"], T["both_orig"] = per(iids, ORIG_BOTH, oe)
    R["both_probe"], T["both_probe"] = per(iids, PROBE_BOTH, pe)

    # paired comparisons: probe_both vs each original condition
    pairs = [
        ("miniswe_original", "both_probe"),
        ("miniswe_free_summary", "both_probe"),
        ("miniswe_spl_localization", "both_probe"),
        ("miniswe_spl_repair", "both_probe"),
        ("miniswe_spl_localization", "miniswe_spl_repair"),
        ("both_probe", "miniswe_spl_repair"),
        ("both_probe", "miniswe_spl_localization"),
    ]
    print("\n=== paired comparisons (left vs right) ===")
    rows = []
    for left, right in pairs:
        g = l = b = n = 0
        tdiffs = []
        for iid in iids:
            rl, rr = R[left].get(iid, False), R[right].get(iid, False)
            if rl and not rr:
                l += 1
            elif not rl and rr:
                g += 1
            elif rl and rr:
                b += 1
            else:
                n += 1
            tdiffs.append(T[left].get(iid, 0) - T[right].get(iid, 0))
        net = g - l
        p = mcnemar_p(g, l)
        mean_td = sum(tdiffs) / len(tdiffs)
        med_td = sorted(tdiffs)[len(tdiffs) // 2]
        rows.append((left, right, g, l, b, n, net, p, mean_td, med_td))
        print(f"{left:24s} vs {right:12s} gain={g:3d} loss={l:3d} both={b:3d} neither={n:3d} "
              f"net={net:+3d} p={p:.6f} meanTokDiff={mean_td:+.0f} medTokDiff={med_td:+.0f}")

    # Holm over the primary family: the 4 SPL-relevant comparisons
    primary = rows[:4]  # original/free_summary/localization/repair vs both_probe
    ps = [r[7] for r in primary]
    hs = holm(ps)
    print("\n=== Holm-corrected (probe_both vs each baseline) ===")
    for r, h in zip(primary, hs):
        print(f"{r[0]:24s} vs both_probe  net={r[6]:+3d}  raw_p={r[7]:.6f}  holm_p={h:.6f}")

    # failure mode: empty-patch count per condition
    print("\n=== empty-patch counts ===")
    for cond in list(CONDS) + ["miniswe_spl_both_orig", "miniswe_spl_both_probe"]:
        empty = sum(1 for iid in iids if not (R.get(cond, {}).get(iid, False) or False)
                    and not (result[cond]["patch"] >= 0 and False))
    # recompute empty patch properly
    for cond, emap in [("miniswe_original", oe), ("miniswe_free_summary", oe),
                       ("miniswe_spl_localization", oe), ("miniswe_spl_repair", oe),
                       ("miniswe_spl_both_orig", oe), ("miniswe_spl_both_probe", pe)]:
        empty = sum(1 for iid in iids if not emap.get((iid, cond), {}).get("patch_generated"))
        print(f"{cond:26s} empty_patch={empty}")


if __name__ == "__main__":
    main()
