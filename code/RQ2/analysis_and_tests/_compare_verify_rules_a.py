import json, os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
FULL = str(ROOT / "data/raw_results/exp2_core/deepseek-v4-pro_full341_thinking")
NEW = str(ROOT / "data/raw_results/exp2_core/deepseek-v4-pro_verify_rules")
groups = json.load(open(ROOT / "data/RQ2/inputs/samples/rule_verification_ids.json", encoding="utf-8"))["groups"]

def load(run):
    by = {}
    for r in json.load(open(os.path.join(run, "evaluation.json"), encoding="utf-8")):
        by[(r["task_id"], r["mode"], r["condition"])] = r
    return by

full = load(FULL)
new = load(NEW)

def c(x): return "✓" if x else "✗"

def report(name, items, want):
    print(f"\n=== {name} ({len(items)}) ===")
    ok = 0
    for t, m in items:
        old = full.get((t, m, "raw_spl_atomic_strict"))
        nw = new.get((t, m, "raw_spl_atomic_strict"))
        if not nw:
            print(f"  {t} [{m}]: MISSING from new run")
            continue
        o = old["correct"] if old else None
        n = nw["correct"]
        good = want(n)
        ok += 1 if good else 0
        mark = "OK" if good else "BAD"
        print(f"  {t} [{m}]: old={c(o) if o is not None else '?'} new={c(n)}  {mark}")
    print(f"  => {ok}/{len(items)} satisfy target")

# regr12: want new correct (True)
report("regr12 (want FIXED)", groups["regr12"], lambda n: n)
# gains4: want new correct (True)
report("gains4 (want KEPT)", groups["gains4"], lambda n: n)
# loopbound_correct5: want new correct (True)
report("loopbound_correct5 (want KEPT)", groups["loopbound_correct5"], lambda n: n)
# data_correct15: want new correct (True, no new breakage)
report("data_correct15 (want no new breakage)", groups["data_correct15"], lambda n: n)
# control_correct8, infoflow_correct8: want new correct (True, unaffected)
report("control_correct8 (want unaffected)", groups["control_correct8"], lambda n: n)
report("infoflow_correct8 (want unaffected)", groups["infoflow_correct8"], lambda n: n)
