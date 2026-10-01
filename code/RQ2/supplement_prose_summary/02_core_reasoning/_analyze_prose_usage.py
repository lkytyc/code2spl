"""Diagnose how the unstructured-SPL condition was used by the model.

This analysis is read-only with respect to existing experiment artifacts.  It
compares the frozen three-condition run with the supplementary unstructured
run and writes one machine-readable JSON report.  No model or SPL builder is
called.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from collections import Counter
from pathlib import Path
from statistics import median
from typing import Any


HERE = Path(__file__).resolve().parent
DEFAULT_ORIGINAL = HERE / "results" / "r" / "deepseek-v4-pro_full341_thinking"
DEFAULT_SUPPLEMENT = HERE / "results" / "r" / "deepseek-v4-pro_full341_unstructured_summary"
FREE_CONDITION = "raw_free_summary"
STRUCTURED_CONDITION = "raw_spl_atomic_strict"
UNSTRUCTURED_CONDITION = "raw_spl_unstructured_summary"

EXAMPLES = [
    ("infoflow_codenet_p00072_s798976958_run_6_70_count_46_2", "source"),
    ("data_codenet_p02962_s348098217_solve_19_91_i_81_6", "source"),
    ("data_gcj_104e05_111e09_main_7_46_wordOne_24_1", "source"),
]


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def sample_key(row: dict[str, Any]) -> tuple[str, str]:
    return str(row["task_id"]), str(row["mode"])


def extract_json_object(text: str) -> dict[str, Any] | None:
    """Extract the first decodable JSON object from a model response."""
    decoder = json.JSONDecoder()
    for match in re.finditer(r"\{", text):
        try:
            value, _ = decoder.raw_decode(text[match.start() :])
        except json.JSONDecodeError:
            continue
        if isinstance(value, dict):
            return value
    return None


def canonical_output(path: Path) -> str | None:
    value = extract_json_object(path.read_text(encoding="utf-8"))
    if value is None:
        return None
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def prediction(path: Path) -> list[list[Any]] | None:
    value = extract_json_object(path.read_text(encoding="utf-8"))
    if not value or len(value) != 1:
        return None
    items = next(iter(value.values()))
    return items if isinstance(items, list) else None


def output_path(root: Path, key: tuple[str, str], condition: str) -> Path:
    task_id, mode = key
    return root / f"{task_id}__{mode}" / condition / "output.txt"


def paired_counts(
    left: dict[tuple[str, str], dict[str, Any]],
    right: dict[tuple[str, str], dict[str, Any]],
) -> dict[str, int]:
    counts: Counter[str] = Counter()
    for key in sorted(right):
        a = bool(left[key]["strict_correct"])
        b = bool(right[key]["strict_correct"])
        counts[
            "both_correct" if a and b else
            "left_only" if a else
            "right_only" if b else
            "both_wrong"
        ] += 1
    return {
        "both_correct": counts["both_correct"],
        "left_only": counts["left_only"],
        "right_only": counts["right_only"],
        "both_wrong": counts["both_wrong"],
        "net_right_minus_left": counts["right_only"] - counts["left_only"],
    }


def sorted_pairs(items: list[list[Any]] | None) -> list[list[Any]] | None:
    if items is None:
        return None
    return sorted(items, key=lambda item: json.dumps(item, ensure_ascii=False))


def set_delta(
    predicted: list[list[Any]] | None,
    expected: list[list[Any]],
) -> tuple[list[list[Any]] | None, list[list[Any]] | None]:
    if predicted is None:
        return None, None
    pred = {tuple(item) for item in predicted}
    gold = {tuple(item) for item in expected}
    return sorted_pairs([list(item) for item in pred - gold]), sorted_pairs(
        [list(item) for item in gold - pred]
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--original-run", type=Path, default=DEFAULT_ORIGINAL)
    parser.add_argument("--supplement-run", type=Path, default=DEFAULT_SUPPLEMENT)
    parser.add_argument(
        "--output",
        type=Path,
        default=DEFAULT_SUPPLEMENT / "unstructured_usage_analysis.json",
    )
    args = parser.parse_args()

    original_rows = load_json(args.original_run / "evaluation.json")
    supplement_rows = load_json(args.supplement_run / "evaluation.json")
    original = {
        (sample_key(row), str(row["condition"])): row for row in original_rows
    }
    unstructured = {sample_key(row): row for row in supplement_rows}
    free = {key: original[(key, FREE_CONDITION)] for key in unstructured}
    structured = {key: original[(key, STRUCTURED_CONDITION)] for key in unstructured}

    if len(unstructured) != 341 or set(free) != set(unstructured) or set(structured) != set(unstructured):
        raise RuntimeError("Expected the same 341 paired samples in all three conditions")

    identity = Counter()
    structured_only: list[tuple[str, str]] = []
    unstructured_only: list[tuple[str, str]] = []
    loss_strata: Counter[str] = Counter()
    loss_same_as_free = 0
    loss_free_also_wrong = 0

    for key, unstructured_row in unstructured.items():
        free_json = canonical_output(output_path(args.original_run, key, FREE_CONDITION))
        structured_json = canonical_output(
            output_path(args.original_run, key, STRUCTURED_CONDITION)
        )
        unstructured_json = canonical_output(
            output_path(args.supplement_run, key, UNSTRUCTURED_CONDITION)
        )
        if all(value is not None for value in (free_json, structured_json, unstructured_json)):
            identity["all_three_parseable"] += 1
        if free_json == unstructured_json:
            identity["free_equals_unstructured"] += 1
        if structured_json == unstructured_json:
            identity["structured_equals_unstructured"] += 1
        if free_json == structured_json == unstructured_json:
            identity["all_three_equal"] += 1

        structured_ok = bool(structured[key]["strict_correct"])
        unstructured_ok = bool(unstructured_row["strict_correct"])
        if structured_ok and not unstructured_ok:
            structured_only.append(key)
            loss_strata[f"{unstructured_row['task_type']}/{unstructured_row['mode']}"] += 1
            loss_same_as_free += int(free_json == unstructured_json)
            loss_free_also_wrong += int(not bool(free[key]["strict_correct"]))
        elif unstructured_ok and not structured_ok:
            unstructured_only.append(key)

    prompts = [
        (args.supplement_run / f"{task_id}__{mode}" / UNSTRUCTURED_CONDITION / "prompt.txt").read_text(
            encoding="utf-8"
        )
        for task_id, mode in sorted(unstructured)
    ]
    prompt_lengths = sorted(map(len, prompts))
    prompt_audit = load_json(args.supplement_run / "prompt_leakage_audit.json")
    card_audit = load_json(args.supplement_run / "card_render_audit.json")

    examples: list[dict[str, Any]] = []
    for key in EXAMPLES:
        expected = structured[key]["official_eval"]["ground_truth"]
        condition_rows: dict[str, Any] = {}
        for condition, root, row in (
            (FREE_CONDITION, args.original_run, free[key]),
            (STRUCTURED_CONDITION, args.original_run, structured[key]),
            (UNSTRUCTURED_CONDITION, args.supplement_run, unstructured[key]),
        ):
            predicted = prediction(output_path(root, key, condition))
            extra, missing = set_delta(predicted, expected)
            condition_rows[condition] = {
                "strict_correct": bool(row["strict_correct"]),
                "prediction": predicted,
                "extra": extra,
                "missing": missing,
            }
        examples.append(
            {
                "task_id": key[0],
                "mode": key[1],
                "ground_truth": expected,
                "conditions": condition_rows,
            }
        )

    free_template = HERE / "methods" / FREE_CONDITION / "prompts" / "prompt.md"
    unstructured_template = HERE / "methods" / UNSTRUCTURED_CONDITION / "prompts" / "prompt.md"
    report = {
        "analysis_scope": {
            "samples": len(unstructured),
            "description": "Post-hoc mechanism audit; no model or SPL-builder calls.",
            "original_run": str(args.original_run),
            "supplement_run": str(args.supplement_run),
        },
        "strict_correct": {
            FREE_CONDITION: sum(bool(row["strict_correct"]) for row in free.values()),
            STRUCTURED_CONDITION: sum(bool(row["strict_correct"]) for row in structured.values()),
            UNSTRUCTURED_CONDITION: sum(
                bool(row["strict_correct"]) for row in unstructured.values()
            ),
        },
        "paired_correctness": {
            "free_to_unstructured": paired_counts(free, unstructured),
            "structured_to_unstructured": paired_counts(structured, unstructured),
        },
        "prediction_identity": dict(identity),
        "structured_only_losses": {
            "count": len(structured_only),
            "same_prediction_as_free_summary": loss_same_as_free,
            "free_summary_also_wrong": loss_free_also_wrong,
            "by_task_type_and_mode": dict(sorted(loss_strata.items())),
            "sample_keys": [f"{task_id}__{mode}" for task_id, mode in structured_only],
        },
        "unstructured_only_gains": {
            "count": len(unstructured_only),
            "sample_keys": [f"{task_id}__{mode}" for task_id, mode in unstructured_only],
        },
        "actual_prompt_audit": {
            "free_and_unstructured_template_sha256_equal": sha256(free_template)
            == sha256(unstructured_template),
            "free_template_sha256": sha256(free_template),
            "unstructured_template_sha256": sha256(unstructured_template),
            "contains_literal_raw_free_summary": sum(
                "raw_free_summary" in prompt.lower() for prompt in prompts
            ),
            "contains_literal_free_summary": sum(
                "free_summary" in prompt.lower() for prompt in prompts
            ),
            "contains_auxiliary_summary_instruction": sum(
                "The summary is auxiliary context only" in prompt for prompt in prompts
            ),
            "contains_may_omit_instruction": sum(
                "may omit exact implementation details" in prompt for prompt in prompts
            ),
            "contains_spl_control_block": sum(
                "## SPL source-bound analysis control" in prompt for prompt in prompts
            ),
            "prompt_chars": {
                "min": prompt_lengths[0],
                "median": median(prompt_lengths),
                "max": prompt_lengths[-1],
            },
            "leakage_audit": {
                "cards_with_tag_leak": prompt_audit["cards_with_tag_leak"],
                "cards_with_protocol_leak": prompt_audit["cards_with_protocol_leak"],
                "any_spl_control_block": prompt_audit["any_spl_control_block"],
            },
        },
        "deterministic_render_audit": {
            key: card_audit[key]
            for key in (
                "cards_total",
                "rendered",
                "passthrough_json_parse_error",
                "content_preservation_failures",
                "tag_leak_cards",
                "payloads_checked_total",
                "rendered_chars",
            )
        },
        "illustrative_examples": examples,
        "interpretation_limits": [
            "The unstructured condition removes field structure and the source-bound reading protocol together.",
            "Textual payload preservation does not establish preservation of hierarchy, addressability, or task usability.",
            "The 5-sample deficit versus raw_free_summary is not statistically significant (see supplement_analysis.json).",
            "The selected examples are explanatory diagnostics and must not be treated as a separately sampled evaluation set.",
        ],
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(f"wrote={args.output}")
    print(json.dumps({
        "strict_correct": report["strict_correct"],
        "prediction_identity": report["prediction_identity"],
        "structured_only_losses": report["structured_only_losses"]["count"],
    }, ensure_ascii=False))


if __name__ == "__main__":
    main()
