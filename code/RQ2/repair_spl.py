from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from common.paths import read_config, read_json, resolve_in_project, write_json, write_text
from common.spl_adapter import SPLConfig, SPLGenerator, recover_spl_by_worker
from common.spl_binding import bind_spl_to_source, normalize_numbered_source, source_for_named_owner


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Repair missing or stale CoRe SPL using task-local source owners only.",
    )
    parser.add_argument("--config", required=True)
    parser.add_argument("--sample-id", action="append", default=[])
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    config = read_config(resolve_in_project(args.config))
    artifact_dir = resolve_in_project(config["artifact_dir"])
    manifest = read_json(artifact_dir / "manifest.json")
    selected = set(args.sample_id)
    generator = None
    results: list[dict] = []

    for item in manifest:
        sample_id = str(item["task_id"])
        if selected and sample_id not in selected:
            continue
        sample_dir = resolve_in_project(item["sample_dir"])
        raw = (sample_dir / "raw_code.txt").read_text(encoding="utf-8")
        language = str(item.get("language") or "python")
        map_path = sample_dir / "spl_by_method.json"
        spl_path = sample_dir / "spl.txt"
        spl_map = read_json(map_path) if map_path.exists() else {}
        if not spl_map and spl_path.exists():
            spl_map = recover_spl_by_worker(spl_path.read_text(encoding="utf-8"))
        bound, _provenance, before_audit = bind_spl_to_source(raw, spl_map, language)
        if bound:
            results.append({
                "sample_id": sample_id,
                "status": "already_source_bound",
                "bound_cards": len(bound),
            })
            continue

        instance = read_json(sample_dir / "item.json") if (sample_dir / "item.json").exists() else {}
        target_owner = str(instance.get("funname") or "")
        owner_source, owner_audit = source_for_named_owner(raw, language, target_owner)
        normalized, _line_map, numbered = normalize_numbered_source(raw)
        generation_source = owner_source or normalized
        record = {
            "sample_id": sample_id,
            "status": "would_rebuild" if args.dry_run else "rebuilt",
            "target_owner": target_owner or None,
            "target_owner_only": bool(owner_source),
            "numbered_source_normalized": numbered,
            "binding_before": before_audit,
            "owner_audit": owner_audit,
        }
        if args.dry_run:
            results.append(record)
            continue

        if generator is None:
            generator = SPLGenerator(SPLConfig(
                mode=config.get("spl_mode", "openai"),
                model=config.get("spl_model", "deepseek-v4-pro"),
                max_output_tokens=int(config.get("spl_max_output_tokens", 4096)),
                api_key=config.get("api_key"),
                api_key_env=config.get("api_key_env", "OPENAI_API_KEY"),
                base_url=config.get("base_url"),
                raw_http=bool(config.get("openai_raw_http", config.get("raw_http", False))),
                timeout_seconds=int(config.get("openai_timeout_seconds", 600)),
                max_retries=int(config.get("max_retries", 5)),
                api_keys=list(config.get("api_keys") or []),
                max_per_key=int(config.get("max_per_key", 1)),
                api_key_pool_file=config.get("api_key_pool_file"),
            ))
        build, rebuilt_map = generator.generate_for_code_with_metrics_and_map(
            generation_source, language, sample_id,
        )
        rebound, _rebound_provenance, after_audit = bind_spl_to_source(
            raw, rebuilt_map, language,
        )
        if not rebound:
            raise RuntimeError(f"Rebuilt SPL for {sample_id} still has no unique source binding")
        write_text(spl_path, build.text)
        write_json(map_path, rebuilt_map)
        write_json(sample_dir / "spl_metadata.json", build.metadata)
        record["binding_after"] = after_audit
        record["build_tokens"] = int(build.metadata.get("total_tokens", 0) or 0)
        write_json(sample_dir / "spl_source_binding.json", after_audit)
        write_json(sample_dir / "spl_regeneration_audit.json", record)
        results.append(record)

    write_json(artifact_dir / "spl_repair_summary.json", results)
    print(f"Checked {len(results)} samples; rebuilt {sum(r['status'] == 'rebuilt' for r in results)}.")


if __name__ == "__main__":
    main()
