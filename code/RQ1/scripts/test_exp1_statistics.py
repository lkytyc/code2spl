from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path


SCRIPT = Path(__file__).with_name("summarize_full100_models.py")
SPEC = importlib.util.spec_from_file_location("exp1_summary", SCRIPT)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class Exp1StatisticsTest(unittest.TestCase):
    def test_exact_mcnemar_is_symmetric(self) -> None:
        self.assertEqual(MODULE.exact_mcnemar_p(8, 5), MODULE.exact_mcnemar_p(5, 8))
        self.assertAlmostEqual(MODULE.exact_mcnemar_p(8, 5), 0.5810546875)
        self.assertEqual(MODULE.exact_mcnemar_p(0, 0), 1.0)

    def test_holm_adjust_preserves_order_and_monotonicity(self) -> None:
        adjusted = MODULE.holm_adjust([0.04, 0.01, 0.03, 0.2])
        self.assertEqual(adjusted, [0.09, 0.04, 0.09, 0.2])

    def test_incremental_condition_is_excluded(self) -> None:
        flattened = {condition for pair in MODULE.SIGNIFICANCE_COMPARISONS for condition in pair}
        self.assertNotIn("skeleton_incremental", flattened)
        self.assertNotIn("skeleton_incremental", MODULE.PAPER_CONDITIONS)
        self.assertEqual(len(MODULE.SIGNIFICANCE_COMPARISONS), 4)

    def test_paired_difference_uses_paired_denominator(self) -> None:
        self.assertAlmostEqual(100.0 * (69 - 42) / 92, 29.347826086956523)


if __name__ == "__main__":
    unittest.main()
