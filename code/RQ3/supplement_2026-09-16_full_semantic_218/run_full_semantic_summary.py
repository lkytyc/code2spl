"""Run the single full-semantic-summary supplement for Experiment 3.

The generated mini-SWE-agent configuration is first built exactly as the
historical ``miniswe_original`` condition.  The only treatment change is that
all frozen SPL behavior statements are converted deterministically to ordinary
prose and appended as one source-behavior summary.  No issue-conditioned
selection, ranking, labels, source excerpt, first command, or repair plan is
added.
"""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path
from typing import Any

import yaml

import flat_semantic_prose as flat
import run as base


MODE = "miniswe_full_semantic_summary"
INTRODUCTION = (
    "The following automatically generated summary describes behavior in the "
    "current pre-fix source. It is auxiliary information, not source code, a "
    "correctness specification, or a repair plan. Verify it against the real "
    "source before deciding any edit."
)
BUILD_AUDIT: dict[str, dict[str, Any]] = {}
_base_build_mini_config = base.build_mini_config
_base_condition_output_complete = base.condition_output_complete


def _raw_entries(sample_dir: Path) -> list[dict[str, Any]]:
    path = sample_dir / "spl_index.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    entries = data.get("entries") if isinstance(data, dict) else None
    if not isinstance(entries, list):
        raise ValueError(f"missing frozen SPL entries: {path}")
    return [dict(entry) for entry in entries if isinstance(entry, dict)]


def _full_prose(sample_dir: Path) -> tuple[str, list[dict[str, Any]]]:
    paragraphs: list[str] = []
    audits: list[dict[str, Any]] = []
    for entry in _raw_entries(sample_dir):
        raw = str(entry.get("spl") or "")
        prose, audit = flat.flatten_entry(
            entry,
            max_chars=max(20_000, len(raw) * 4),
        )
        if audit["sentences_delivered"] != audit["sentences_available"]:
            raise AssertionError(f"incomplete semantic conversion: {audit}")
        paragraphs.append(prose.strip())
        audits.append(audit)
    text = "\n\n".join(paragraphs).strip()
    hits = flat.forbidden_hits(text)
    if hits:
        raise AssertionError(f"structured SPL markers remain in prose: {hits}")
    return text, audits


def build_mini_config(**kwargs: Any) -> Path:
    mode = str(kwargs.get("mode") or "")
    if mode != MODE:
        return _base_build_mini_config(**kwargs)

    # Build the exact original-system agent configuration first.  Calling the
    # original mode also prevents SPL-specific progress rules and tool payloads.
    original_kwargs = dict(kwargs)
    original_kwargs["mode"] = "miniswe_original"
    path = _base_build_mini_config(**original_kwargs)
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    original_template = str(data.get("agent", {}).get("instance_template", ""))

    sample_dir = Path(kwargs["sample_dir"])
    prose, entry_audits = _full_prose(sample_dir)
    # One frozen scope contains a Python module with no function-level Worker,
    # hence no SPL behavior fact exists.  Preserve the predefined sample but
    # make its treatment byte-for-byte the Original template rather than
    # inventing a synthetic summary or adding an empty-context instruction.
    treatment_injected = bool(prose)
    if treatment_injected:
        treatment = INTRODUCTION + "\n\n" + prose
        data.setdefault("agent", {})["instance_template"] = (
            original_template.rstrip() + "\n\n" + treatment + "\n"
        )
    path.write_text(
        yaml.safe_dump(data, sort_keys=False, allow_unicode=True),
        encoding="utf-8",
        newline="\n",
    )

    BUILD_AUDIT[str(sample_dir)] = {
        "condition": MODE,
        "base_condition": "miniswe_original",
        "only_change": (
            "append_complete_spl_derived_behavior_as_ordinary_prose"
            if treatment_injected
            else "no_change_no_function_level_spl_available"
        ),
        "treatment_context_injected": treatment_injected,
        "no_function_level_spl_available": not treatment_injected,
        "issue_used_for_selection": False,
        "issue_used_for_conversion": False,
        "selection_method": "all_frozen_entries_in_stored_order",
        "keyword_search_or_ranking": False,
        "source_excerpt_injected": False,
        "first_command_injected": False,
        "repair_plan_injected": False,
        "spl_progress_rule_injected": False,
        "entry_count": len(entry_audits),
        "sentences_available": sum(int(a["sentences_available"]) for a in entry_audits),
        "sentences_delivered": sum(int(a["sentences_delivered"]) for a in entry_audits),
        "semantic_characters": len(prose),
        "semantic_tokens": flat.token_count(prose),
        "structured_marker_hits": flat.forbidden_hits(prose),
        "original_instance_template_sha256": hashlib.sha256(
            original_template.encode("utf-8")
        ).hexdigest(),
    }
    # Persist after every prepared sample so a stopped/resumed 218-sample run
    # never loses the material audit accumulated before the interruption.
    _write_audit_payload(kwargs["config"])
    return path


def _write_audit_payload(config: dict[str, Any]) -> None:
    run_dir = base.resolve_in_project(config["run_dir"])
    run_dir.mkdir(parents=True, exist_ok=True)
    audit_path = run_dir / "full_semantic_material_audit.json"
    existing_samples: dict[str, Any] = {}
    if audit_path.exists():
        try:
            existing = json.loads(audit_path.read_text(encoding="utf-8"))
            existing_samples = dict(existing.get("samples") or {})
        except Exception:
            # A malformed pre-existing audit must never stop a repair run; the
            # new atomic payload below replaces it with valid JSON.
            existing_samples = {}
    existing_samples.update(BUILD_AUDIT)
    payload = {
        "experiment": "experiment_3_full_semantic_summary_supplement",
        "comparison": "saved_miniswe_original_vs_new_full_semantic_summary",
        "condition": MODE,
        "agent_model": config.get("mini_model_name") or config.get("model"),
        "temperature": config.get("temperature"),
        "step_limit": config.get("mini_step_limit"),
        "max_output_tokens": config.get("max_output_tokens"),
        "introduction": INTRODUCTION,
        "samples": existing_samples,
    }
    audit_path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2),
        encoding="utf-8",
        newline="\n",
    )


def _write_audit(config_path: Path) -> None:
    config_path = base.resolve_in_project(config_path)
    config = json.loads(config_path.read_text(encoding="utf-8"))
    _write_audit_payload(config)


def _condition_complete_except_docker_interruption(
    out_dir: Path,
    mode: str,
    expected_spl_protocol: str,
) -> bool:
    """Resume only runs that failed before an agent/container was created.

    A Docker Desktop shutdown writes an otherwise well-formed completion marker
    with a nonzero ``docker run`` return code.  Such a marker is not an agent
    outcome and must not be treated as a completed experimental observation.
    Other no-patch trajectories (limits, format errors, and normal agent exits)
    remain completed and are never retried by this recovery rule.
    """
    if not _base_condition_output_complete(out_dir, mode, expected_spl_protocol):
        return False
    try:
        status = base.read_json(out_dir / "baseline_status.json")
        failure = status.get("failure") or {}
        stderr = str(failure.get("stderr_tail") or "")
        return_code = failure.get("returncode")
    except Exception:
        return True
    is_docker_start_failure = (
        return_code not in (None, 0)
        and "CalledProcessError" in stderr
        and "['docker', 'run'" in stderr
    )
    return not is_docker_start_failure


if __name__ == "__main__":
    base.build_mini_config = build_mini_config
    base.condition_output_complete = _condition_complete_except_docker_interruption
    try:
        base.main()
    finally:
        for index, arg in enumerate(sys.argv):
            if arg == "--config" and index + 1 < len(sys.argv):
                _write_audit(Path(sys.argv[index + 1]))
                break
