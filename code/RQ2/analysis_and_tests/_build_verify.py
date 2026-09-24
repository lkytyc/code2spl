import json, os, random
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
RUN = str(ROOT / "data/raw_results/exp2_core/deepseek-v4-pro_full341_thinking")
rows = json.load(open(os.path.join(RUN, "evaluation.json"), encoding="utf-8"))
by = {}
for r in rows:
    by[(r["task_id"], r["mode"], r["condition"])] = r

def sk(t, m): return f"{t}::{m}"

# --- targeted groups (from diagnosis) ---
regr = [
    ("data_codenet_p02750_s264552825_solve_1_28_dp_17_8", "source"),
    ("data_codenet_p03040_s460303459_solve_12_62_lsum_42_4", "source"),
    ("data_codenet_p03089_s926931317_main_7_106_com_77_5", "source"),
    ("data_codenet_p03092_s117422561_main_7_70_dpmax_47_5", "trace"),
    ("data_codenet_p03263_s445539961_solve_6_99_x_73_5", "source"),
    ("data_gcj_20993c_2928ec_vestigial_1_37_column_digits_26_4", "source"),
    ("data_gcj_20993c_2928ec_2928ec_vestigial_1_37_i_24_7", "source"),
    ("data_gcj_3172d1_325a14_calc_1_47_tmp_12_2", "source"),
    ("data_gcj_3774db_378b24_ILA_1_60_end_49_9", "source"),
    ("data_gcj_459f2_4981c_solve_1_67_shadowed_39_7", "source"),
    ("data_gcj_459f2_4981c_solve_1_67_shadowed_50_7", "source"),
    ("data_gcj_7966_2bc41_hackTheSystem_10_70_c_54_7", "source"),
]
# fix a typo'd id above (vestigial i_24_7)
regr = [(t.replace("_2928ec_2928ec_", "_2928ec_"), m) for (t, m) in regr]

gains = [
    ("data_codenet_p02670_s760310872_main_8_63_ii_20_3", "source"),
    ("data_codenet_p02962_s348098217_solve_19_91_i_81_6", "source"),
    ("data_gcj_104e05_111e09_main_7_46_wrd1_24_4", "source"),
    ("data_gcj_3386d0_33e74d_main_4_92_turn_7_1", "trace"),
]

# loop-bound cases that are currently CORRECT (want to keep correct with syntax-aware rule)
loopbound_correct = [
    ("data_gcj_1461c8_14c548_solve_5_55_k_24_1", "source"),
    ("data_gcj_317409_3237d4_main_4_100_i_23_5", "source"),
    ("data_gcj_104e03_10a698_alienpylon_15_54_k_44_3", "source"),
    ("data_gcj_2fff7_330ba_main_22_75_P_42_7", "source"),
    ("data_gcj_459f2_47567_solve_18_98_i_33_3", "source"),
]

# currently-correct data samples (regression check) — pick a deterministic spread
data_correct = []
data_keys = [(t, m) for (t, m, c) in by.keys() if c == "official_raw" and by[(t, m, c)]["task_type"] == "data"]
already = set(sk(t, m) for t, m in regr + gains + loopbound_correct)
for t, m in sorted(data_keys):
    if sk(t, m) in already:
        continue
    b = by[(t, m, "official_raw")]
    s = by.get((t, m, "raw_spl_atomic_strict"))
    if b["correct"] and s and s["correct"]:
        data_correct.append((t, m))
# take a deterministic spread of 15
step = max(1, len(data_correct) // 15)
data_correct = data_correct[::step][:15]

# control + infoflow currently-correct samples (confirm unaffected) — 8 each
def pick_correct(task, n):
    out = []
    for (t, m, c) in sorted(by.keys()):
        if c != "official_raw" or by[(t, m, c)]["task_type"] != task:
            continue
        b = by[(t, m, "official_raw")]
        s = by.get((t, m, "raw_spl_atomic_strict"))
        if b["correct"] and s and s["correct"]:
            out.append((t, m))
    st = max(1, len(out) // n)
    return out[::st][:n]

ctrl_correct = pick_correct("control", 8)
info_correct = pick_correct("infoflow", 8)

groups = {
    "regr12": regr,
    "gains4": gains,
    "loopbound_correct5": loopbound_correct,
    "data_correct15": data_correct,
    "control_correct8": ctrl_correct,
    "infoflow_correct8": info_correct,
}
all_ids = []
for name, items in groups.items():
    for t, m in items:
        all_ids.append(sk(t, m))

out = {"experiment": "core_verify_rules", "n": len(all_ids), "sample_ids": all_ids, "groups": groups}
path = str(ROOT / "data/RQ2/inputs/samples/rule_verification_ids.json")
open(path, "w", encoding="utf-8").write(json.dumps(out, indent=2))
print("wrote", len(all_ids), "samples to", path)
for name, items in groups.items():
    print(f"  {name}: {len(items)}")
