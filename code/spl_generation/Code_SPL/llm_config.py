from __future__ import annotations

import os
import time
from openai import OpenAI


def get_openai_config() -> tuple[str | None, str | None, str]:
    api_key = os.getenv("OPENAI_API_KEY") or os.getenv("CODE_SPL_API_KEY")
    base_url = os.getenv("OPENAI_BASE_URL") or os.getenv("CODE_SPL_BASE_URL") or "https://api.openai.com/v1"
    model = os.getenv("CODE_SPL_MODEL") or os.getenv("OPENAI_MODEL") or "gpt-4o"
    return api_key, base_url, model


def create_client() -> OpenAI | None:
    api_key, base_url, _model = get_openai_config()
    if not api_key:
        return None
    return OpenAI(api_key=api_key, base_url=base_url)


def require_client(client: OpenAI | None) -> OpenAI:
    if client is None:
        raise RuntimeError("OpenAI API key missing. Set OPENAI_API_KEY or CODE_SPL_API_KEY.")
    return client


def chat_completion_with_retry(client: OpenAI | None, *, model: str, messages: list[dict], temperature: float = 0.0, max_tokens: int = 20000, retries: int = 3) -> str:
    last_error: Exception | None = None
    real_client = require_client(client)
    for attempt in range(retries):
        try:
            response = real_client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens,
            )
            return response.choices[0].message.content.strip()
        except Exception as exc:
            last_error = exc
            if attempt + 1 >= retries:
                break
            time.sleep(2 ** attempt)
    raise RuntimeError(f"LLM call failed after {retries} attempts: {last_error}")
