"""Consolidate the SPL structure ablation (tagged vs compact) across models.

Compares, per model, the frozen tagged conditions (`spl_only`, `skeleton_spl`)
against the compact no-tag conditions (`spl_only_compact`, `skeleton_spl_compact`)
on the identical task set and SPL content.

Reports both the raw n=100 view and the reference-valid view (tasks whose gold
solution also passes in this environment), plus McNemar exact tests, token
usage, and wall-clock/resource data. Writes one JSON per model run.
"""

from __future__ import annotations

import json
import sys
from math import comb
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]

# model -> (tagged run dir, compact run dir)
MODELS = {
    "gpt-5.4-mini": (
        "data/raw_results/exp1_classeval/model_runs/gpt-5.4-mini/full100",
        "data/raw_results/exp1_classeval/model_runs/gpt-5.4-mini/full100_spl_structure_ablation",
    ),
    "gpt-5.4": (
        "data/raw_results/exp1_classeval/model_runs/gpt-5.4/full100",
        "data/raw_results/exp1_classeval/model_runs/gpt-5.4/full100_spl_structure_ablation",
    ),
    "deepseek-v4-pro": (
        "data/raw_results/exp1_classeval/model_runs/deepseek-v4-pro/full100",
        "data/raw_results/exp1_classeval/model_runs/deepseek-v4-pro/full100_spl_structure_ablation",
    ),
    "deepseek-v4-flash-0731": (
        "data/raw_results/exp1_classeval/model_runs/deepseek-v4-flash/full100",
        "data/raw_results/exp1_classeval/model_runs/deepseek-v4-flash-0731/full100_spl_structure_ablation",
    ),
    "claude-opus-5": (
        "data/raw_results/exp1_classeval/model_runs/claude-opus-5/full100",
        "data/raw_results/exp1_classeval/model_runs/claude-opus-5/full100_spl_structure_ablation",
    ),
}

PAIRS = [("spl_only", "spl_only_compact"), ("skeleton_spl", "skeleton_spl_compact")]


def read_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def mcnemar_exact(b: int, c: int) -> dict:
    """Two-sided exact McNemar (binomial) test on discordant pairs."""
    n = b + c
    if n == 0:
        return {"b_tagged_only": b, "c_compact_only": c, "n_discordant": 0, "p_value": 1.0}
    k = min(b, c)
    tail = sum(comb(n, i) for i in range(0, k + 1)) / (2 ** n)
    p = min(1.0, 2.0 * tail)
    return {"b_tagged_only": b, "c_compact_only": c, "n_discordant": n, "p_value": p}


def load_run(run_dir: Path):
    """Return (rows_by_task_condition, valid_task_ids, reference_rows)."""
    ev = read_json(run_dir / "evaluation.json")
    by_key = {(r["task_id"], r["condition"]): r for r in ev}
    ref_path = run_dir / "reference_evaluation.json"
    valid = None
    if ref_path.exists():
        ref = read_json(ref_path)
        # reference_evaluation.json rows use `class_test_ok` for the gold solution.
        valid = {r["task_id"] for r in ref if r.get("class_test_ok")}
    return by_key, valid, ev


def pct(hits: int, total: int) -> float | None:
    return (hits / total) if total else None


def reference_invalid(run_dir: Path) -> set[str]:
    path = run_dir / "reference_evaluation.json"
    if not path.exists():
        return set()
    ref = read_json(path)
    return {r["task_id"] for r in ref if not r.get("class_test_ok")}


def compare(tagged_dir: Path, compact_dir: Path, excluded: set[str]) -> dict:
    t_by, _t_valid, t_ev = load_run(tagged_dir)
    c_by, _c_valid, c_ev = load_run(compact_dir)
    all_tasks = sorted({r["task_id"] for r in t_ev} | {r["task_id"] for r in c_ev})
    # A single fixed exclusion set is applied to every model so that the
    # denominator is identical across models and conditions.
    valid_tasks = [tid for tid in all_tasks if tid not in excluded]

    out = {
        "tagged_run_dir": str(tagged_dir.relative_to(ROOT)).replace("\\", "/"),
        "compact_run_dir": str(compact_dir.relative_to(ROOT)).replace("\\", "/"),
        "n_total": len(all_tasks),
        "n_valid": len(valid_tasks),
        "excluded_tasks": sorted(t for t in excluded if t in set(all_tasks)),
        "tagged_reference_invalid": sorted(reference_invalid(tagged_dir)),
        "compact_reference_invalid": sorted(reference_invalid(compact_dir)),
        "conditions": {},
    }

    for tag_cond, comp_cond in PAIRS:
        entry: dict = {"tagged_condition": tag_cond, "compact_condition": comp_cond}
        for label, tasks in (("raw_n100", all_tasks), ("valid_only", valid_tasks)):
            t_hits = c_hits = b = c = 0
            t_syn = c_syn = 0
            rows_n = 0
            for tid in tasks:
                t_row = t_by.get((tid, tag_cond))
                c_row = c_by.get((tid, comp_cond))
                if t_row is None or c_row is None:
                    continue
                rows_n += 1
                t_ok = bool(t_row.get("class_test_ok"))
                c_ok = bool(c_row.get("class_test_ok"))
                t_hits += int(t_ok)
                c_hits += int(c_ok)
                t_syn += int(bool(t_row.get("syntax_ok")))
                c_syn += int(bool(c_row.get("syntax_ok")))
                b += int(t_ok and not c_ok)
                c += int(c_ok and not t_ok)
            entry[label] = {
                "n": rows_n,
                "tagged_passes": t_hits,
                "compact_passes": c_hits,
                "tagged_pass_rate": pct(t_hits, rows_n),
                "compact_pass_rate": pct(c_hits, rows_n),
                "tagged_syntax_rate": pct(t_syn, rows_n),
                "compact_syntax_rate": pct(c_syn, rows_n),
                "delta_tagged_minus_compact": (pct(t_hits, rows_n) or 0) - (pct(c_hits, rows_n) or 0),
                "mcnemar": mcnemar_exact(b, c),
            }
        out["conditions"][tag_cond] = entry

    return out


def usage_for(run_dir: Path) -> dict:
    out = {}
    for name in ("usage_summary.json", "cost_summary.json", "enhanced_summary.json", "summary.json"):
        p = run_dir / name
        if p.exists():
            out[name] = read_json(p)
    res = run_dir / "resource_usage" / "pipeline.json"
    if res.exists():
        row = read_json(res)
        out["pipeline"] = {
            "total_wall_seconds_all_attempts": row.get("total_wall_seconds_all_attempts"),
            "peak_process_tree_rss_mib": row.get("peak_process_tree_rss_mib"),
            "stages": [
                {"stage": s.get("stage"), "wall_seconds": s.get("wall_seconds"), "returncode": s.get("returncode")}
                for s in row.get("stages", [])
            ],
        }
    return out


def main() -> int:
    only = sys.argv[1:] or list(MODELS)
    aggregate: dict = {"models": {}, "shared_exclusion_set": []}

    # ── Reference-agreement diagnostic ───────────────────────────────────
    # Every run dir re-executes the gold solution. A task whose gold passes in
    # some runs and fails in others is nondeterministic (unseeded random,
    # timing) or resource-sensitive, and must be excluded from every model so
    # the denominator is comparable.
    agreement: dict[str, dict] = {}
    for model in only:
        for rel in MODELS[model]:
            run_dir = ROOT / rel
            path = run_dir / "reference_evaluation.json"
            if not path.exists():
                continue
            for row in read_json(path):
                rec = agreement.setdefault(row["task_id"], {"runs": 0, "ok": 0})
                rec["runs"] += 1
                rec["ok"] += int(bool(row.get("class_test_ok")))
    flaky = sorted(t for t, r in agreement.items() if 0 < r["ok"] < r["runs"])
    stable_bad = sorted(t for t, r in agreement.items() if r["ok"] == 0)
    print(f"reference never passes ({len(stable_bad)}): {stable_bad}")
    print(f"reference flaky ({len(flaky)}): "
          + ", ".join(f"{t}({agreement[t]['ok']}/{agreement[t]['runs']})" for t in flaky))
    aggregate["reference_agreement"] = agreement
    aggregate["reference_stable_failures"] = stable_bad
    aggregate["reference_flaky_tasks"] = flaky

    # Shared exclusion set: any task whose gold solution is not evaluable in
    # this environment for at least one model/condition. Applied identically
    # to every model so the denominators match.
    excluded: set[str] = set()
    for model in only:
        tagged_rel, compact_rel = MODELS[model]
        for rel in (tagged_rel, compact_rel):
            excluded |= reference_invalid(ROOT / rel)
    print(f"shared exclusion set ({len(excluded)}): {sorted(excluded)}")
    aggregate["shared_exclusion_set"] = sorted(excluded)

    for model in only:
        tagged_rel, compact_rel = MODELS[model]
        tagged_dir = ROOT / tagged_rel
        compact_dir = ROOT / compact_rel
        if not (tagged_dir / "evaluation.json").exists() or not (compact_dir / "evaluation.json").exists():
            print(f"[skip] {model}: missing evaluation.json "
                  f"(tagged={tagged_dir.exists()}/{compact_dir.exists()})")
            continue
        result = compare(tagged_dir, compact_dir, excluded)
        result["model"] = model
        result["tagged_usage"] = usage_for(tagged_dir)
        result["compact_usage"] = usage_for(compact_dir)
        out_path = compact_dir / "structure_ablation_comparison.json"
        out_path.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

        print(f"\n=== {model} ===")
        print(f"  n_total={result['n_total']}  n_valid={result['n_valid']}  "
              f"excluded={result['excluded_tasks']}")
        for tag_cond, entry in result["conditions"].items():
            v = entry["valid_only"]
            r = entry["raw_n100"]
            fmt = lambda x: "  n/a" if x is None else f"{x:.1%}"
            print(f"  {tag_cond:14s} tagged {fmt(v['tagged_pass_rate'])} "
                  f"({v['tagged_passes']}/{v['n']}) vs compact {fmt(v['compact_pass_rate'])} "
                  f"({v['compact_passes']}/{v['n']})  "
                  f"b={v['mcnemar']['b_tagged_only']} c={v['mcnemar']['c_compact_only']} "
                  f"p={v['mcnemar']['p_value']:.4f}   "
                  f"[raw100: {fmt(r['tagged_pass_rate'])} vs {fmt(r['compact_pass_rate'])}]")
        print(f"  wrote {out_path.relative_to(ROOT)}")
        aggregate["models"][model] = {
            "n_valid": result["n_valid"],
            "excluded_tasks": result["excluded_tasks"],
            "tagged_run_dir": result["tagged_run_dir"],
            "compact_run_dir": result["compact_run_dir"],
            "conditions": result["conditions"],
            "tagged_usage": result["tagged_usage"],
            "compact_usage": result["compact_usage"],
        }

    agg_path = ROOT / "data/results/exp1_classeval/model_runs/structure_ablation_all_models.json"
    if aggregate["models"]:
        agg_path.write_text(json.dumps(aggregate, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(f"\nwrote aggregate: {agg_path.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
