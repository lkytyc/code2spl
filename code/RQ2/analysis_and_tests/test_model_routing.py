from __future__ import annotations

from pathlib import Path

from prepare import build_spl_config, load_prepared_input_candidates


def test_spl_transport_is_independent_from_inference_transport() -> None:
    config = {
        "model": "gpt-5.4",
        "base_url": "https://inference.example/v1",
        "api_key_pool_file": "inference-keys.json",
        "openai_raw_http": True,
        "max_per_key": 2,
        "max_retries": 3,
        "spl_model": "deepseek-v4-flash",
        "spl_base_url": "https://spl.example/v1",
        "spl_api_key_pool_file": "spl-keys.json",
        "spl_openai_raw_http": False,
        "spl_max_per_key": 1,
        "spl_max_retries": 5,
        "spl_thinking": "enabled",
    }

    routed = build_spl_config(config)

    assert routed.model == "deepseek-v4-flash"
    assert routed.base_url == "https://spl.example/v1"
    assert routed.api_key_pool_file == "spl-keys.json"
    assert routed.raw_http is False
    assert routed.max_per_key == 1
    assert routed.max_retries == 5
    assert routed.thinking == "enabled"


def test_spl_transport_keeps_backward_compatible_fallbacks() -> None:
    config = {
        "spl_model": "legacy-spl-model",
        "base_url": "https://shared.example/v1",
        "api_key_pool_file": "shared-keys.json",
        "openai_raw_http": True,
        "max_per_key": 3,
        "max_retries": 4,
    }

    routed = build_spl_config(config)

    assert routed.model == "legacy-spl-model"
    assert routed.base_url == "https://shared.example/v1"
    assert routed.api_key_pool_file == "shared-keys.json"
    assert routed.raw_http is True
    assert routed.max_per_key == 3
    assert routed.max_retries == 4


def test_frozen_input_loader_ignores_old_spl_and_restores_sample_identity(tmp_path: Path) -> None:
    task_id = "data_example__source"
    sample_dir = tmp_path / task_id
    sample_dir.mkdir()
    (sample_dir / "raw_code.txt").write_text("def f():\n    return 1\n", encoding="utf-8")
    (sample_dir / "official_prompt.txt").write_text("PROMPT", encoding="utf-8")
    (sample_dir / "question.txt").write_text("QUESTION", encoding="utf-8")
    (sample_dir / "gold.txt").write_text("GOLD", encoding="utf-8")
    (sample_dir / "item.json").write_text('{"task_id":"data_example"}', encoding="utf-8")
    (sample_dir / "spl.txt").write_text("OLD SPL MUST NOT BE READ", encoding="utf-8")
    (tmp_path / "manifest.json").write_text(
        '[{"task_id":"data_example__source","benchmark_task_id":"data_example",'
        '"sample_key":"data_example::source","mode":"source","task_type":"data",'
        '"language":"python","index":7}]',
        encoding="utf-8",
    )

    candidates = load_prepared_input_candidates(tmp_path)

    assert len(candidates) == 1
    assert candidates[0]["sample_key"] == "data_example::source"
    assert candidates[0]["frozen_question"] == "QUESTION"
    assert candidates[0]["frozen_gold"] == "GOLD"
    assert "spl" not in candidates[0]
