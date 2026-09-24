import argparse
import json
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_PLAN = ROOT / "runs" / "exp6_complex_top20_swebench_verified_20260721" / "optimized_plan" / "pipeline_plan.json"


def read_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8", errors="replace"))


def write_json(path: Path, data) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=True, indent=2) + "\n", encoding="utf-8")


def resolve_path(value: str | Path) -> Path:
    path = Path(value)
    return path if path.is_absolute() else ROOT / path


def aggregate_rows(plan: dict) -> tuple[list[dict], list[dict]]:
    rows = []
    missing = []
    for unit in plan.get("units", []):
        config = read_json(resolve_path(unit["config_path"]))
        evaluation_path = resolve_path(config["run_dir"]) / "evaluation.json"
        if not evaluation_path.exists():
            missing.append(
                {
                    "unit_no": unit["unit_no"],
                    "instance_id": unit["instance_id"],
                    "reason": "evaluation_json_missing",
                    "path": str(evaluation_path),
                }
            )
            continue
        try:
            unit_rows = read_json(evaluation_path)
        except (json.JSONDecodeError, OSError) as exc:
            missing.append(
                {
                    "unit_no": unit["unit_no"],
                    "instance_id": unit["instance_id"],
                    "reason": f"evaluation_json_invalid: {exc!r}",
                    "path": str(evaluation_path),
                }
            )
            continue
        for row in unit_rows:
            enriched = dict(row)
            enriched.update(
                {
                    "complexity_rank": unit.get("rank"),
                    "complexity_score": unit.get("complexity_score"),
                    "difficulty": unit.get("difficulty"),
                    "pipeline_unit_no": unit["unit_no"],
                    "pipeline_wave_no": unit["wave_no"],
                    "env_group": unit.get("env_group"),
                }
            )
            rows.append(enriched)
    return rows, missing


def summarize(rows: list[dict], conditions: list[str], expected_instances: int) -> dict:
    grouped: dict[str, list[dict]] = defaultdict(list)
    for row in rows:
        grouped[str(row.get("condition"))].append(row)
    by_condition = {}
    for condition in conditions:
        condition_rows = grouped.get(condition, [])
        by_condition[condition] = {
            "rows": len(condition_rows),
            "expected_instances": expected_instances,
            "patch_generated": sum(bool(row.get("patch_generated")) for row in condition_rows),
            "evaluation_available": sum(bool(row.get("evaluation_available")) for row in condition_rows),
            "resolved": sum(row.get("resolved") is True for row in condition_rows),
            "unresolved": sum(row.get("resolved") is False for row in condition_rows),
            "missing_rows": max(0, expected_instances - len(condition_rows)),
        }
    return by_condition


def write_report(path: Path, plan: dict, rows: list[dict], missing: list[dict], summary: dict) -> None:
    lines = [
        "# Exp6 Complex Top20 Pipeline Results",
        "",
        f"Generated: {datetime.now(timezone.utc).isoformat()}",
        "",
        f"- Planned instances: {len(plan.get('units', []))}",
        f"- Collected condition rows: {len(rows)}",
        f"- Units without complete evaluation JSON: {len(missing)}",
        "",
        "## Outcome by condition",
        "",
        "| condition | rows | patches | evaluated | resolved | unresolved | missing |",
        "|---|---:|---:|---:|---:|---:|---:|",
    ]
    for condition in plan.get("conditions", []):
        item = summary[condition]
        lines.append(
            f"| {condition} | {item['rows']} | {item['patch_generated']} | "
            f"{item['evaluation_available']} | {item['resolved']} | {item['unresolved']} | {item['missing_rows']} |"
        )
    lines.extend(["", "## Per-instance harness result", "", "| rank | instance | condition | patch | evaluation | resolved |", "|---:|---|---|---:|---:|---:|"])
    for row in sorted(rows, key=lambda item: (int(item.get("complexity_rank") or 9999), str(item.get("condition")))):
        patch = "Y" if row.get("patch_generated") else "N"
        evaluated = "Y" if row.get("evaluation_available") else "N"
        resolved = "Y" if row.get("resolved") is True else ("N" if row.get("resolved") is False else "NA")
        lines.append(
            f"| {row.get('complexity_rank')} | `{row.get('instance_id')}` | {row.get('condition')} | {patch} | {evaluated} | {resolved} |"
        )
    if missing:
        lines.extend(["", "## Missing evaluations", ""])
        for item in missing:
            lines.append(f"- `{item['instance_id']}`: {item['reason']}")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Aggregate per-instance Exp6 pipeline evaluations without running harness.")
    parser.add_argument("--plan", type=Path, default=DEFAULT_PLAN)
    parser.add_argument("--out-dir", type=Path)
    parser.add_argument("--require-complete", action="store_true")
    args = parser.parse_args()

    plan_path = resolve_path(args.plan)
    plan = read_json(plan_path)
    out_dir = resolve_path(args.out_dir) if args.out_dir else plan_path.parent / "results"
    rows, missing = aggregate_rows(plan)
    summary = summarize(rows, plan.get("conditions", []), len(plan.get("units", [])))
    payload = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "plan": str(plan_path),
        "complete": not missing and len(rows) == len(plan.get("units", [])) * len(plan.get("conditions", [])),
        "planned_instances": len(plan.get("units", [])),
        "collected_rows": len(rows),
        "missing_units": missing,
        "by_condition": summary,
    }
    write_json(out_dir / "combined_evaluation.json", rows)
    write_json(out_dir / "summary.json", payload)
    write_report(out_dir / "report.md", plan, rows, missing, summary)
    print(json.dumps({"complete": payload["complete"], "collected_rows": len(rows), "missing_units": len(missing)}, indent=2))
    print(f"Results: {out_dir}")
    return 0 if payload["complete"] or not args.require_complete else 3


if __name__ == "__main__":
    raise SystemExit(main())
