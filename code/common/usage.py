from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any

from .paths import write_json
from .providers import GenerationResult


@dataclass
class UsageTotals:
    calls: int = 0
    elapsed_seconds: float = 0.0
    input_tokens: int = 0
    output_tokens: int = 0
    reasoning_tokens: int = 0
    total_tokens: int = 0
    missing_token_records: int = 0

    def add(self, metadata: dict[str, Any] | None) -> None:
        if not metadata:
            return
        calls = metadata.get("calls", 1)
        self.calls += int(1 if calls is None else calls)
        self.elapsed_seconds += float(metadata.get("elapsed_seconds", 0) or 0)
        raw_usage = metadata.get("raw_usage") if isinstance(metadata.get("raw_usage"), dict) else {}
        if metadata.get("input_tokens") is None and raw_usage.get("prompt_tokens") is not None:
            metadata = dict(metadata)
            metadata["input_tokens"] = raw_usage.get("prompt_tokens")
        if metadata.get("output_tokens") is None and raw_usage.get("completion_tokens") is not None:
            metadata = dict(metadata)
            metadata["output_tokens"] = raw_usage.get("completion_tokens")
        if metadata.get("reasoning_tokens") is None:
            completion_details = raw_usage.get("completion_tokens_details") if isinstance(raw_usage.get("completion_tokens_details"), dict) else {}
            if completion_details.get("reasoning_tokens") is not None:
                metadata = dict(metadata)
                metadata["reasoning_tokens"] = completion_details.get("reasoning_tokens")
        if metadata.get("total_tokens") is None and raw_usage.get("total_tokens") is not None:
            metadata = dict(metadata)
            metadata["total_tokens"] = raw_usage.get("total_tokens")
        saw_tokens = False
        for key in ("input_tokens", "output_tokens", "reasoning_tokens", "total_tokens"):
            value = metadata.get(key)
            if value is not None:
                setattr(self, key, getattr(self, key) + int(value))
                saw_tokens = True
        if not saw_tokens:
            self.missing_token_records += 1

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def generation_metadata(result: GenerationResult, *, role: str, condition: str | None = None) -> dict[str, Any]:
    metadata = result.to_metadata()
    metadata["role"] = role
    metadata["condition"] = condition
    metadata["calls"] = 1
    return metadata


def write_generation_result(out_dir: Path, result: GenerationResult, *, role: str, condition: str | None = None) -> None:
    (out_dir / "output.txt").write_text(result.text, encoding="utf-8")
    write_json(out_dir / "call_metadata.json", generation_metadata(result, role=role, condition=condition))


def read_metadata(path: Path) -> dict[str, Any] | None:
    if not path.exists():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return None


def summarize_usage(rows: list[dict[str, Any]], *, group_key: str = "condition") -> dict[str, dict[str, Any]]:
    grouped: dict[str, UsageTotals] = {}
    for row in rows:
        key = str(row.get(group_key, "unknown"))
        grouped.setdefault(key, UsageTotals()).add(row.get("llm_usage"))
        grouped.setdefault(key, UsageTotals()).add(row.get("spl_usage"))
        grouped.setdefault(key, UsageTotals()).add(row.get("summary_usage"))
    return {key: totals.to_dict() for key, totals in grouped.items()}
