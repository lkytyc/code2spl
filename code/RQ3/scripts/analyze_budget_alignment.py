from __future__ import annotations

"""Budget-probe analysis: paired compare original `miniswe_spl_both` (138/218)
vs budget-matched probe `miniswe_spl_both` (4/750/2/1400), plus reference
against repair/localization in the ORIGINAL run.

Reads evaluation.json per unit from both run dirs, does:
  - overall resolved/patch counts per condition
  - paired exact McNemar (probe vs original-both) and flips listing
  - Wilson 95% CI on resolved/218
"""

import json
from collections import defaultdict
from math import sqrt
from pathlib import Path

EXP6 = Path(__file__).resolve().parents[1]
ORIG = EXP6 / "data/results/reproduced_runs/random218/units"
PROBE = EXP6 / "data/results/reproduced_runs/random218_budget_aligned/units"

COND = "miniswe_spl_both"


def load_cond(run_units: Path, cond: str) -> dict[str, dict]:
    out = {}
    for ep in sorted(run_units.glob("unit_*/runs/evaluation.json")):
        rows = json.loads(ep.read_text(encoding="utf-8"))
        for r in rows:
            if isinstance(r, dict) and r.get("condition") == cond:
                iid = r.get("instance_id") or ep.parts[-3]
                out[iid] = r
    return out


def wilson(k: int, n: int, z: float = 1.96) -> tuple[float, float]:
    if n == 0:
        return (0.0, 0.0)
    p = k / n
    denom = 1 + z * z / n
    centre = p + z * z / (2 * n)
    half = z * sqrt(p * (1 - p) / n + z * z / (4 * n * n))
    return ((centre - half) / denom, (centre + half) / denom)


def mcnemar(b: int, c: int) -> float:
    """b = probe-only-gain, c = orig-only-gain. Exact binomial two-sided."""
    if b + c == 0:
        return 1.0
    from math import comb
    n = b + c
    p = 0.5
    lo = min(b, c)
    hi = max(b, c)
    tail = sum(comb(n, i) * (p ** n) for i in range(0, lo + 1))
    tail += sum(comb(n, i) * (p ** n) for i in range(hi, n + 1))
    return min(1.0, tail)


def main() -> None:
    orig = load_cond(ORIG, COND)
    probe = load_cond(PROBE, COND)
    # reference conditions in original run
    ref = {}
    for cond in ("miniswe_original", "miniswe_free_summary",
                 "miniswe_spl_localization", "miniswe_spl_repair"):
        ref[cond] = load_cond(ORIG, cond)

    keys = sorted(set(orig) | set(probe))
    print(f"instances: orig={len(orig)} probe={len(probe)} union={len(keys)}")

    def resolved(d: dict, iid: str) -> bool:
        return bool(d.get(iid, {}).get("resolved"))

    def patched(d: dict, iid: str) -> bool:
        return bool(d.get(iid, {}).get("patch_generated"))

    # counts
    print("\n=== resolved / patch (denominator = 218) ===")
    for name, d in [("orig_both", orig), ("probe_both", probe)]:
        r = sum(resolved(d, k) for k in keys)
        p = sum(patched(d, k) for k in keys)
        lo, hi = wilson(r, len(keys))
        print(f"{name:12s} resolved={r}/218 ({r/len(keys)*100:.1f}%) [{lo*100:.1f},{hi*100:.1f}]  patch={p}")

    print("\n=== reference (original run, same 218) ===")
    for name, d in ref.items():
        r = sum(resolved(d, k) for k in keys)
        p = sum(patched(d, k) for k in keys)
        lo, hi = wilson(r, len(keys))
        print(f"{name:22s} resolved={r}/218 ({r/len(keys)*100:.1f}%) [{lo*100:.1f},{hi*100:.1f}]  patch={p}")

    # paired flips: probe vs orig_both
    gain = []   # orig fail -> probe resolved
    loss = []   # orig resolved -> probe fail
    for k in keys:
        o, pr = resolved(orig, k), resolved(probe, k)
        if not o and pr:
            gain.append(k)
        elif o and not pr:
            loss.append(k)
    b, c = len(gain), len(loss)
    print(f"\n=== paired flips probe vs orig_both ===")
    print(f"probe-gain (orig fail -> probe resolved): {b}")
    for k in gain:
        print(f"   + {k}")
    print(f"probe-loss (orig resolved -> probe fail): {c}")
    for k in loss:
        print(f"   - {k}")
    print(f"McNemar (two-sided exact): p={mcnemar(b, c):.6f}")

    # also which flips are empty-patch -> resolved, or patch-not-resolved -> resolved
    print("\n=== gain instances: original failure mode ===")
    for k in gain:
        o = orig[k]
        mode = "empty_patch" if not o.get("patch_generated") else "patch_not_resolved"
        print(f"   {k}: {mode}")

    print("\n=== loss instances: probe failure mode ===")
    for k in loss:
        p = probe[k]
        mode = "empty_patch" if not p.get("patch_generated") else "patch_not_resolved"
        print(f"   {k}: {mode}")


if __name__ == "__main__":
    main()
