from __future__ import annotations

import json
import random
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import Callable, TypeVar

from .paths import resolve_in_project


T = TypeVar("T")
R = TypeVar("R")


def _candidate_item_ids(item: dict) -> list[str]:
    candidates: list[str] = []

    def add(value: object) -> None:
        if value is None:
            return
        text = str(value).strip()
        if text and text not in candidates:
            candidates.append(text)
        normalized = text.replace("/", "_")
        if normalized and normalized not in candidates:
            candidates.append(normalized)

    for key in ("sample_id", "sample_key", "instance_id", "task_id", "full_name", "id"):
        add(item.get(key))

    task_id = item.get("task_id")
    mode = item.get("mode") or item.get("_mode")
    if task_id is not None and mode is not None:
        add(f"{task_id}::{mode}")

    project = item.get("project")
    bug_id = item.get("bug_id")
    if project is not None and bug_id is not None:
        add(f"{project}_{bug_id}")
        add(f"{project}-{bug_id}")

    for nested_key in ("item", "task", "bug"):
        nested = item.get(nested_key)
        if isinstance(nested, dict):
            for value in _candidate_item_ids(nested):
                add(value)
    return candidates


def load_frozen_sample_ids(path: str | Path) -> list[str]:
    resolved = resolve_in_project(path)
    if resolved.suffix.lower() == ".txt":
        ids = [line.strip() for line in resolved.read_text(encoding="utf-8").splitlines() if line.strip()]
    else:
        payload = json.loads(resolved.read_text(encoding="utf-8"))
        if isinstance(payload, dict):
            payload = payload.get("sample_ids")
        if not isinstance(payload, list):
            raise ValueError(f"Frozen sample file must contain a list or sample_ids list: {resolved}")
        ids = [str(value).strip() for value in payload if str(value).strip()]

    duplicates = sorted({sample_id for sample_id in ids if ids.count(sample_id) > 1})
    if duplicates:
        raise ValueError(f"Frozen sample file contains duplicate IDs: {duplicates[:10]}")
    return ids


def selected_items(items: list[dict], config: dict) -> list[dict]:
    indexed = []
    for pos, item in enumerate(items):
        copied = dict(item)
        copied.setdefault("index", pos)
        indexed.append(copied)

    # Stage 0: frozen benchmark IDs. This is the formal-experiment path and
    # intentionally takes precedence over ad-hoc index/range sampling.
    sample_ids_file = config.get("sample_ids_file")
    if sample_ids_file:
        frozen_ids = load_frozen_sample_ids(sample_ids_file)
        by_id: dict[str, dict] = {}
        ambiguous: set[str] = set()
        for item in indexed:
            for candidate in _candidate_item_ids(item):
                if candidate in by_id and by_id[candidate] is not item:
                    ambiguous.add(candidate)
                else:
                    by_id[candidate] = item
        selected: list[dict] = []
        missing: list[str] = []
        seen_objects: set[int] = set()
        for sample_id in frozen_ids:
            if sample_id in ambiguous:
                raise ValueError(
                    f"Frozen sample ID is ambiguous in the population: {sample_id}. "
                    "Use a benchmark-specific composite ID."
                )
            item = by_id.get(sample_id)
            if item is None:
                missing.append(sample_id)
                continue
            marker = id(item)
            if marker in seen_objects:
                raise ValueError(f"Multiple frozen IDs resolve to the same population item: {sample_id}")
            seen_objects.add(marker)
            selected.append(item)
        if missing and config.get("strict_sample_ids", True):
            raise ValueError(
                f"{len(missing)} frozen sample IDs were not found in the population from "
                f"{sample_ids_file}: {missing[:10]}"
            )
        return selected

    # Stage 1: exact index selection (bypasses all other filters).
    indices = config.get("indices")
    if indices:
        wanted = {int(i) for i in indices}
        return [item for item in indexed if int(item["index"]) in wanted]

    # Stage 2: range filtering (narrows the pool)
    start = config.get("start_index")
    end = config.get("end_index")
    if start is not None or end is not None:
        lo = int(start or 0)
        hi = int(end) if end is not None else len(indexed)
        indexed = [item for item in indexed if lo <= int(item["index"]) < hi]

    # Stage 3: random sampling from the current pool
    random_sample = config.get("random_sample")
    if random_sample is not None:
        n = int(random_sample)
        if n < len(indexed):
            seed = config.get("random_seed")
            rng = random.Random(seed)
            indexed = rng.sample(indexed, n)
        return indexed

    # Stage 4: deterministic "take first N"
    limit = config.get("limit")
    if limit is not None:
        indexed = indexed[: int(limit)]
    return indexed


def run_ordered(items: list[T], worker: Callable[[T], R], max_workers: int, continue_on_error: bool = False) -> tuple[list[R], list[dict]]:
    errors: list[dict] = []
    if max_workers <= 1:
        results = []
        for index, item in enumerate(items):
            try:
                results.append(worker(item))
            except Exception as exc:
                if not continue_on_error:
                    raise
                errors.append({"index": index, "error": repr(exc), "item": item if isinstance(item, dict) else str(item)})
        return results, errors

    results: list[R | None] = [None] * len(items)
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_index = {executor.submit(worker, item): index for index, item in enumerate(items)}
        for future in as_completed(future_to_index):
            index = future_to_index[future]
            try:
                results[index] = future.result()
            except Exception as exc:
                if not continue_on_error:
                    raise
                item = items[index]
                errors.append({"index": index, "error": repr(exc), "item": item if isinstance(item, dict) else str(item)})
    return [result for result in results if result is not None], sorted(errors, key=lambda row: row["index"])


def generation_kwargs(
    config: dict,
    *,
    model_key: str = "model",
    max_tokens_key: str = "max_output_tokens",
    thinking_key: str = "thinking",
) -> dict:
    thinking = config.get(thinking_key)
    if thinking is None and thinking_key != "thinking":
        thinking = config.get("thinking")
    return {
        "provider": config.get("provider", "openai"),
        "model": config.get(model_key, "gpt-4o-2024-11-20"),
        "temperature": float(config.get("temperature", 0)),
        "max_output_tokens": int(config.get(max_tokens_key, 4096)),
        "thinking": thinking,
        "reasoning_effort": config.get("reasoning_effort"),
        "api_key": config.get("api_key") or config.get("openai_api_key"),
        "api_key_env": config.get("api_key_env", "OPENAI_API_KEY"),
        "base_url": config.get("base_url") or config.get("openai_base_url"),
        "max_retries": int(config.get("max_retries", 3)),
        "retry_backoff_seconds": float(config.get("retry_backoff_seconds", 2.0)),
        "raw_http": bool(config.get("openai_raw_http", config.get("raw_http", False))),
        "timeout_seconds": int(config.get("openai_timeout_seconds", config.get("timeout_seconds", 180))),
        "api_keys": list(config.get("api_keys") or []),
        "max_per_key": int(config.get("max_per_key", 1)),
        "api_key_pool_file": config.get("api_key_pool_file"),
    }
