from __future__ import annotations

import re
from typing import Any


# ── tiktoken-backed token counter (with graceful fallback) ────────────────

def _load_tiktoken_encoding(model: str = "gpt-4o"):
    """Return a tiktoken encoding for *model*, or None if unavailable."""
    try:
        import tiktoken  # type: ignore[import-untyped]
    except ImportError:
        return None
    try:
        return tiktoken.encoding_for_model(model)
    except KeyError:
        try:
            return tiktoken.get_encoding("o200k_base")
        except Exception:
            return None


_ENCODING = _load_tiktoken_encoding()


def token_count(text: str) -> int:
    """Return the token count of *text* using the model-aware tokenizer.

    When ``tiktoken`` is installed the count uses the ``gpt-4o`` encoding
    (``o200k_base`` fallback).  Otherwise it falls back to a conservative
    character-based estimate (``len(text) // 3.5``) which is more accurate
    than the previous ``len(text) // 4`` for typical Python / Java / English
    natural-language text.
    """
    if _ENCODING is not None:
        return len(_ENCODING.encode(text))
    # Conservative fallback: typical code/NL text averages ~3.5 chars/token
    # for current-gen tokenizers (o200k / cl100k).
    return max(1, int(len(text) / 3.5)) if text else 0


def tokenizer_name() -> str:
    if _ENCODING is not None:
        return getattr(_ENCODING, "name", "tiktoken")
    return "char_div_3.5_fallback"


# ── structured summary token-budget audit ──────────────────────────────────

def summary_control_metrics(
    raw_code: str,
    spl: str,
    free_summary: str,
    structured_summary: str,
    compressed_raw: str,
    config: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Compute token-budget control metrics comparing SPL vs summaries."""
    config = config or {}
    spl_tokens = token_count(spl)
    structured_tokens = token_count(structured_summary)
    free_tokens = token_count(free_summary)
    compressed_tokens = token_count(compressed_raw)
    min_ratio = float(config.get("structured_summary_token_ratio_min", 0.75))
    max_ratio = float(config.get("structured_summary_token_ratio_max", 1.25))
    ratio = structured_tokens / spl_tokens if spl_tokens else None
    return {
        "raw_code_chars": len(raw_code),
        "raw_code_tokens": token_count(raw_code),
        "tokenizer": tokenizer_name(),
        "spl_chars": len(spl),
        "spl_tokens": spl_tokens,
        "compressed_raw_chars": len(compressed_raw),
        "compressed_raw_tokens": compressed_tokens,
        "compressed_raw_to_spl_token_ratio": compressed_tokens / spl_tokens if spl_tokens else None,
        "free_summary_chars": len(free_summary),
        "free_summary_tokens": free_tokens,
        "free_summary_to_spl_token_ratio": free_tokens / spl_tokens if spl_tokens else None,
        "structured_summary_chars": len(structured_summary),
        "structured_summary_tokens": structured_tokens,
        "structured_summary_to_spl_token_ratio": ratio,
        "structured_summary_ratio_min": min_ratio,
        "structured_summary_ratio_max": max_ratio,
        "structured_summary_token_control_ok": bool(ratio is not None and min_ratio <= ratio <= max_ratio),
        "note": "Token counts use tiktoken (o200k_base) when available; fallback is char/3.5.",
    }


# ── syntax-preserving code compression ─────────────────────────────────────

def compress_code_to_token_budget(text: str, target_tokens: int) -> str:
    """Compress source code to roughly fit within *target_tokens* while
    preserving syntactic integrity.

    Unlike simple truncation, this function removes whole lines from the
    middle of functions while keeping the header, signature, and tail
    intact so the code remains parseable.
    """
    if target_tokens <= 0:
        return ""
    if token_count(text) <= target_tokens:
        return text

    lines = text.splitlines()
    if len(lines) <= 20:
        # Not enough lines to meaningfully compress; fall back to
        # budget-aware truncation that preserves head and tail.
        budget_chars = max(200, target_tokens * 4)
        head_chars = budget_chars * 2 // 3
        tail_chars = budget_chars - head_chars
        return (
            text[:head_chars].rstrip()
            + "\n# … {chars} chars / ~{tokens} tokens truncated for budget control …\n"
            + text[-tail_chars:].lstrip()
        )

    # Keep first 25% of lines (imports, class/function signatures) and
    # last 15% of lines (return statements, closing braces), sample the
    # middle 35% of lines from the middle region.
    head_count = max(3, len(lines) // 4)
    tail_count = max(3, len(lines) * 15 // 100)
    middle_start = head_count
    middle_end = len(lines) - tail_count
    middle_available = middle_end - middle_start
    if middle_available <= 0:
        return text

    # Sample approximately every Nth line from the middle.
    target_middle_lines = max(2, len(lines) * 35 // 100)
    step = max(1, middle_available // target_middle_lines)
    sampled: list[int] = []
    for i in range(middle_start, middle_end, step):
        if len(sampled) < target_middle_lines:
            sampled.append(i)

    kept_lines: list[str] = []
    kept_lines.extend(lines[:head_count])
    kept_lines.append(
        f"# … {middle_available} lines compressed (step={step}) for token budget …"
    )
    for i in sampled:
        kept_lines.append(lines[i])
    kept_lines.append(
        f"# … continuing after compressed region …"
    )
    kept_lines.extend(lines[-tail_count:])

    compressed = "\n".join(kept_lines)
    if token_count(compressed) > target_tokens * 1.2:
        # Still over budget — keep only head and tail.
        budget_chars = max(200, target_tokens * 4)
        head_chars = budget_chars * 2 // 3
        tail_chars = budget_chars - head_chars
        compressed = (
            text[:head_chars].rstrip()
            + "\n# … chars truncated for strict token budget …\n"
            + text[-tail_chars:].lstrip()
        )
    return compressed
