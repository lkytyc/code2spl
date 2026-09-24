import json, sys, os
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
RUN = str(ROOT / "data/raw_results/exp2_core/deepseek-v4-pro_full341_thinking")
rows = json.load(open(os.path.join(RUN, "evaluation.json"), encoding="utf-8"))

# index by (task_id, mode, condition) -> row  (mode disambiguates source/trace sharing a task_id)
by = {}
for r in rows:
    by[(r["task_id"], r.get("mode"), r["condition"])] = r

task_types = ["data", "control", "infoflow"]

def compare(base_cond, spl_cond):
    out = {}
    for tt in task_types:
        gain = regr = both_wrong = both_right = n = 0
        gain_ids, regr_ids = [], []
        # collect task_ids from base condition
        for (tid, mode, c), r in by.items():
            if c != base_cond:
                continue
            if r["task_type"] != tt:
                continue
            n += 1
            b = by.get((tid, mode, base_cond))
            s = by.get((tid, mode, spl_cond))
            if b is None or s is None:
                continue
            bc, sc = b["correct"], s["correct"]
            if not bc and sc:
                gain += 1; gain_ids.append(tid)
            elif bc and not sc:
                regr += 1; regr_ids.append(tid)
            elif not bc and not sc:
                both_wrong += 1
            else:
                both_right += 1
        out[tt] = dict(n=n, gain=gain, regr=regr, both_wrong=both_wrong, both_right=both_right,
                       gain_ids=gain_ids, regr_ids=regr_ids)
    return out

for base in ["official_raw", "raw_free_summary"]:
    print(f"\n===== raw_spl_atomic_strict vs {base} =====")
    res = compare(base, "raw_spl_atomic_strict")
    for tt in task_types:
        d = res[tt]
        print(f"\n[{tt}] n={d['n']}  gain={d['gain']}  regr={d['regr']}  both_wrong={d['both_wrong']}  both_right={d['both_right']}")
        print(f"  net = gain - regr = {d['gain']-d['regr']}")
        if d['gain_ids']:
            print(f"  GAIN ({len(d['gain_ids'])}): {d['gain_ids'][:12]}{'...' if len(d['gain_ids'])>12 else ''}")
        if d['regr_ids']:
            print(f"  REGR ({len(d['regr_ids'])}): {d['regr_ids'][:12]}{'...' if len(d['regr_ids'])>12 else ''}")
