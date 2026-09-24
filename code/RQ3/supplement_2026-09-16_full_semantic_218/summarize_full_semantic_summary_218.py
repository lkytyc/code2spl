"""Create a reproducible Original-vs-full-semantic comparison after stage 2."""

from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path
from typing import Any


HERE = Path(__file__).resolve().parent
PROJECT = HERE.parents[2]
sys.path.insert(0, str(HERE.parents[1]))  # the package's code/ directory
from common.env import expand  # noqa: E402
MODE = "miniswe_full_semantic_summary"


def pkg(value: str | Path) -> Path:
    """A package path from a config value carrying the $PROJECT_ROOT marker."""
    path = Path(expand(str(value)))
    return path if path.is_absolute() else PROJECT / path


def pkg(value: str | Path) -> Path:
    """A package path from a config value carrying the $PROJECT_ROOT marker."""
    path = Path(expand(str(value)))
    return path if path.is_absolute() else PROJECT / path


def read_json(path: Path, default: Any) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return default


def read_condition(run_dir: Path, instance_id: str, mode: str) -> dict[str, Any]:
    condition_dir = run_dir / instance_id / mode
    marker = read_json(condition_dir / "condition_complete.json", {})
    usage = read_json(condition_dir / "call_metadata.json", {})
    patch = condition_dir / "patch.diff"
    return {
        "complete": bool(marker.get("complete")),
        "patch_chars": int(marker.get("patch_chars") or (patch.stat().st_size if patch.exists() else 0)),
        "patch_generated": bool(patch.exists() and patch.stat().st_size),
        "calls": int(usage.get("calls") or 0),
        "input_tokens": int(usage.get("input_tokens") or 0),
        "output_tokens": int(usage.get("output_tokens") or 0),
        "total_tokens": int(usage.get("total_tokens") or 0),
        "elapsed_seconds": float(usage.get("elapsed_seconds") or 0),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--config",
        default="$PROJECT_ROOT/data/RQ3/settings/configs/random218_full_semantic_summary/full_semantic_summary_218_evaluation_config.json",
    )
    args = parser.parse_args()
    config = read_json(pkg(args.config), {})
    artifact_dir = pkg(config["artifact_dir"])
    run_dir = pkg(config["run_dir"])
    original_root = pkg(config["original_results_root"])
    manifest = read_json(artifact_dir / "manifest.json", [])
    evaluation_rows = read_json(run_dir / "evaluation.json", [])
    evaluation_by_id = {str(row.get("instance_id")): row for row in evaluation_rows if isinstance(row, dict)}

    rows: list[dict[str, Any]] = []
    for item in manifest:
        index = int(item["index"])
        instance_id = str(item["instance_id"])
        old_run = original_root / "units" / f"unit_{index + 1:03d}_{instance_id}" / "runs"
        original = read_condition(old_run, instance_id, "miniswe_original")
        treatment = read_condition(run_dir, instance_id, MODE)
        eval_row = evaluation_by_id.get(instance_id, {})
        resolved = eval_row.get("resolved") if eval_row.get("evaluation_available") else None
        rows.append(
            {
                "index": index,
                "instance_id": instance_id,
                "original_patch_generated": original["patch_generated"],
                "original_patch_chars": original["patch_chars"],
                "original_calls": original["calls"],
                "original_total_tokens": original["total_tokens"],
                "original_elapsed_seconds": original["elapsed_seconds"],
                "semantic_patch_generated": treatment["patch_generated"],
                "semantic_patch_chars": treatment["patch_chars"],
                "semantic_calls": treatment["calls"],
                "semantic_total_tokens": treatment["total_tokens"],
                "semantic_elapsed_seconds": treatment["elapsed_seconds"],
                "semantic_evaluation_available": bool(eval_row.get("evaluation_available")),
                "semantic_resolved": resolved,
                "semantic_failure": str((eval_row.get("eval_status") or {}).get("reason") or ""),
            }
        )

    resolved_rows = [row for row in rows if row["semantic_resolved"] is not None]
    summary = {
        "sample_count": len(rows),
        "original_patch_count": sum(bool(row["original_patch_generated"]) for row in rows),
        "semantic_patch_count": sum(bool(row["semantic_patch_generated"]) for row in rows),
        "semantic_evaluated_count": len(resolved_rows),
        "semantic_resolved_count": sum(bool(row["semantic_resolved"]) for row in resolved_rows),
        "original_total_tokens": sum(row["original_total_tokens"] for row in rows),
        "semantic_total_tokens": sum(row["semantic_total_tokens"] for row in rows),
        "original_calls": sum(row["original_calls"] for row in rows),
        "semantic_calls": sum(row["semantic_calls"] for row in rows),
        "evaluation_incomplete_count": sum(row["semantic_resolved"] is None and row["semantic_patch_generated"] for row in rows),
    }
    run_dir.mkdir(parents=True, exist_ok=True)
    with (run_dir / "original_vs_full_semantic_per_instance.csv").open("w", encoding="utf-8-sig", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]) if rows else [])
        writer.writeheader()
        writer.writerows(rows)
    (run_dir / "original_vs_full_semantic_summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8", newline="\n"
    )
    report = [
        "# Experiment 3 Supplementary Experiment: Full Semantic Free Summary Results on the 218 Samples",
        "",
        "This report compares the historical `miniswe_original` with the single added condition `miniswe_full_semantic_summary`. The added condition appends only a full SPL-derived ordinary natural-language behavior summary; it uses no keyword localization, relevance ranking, source excerpting, patch plan, or SPL-specific execution strategy.",
        "",
        f"- Sample count: {summary['sample_count']}",
        f"- Original submitted patches: {summary['original_patch_count']}",
        f"- Full-semantic condition submitted patches: {summary['semantic_patch_count']}",
        f"- Patches with completed official evaluation: {summary['semantic_evaluated_count']}",
        f"- Official resolved: {summary['semantic_resolved_count']}",
        f"- Original total tokens: {summary['original_total_tokens']}",
        f"- Full-semantic total tokens: {summary['semantic_total_tokens']}",
        "",
        "Per-instance results are in `original_vs_full_semantic_per_instance.csv`; the original condition metrics come from the frozen `random218` result tree, and Original was not re-run.",
    ]
    (run_dir / "ORIGINAL_VS_FULL_SEMANTIC_218_REPORT.md").write_text(
        "\n".join(report) + "\n", encoding="utf-8", newline="\n"
    )
    print(json.dumps(summary, ensure_ascii=False))


if __name__ == "__main__":
    main()
