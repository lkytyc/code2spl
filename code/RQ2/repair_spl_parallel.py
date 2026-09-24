from __future__ import annotations

"""Parallel re-run of empty/malformed SPL cards.

Regenerates ONLY the samples listed in ``sample_ids_file`` (the 65 bad cards),
replicating prepare.py's per-sample SPL build, but with one SPLGenerator per
worker thread and no snapshot writes.  Cross-thread API-key throttling is
handled by FileApiKeyLeasePool (shared lock dirs), so this is safe to run with
many workers.
"""

import argparse
import json
import sys
import threading
import traceback
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from common.paths import ensure_dir, read_config, resolve_in_project, write_json  # noqa: E402
from common.run_utils import selected_items  # noqa: E402
from common.spl_adapter import SPLGenerator  # noqa: E402
from common.spl_binding import (  # noqa: E402
    bind_spl_to_source,
    normalize_numbered_source,
    python2_compatibility_source,
    source_for_named_owner,
)
from common.token_utils import compress_code_to_token_budget, token_count  # noqa: E402

# Reuse the config/loader helpers from prepare.py (its main() is guarded).
from prepare import build_spl_config, load_prepared_input_candidates, guess_language  # noqa: E402


BAD_MARKERS = ("# JSON_PARSE_ERROR", "Empty LLM output")


class _ThreadLocalGenerator(threading.local):
    def __init__(self) -> None:
        self.spl: SPLGenerator | None = None


_TLS = _ThreadLocalGenerator()


def get_spl(config: dict) -> SPLGenerator:
    if _TLS.spl is None:
        _TLS.spl = SPLGenerator(build_spl_config(config))
    return _TLS.spl


def _is_bad(spl_text: str) -> bool:
    if not spl_text or not spl_text.strip():
        return True
    return any(marker in spl_text for marker in BAD_MARKERS)


def process_one(entry: dict, config: dict, artifact_dir: Path) -> dict:
    spl = get_spl(config)
    item = entry["item"]
    code = entry["code"]
    sample_id = str(entry["task_id"])
    language = guess_language(item, code)
    sample_dir = ensure_dir(artifact_dir / sample_id)

    # Re-materialize the immutable inputs (idempotent, matches prepare.py).
    (sample_dir / "raw_code.txt").write_text(code, encoding="utf-8")
    (sample_dir / "official_prompt.txt").write_text(entry["official_prompt"], encoding="utf-8")
    (sample_dir / "question.txt").write_text(
        str(entry.get("frozen_question") or ""), encoding="utf-8"
    )
    frozen_gold = entry.get("frozen_gold")
    (sample_dir / "gold.txt").write_text(
        str(frozen_gold) if frozen_gold is not None else json.dumps(item.get("groundtruth", item.get("label", "")), ensure_ascii=False),
        encoding="utf-8",
    )
    write_json(sample_dir / "item.json", item)

    target_owner = str(item.get("funname") or "")
    owner_source, owner_audit = source_for_named_owner(
        code, language, target_owner,
        source_start_line=item.get("start"),
        source_end_line=item.get("end"),
    ) if target_owner else ("", {})
    normalized_source, _line_map, numbered = normalize_numbered_source(code)
    generation_source = owner_source or normalized_source
    compatibility_audit = {"applied": False, "reason": "not_needed"}
    if language == "python":
        generation_source, compatibility_audit = python2_compatibility_source(generation_source)

    spl_result, spl_by_method = spl.generate_for_code_with_metrics_and_map(
        generation_source, language, sample_id
    )
    spl_text = spl_result.text

    (sample_dir / "spl.txt").write_text(spl_text, encoding="utf-8")
    write_json(sample_dir / "spl_metadata.json", spl_result.metadata)
    write_json(sample_dir / "spl_by_method.json", spl_by_method)
    write_json(sample_dir / "spl_regeneration_audit.json", {
        "reason": "parallel_repair_65",
        "target_owner": target_owner or None,
        "target_owner_only": bool(owner_source),
        "numbered_source_normalized": numbered,
        "owner_audit": owner_audit,
        "compatibility_audit": compatibility_audit,
    })
    _bound_spl, _src_prov, binding_audit = bind_spl_to_source(code, spl_by_method, language)
    write_json(sample_dir / "spl_source_binding.json", binding_audit)

    compressed_raw = compress_code_to_token_budget(code, token_count(spl_text))
    (sample_dir / "compressed_raw.txt").write_text(compressed_raw, encoding="utf-8")

    return {"sample_id": sample_id, "ok": not _is_bad(spl_text), "bytes": len(spl_text)}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", required=True)
    parser.add_argument("--max-workers", type=int, default=14)
    args = parser.parse_args()

    config = read_config(resolve_in_project(args.config))
    artifact_dir = ensure_dir(resolve_in_project(config["artifact_dir"]))

    seed_dir = config.get("prepared_input_seed_dir")
    if not seed_dir:
        raise ValueError("parallel repair requires prepared_input_seed_dir")
    candidates = load_prepared_input_candidates(resolve_in_project(seed_dir))
    selected = selected_items(candidates, config)
    print(f"Selected {len(selected)} samples to repair", flush=True)

    ok = 0
    bad = 0
    errors = 0
    with ThreadPoolExecutor(max_workers=args.max_workers) as pool:
        futures = {pool.submit(process_one, entry, config, artifact_dir): entry["task_id"] for entry in selected}
        done = 0
        for fut in as_completed(futures):
            sample_id = futures[fut]
            done += 1
            try:
                result = fut.result()
                if result["ok"]:
                    ok += 1
                else:
                    bad += 1
                print(f"[{done}/{len(selected)}] {sample_id}: ok={result['ok']} bytes={result['bytes']}", flush=True)
            except Exception as exc:
                errors += 1
                print(f"[{done}/{len(selected)}] {sample_id}: ERROR {exc}", flush=True)
                traceback.print_exc()

    print(f"\nDONE ok={ok} bad={bad} errors={errors}", flush=True)


if __name__ == "__main__":
    main()
