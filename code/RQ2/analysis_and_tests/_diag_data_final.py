import json, os, re, glob
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
RUN = str(ROOT / "data/raw_results/exp2_core/deepseek-v4-pro_full341_thinking")
rows = json.load(open(os.path.join(RUN, "evaluation.json"), encoding="utf-8"))
by = {}
for r in rows:
    by[(r["task_id"], r["mode"], r["condition"])] = r

def parse_pred(tid, mode, cond):
    d = os.path.join(RUN, f"{tid}__{mode}", cond, "output.txt")
    if not os.path.exists(d):
        return None
    txt = open(d, encoding="utf-8").read()
    # find the outermost {...} json block
    start = txt.find("{")
    if start < 0:
        return ("<unparsed>", txt[:200])
    depth = 0
    for i in range(start, len(txt)):
        if txt[i] == "{":
            depth += 1
        elif txt[i] == "}":
            depth -= 1
            if depth == 0:
                try:
                    obj = json.loads(txt[start:i+1])
                except Exception:
                    return ("<parse-fail>", txt[start:i+1][:200])
                if "DataDependenceSources" in obj:
                    return obj["DataDependenceSources"]
                if "edges" in obj or "trace" in obj or "nodes" in obj:
                    return obj
                return obj
    return ("<unparsed>", txt[:200])

def sk(x):
    return x  # keep [var, line] as list

print("=" * 100)
print("DATA REGRESSIONS (baseline correct, SPL wrong) — full detail")
print("=" * 100)
n = 0
for (t, m, c) in sorted(by.keys()):
    if c != "official_raw" or by[(t, m, c)]["task_type"] != "data":
        continue
    b = by[(t, m, "official_raw")]
    s = by.get((t, m, "raw_spl_atomic_strict"))
    if not s or b["correct"] or s["correct"]:
        continue
    n += 1
    oe = b["official_eval"]
    pred = parse_pred(t, m, "raw_spl_atomic_strict")
    if "ground_truth" in oe:
        gt = sorted([tuple(x) for x in oe["ground_truth"]])
        pred_disp = sorted([tuple(x) for x in pred]) if (pred is not None and not isinstance(pred, tuple)) else pred
        print(f"\n### [{n}] {t} [{m}]  GT={len(gt)} SPL={s['official_eval'].get('total_pred')}")
        print(f"  GT : {gt}")
        print(f"  SPL: {pred_disp}")
    else:
        # trace mode
        print(f"\n### [{n}] {t} [{m}]  (trace) correct_edges={oe.get('correct_edges')}/{oe.get('total_edges')}")
        print(f"  SPL pred: {pred}")

print("\n\n" + "=" * 100)
print("DATA GAINS (baseline wrong, SPL correct)")
print("=" * 100)
n = 0
for (t, m, c) in sorted(by.keys()):
    if c != "official_raw" or by[(t, m, c)]["task_type"] != "data":
        continue
    b = by[(t, m, "official_raw")]
    s = by.get((t, m, "raw_spl_atomic_strict"))
    if not s or b["correct"] or not s["correct"]:
        continue
    n += 1
    oe = b["official_eval"]
    pred = parse_pred(t, m, "raw_spl_atomic_strict")
    if "ground_truth" in oe:
        gt = sorted([tuple(x) for x in oe["ground_truth"]])
        pred_disp = sorted([tuple(x) for x in pred]) if (pred is not None and not isinstance(pred, tuple)) else pred
        print(f"\n### [{n}] {t} [{m}]  GT={len(gt)} SPL={s['official_eval'].get('total_pred')}")
        print(f"  GT : {gt}")
        print(f"  SPL: {pred_disp}")
    else:
        print(f"\n### [{n}] {t} [{m}]  (trace) correct_edges={oe.get('correct_edges')}/{oe.get('total_edges')}")
        print(f"  SPL pred: {pred}")
