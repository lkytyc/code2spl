from __future__ import annotations

import csv
import hashlib
import json
import shutil
from pathlib import Path


LONG_ROOT = Path(__file__).resolve().parents[3]
SHORT_ROOT = Path(r"C:\e")
ROOT = SHORT_ROOT if SHORT_ROOT.exists() and (SHORT_ROOT / "experiments").exists() else LONG_ROOT
EXP = ROOT
SOURCE = EXP / "data/raw_results/exp3_swebench/budget_relaxation_80step_stratified30"
SOURCE_INPUT = EXP / "data/RQ3/inputs/budget_relaxation_80step_stratified30"
PACKAGE = ROOT / "spl_reproducibility_package"
EXP3 = PACKAGE / "exp3_swebench"
NAME = "budget_relaxation_80step_stratified30"


def copy_file(source: Path, target: Path) -> None:
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, target)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> None:
    target_results = EXP3 / "results" / NAME
    if target_results.exists():
        raise FileExistsError(f"Refusing to overwrite existing package directory: {target_results}")
    shutil.copytree(SOURCE, target_results, copy_function=shutil.copy2)

    target_input = EXP3 / "inputs" / NAME
    shutil.copytree(SOURCE_INPUT, target_input, copy_function=shutil.copy2)
    copy_file(SOURCE / "selection_audit.json", target_input / "selection_audit.json")

    target_settings = EXP3 / "settings" / NAME
    shutil.copytree(SOURCE / "configs", target_settings, copy_function=shutil.copy2)
    copy_file(SOURCE / "experiment_manifest.json", target_settings / "experiment_manifest.json")

    target_code = EXP3 / "code" / "supplement_2026-09-19_budget_relaxation_80step"
    scripts = [
        "prepare_budget_relaxation_80step.py",
        "run_budget_relaxation_80step.py",
        "rerun_budget80_unavailable_eval.py",
        "summarize_budget_relaxation_80step.py",
        "package_budget_relaxation_80step.py",
    ]
    for script in scripts:
        copy_file(EXP / "scripts" / script, target_code / script)

    document = SOURCE / "exp3_budget_relaxation_80step_supplement.md"
    copy_file(document, EXP3 / "documentation" / document.name)
    copy_file(document, PACKAGE / document.name)

    package_readme = target_results / "README.md"
    package_readme.write_text(
        "# Experiment 3 Budget Relaxation (80 steps, stratified 30)\n\n"
        "This directory is a lossless copy of the completed supplement run.\n\n"
        "- `runs/`: all 180 agent outputs, trajectories, patches, model usage, and final SWE-bench evaluation.\n"
        "- `per_task_budget80_results.csv`: paper-ready 30 x 6 task-level table (UTF-8 BOM).\n"
        "- `budget80_summary.json`: aggregate, paired, transition, and stratum statistics.\n"
        "- `selection_audit.json`: deterministic sample selection evidence.\n"
        "- `exp3_budget_relaxation_80step_supplement.md`: complete experiment report.\n"
        "- `configs/`: exact launch/evaluation configs; no API credential is stored.\n"
        "- `execution/`: stage logs, including the two infrastructure-only evaluation retries.\n\n"
        "Frozen source/SPL/summary inputs are shared with the existing package directories "
        "`exp3_swebench/inputs/precomputed_random218_deepseek-v4-flash` and "
        "`exp3_swebench/spl_assets/random218_deepseek-v4-flash`; they were reused, not rebuilt.\n",
        encoding="utf-8",
    )

    roots = [target_results, target_input, target_settings, target_code]
    files = sorted({path for root in roots for path in root.rglob("*") if path.is_file()})
    inventory_path = target_results / "PACKAGE_FILE_INVENTORY.csv"
    with inventory_path.open("w", encoding="utf-8-sig", newline="") as stream:
        writer = csv.writer(stream)
        writer.writerow(["relative_path", "size_bytes", "sha256"])
        for path in files:
            writer.writerow([path.relative_to(PACKAGE).as_posix(), path.stat().st_size, sha256(path)])

    audit = {
        "package_subtree": f"exp3_swebench/results/{NAME}",
        "source_subtree": SOURCE.relative_to(ROOT).as_posix(),
        "copied_result_files_before_inventory": sum(1 for p in SOURCE.rglob("*") if p.is_file()),
        "packaged_files_in_audited_roots": len(files),
        "evaluation_rows": len(json.loads((target_results / "runs/evaluation.json").read_text(encoding="utf-8"))),
        "per_task_csv_data_rows": sum(1 for _ in (target_results / "per_task_budget80_results.csv").open(encoding="utf-8-sig")) - 1,
        "credential_scan": "performed after packaging",
    }
    (target_results / "PACKAGE_AUDIT.json").write_text(
        json.dumps(audit, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(audit, ensure_ascii=False))


if __name__ == "__main__":
    main()
