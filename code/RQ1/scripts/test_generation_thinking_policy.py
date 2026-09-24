from __future__ import annotations

import sys
import unittest
from pathlib import Path


EXPERIMENTS_ROOT = Path(__file__).resolve().parents[2]
if str(EXPERIMENTS_ROOT) not in sys.path:
    sys.path.insert(0, str(EXPERIMENTS_ROOT))

from common.run_utils import generation_kwargs
from common.providers import completion_token_budget


class GenerationThinkingPolicyTest(unittest.TestCase):
    def test_stage_specific_policy_wins(self) -> None:
        config = {"thinking": "enabled", "generation_thinking": "disabled"}
        self.assertEqual(
            generation_kwargs(config, thinking_key="generation_thinking")["thinking"],
            "disabled",
        )

    def test_stage_specific_policy_falls_back_to_global(self) -> None:
        config = {"thinking": "enabled"}
        self.assertEqual(
            generation_kwargs(config, thinking_key="generation_thinking")["thinking"],
            "enabled",
        )

    def test_default_behavior_is_unchanged(self) -> None:
        self.assertIsNone(generation_kwargs({})["thinking"])

    def test_disabled_thinking_does_not_expand_deepseek_budget(self) -> None:
        self.assertEqual(
            completion_token_budget("deepseek-v4-flash", "https://api.deepseek.com", 4096, "disabled"),
            4096,
        )

    def test_enabled_thinking_keeps_reasoning_headroom(self) -> None:
        self.assertEqual(
            completion_token_budget("deepseek-v4-flash", "https://api.deepseek.com", 4096, "enabled"),
            16384,
        )


if __name__ == "__main__":
    unittest.main()
