"""Prepare and audit the 218-sample full-semantic-summary supplement.

This script only assembles a deterministic manifest from the already frozen
random218 units and verifies every existing SPL index can be fully converted to
ordinary prose.  It never calls an LLM, rebuilds SPL, downloads data, or starts
Docker.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path
from typing import Any

import flat_semantic_prose as flat


HERE = Path(__file__).resolve().parent
PROJECT = HERE.parents[2]
sys.path.insert(0, str(HERE.parents[1]))  # the package's code/ directory
from common.env import expand  # noqa: E402
UNITS_ROOT = PROJECT / "data" / "RQ3" / "inputs" / "unit_manifests_random218"


def pkg(value: str | Path) -> Path:
    """A package path from a config value carrying the $PROJECT_ROOT marker."""
    path = Path(expand(str(value)))
    return path if path.is_absolute() else PROJECT / path


def pkg(value: str | Path) -> Path:
    """A package path from a config value carrying the $PROJECT_ROOT marker."""
    path = Path(expand(str(value)))
    return path if path.is_absolute() else PROJECT / path


def _load_unit_manifest(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, list) or len(data) != 1 or not isinstance(data[0], dict):
        raise ValueError(f"invalid unit manifest: {path}")
    return dict(data[0])


def _full_semantic_audit(sample_dir: Path) -> dict[str, Any]:
    index_path = sample_dir / "spl_index.json"
    data = json.loads(index_path.read_text(encoding="utf-8"))
    entries = data.get("entries") if isinstance(data, dict) else None
    if not isinstance(entries, list):
        raise ValueError(f"missing SPL entries: {index_path}")
    prose_parts: list[str] = []
    entry_count = sentences_available = sentences_delivered = 0
    for entry in entries:
        if not isinstance(entry, dict):
            continue
        raw = str(entry.get("spl") or "")
        prose, audit = flat.flatten_entry(entry, max_chars=max(20_000, len(raw) * 4))
        if audit["sentences_delivered"] != audit["sentences_available"]:
            raise AssertionError(f"incomplete conversion for {index_path}: {audit}")
        prose_parts.append(prose)
        entry_count += 1
        sentences_available += int(audit["sentences_available"])
        sentences_delivered += int(audit["sentences_delivered"])
    text = "\n\n".join(prose_parts)
    hits = flat.forbidden_hits(text)
    if hits:
        raise AssertionError(f"structured marker remains in {index_path}: {hits}")
    return {
        "semantic_available": bool(entry_count),
        "no_function_level_spl_available": not bool(entry_count),
        "entry_count": entry_count,
        "sentences_available": sentences_available,
        "sentences_delivered": sentences_delivered,
        "semantic_characters": len(text),
        "semantic_tokens": flat.token_count(text),
        "structured_marker_hits": hits,
        "spl_index_sha256": hashlib.sha256(index_path.read_bytes()).hexdigest(),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output-dir",
        default="$PROJECT_ROOT/data/RQ3/inputs/random218_full_semantic_summary",
        help="Project-relative directory for the combined manifest and audit.",
    )
    args = parser.parse_args()
    output_dir = pkg(args.output_dir)
    unit_dirs = sorted((p for p in UNITS_ROOT.iterdir() if p.is_dir()), key=lambda p: p.name)
    if len(unit_dirs) != 218:
        raise RuntimeError(f"expected 218 frozen unit directories, found {len(unit_dirs)}")

    manifest: list[dict[str, Any]] = []
    audit_rows: list[dict[str, Any]] = []
    for unit_dir in unit_dirs:
        item = _load_unit_manifest(unit_dir / "manifest.json")
        sample_dir = pkg(item["sample_dir"])
        if not (sample_dir / "swebench_instance.jsonl").exists():
            raise FileNotFoundError(f"missing frozen instance: {sample_dir}")
        item_audit = _full_semantic_audit(sample_dir)
        manifest.append(item)
        audit_rows.append({"index": item["index"], "instance_id": item["instance_id"], **item_audit})

    indices = [int(item["index"]) for item in manifest]
    if indices != list(range(218)):
        raise AssertionError("combined manifest indices are not exactly 0..217")
    if len({str(item["instance_id"]) for item in manifest}) != 218:
        raise AssertionError("duplicate instance ID in combined manifest")

    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8", newline="\n"
    )
    payload = {
        "experiment": "full_semantic_summary_218_preflight",
        "sample_count": len(manifest),
        "issue_used_for_selection": False,
        "issue_used_for_conversion": False,
        "selection_method": "all_frozen_entries_in_stored_order",
        "model_called_during_preflight": False,
        "total_entry_count": sum(row["entry_count"] for row in audit_rows),
        "total_semantic_tokens": sum(row["semantic_tokens"] for row in audit_rows),
        "total_semantic_characters": sum(row["semantic_characters"] for row in audit_rows),
        "samples": audit_rows,
    }
    (output_dir / "preflight_audit.json").write_text(
        json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8", newline="\n"
    )
    print(
        "prepared_samples={sample_count} entries={total_entry_count} "
        "semantic_tokens={total_semantic_tokens}".format(**payload)
    )


if __name__ == "__main__":
    sys.exit(main())
