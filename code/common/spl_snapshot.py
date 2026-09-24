from __future__ import annotations

import hashlib
import json
import re
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable

from .paths import ensure_dir, ensure_under_project, write_json


SNAPSHOT_SCHEMA = "spl-snapshot-v1"


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def _safe_sample_key(sample_id: str) -> str:
    readable = re.sub(r"[^A-Za-z0-9_.-]+", "__", sample_id).strip("._-") or "sample"
    suffix = hashlib.sha256(sample_id.encode("utf-8")).hexdigest()[:12]
    return f"{readable[:120]}--{suffix}"


def _collect_assets(source_dir: Path, relative_paths: Iterable[str | Path]) -> list[Path]:
    files: list[Path] = []
    for value in relative_paths:
        relative = Path(value)
        if relative.is_absolute() or ".." in relative.parts:
            raise ValueError(f"Snapshot asset must be relative to its source directory: {value}")
        source = source_dir / relative
        if not source.exists():
            raise FileNotFoundError(f"SPL snapshot asset does not exist: {source}")
        if source.is_dir():
            files.extend(path for path in source.rglob("*") if path.is_file())
        else:
            files.append(source)
    return sorted(set(files), key=lambda path: path.relative_to(source_dir).as_posix())


def snapshot_sample_assets(
    source_dir: str | Path,
    snapshot_root: str | Path,
    sample_id: str,
    relative_paths: Iterable[str | Path],
    *,
    provenance: dict | None = None,
    overwrite: bool = False,
) -> Path:
    source_root = ensure_under_project(source_dir)
    root = ensure_dir(snapshot_root)
    files = _collect_assets(source_root, relative_paths)
    if not files:
        raise ValueError(f"No SPL assets were selected for snapshot sample {sample_id}")

    entry_dir = root / "instances" / _safe_sample_key(sample_id)
    assets_dir = entry_dir / "assets"
    records = []
    for source in files:
        relative = source.relative_to(source_root)
        records.append(
            {
                "path": relative.as_posix(),
                "bytes": source.stat().st_size,
                "sha256": _sha256(source),
            }
        )

    manifest_path = entry_dir / "manifest.json"
    if manifest_path.exists() and not overwrite:
        existing = json.loads(manifest_path.read_text(encoding="utf-8"))
        if existing.get("sample_id") == sample_id and existing.get("files") == records:
            verify_sample_snapshot(entry_dir)
            return entry_dir
        raise FileExistsError(
            f"Refusing to overwrite a different SPL snapshot for {sample_id}: {entry_dir}"
        )

    if entry_dir.exists():
        shutil.rmtree(entry_dir)
    ensure_dir(assets_dir)
    for source in files:
        relative = source.relative_to(source_root)
        target = assets_dir / relative
        ensure_dir(target.parent)
        shutil.copy2(source, target)

    write_json(
        manifest_path,
        {
            "schema": SNAPSHOT_SCHEMA,
            "sample_id": sample_id,
            "created_at": datetime.now(timezone.utc).isoformat(),
            "source_dir": str(source_root),
            "provenance": provenance or {},
            "file_count": len(records),
            "total_bytes": sum(record["bytes"] for record in records),
            "files": records,
        },
    )
    verify_sample_snapshot(entry_dir)
    return entry_dir


def sample_snapshot_dir(snapshot_root: str | Path, sample_id: str) -> Path:
    return ensure_under_project(snapshot_root) / "instances" / _safe_sample_key(sample_id)


def verify_sample_snapshot(entry_dir: str | Path) -> dict:
    entry = ensure_under_project(entry_dir)
    manifest_path = entry / "manifest.json"
    if not manifest_path.exists():
        raise FileNotFoundError(f"SPL snapshot manifest is missing: {manifest_path}")
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    if manifest.get("schema") != SNAPSHOT_SCHEMA:
        raise ValueError(f"Unsupported SPL snapshot schema in {manifest_path}")
    for record in manifest.get("files", []):
        asset = entry / "assets" / Path(record["path"])
        if not asset.is_file():
            raise FileNotFoundError(f"SPL snapshot asset is missing: {asset}")
        if asset.stat().st_size != int(record["bytes"]) or _sha256(asset) != record["sha256"]:
            raise ValueError(f"SPL snapshot checksum mismatch: {asset}")
    return manifest


def restore_sample_snapshot(
    snapshot_root: str | Path,
    sample_id: str,
    destination_dir: str | Path,
    *,
    overwrite: bool = False,
) -> bool:
    entry_dir = sample_snapshot_dir(snapshot_root, sample_id)
    if not entry_dir.exists():
        return False
    manifest = verify_sample_snapshot(entry_dir)
    destination = ensure_dir(destination_dir)
    for record in manifest["files"]:
        source = entry_dir / "assets" / Path(record["path"])
        target = destination / Path(record["path"])
        if target.exists() and not overwrite:
            if target.is_file() and target.stat().st_size == source.stat().st_size and _sha256(target) == record["sha256"]:
                continue
            raise FileExistsError(f"Refusing to replace a different restored SPL asset: {target}")
        ensure_dir(target.parent)
        shutil.copy2(source, target)
    return True


def build_snapshot_manifest(snapshot_root: str | Path, *, metadata: dict | None = None) -> dict:
    root = ensure_dir(snapshot_root)
    entries = []
    instances_dir = root / "instances"
    if instances_dir.exists():
        for entry_dir in sorted(path for path in instances_dir.iterdir() if path.is_dir()):
            manifest = verify_sample_snapshot(entry_dir)
            entries.append(
                {
                    "sample_id": manifest["sample_id"],
                    "entry": str(entry_dir.relative_to(root)).replace("\\", "/"),
                    "file_count": manifest["file_count"],
                    "total_bytes": manifest["total_bytes"],
                    "provenance": manifest.get("provenance", {}),
                }
            )
    result = {
        "schema": SNAPSHOT_SCHEMA,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "metadata": metadata or {},
        "sample_count": len(entries),
        "file_count": sum(entry["file_count"] for entry in entries),
        "total_bytes": sum(entry["total_bytes"] for entry in entries),
        "entries": entries,
    }
    write_json(root / "manifest.json", result)
    return result
