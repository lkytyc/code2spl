import importlib.util
import json
import re
import tempfile
import unittest
from pathlib import Path

import yaml


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
HISTORICAL_ARTIFACTS = (
    ROOT
    / "artifacts"
    / "smoke_runs"
    / "smoke_20260618_054329"
    / "smoke_swebench_verified_agentless"
)
HISTORICAL_RUN = (
    ROOT
    / "runs"
    / "smoke_runs"
    / "smoke_20260618_054329_rerun_20260704_231705"
)


def load_run_module():
    spec = importlib.util.spec_from_file_location("exp6_miniswe_run", HERE / "run.py")
    if spec is None or spec.loader is None:
        raise RuntimeError("Cannot load Experiment 6 run.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


run = load_run_module()


def historical_config() -> dict:
    config_path = next((HISTORICAL_RUN / "configs").glob("config.exp6_idx*.json"))
    config = json.loads(config_path.read_text(encoding="utf-8"))
    config["mini_spl_protocol"] = run.LEGACY_SPL_PROTOCOL
    return config


def card_identities(text: str) -> list[tuple[str, str, str]]:
    return re.findall(
        r"^### SPL Controller Card \d+\nRole: (.*?)\nFile: (.*?)\nFunction: (.*?)$",
        text,
        re.MULTILINE,
    )


class OriginalExp6CompatibilityTests(unittest.TestCase):
    def test_missing_protocol_reproduces_original_workflow(self):
        self.assertEqual(run.spl_protocol({}), run.LEGACY_SPL_PROTOCOL)

    def test_original_patch_plan_matches_successful_run_exactly(self):
        instance_id = "astropy__astropy-13236"
        mode = "miniswe_spl_both"
        generated = run.build_payload_files(
            HISTORICAL_ARTIFACTS / instance_id,
            mode,
            historical_config(),
        )["/tmp/spl_tools/patch_plan.md"]
        saved = (
            HISTORICAL_RUN
            / "smoke_swebench_miniswe"
            / instance_id
            / mode
            / "payload_tools"
            / "patch_plan.md"
        ).read_text(encoding="utf-8")
        self.assertEqual(generated, saved)

    def test_all_saved_controller_card_identities_are_preserved(self):
        config = historical_config()
        output_root = HISTORICAL_RUN / "smoke_swebench_miniswe"
        comparisons = 0
        for instance_dir in sorted(output_root.iterdir()):
            sample_dir = HISTORICAL_ARTIFACTS / instance_dir.name
            if not instance_dir.is_dir() or not sample_dir.exists():
                continue
            for mode in (
                "miniswe_spl_localization",
                "miniswe_spl_repair",
                "miniswe_spl_both",
            ):
                saved_path = instance_dir / mode / "payload_tools" / "source_bound_cards.md"
                if not saved_path.exists():
                    continue
                generated = run.build_payload_files(sample_dir, mode, config)[
                    "/tmp/spl_tools/source_bound_cards.md"
                ]
                saved = saved_path.read_text(encoding="utf-8")
                self.assertEqual(card_identities(generated), card_identities(saved))
                comparisons += 1
        self.assertEqual(comparisons, 36)

    def test_frozen_prompt_addenda_are_exact_historical_substrings(self):
        expected = {
            "miniswe_spl_localization": "## SPL Localization Workflow",
            "miniswe_spl_repair": "## SPL Repair Workflow",
            "miniswe_spl_both": "## SPL Localization + Repair Workflow",
        }
        for mode, heading in expected.items():
            addendum = run.load_prompt_addendum(mode)
            self.assertTrue(addendum.startswith(heading))
            self.assertNotIn("role-conditioned", addendum.lower())
            self.assertNotIn("role-combination", addendum.lower())
            saved_config_path = next(
                (HISTORICAL_RUN / "smoke_swebench_miniswe").glob(f"*/{mode}/mini_config.yaml")
            )
            saved_config = yaml.safe_load(saved_config_path.read_text(encoding="utf-8"))
            self.assertIn(addendum, saved_config["agent"]["instance_template"])

    def test_main_config_locks_successful_case_limits(self):
        config = json.loads((HERE / "config.smoke.json").read_text(encoding="utf-8"))
        expected = {
            "model": "deepseek-v4-pro",
            "spl_model": "deepseek-v4-pro",
            "summary_model": "deepseek-v4-pro",
            "mini_step_limit": 36,
            "mini_wall_time_limit_seconds": 1200,
            "mini_command_timeout_seconds": 2400,
            "mini_spl_protocol": run.LEGACY_SPL_PROTOCOL,
            "mini_spl_controller_cards": 4,
            "mini_spl_controller_spl_chars": 750,
            "mini_spl_prompt_cards": 2,
            "mini_source_bound_source_chars": 1400,
            "mini_spl_both_controller_cards": 3,
            "mini_spl_both_controller_spl_chars": 600,
            "mini_spl_both_prompt_cards": 1,
            "mini_spl_both_source_bound_source_chars": 1200,
        }
        for key, value in expected.items():
            self.assertEqual(config.get(key), value, key)

    def test_resume_rejects_output_from_another_protocol(self):
        with tempfile.TemporaryDirectory(dir=HERE) as temporary:
            out_dir = Path(temporary)
            (out_dir / "baseline_status.json").write_text(
                json.dumps({"mode": "miniswe_spl_both"}),
                encoding="utf-8",
            )
            (out_dir / "call_metadata.json").write_text("{}", encoding="utf-8")
            (out_dir / "patch.diff").write_text("", encoding="utf-8")
            (out_dir / "condition_complete.json").write_text(
                json.dumps(
                    {
                        "complete": True,
                        "mode": "miniswe_spl_both",
                        "spl_protocol": "other_protocol",
                    }
                ),
                encoding="utf-8",
            )
            self.assertFalse(
                run.condition_output_complete(
                    out_dir,
                    "miniswe_spl_both",
                    run.LEGACY_SPL_PROTOCOL,
                )
            )


if __name__ == "__main__":
    unittest.main()
