from __future__ import annotations

import sys
import unittest
from pathlib import Path


sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from common.codebleu import compute_codebleu


class InvalidPythonCodeBleuTest(unittest.TestCase):
    def test_indentation_error_is_scored_instead_of_aborting_batch(self) -> None:
        reference = "class Example:\n    def value(self):\n        return 1\n"
        candidate = "class Example:\n    def value(self):\n        return 1\n  return 2\n"

        result = compute_codebleu(reference, candidate)

        self.assertEqual(result["syntax_match"], 0.0)
        self.assertEqual(result["dataflow_match"], 0.0)
        self.assertGreaterEqual(result["score"], 0.0)
        self.assertLessEqual(result["score"], 1.0)


if __name__ == "__main__":
    unittest.main()
