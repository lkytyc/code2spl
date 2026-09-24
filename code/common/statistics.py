"""Statistical tests and confidence intervals for experiment evaluation."""

from __future__ import annotations

import math
import random
from collections import defaultdict
from typing import Any


def wilson_ci(hits: int, total: int, z: float = 1.96) -> dict[str, float | None]:
    """Wilson score interval for a binomial proportion."""
    if total <= 0:
        return {"rate": None, "ci_low": None, "ci_high": None}
    phat = hits / total
    denom = 1 + z * z / total
    centre = phat + z * z / (2 * total)
    margin = z * math.sqrt((phat * (1 - phat) + z * z / (4 * total)) / total)
    return {
        "rate": phat,
        "ci_low": max(0.0, (centre - margin) / denom),
        "ci_high": min(1.0, (centre + margin) / denom),
    }


def binary_condition_statistics(
    rows: list[dict[str, Any]],
    metrics: list[str],
    condition_key: str = "condition",
) -> dict[str, Any]:
    """Per-condition Wilson CI for a set of binary metrics."""
    grouped: dict[str, dict[str, dict[str, int]]] = defaultdict(
        lambda: defaultdict(lambda: {"hits": 0, "total": 0})
    )
    for row in rows:
        condition = str(row.get(condition_key, "unknown"))
        for metric in metrics:
            value = row.get(metric)
            if value is None:
                continue
            grouped[condition][metric]["total"] += 1
            grouped[condition][metric]["hits"] += int(bool(value))

    out: dict[str, Any] = {}
    for condition, metric_rows in grouped.items():
        out[condition] = {}
        for metric, counts in metric_rows.items():
            out[condition][metric] = counts | wilson_ci(counts["hits"], counts["total"])
    return out


def paired_binary_deltas(
    rows: list[dict[str, Any]],
    pairs: list[tuple[str, str]],
    metrics: list[str],
) -> dict[str, Any]:
    """Paired delta (treatment - baseline) with normal-approx CI for binary metrics."""
    by_sample_condition: dict[tuple[str, str], dict[str, Any]] = {}
    for row in rows:
        sample_id = str(
            row.get("task_id")
            or row.get("bug_id")
            or row.get("sample_id")
            or row.get("instance_id")
            or row.get("index")
        )
        by_sample_condition[(sample_id, str(row.get("condition")))] = row

    out: dict[str, Any] = {}
    for baseline, treatment in pairs:
        pair_key = f"{treatment}_minus_{baseline}"
        out[pair_key] = {}
        sample_ids = {
            sample_id
            for sample_id, condition in by_sample_condition
            if condition == baseline and (sample_id, treatment) in by_sample_condition
        }
        for metric in metrics:
            diffs = []
            for sample_id in sorted(sample_ids):
                left = by_sample_condition[(sample_id, baseline)].get(metric)
                right = by_sample_condition[(sample_id, treatment)].get(metric)
                if left is None or right is None:
                    continue
                diffs.append(int(bool(right)) - int(bool(left)))
            if not diffs:
                out[pair_key][metric] = {"n": 0, "mean_delta": None}
                continue
            mean = sum(diffs) / len(diffs)
            variance = sum((v - mean) ** 2 for v in diffs) / max(1, len(diffs) - 1)
            stderr = math.sqrt(variance / len(diffs)) if len(diffs) > 1 else 0.0
            out[pair_key][metric] = {
                "n": len(diffs),
                "mean_delta": mean,
                "ci_low": mean - 1.96 * stderr,
                "ci_high": mean + 1.96 * stderr,
            }
    return out


# ---------------------------------------------------------------------------
# Bootstrap confidence intervals
# ---------------------------------------------------------------------------

def paired_bootstrap_ci(
    rows: list[dict[str, Any]],
    baseline: str,
    treatment: str,
    metric: str,
    n_bootstrap: int = 10000,
    seed: int = 42,
    condition_key: str = "condition",
) -> dict[str, Any]:
    """Bootstrap 95% CI for the paired difference (treatment - baseline) on a binary metric.

    Returns mean_delta, ci_low, ci_high, and the full bootstrap distribution summary.
    """
    by_sample: dict[str, dict[str, Any]] = {}
    sample_id_key = _sample_id_key(rows)
    for row in rows:
        sid = str(row.get(sample_id_key, row.get("index", "")))
        cond = str(row.get(condition_key, ""))
        by_sample.setdefault(sid, {})[cond] = row

    # Build paired observations
    diffs: list[float] = []
    contingency = {"both_pass": 0, "baseline_only": 0, "treatment_only": 0, "both_fail": 0}
    for sid, conds in by_sample.items():
        b_val = conds.get(baseline, {}).get(metric)
        t_val = conds.get(treatment, {}).get(metric)
        if b_val is None or t_val is None:
            continue
        b = int(bool(b_val))
        t = int(bool(t_val))
        diffs.append(float(t - b))
        if b and t:
            contingency["both_pass"] += 1
        elif b and not t:
            contingency["baseline_only"] += 1
        elif not b and t:
            contingency["treatment_only"] += 1
        else:
            contingency["both_fail"] += 1

    if not diffs:
        return {"n_pairs": 0, "mean_delta": None, "ci_low": None, "ci_high": None}

    rng = random.Random(seed)
    mean_delta = sum(diffs) / len(diffs)
    boot_means: list[float] = []
    n = len(diffs)
    for _ in range(n_bootstrap):
        sample = [diffs[rng.randint(0, n - 1)] for _ in range(n)]
        boot_means.append(sum(sample) / n)
    boot_means.sort()
    ci_low = boot_means[int(0.025 * n_bootstrap)]
    ci_high = boot_means[int(0.975 * n_bootstrap)]

    return {
        "n_pairs": n,
        "mean_delta": mean_delta,
        "ci_low": ci_low,
        "ci_high": ci_high,
        "contingency": contingency,
        "method": "paired_bootstrap_percentile",
        "n_bootstrap": n_bootstrap,
    }


def bootstrap_mrr_ci(
    mrr_values: list[float],
    n_bootstrap: int = 10000,
    seed: int = 42,
) -> dict[str, Any]:
    """Bootstrap 95% CI for Mean Reciprocal Rank (continuous metric)."""
    if not mrr_values:
        return {"mean": None, "ci_low": None, "ci_high": None, "n": 0}
    rng = random.Random(seed)
    n = len(mrr_values)
    mean_mrr = sum(mrr_values) / n
    boot_means: list[float] = []
    for _ in range(n_bootstrap):
        sample = [mrr_values[rng.randint(0, n - 1)] for _ in range(n)]
        boot_means.append(sum(sample) / n)
    boot_means.sort()
    return {
        "n": n,
        "mean": mean_mrr,
        "ci_low": boot_means[int(0.025 * n_bootstrap)],
        "ci_high": boot_means[int(0.975 * n_bootstrap)],
        "method": "bootstrap_percentile",
        "n_bootstrap": n_bootstrap,
    }


def bootstrap_mean_ci(
    values: list[float],
    n_bootstrap: int = 10000,
    seed: int = 42,
) -> dict[str, Any]:
    """Bootstrap 95% CI for any continuous metric mean."""
    if not values:
        return {"mean": None, "ci_low": None, "ci_high": None, "n": 0}
    rng = random.Random(seed)
    n = len(values)
    mean_val = sum(values) / n
    boot_means: list[float] = []
    for _ in range(n_bootstrap):
        sample = [values[rng.randint(0, n - 1)] for _ in range(n)]
        boot_means.append(sum(sample) / n)
    boot_means.sort()
    return {
        "n": n,
        "mean": mean_val,
        "ci_low": boot_means[int(0.025 * n_bootstrap)],
        "ci_high": boot_means[int(0.975 * n_bootstrap)],
        "method": "bootstrap_percentile",
        "n_bootstrap": n_bootstrap,
    }


# ---------------------------------------------------------------------------
# McNemar test for paired binary outcomes
# ---------------------------------------------------------------------------

def mcnemar_test(
    rows: list[dict[str, Any]],
    baseline: str,
    treatment: str,
    metric: str,
    condition_key: str = "condition",
) -> dict[str, Any]:
    """McNemar's exact test (binomial) for paired binary data.

    H0: marginal probabilities are equal (baseline and treatment have same success rate).
    """
    by_sample: dict[str, dict[str, Any]] = {}
    sample_id_key = _sample_id_key(rows)
    for row in rows:
        sid = str(row.get(sample_id_key, row.get("index", "")))
        cond = str(row.get(condition_key, ""))
        by_sample.setdefault(sid, {})[cond] = row

    b_only = 0  # baseline=1, treatment=0  (discordant: baseline only)
    t_only = 0  # baseline=0, treatment=1  (discordant: treatment only)
    for sid, conds in by_sample.items():
        b_val = conds.get(baseline, {}).get(metric)
        t_val = conds.get(treatment, {}).get(metric)
        if b_val is None or t_val is None:
            continue
        b = int(bool(b_val))
        t = int(bool(t_val))
        if b == 1 and t == 0:
            b_only += 1
        elif b == 0 and t == 1:
            t_only += 1

    n_discordant = b_only + t_only
    if n_discordant == 0:
        return {
            "n_discordant": 0,
            "statistic": None,
            "p_value": None,
            "significant": None,
            "method": "mcnemar_exact_binomial",
            "note": "No discordant pairs — test undefined.",
        }

    # Exact binomial test: under H0, b_only ~ Binomial(n_discordant, 0.5)
    from math import comb

    # Two-sided p-value
    p_exact = 0.0
    for k in range(n_discordant + 1):
        prob = comb(n_discordant, k) * (0.5 ** n_discordant)
        if abs(k - n_discordant / 2) >= abs(b_only - n_discordant / 2):
            p_exact += prob

    return {
        "n_discordant": n_discordant,
        "baseline_only": b_only,
        "treatment_only": t_only,
        "statistic": b_only,  # test statistic under binomial
        "p_value": min(p_exact, 1.0),
        "significant": p_exact < 0.05,
        "method": "mcnemar_exact_binomial",
    }


# ---------------------------------------------------------------------------
# Effect size
# ---------------------------------------------------------------------------

def cohens_h(p1: float, p2: float) -> float:
    """Cohen's h effect size for two proportions.

    h = 2 * (arcsin(sqrt(p1)) - arcsin(sqrt(p2)))
    Interpretation: 0.2 = small, 0.5 = medium, 0.8 = large.
    """
    import math

    p1 = max(0.0001, min(0.9999, p1))
    p2 = max(0.0001, min(0.9999, p2))
    return 2.0 * (math.asin(math.sqrt(p1)) - math.asin(math.sqrt(p2)))


def compute_cohens_h_from_rows(
    rows: list[dict[str, Any]],
    baseline: str,
    treatment: str,
    metric: str,
    condition_key: str = "condition",
) -> dict[str, Any]:
    """Compute Cohen's h for two conditions from per-sample rows."""
    b_hits, b_total = 0, 0
    t_hits, t_total = 0, 0
    for row in rows:
        cond = str(row.get(condition_key, ""))
        val = row.get(metric)
        if val is None:
            continue
        if cond == baseline:
            b_total += 1
            b_hits += int(bool(val))
        elif cond == treatment:
            t_total += 1
            t_hits += int(bool(val))
    if b_total == 0 or t_total == 0:
        return {"cohens_h": None, "baseline_rate": None, "treatment_rate": None}
    p1 = b_hits / b_total
    p2 = t_hits / t_total
    h = cohens_h(p1, p2)
    return {
        "cohens_h": h,
        "baseline_rate": p1,
        "treatment_rate": p2,
        "baseline_hits": b_hits,
        "baseline_total": b_total,
        "treatment_hits": t_hits,
        "treatment_total": t_total,
        "interpretation": (
            "negligible"
            if abs(h) < 0.2
            else "small"
            if abs(h) < 0.5
            else "medium"
            if abs(h) < 0.8
            else "large"
        ),
    }


# ---------------------------------------------------------------------------
# Benjamini-Hochberg FDR correction
# ---------------------------------------------------------------------------

def benjamini_hochberg(p_values: list[tuple[str, float]], alpha: float = 0.05) -> dict[str, Any]:
    """Apply BH procedure for FDR control across multiple hypothesis tests.

    Args:
        p_values: List of (test_name, p_value) tuples.
        alpha: FDR threshold.

    Returns:
        Dict with corrected significance for each test.
    """
    if not p_values:
        return {"corrected": [], "n_tests": 0}

    # Sort by p-value ascending
    sorted_tests = sorted(p_values, key=lambda x: x[1])
    n = len(sorted_tests)
    significant: list[dict[str, Any]] = []
    last_sig_idx = -1

    for rank, (name, p) in enumerate(sorted_tests, start=1):
        threshold = (rank / n) * alpha
        is_sig = p <= threshold
        significant.append({"test": name, "p_value": p, "rank": rank, "bh_threshold": threshold, "significant": is_sig})
        if is_sig:
            last_sig_idx = rank - 1

    # All tests up to last_sig_idx are significant
    for i, entry in enumerate(significant):
        entry["bh_significant"] = i <= last_sig_idx

    return {
        "corrected": significant,
        "n_tests": n,
        "alpha": alpha,
        "n_significant_bh": last_sig_idx + 1,
    }


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _sample_id_key(rows: list[dict[str, Any]]) -> str:
    for key in ("task_id", "bug_id", "instance_id", "sample_id"):
        if any(key in r for r in rows):
            return key
    return "index"


def compute_continuous_metric_rows(
    rows: list[dict[str, Any]],
    metric: str,
    condition_key: str = "condition",
) -> dict[str, list[float]]:
    """Extract a continuous metric per condition from per-sample rows."""
    grouped: dict[str, list[float]] = defaultdict(list)
    for row in rows:
        cond = str(row.get(condition_key, "unknown"))
        val = row.get(metric)
        if val is not None:
            try:
                grouped[cond].append(float(val))
            except (ValueError, TypeError):
                pass
    return dict(grouped)


def paired_bootstrap_ci_continuous(
    rows: list[dict[str, Any]],
    baseline: str,
    treatment: str,
    metric: str,
    n_bootstrap: int = 10000,
    seed: int = 42,
    condition_key: str = "condition",
) -> dict[str, Any]:
    """Paired bootstrap CI for a continuous metric difference (treatment - baseline)."""
    by_sample: dict[str, dict[str, Any]] = {}
    sample_id_key = _sample_id_key(rows)
    for row in rows:
        sid = str(row.get(sample_id_key, row.get("index", "")))
        cond = str(row.get(condition_key, ""))
        by_sample.setdefault(sid, {})[cond] = row

    diffs: list[float] = []
    for sid, conds in by_sample.items():
        b_val = conds.get(baseline, {}).get(metric)
        t_val = conds.get(treatment, {}).get(metric)
        if b_val is None or t_val is None:
            continue
        try:
            diffs.append(float(t_val) - float(b_val))
        except (ValueError, TypeError):
            continue

    if not diffs:
        return {"n_pairs": 0, "mean_delta": None, "ci_low": None, "ci_high": None}

    rng = random.Random(seed)
    n = len(diffs)
    mean_delta = sum(diffs) / n
    boot_means: list[float] = []
    for _ in range(n_bootstrap):
        sample = [diffs[rng.randint(0, n - 1)] for _ in range(n)]
        boot_means.append(sum(sample) / n)
    boot_means.sort()
    return {
        "n_pairs": n,
        "mean_delta": mean_delta,
        "ci_low": boot_means[int(0.025 * n_bootstrap)],
        "ci_high": boot_means[int(0.975 * n_bootstrap)],
        "method": "paired_bootstrap_percentile_continuous",
        "n_bootstrap": n_bootstrap,
    }
