from __future__ import annotations

import json
import random
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
EXP = ROOT
SOURCE_RESULTS = EXP / "data/raw_results/exp3_swebench/random218_compact"
SOURCE_MANIFEST = EXP / "data/RQ3/inputs/random218_full_semantic_summary/manifest.json"
STUDY = "budget_relaxation_80step_stratified30"
ARTIFACT_DIR = EXP / "data/RQ3/inputs" / STUDY
RESULT_DIR = EXP / "data/results/reproduced_runs" / STUDY
CONFIG_DIR = RESULT_DIR / "configs"
RUN_DIR = RESULT_DIR / "runs"
SEED = 12680


def read_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(data, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def project_relative(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def resolve_categories() -> tuple[dict[str, list[dict]], list[dict]]:
    manifest = read_json(SOURCE_MANIFEST)
    by_id = {row["instance_id"]: row for row in manifest}
    categories: dict[str, list[dict]] = {
        "spl_only": [],
        "original_only": [],
        "neither": [],
        "both": [],
    }
    audit_rows: list[dict] = []
    for unit_dir in sorted((SOURCE_RESULTS / "units").glob("unit_*")):
        rows = read_json(unit_dir / "runs/evaluation.json")
        instance_id = next(row["instance_id"] for row in rows if isinstance(row, dict))
        verdict = {row["condition"]: bool(row.get("resolved")) for row in rows}
        original = verdict["miniswe_original"]
        repair = verdict["miniswe_spl_repair"]
        if original and repair:
            category = "both"
        elif original:
            category = "original_only"
        elif repair:
            category = "spl_only"
        else:
            category = "neither"
        item = dict(by_id[instance_id])
        categories[category].append(item)
        audit_rows.append(
            {
                "instance_id": instance_id,
                "source_unit": unit_dir.name,
                "original_36_resolved": original,
                "spl_repair_36_resolved": repair,
                "stratum": category,
            }
        )
    return categories, audit_rows


def sanitized_config(source: dict, *, conditions: list[str]) -> dict:
    cfg = dict(source)
    for key in ("api_key", "api_keys", "api_key_pool_file"):
        cfg.pop(key, None)
    cfg.update(
        {
            "artifact_dir": project_relative(ARTIFACT_DIR),
            "run_dir": project_relative(RUN_DIR),
            "provider": "openai",
            "model": "DeepSeek-V4-Pro",
            "api_key": None,
            "api_keys": [],
            "api_key_env": "OPENAI_API_KEY",
            "api_key_pool_file": None,
            "base_url": "https://api.scnet.cn/api/llm/v1",
            "mini_step_limit": 80,
            "conditions": conditions,
            "indices": [],
            "run_swebench_harness": False,
            "resume_existing_conditions": True,
            "resume_existing_evaluations": True,
            "force_rerun_swebench_harness": False,
            "reuse_existing_swebench_harness_only": False,
            "swebench_harness_run_id_prefix": "exp3_budget80_s30",
            "smoke_run_id": "exp3_budget80_s30",
            "experiment_label": (
                "Experiment 3 budget relaxation: fixed stratified 30 instances, "
                "80 interaction steps, frozen SPL/summary assets reused."
            ),
        }
    )
    return cfg


def main() -> None:
    categories, audit_rows = resolve_categories()
    assert {key: len(value) for key, value in categories.items()} == {
        "spl_only": 36,
        "original_only": 7,
        "neither": 68,
        "both": 107,
    }
    rng = random.Random(SEED)
    selected = (
        list(categories["original_only"])
        + rng.sample(categories["spl_only"], 12)
        + rng.sample(categories["neither"], 11)
    )
    selected.sort(key=lambda row: int(row["index"]))
    selected_ids = {row["instance_id"] for row in selected}
    selected_audit = [row for row in audit_rows if row["instance_id"] in selected_ids]
    selected_audit.sort(key=lambda row: next(x["index"] for x in selected if x["instance_id"] == row["instance_id"]))

    write_json(ARTIFACT_DIR / "manifest.json", selected)
    write_json(
        RESULT_DIR / "selection_audit.json",
        {
            "study": STUDY,
            "selection_source": "final 36-step random218 evaluator results",
            "seed": SEED,
            "population": 218,
            "excluded_stratum": {"both_resolved": 107, "selected": 0},
            "selected_strata": {
                "original_only": {"available": 7, "selected": 7},
                "spl_only": {"available": 36, "selected": 12},
                "neither": {"available": 68, "selected": 11},
            },
            "selected_count": len(selected),
            "instances": selected_audit,
        },
    )

    base_main = read_json(SOURCE_RESULTS / "configs/unit_001_pydata__xarray-3151.json")
    main_conditions = [
        "miniswe_original",
        "miniswe_free_summary",
        "miniswe_spl_localization",
        "miniswe_spl_repair",
        "miniswe_spl_both",
    ]
    main_cfg = sanitized_config(base_main, conditions=main_conditions)
    semantic_cfg = sanitized_config(base_main, conditions=["miniswe_full_semantic_summary"])
    eval_cfg = sanitized_config(
        base_main,
        conditions=main_conditions + ["miniswe_full_semantic_summary"],
    )
    eval_cfg["run_swebench_harness"] = True

    write_json(CONFIG_DIR / "generation_main_five.json", main_cfg)
    write_json(CONFIG_DIR / "generation_full_semantic.json", semantic_cfg)
    write_json(CONFIG_DIR / "evaluation_all_six.json", eval_cfg)
    write_json(
        RESULT_DIR / "experiment_manifest.json",
        {
            "study": STUDY,
            "sample_count": 30,
            "method_count": 6,
            "work_items": 180,
            "step_limit": 80,
            "temperature": main_cfg["temperature"],
            "max_output_tokens": main_cfg["max_output_tokens"],
            "max_workers": main_cfg["max_workers"],
            "model": main_cfg["model"],
            "base_url": main_cfg["base_url"],
            "credential_policy": "OPENAI_API_KEY process environment only; no key persisted",
            "frozen_assets_reused": True,
            "generation_before_evaluation": True,
            "conditions": eval_cfg["conditions"],
            "configs": {
                "main_generation": project_relative(CONFIG_DIR / "generation_main_five.json"),
                "semantic_generation": project_relative(CONFIG_DIR / "generation_full_semantic.json"),
                "evaluation": project_relative(CONFIG_DIR / "evaluation_all_six.json"),
            },
        },
    )
    print(f"Prepared {len(selected)} instances and 180 work items in {RESULT_DIR}")


if __name__ == "__main__":
    main()
