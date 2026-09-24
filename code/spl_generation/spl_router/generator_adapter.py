from __future__ import annotations

import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from spl_core.symbols import SourceSymbol


@dataclass
class GeneratedSPL:
    text: str
    metadata: dict[str, Any]


class ExistingSPLGeneratorAdapter:
    """Thin wrapper around the project's existing SPL generator.

    The adapter intentionally receives only a single function/method body plus
    deterministic static metadata. Task text and SWE-bench issue text must not
    be passed into this layer.
    """

    def __init__(self, config: dict[str, Any] | None = None):
        self.config = config or {}
        self._generator = None

    def _load_generator(self):
        if self._generator is not None:
            return self._generator
        project_root = Path(__file__).resolve().parents[2]
        experiments_root = project_root / "code"
        if str(experiments_root) not in sys.path:
            sys.path.insert(0, str(experiments_root))
        from common.spl_adapter import SPLConfig, SPLGenerator

        cfg = SPLConfig(
            mode=str(self.config.get("spl_mode", self.config.get("mode", "mock"))),
            model=str(self.config.get("spl_model", self.config.get("model", "mock"))),
            max_output_tokens=int(self.config.get("spl_max_output_tokens", self.config.get("max_output_tokens", 2048))),
            api_key=self.config.get("api_key"),
            api_key_env=str(self.config.get("api_key_env", "OPENAI_API_KEY")),
            base_url=self.config.get("base_url"),
            raw_http=bool(self.config.get("raw_http", False)),
            timeout_seconds=int(self.config.get("timeout_seconds", self.config.get("spl_timeout_seconds", 600))),
            max_retries=int(self.config.get("max_retries", self.config.get("spl_max_retries", 3))),
            api_keys=self.config.get("api_keys"),
            max_per_key=int(self.config.get("max_per_key", 1)),
            api_key_pool_file=self.config.get("api_key_pool_file"),
        )
        self._generator = SPLGenerator(cfg)
        return self._generator

    def generate(self, symbol: SourceSymbol) -> GeneratedSPL:
        generator = self._load_generator()
        stem = _safe_stem(symbol.symbol_id)
        result, spl_by_method = generator.generate_for_code_with_metrics_and_map(
            symbol.code,
            symbol.language,
            stem,
        )
        short_name = symbol.symbol.split(".")[-1]
        text = (
            spl_by_method.get(symbol.symbol)
            or spl_by_method.get(short_name)
            or result.text
        )
        metadata = dict(result.metadata)
        metadata.update({
            "generator_adapter": "common.spl_adapter.SPLGenerator",
            "generator_input_scope": "single_function_static_context",
            "issue_text_visible_to_generator": False,
            "symbol_id": symbol.symbol_id,
            "source_hash": symbol.content_hash,
        })
        return GeneratedSPL(text=text, metadata=metadata)


def _safe_stem(value: str) -> str:
    safe = "".join(ch if ch.isalnum() else "_" for ch in value)
    return safe[:120] or "spl_symbol"
