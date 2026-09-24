import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path


HERE = Path(__file__).resolve().parent


def load_module(name: str, filename: str):
    spec = importlib.util.spec_from_file_location(name, HERE / filename)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot load {filename}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


planner = load_module("exp6_complex_planner", "plan_complex_batches.py")
runner = load_module("exp6_complex_runner", "run_complex_batches.py")


class ComplexPipelineTests(unittest.TestCase):
    def test_waves_keep_environment_groups_together_when_they_fit(self):
        records = [
            {"instance_id": "a__a-1", "repo": "a/a", "version": "1", "rank": 1},
            {"instance_id": "b__b-1", "repo": "b/b", "version": "1", "rank": 2},
            {"instance_id": "a__a-2", "repo": "a/a", "version": "1", "rank": 3},
        ]
        waves = planner.make_waves(records, 2)
        self.assertEqual(
            [[row["instance_id"] for row in wave] for wave in waves],
            [["a__a-1", "a__a-2"], ["b__b-1"]],
        )

    def test_stage_checkpoints_accept_completed_empty_patch_attempts(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            artifact_dir = root / "artifact"
            run_dir = root / "run"
            config_path = root / "config.json"
            conditions = ["original", "spl_both"]
            config = {
                "artifact_dir": str(artifact_dir),
                "run_dir": str(run_dir),
                "conditions": conditions,
            }
            config_path.write_text(json.dumps(config), encoding="utf-8")
            unit = {
                "unit_no": 1,
                "wave_no": 1,
                "unit_name": "unit_01",
                "instance_id": "a__a-1",
                "config_path": str(config_path),
            }

            self.assertFalse(runner.prepare_complete(unit, config))
            artifact_dir.mkdir()
            (artifact_dir / "manifest.json").write_text(
                json.dumps([{"instance_id": unit["instance_id"]}]), encoding="utf-8"
            )
            self.assertTrue(runner.prepare_complete(unit, config))

            instance_dir = run_dir / unit["instance_id"]
            for condition in conditions:
                out_dir = instance_dir / condition
                out_dir.mkdir(parents=True)
                (out_dir / "baseline_status.json").write_text(json.dumps({"mode": condition}), encoding="utf-8")
                (out_dir / "call_metadata.json").write_text("{}", encoding="utf-8")
                (out_dir / "patch.diff").write_text("", encoding="utf-8")
                (out_dir / "condition_complete.json").write_text(
                    json.dumps({"complete": True, "mode": condition}), encoding="utf-8"
                )
            self.assertTrue(runner.run_complete(unit, config))

            rows = [{"instance_id": unit["instance_id"], "condition": condition} for condition in conditions]
            (run_dir / "evaluation.json").write_text(json.dumps(rows), encoding="utf-8")
            self.assertTrue(runner.evaluate_complete(unit, config))

    def test_unit_selection_is_independent_of_wave_boundaries(self):
        plan = {"units": [{"unit_no": number} for number in range(1, 7)]}
        selected = runner.selected_units(plan, 2, 4)
        self.assertEqual([unit["unit_no"] for unit in selected], [2, 3, 4])

    def test_memory_gate_does_not_launch_a_command(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            sentinel = root / "started.txt"
            result = runner.run_cmd(
                [sys.executable, "-c", f"from pathlib import Path; Path({str(sentinel)!r}).write_text('started')"],
                root / "logs",
                "memory_gate",
                timeout=30,
                min_free_gb=None,
                min_available_memory_gb=999999.0,
                resource_wait_timeout=0,
                launch_stagger_seconds=0,
            )
            self.assertTrue(result["resource_wait_timeout"])
            self.assertFalse(sentinel.exists())

    def test_execution_input_hash_guard_detects_drift(self):
        with tempfile.TemporaryDirectory() as temporary:
            locked_file = Path(temporary) / "locked.txt"
            locked_file.write_text("original", encoding="utf-8")
            plan = {
                "execution_input_hashes": {
                    str(locked_file): runner.file_sha256(locked_file),
                }
            }
            self.assertEqual(runner.validate_locked_execution_inputs(plan), [])
            locked_file.write_text("changed", encoding="utf-8")
            failures = runner.validate_locked_execution_inputs(plan)
            self.assertEqual(len(failures), 1)
            self.assertEqual(failures[0]["reason"], "sha256_mismatch")


if __name__ == "__main__":
    unittest.main()
