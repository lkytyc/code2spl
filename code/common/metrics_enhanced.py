"""Enhanced metrics: cost estimation, time tracking, token overhead calculations."""

from __future__ import annotations

from collections import defaultdict
from typing import Any

# ── Model pricing (USD per 1M tokens) ──────────────────────
# Prices as of 2025/2026. Adjust as needed.
MODEL_PRICING: dict[str, dict[str, float]] = {
    "deepseek-v4-pro":   {"input": 0.55, "output": 2.19, "reasoning": 2.19},
    "deepseek-v4-flash": {"input": 0.14, "output": 0.55, "reasoning": 0.55},
    "deepseek-v3":       {"input": 0.27, "output": 1.10, "reasoning": 1.10},
    "gpt-4o":            {"input": 2.50, "output": 10.00, "reasoning": 10.00},
    "gpt-4o-mini":       {"input": 0.15, "output": 0.60, "reasoning": 0.60},
    "claude-sonnet-4-6": {"input": 3.00, "output": 15.00, "reasoning": 15.00},
    "claude-opus-4-8":   {"input": 15.00, "output": 75.00, "reasoning": 75.00},
}


def estimate_cost(
    input_tokens: int,
    output_tokens: int,
    reasoning_tokens: int = 0,
    model: str = "deepseek-v4-pro",
) -> float | None:
    """Estimate USD cost for a single LLM call."""
    pricing = MODEL_PRICING.get(model)
    if not pricing:
        return None
    cost = 0.0
    cost += (input_tokens / 1_000_000) * pricing.get("input", 0.0)
    cost += (output_tokens / 1_000_000) * pricing.get("output", 0.0)
    # Reasoning tokens are typically billed as output tokens
    if reasoning_tokens:
        # Don't double-count if output already includes reasoning
        pass
    return cost


def aggregate_cost_summary(
    rows: list[dict[str, Any]],
    model: str = "deepseek-v4-pro",
    group_key: str = "condition",
    usage_keys: tuple[str, ...] = ("llm_usage", "spl_usage", "summary_usage"),
) -> dict[str, Any]:
    """Aggregate detailed cost and token metrics across all conditions.

    Returns per-condition:
      - Total tokens split by inference / SPL generation / summary generation
      - Cost estimates
      - Per-sample averages
      - Token overhead (SPL + summary tokens as fraction of inference tokens)
    """
    grouped: dict[str, dict[str, list[dict[str, Any]]]] = defaultdict(
        lambda: defaultdict(list)
    )

    for row in rows:
        cond = str(row.get(group_key, "unknown"))
        for usage_key in usage_keys:
            usage = row.get(usage_key)
            if isinstance(usage, dict) and usage:
                grouped[cond][usage_key].append(usage)

    result: dict[str, Any] = {}
    for cond, usage_dict in grouped.items():
        result[cond] = {}
        # Inference-only totals (llm_usage only, excluding spl/summary)
        llm_input = 0
        llm_output = 0
        llm_reasoning = 0
        llm_calls = 0
        llm_elapsed = 0.0
        # All-usage totals (for per-key tracking)
        total_input = 0
        total_output = 0
        total_reasoning = 0
        total_calls = 0
        total_elapsed = 0.0

        for usage_key, usages in usage_dict.items():
            key_input = sum(int(u.get("input_tokens", 0) or 0) for u in usages)
            key_output = sum(int(u.get("output_tokens", 0) or 0) for u in usages)
            key_reasoning = sum(int(u.get("reasoning_tokens", 0) or 0) for u in usages)
            key_calls = sum(int(u.get("calls", 1) or 1) for u in usages)
            key_elapsed = sum(float(u.get("elapsed_seconds", 0) or 0) for u in usages)

            result[cond][f"{usage_key}_input_tokens"] = key_input
            result[cond][f"{usage_key}_output_tokens"] = key_output
            result[cond][f"{usage_key}_reasoning_tokens"] = key_reasoning
            result[cond][f"{usage_key}_total_tokens"] = key_input + key_output
            result[cond][f"{usage_key}_calls"] = key_calls
            result[cond][f"{usage_key}_elapsed_seconds"] = key_elapsed

            if usage_key == "llm_usage":
                llm_input = key_input
                llm_output = key_output
                llm_reasoning = key_reasoning
                llm_calls = key_calls
                llm_elapsed = key_elapsed

            total_input += key_input
            total_output += key_output
            total_reasoning += key_reasoning
            total_calls += key_calls
            total_elapsed += key_elapsed

        # Inference-only metrics (llm_usage only)
        result[cond]["inference_input_tokens"] = llm_input
        result[cond]["inference_output_tokens"] = llm_output
        result[cond]["inference_reasoning_tokens"] = llm_reasoning
        result[cond]["inference_total_tokens"] = llm_input + llm_output
        result[cond]["inference_calls"] = llm_calls
        result[cond]["total_elapsed_seconds"] = total_elapsed

        # Per-sample averages (inference only)
        n_samples = len(usage_dict.get("llm_usage", []))
        if n_samples > 0:
            result[cond]["tokens_per_sample"] = (llm_input + llm_output) / n_samples
            result[cond]["cost_per_sample_usd"] = estimate_cost(
                llm_input // max(1, n_samples),
                llm_output // max(1, n_samples),
                llm_reasoning // max(1, n_samples),
                model,
            )
            result[cond]["elapsed_seconds_per_sample"] = total_elapsed / n_samples
        else:
            result[cond]["tokens_per_sample"] = 0
            result[cond]["cost_per_sample_usd"] = 0.0
            result[cond]["elapsed_seconds_per_sample"] = 0.0

        # Total inference cost (llm_usage only)
        result[cond]["inference_cost_usd"] = estimate_cost(
            llm_input, llm_output, llm_reasoning, model
        )
        # Total cost (inference + SPL build)
        result[cond]["total_cost_usd"] = estimate_cost(
            total_input, total_output, total_reasoning, model
        )

        # Token overhead: SPL + summary tokens as fraction of inference
        llm_total = llm_input + llm_output
        spl_total = sum(
            int(u.get("input_tokens", 0) or 0) + int(u.get("output_tokens", 0) or 0)
            for u in usage_dict.get("spl_usage", [])
        )
        summary_total = sum(
            int(u.get("input_tokens", 0) or 0) + int(u.get("output_tokens", 0) or 0)
            for u in usage_dict.get("summary_usage", [])
        )
        result[cond]["token_overhead_spl_ratio"] = (
            spl_total / llm_total if llm_total > 0 else 0.0
        )
        result[cond]["token_overhead_summary_ratio"] = (
            summary_total / llm_total if llm_total > 0 else 0.0
        )
        result[cond]["total_overhead_tokens"] = spl_total + summary_total

    return result


def compute_cost_per_metric(
    cost_summary: dict[str, Any],
    aggregated_metrics: dict[str, Any],
    metric_key: str = "pass_at_1",
    hits_field: str = "hits",
) -> dict[str, Any]:
    """Compute cost per successful unit (e.g. cost/pass, cost/resolved).

    Args:
        cost_summary: Output of aggregate_cost_summary()
        aggregated_metrics: Per-condition aggregate metrics dict.
            Each value is a dict of metrics which may contain:
            - Numeric counts directly (e.g. {"correct": 10})
            - Rates as floats (e.g. {"method_recall_at_1": 0.5}) — in this case
              the function looks for "outputs" or "reportable_outputs" to
              estimate actual hit counts.
            - Dicts with hits/total (e.g. {"pass_at_1": {"hits": 5, "total": 10}})
        metric_key: Key in the per-condition metrics dict
        hits_field: Field name within the metric value if it's a dict

    Returns:
        dict mapping condition -> cost per hit
    """
    result: dict[str, Any] = {}
    for cond, costs in cost_summary.items():
        cond_metrics = aggregated_metrics.get(cond, {})
        if not isinstance(cond_metrics, dict):
            hits = 0
        else:
            metric_data = cond_metrics.get(metric_key, 0)
            if isinstance(metric_data, dict):
                hits = int(metric_data.get(hits_field, 0) or 0)
            elif isinstance(metric_data, (int, float)):
                val = float(metric_data)
                if 0 < val <= 1:
                    # Rate — estimate hits from total
                    total = int(cond_metrics.get("reportable_outputs",
                               cond_metrics.get("outputs",
                               cond_metrics.get("resolved_total",
                               cond_metrics.get("total", 0)) or 0)))
                    hits = int(round(val * total))
                else:
                    hits = int(val)
            else:
                hits = 0
        total_cost = costs.get("total_cost_usd")
        result[cond] = {
            "total_cost_usd": total_cost,
            "hits": hits,
            "cost_per_hit_usd": total_cost / hits if total_cost is not None and hits > 0 else None,
        }
    return result


def track_phase_times(
    phase_times: list[dict[str, float]],
    phase_names: list[str],
) -> dict[str, Any]:
    """Aggregate per-phase wall-clock timing.

    Args:
        phase_times: List of per-sample dicts, each with keys like
            {"prepare": 1.0, "run": 5.0, "evaluate": 2.0}
        phase_names: Expected phase names in order.

    Returns:
        dict with mean, median, p95, total per phase.
    """
    if not phase_times:
        return {"n": 0}

    aggregated: dict[str, list[float]] = {name: [] for name in phase_names}
    for entry in phase_times:
        for name in phase_names:
            val = entry.get(name, 0.0)
            if val is not None:
                aggregated[name].append(float(val))

    result: dict[str, Any] = {"n": len(phase_times)}
    for name in phase_names:
        vals = sorted(aggregated[name])
        if not vals:
            continue
        n = len(vals)
        result[name] = {
            "mean": sum(vals) / n,
            "median": vals[n // 2],
            "p95": vals[int(0.95 * (n - 1))],
            "total": sum(vals),
            "min": vals[0],
            "max": vals[-1],
        }
    return result


def format_token_count(n: int) -> str:
    """Human-readable token count."""
    if n >= 1_000_000:
        return f"{n / 1_000_000:.1f}M"
    if n >= 1_000:
        return f"{n / 1_000:.0f}K"
    return str(n)


def format_cost_usd(usd: float | None) -> str:
    """Human-readable USD cost."""
    if usd is None:
        return "N/A"
    if usd >= 100:
        return f"${usd:.2f}"
    if usd >= 1:
        return f"${usd:.3f}"
    if usd >= 0.01:
        return f"${usd:.4f}"
    return f"${usd:.6f}"
