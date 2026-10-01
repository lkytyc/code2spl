"""Exp2 supplement: SPL semantic content with the keyword structure removed.

Compares the new `raw_spl_unstructured_summary` condition against the three
frozen Exp2 conditions, on the same 341 frozen samples, and writes the tables
that the supplement document quotes.

Metrics, all on the 341-sample denominator (no per-condition drops):
  strict_correct / correct / parsed, with Wilson 95% intervals.
Pairing is on (task_id, mode): the two `mode` values of one task_id are two
different samples, so they must not be collapsed.
Significance is the two-sided exact McNemar test.  The three overall
comparisons form the primary family and get a Holm correction; the stratified
breakdowns are descriptive and are reported uncorrected, as a family of
stratified tests would not be a pre-specified family.

Reads only; writes only into the new run directory.
"""

from __future__ import annotations

import json
import math
import os
import sys
from collections import defaultdict

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
PACKAGE_ROOT = os.path.dirname(os.path.dirname(ROOT))
PACKAGE_ROOT = os.path.dirname(os.path.dirname(ROOT))
FROZEN = os.path.join(PACKAGE_ROOT, "data/raw_results/exp2_core/deepseek-v4-pro_full341_thinking")
NEW = os.path.join(
    PACKAGE_ROOT, "data/raw_results/exp2_core/deepseek-v4-pro_full341_unstructured_summary"
)

BASELINES = ["official_raw", "raw_free_summary", "raw_spl_atomic_strict"]
NEW_COND = "raw_spl_unstructured_summary"
TASK_TYPES = ["control", "data", "infoflow"]
MODES = ["source", "trace"]
FROZEN_POOL = BASELINES + [NEW_COND]  # conditions present across the two run dirs

Z = 1.959963984540054


def wilson(k: int, n: int) -> tuple[float, float]:
    if n == 0:
        return (0.0, 0.0)
    p = k / n
    d = 1 + Z * Z / n
    centre = (p + Z * Z / (2 * n)) / d
    half = Z * math.sqrt(p * (1 - p) / n + Z * Z / (4 * n * n)) / d
    return (max(0.0, centre - half), min(1.0, centre + half))


def mcnemar_exact(b: int, c: int) -> float:
    """Two-sided exact McNemar p-value; b/c are the two discordant counts."""
    n = b + c
    if n == 0:
        return 1.0
    k = min(b, c)
    tail = sum(math.comb(n, i) for i in range(k + 1)) / (2 ** n)
    return min(1.0, 2 * tail)


def holm(pvals: list[float]) -> list[float]:
    m = len(pvals)
    order = sorted(range(m), key=lambda i: pvals[i])
    out = [0.0] * m
    running = 0.0
    for rank, i in enumerate(order):
        adj = min(1.0, pvals[i] * (m - rank))
        running = max(running, adj)
        out[i] = running
    return out


def load_rows(path: str) -> list[dict]:
    with open(os.path.join(path, "evaluation.json"), encoding="utf-8") as fh:
        return json.load(fh)


def index(rows: list[dict]) -> dict[tuple[str, str], dict[str, dict]]:
    """(task_id, mode) -> condition -> row."""
    out: dict[tuple[str, str], dict[str, dict]] = defaultdict(dict)
    for r in rows:
        out[(r["task_id"], r.get("mode"))][r["condition"]] = r
    return out


def counts(rows: list[dict]) -> dict:
    n = len(rows)
    return {
        "n": n,
        "strict_correct": sum(bool(r["strict_correct"]) for r in rows),
        "correct": sum(bool(r["correct"]) for r in rows),
        "parsed": sum(bool(r["parsed"]) for r in rows),
    }


def table(by_cond: dict[str, list[dict]], keys: list[str]) -> dict:
    out = {}
    for cond in keys:
        c = counts(by_cond[cond])
        lo, hi = wilson(c["strict_correct"], c["n"])
        out[cond] = {**c, "strict_ci95": [round(lo, 4), round(hi, 4)]}
    return out


def main() -> int:
    frozen_rows = load_rows(FROZEN)
    new_rows = load_rows(NEW)
    for r in new_rows:
        r["condition"] = NEW_COND  # single-condition run; name it explicitly

    all_rows = frozen_rows + new_rows
    pairs = index(all_rows)

    # sanity: every pair must carry all four conditions
    missing = []
    for key, conds in pairs.items():
        for cond in FROZEN_POOL:
            if cond not in conds:
                missing.append((key, cond))
    if missing:
        print(f"ERROR: {len(missing)} (sample, condition) slots missing, e.g. {missing[:5]}")
        return 1

    by_cond: dict[str, list[dict]] = defaultdict(list)
    for conds in pairs.values():
        for cond, r in conds.items():
            by_cond[cond].append(r)

    result: dict = {"n_pairs": len(pairs), "overall": table(by_cond, FROZEN_POOL)}

    # --- stratified ---------------------------------------------------------
    for field, levels in (("task_type", TASK_TYPES), ("mode", MODES)):
        result[f"by_{field}"] = {}
        for lv in levels:
            sub = defaultdict(list)
            for conds in pairs.values():
                r0 = conds[NEW_COND]
                if r0.get(field) != lv:
                    continue
                for cond, r in conds.items():
                    sub[cond].append(r)
            result[f"by_{field}"][lv] = table(sub, FROZEN_POOL)

    # --- task_type x mode (mirrors the main report's 8.2 table) --------------
    result["by_task_type_mode"] = {}
    for tt in TASK_TYPES:
        for md in MODES:
            sub = defaultdict(list)
            for conds in pairs.values():
                r0 = conds[NEW_COND]
                if r0.get("task_type") != tt or r0.get("mode") != md:
                    continue
                for cond, r in conds.items():
                    sub[cond].append(r)
            if not sub[NEW_COND]:
                continue
            result["by_task_type_mode"][f"{tt}_{md}"] = table(sub, FROZEN_POOL)

    # --- paired significance -------------------------------------------------
    def paired(subset_keys, base_cond, test_cond=NEW_COND):
        b = c = both = neither = 0
        for key in subset_keys:
            t, s = pairs[key][test_cond], pairs[key][base_cond]
            tc, bc = bool(t["strict_correct"]), bool(s["strict_correct"])
            if tc and not bc:
                b += 1
            elif bc and not tc:
                c += 1
            elif tc and bc:
                both += 1
            else:
                neither += 1
        return {"b_new_only": b, "c_base_only": c, "both": both, "neither": neither,
                "net": b - c, "p_exact": mcnemar_exact(b, c)}

    all_keys = list(pairs.keys())
    overall = {base: paired(all_keys, base) for base in BASELINES}
    ps = holm([overall[b]["p_exact"] for b in BASELINES])
    for base, adj in zip(BASELINES, ps):
        overall[base]["p_holm"] = adj
    result["mcnemar_overall"] = overall

    result["mcnemar_by_task_type"] = {}
    for tt in TASK_TYPES:
        keys = [k for k in all_keys if pairs[k][NEW_COND].get("task_type") == tt]
        result["mcnemar_by_task_type"][tt] = {b: paired(keys, b) for b in BASELINES}

    result["mcnemar_by_mode"] = {}
    for md in MODES:
        keys = [k for k in all_keys if pairs[k][NEW_COND].get("mode") == md]
        result["mcnemar_by_mode"][md] = {b: paired(keys, b) for b in BASELINES}

    # --- sensitivity: drop samples whose frozen card no longer exists --------
    # `run.py` reads each sample's cards from `artifact_dir/<sample>/spl_by_method.json`.
    # 38 of the 341 frozen cards were empty `# JSON_PARSE_ERROR` dumps at the time
    # the OLD-protocol batch ran and were regenerated afterwards, so the frozen
    # `raw_spl_atomic_strict` arm used a 55-character placeholder on exactly those
    # samples while this arm uses the regenerated card.  That drift favours this
    # arm, so the comparison is re-run on the 303 card-identical samples.
    import re as _re
    blk = _re.compile(r"```spl\n(.*?)\n```", _re.S)
    art = os.path.join(PACKAGE_ROOT, "data/RQ2/spl_assets/builder_run_deepseek-v4-flash/artifacts")
    frozen_run = FROZEN
    drifted = []
    for key in all_keys:
        # the run directory is `<task_id>__<mode>`; `task_id` alone is ambiguous
        # because one task_id contributes both a `source` and a `trace` sample
        sample_id = f"{key[0]}__{key[1]}"
        p = os.path.join(frozen_run, sample_id, "raw_spl_atomic_strict", "prompt.txt")
        ap = os.path.join(art, sample_id, "spl_by_method.json")
        if not (os.path.isfile(p) and os.path.isfile(ap)):
            drifted.append(sample_id)
            continue
        with open(p, encoding="utf-8") as fh:
            frozen_cards = [c.strip() for c in blk.findall(fh.read())]
        with open(ap, encoding="utf-8") as fh:
            current = {str(v).strip() for v in json.load(fh).values()}
        if not frozen_cards or any(c not in current for c in frozen_cards):
            drifted.append(sample_id)
    clean_keys = [k for k in all_keys if f"{k[0]}__{k[1]}" not in set(drifted)]
    result["card_drift"] = {
        "samples_dropped": len(all_keys) - len(clean_keys),
        "sample_ids": sorted(set(drifted)),
        "note": ("frozen arm saw an empty placeholder card on these samples; "
                 "this arm saw the regenerated card"),
    }
    result["mcnemar_clean_subset"] = {b: paired(clean_keys, b) for b in BASELINES}
    ps = holm([result["mcnemar_clean_subset"][b]["p_exact"] for b in BASELINES])
    for base, adj in zip(BASELINES, ps):
        result["mcnemar_clean_subset"][base]["p_holm"] = adj
    result["clean_subset_overall"] = {
        cond: counts([pairs[k][cond] for k in clean_keys]) for cond in FROZEN_POOL
    }

    # --- usage ---------------------------------------------------------------
    usage = {}
    for cond in FROZEN_POOL:
        inp = out = tot = calls = 0
        secs = 0.0
        for r in by_cond[cond]:
            u = r.get("llm_usage") or {}
            inp += u.get("input_tokens", 0)
            out += u.get("output_tokens", 0)
            tot += u.get("total_tokens", 0)
            calls += u.get("calls", 0)
            secs += u.get("elapsed_seconds", 0.0)
        usage[cond] = {"calls": calls, "input_tokens": inp, "output_tokens": out,
                       "total_tokens": tot, "api_seconds": round(secs, 1)}
    result["usage"] = usage

    out_path = os.path.join(NEW, "supplement_analysis.json")
    with open(out_path, "w", encoding="utf-8") as fh:
        json.dump(result, fh, ensure_ascii=False, indent=2)

    # --- console -------------------------------------------------------------
    print(f"paired samples: {result['n_pairs']}")
    print(f"{'condition':<28} {'strict':>8} {'ok':>5} {'corr':>8} {'parsed':>8} "
          f"{'strict%':>8}  Wilson95")
    for cond in FROZEN_POOL:
        c = result["overall"][cond]
        lo, hi = c["strict_ci95"]
        print(f"{cond:<28} {c['strict_correct']:>5}/341 {c['n']:>5} {c['correct']:>5}/341 "
              f"{c['parsed']:>5}/341 {100*c['strict_correct']/c['n']:>7.1f}%  "
              f"[{100*lo:.1f}, {100*hi:.1f}]")

    print("\nMcNemar (exact), new vs baseline -- strict_correct:")
    for base in BASELINES:
        d = overall[base]
        print(f"  vs {base:<26} b={d['b_new_only']:>3} c={d['c_base_only']:>3} "
              f"net={d['net']:>+4}  p={d['p_exact']:.3g}  p_holm={d['p_holm']:.3g}")

    print("\nstratified by task_type (net = gains - regressions):")
    for tt in TASK_TYPES:
        n = len([k for k in all_keys if pairs[k][NEW_COND].get("task_type") == tt])
        row = "  ".join(
            f"{b.split('raw_')[-1][:9]}: {result['mcnemar_by_task_type'][tt][b]['net']:+d}"
            f"(p={result['mcnemar_by_task_type'][tt][b]['p_exact']:.2g})"
            for b in BASELINES
        )
        print(f"  [{tt:<8} n={n:>3}] {row}")

    print("\nstratified by mode:")
    for md in MODES:
        n = len([k for k in all_keys if pairs[k][NEW_COND].get("mode") == md])
        row = "  ".join(
            f"{b.split('raw_')[-1][:9]}: {result['mcnemar_by_mode'][md][b]['net']:+d}"
            f"(p={result['mcnemar_by_mode'][md][b]['p_exact']:.2g})"
            for b in BASELINES
        )
        print(f"  [{md:<8} n={n:>3}] {row}")

    print(f"\nsensitivity: dropping {result['card_drift']['samples_dropped']} samples whose "
          f"frozen card was later regenerated (n={len(clean_keys)}):")
    for cond in FROZEN_POOL:
        c = result["clean_subset_overall"][cond]
        print(f"  {cond:<30} {c['strict_correct']:>3}/{c['n']}")
    for base in BASELINES:
        d = result["mcnemar_clean_subset"][base]
        print(f"  vs {base:<26} b={d['b_new_only']:>3} c={d['c_base_only']:>3} "
              f"net={d['net']:>+4}  p={d['p_exact']:.3g}  p_holm={d['p_holm']:.3g}")

    print("\nby task_type x mode (strict):")
    for k, tab in result["by_task_type_mode"].items():
        cells = "  ".join(f"{c.split('raw_')[-1][:9]} {tab[c]['strict_correct']}/{tab[c]['n']}"
                          for c in FROZEN_POOL)
        print(f"  [{k:<16}] {cells}")

    print("\nusage:")
    for cond in FROZEN_POOL:
        u = usage[cond]
        print(f"  {cond:<28} calls={u['calls']:>4} in={u['input_tokens']:>9,} "
              f"out={u['output_tokens']:>9,} total={u['total_tokens']:>9,}")

    print(f"\nwrote {out_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
