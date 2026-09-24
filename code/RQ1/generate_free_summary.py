from __future__ import annotations

import argparse
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from common.paths import read_config, read_json, resolve_in_project, write_json, write_text
from common.providers import GenerationConfig, ModelClient
from common.run_utils import generation_kwargs, run_ordered, selected_items
from common.token_utils import summary_control_metrics, token_count
from common.usage import generation_metadata


FREE_SUMMARY_PROTOCOL = "free_summary"


FREE_SUMMARY_PROMPT = """Summarize what the code does in ordinary natural language.

Rules:
- Describe behavior, inputs, outputs, and important method/class interactions.
- Do not copy large code spans.
- Do not infer requirements that are not present in the code.
- Do not write replacement code.
- Output only the summary text.

CODE:
{code}
"""

FREE_SUMMARY_PROMPT_SHA256 = hashlib.sha256(FREE_SUMMARY_PROMPT.encode("utf-8")).hexdigest()


STRUCTURED_SUMMARY_PROMPT = """You are generating an information-controlled structured natural-language baseline.

Task: describe the class with enough detail to reconstruct method behavior and method/field dependencies, but do not use SPL tags or SPL syntax.

Rules:
- Use ordinary natural language with stable section headings.
- Cover constructor behavior, fields, public methods, inputs, outputs, side effects, branches, exceptions, and inter-method calls when present.
- Do not copy large code spans.
- Do not invent behavior not supported by the code.
- Output only the structured description.

CODE:
{code}
"""


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", required=True)
    args = parser.parse_args()

    config = read_config(resolve_in_project(args.config))
    artifact_dir = resolve_in_project(config["artifact_dir"])
    manifest = read_json(artifact_dir / "manifest.json")
    summary_config = dict(config)
    summary_config["provider"] = config.get("summary_provider", config.get("provider", "openai"))
    summary_config["summary_temperature"] = 0
    client = ModelClient(
        GenerationConfig(
            **generation_kwargs(
                summary_config,
                model_key="summary_model",
                max_tokens_key="summary_max_output_tokens",
            )
        )
    )
    metadata = {
        "protocol": FREE_SUMMARY_PROTOCOL,
        "prompt_sha256": FREE_SUMMARY_PROMPT_SHA256,
        "provider": config.get("summary_provider", "openai"),
        "model": config.get("summary_model", "gpt-4o-mini-2024-07-18"),
        "temperature": 0,
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
    }

    selected = selected_items(manifest, config)

    def work(item: dict) -> str:
        sample_dir = resolve_in_project(item["sample_dir"])
        code = (sample_dir / "raw_code.py").read_text(encoding="utf-8")
        spl = (sample_dir / "spl.txt").read_text(encoding="utf-8") if (sample_dir / "spl.txt").exists() else ""
        prompt = FREE_SUMMARY_PROMPT.format(code=code)
        result = client.generate_with_metrics(prompt)
        summary = (result.text or "").strip()
        structured_prompt = STRUCTURED_SUMMARY_PROMPT.format(code=code)
        structured_result = client.generate_with_metrics(structured_prompt)
        structured_summary = (structured_result.text or "").strip()
        write_text(sample_dir / "free_summary_prompt.txt", prompt)
        write_text(sample_dir / "free_summary.txt", summary + "\n")
        write_json(sample_dir / "free_summary_metadata.json", metadata | generation_metadata(result, role="free_summary_generation", condition="free_summary"))
        write_text(sample_dir / "structured_summary_prompt.txt", structured_prompt)
        write_text(sample_dir / "structured_summary.txt", structured_summary + "\n")
        write_json(sample_dir / "structured_summary_metadata.json", metadata | generation_metadata(structured_result, role="structured_summary_generation", condition="structured_summary"))
        write_json(sample_dir / "summary_control_metrics.json", summary_control_metrics(code, spl, summary, structured_summary, "", config))
        # Mark summaries as generated so run.py can validate they are ready.
        pending = sample_dir / ".summary_pending.json"
        if pending.exists():
            pending.unlink()
        return item["task_id"]

    _results, errors = run_ordered(selected, work, int(config.get("max_workers", 1)), bool(config.get("continue_on_error", True)))
    if errors:
        write_json(artifact_dir / "free_summary_errors.json", errors)
    print(f"Generated OpenAI summaries for {len(selected)} ClassEval samples")


if __name__ == "__main__":
    main()
