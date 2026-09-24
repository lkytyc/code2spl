from __future__ import annotations

import os
import gzip
import hashlib
import json
import shutil
import threading
import time
import urllib.error
import urllib.request
import uuid
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any

try:
    from . import env as _env
except ImportError:  # imported as a top-level module via a script's sys.path
    import env as _env

# Reading `.env` here means every entry point that can reach a model has picked
# up the package settings before the first request, without each of them having
# to remember to do it.  A shell variable already set takes precedence.
_env.load_env()


def base_url_from_env() -> str | None:
    """The endpoint a run should use when its config does not name one.

    ``SPL_BASE_URL`` is the package-wide override; ``OPENAI_BASE_URL`` is the
    conventional name an OpenAI-compatible toolchain already sets.  Neither is
    consulted when the config carries its own ``base_url``.
    """
    return _env.get("SPL_BASE_URL") or _env.get("OPENAI_BASE_URL")


def keys_from_env(role: str | None = None) -> list[str]:
    """Keys available from the environment, in order of specificity.

    ``role`` names the stage — ``"builder"`` for the run that produces SPL,
    ``"task"`` for the run that consumes it — and its variables are tried
    first.  A stage that has no key of its own falls back to the shared pool,
    so a single ``OPENAI_API_KEY`` is enough to run everything.
    """
    names = []
    if role:
        names += [f"SPL_{role.upper()}_API_KEY", f"SPL_{role.upper()}_API_KEYS"]
    names += ["SPL_API_KEY", "OPENAI_API_KEY", "OPENAI_API_KEYS"]
    keys: list[str] = []
    for name in names:
        for key in _env.get_list(name):
            if key not in keys:
                keys.append(key)
    return keys


def completion_token_budget(
    model: str | None,
    base_url: str | None,
    max_output_tokens: int,
    thinking: str | None,
) -> int:
    """Include reasoning headroom only when DeepSeek thinking is active."""
    is_deepseek = "deepseek" in (model or "").lower() or "deepseek" in (base_url or "").lower()
    multiplier = 4.0 if is_deepseek and thinking != "disabled" else 1.0
    return max(1, int(max_output_tokens * multiplier))


# ── API Key Pool ─────────────────────────────────────────────────────────
class ApiKeyPool:
    """Thread-safe pool of API keys with per-key concurrency limits.

    Usage::

        pool = ApiKeyPool(["sk-aaa", "sk-bbb", "sk-ccc"], max_per_key=3)
        key = pool.acquire()   # blocks until a key is available
        try:
            ...  # make API call with ``key``
        finally:
            pool.release(key)
    """

    def __init__(self, keys: list[str], max_per_key: int = 5):
        if not keys:
            raise ValueError("ApiKeyPool requires at least one API key")
        self._keys = list(keys)
        self._max_per_key = max_per_key
        self._semaphores = {k: threading.BoundedSemaphore(max_per_key) for k in keys}
        self._lock = threading.Lock()
        self._index = 0

    def acquire(self) -> str:
        while True:
            with self._lock:
                for _ in range(len(self._keys)):
                    key = self._keys[self._index]
                    self._index = (self._index + 1) % len(self._keys)
                    sem = self._semaphores[key]
                    if sem.acquire(blocking=False):
                        return key
            time.sleep(0.05)

    def release(self, key: str) -> None:
        sem = self._semaphores.get(key)
        if sem is not None:
            sem.release()


# ── Configuration ────────────────────────────────────────────────────────
class FileApiKeyLeasePool:
    """Cross-process API key lease pool backed by atomic lock directories."""

    def __init__(self, pool_file: str | os.PathLike[str]):
        self.pool_file = Path(pool_file)
        data = json.loads(self.pool_file.read_text(encoding="utf-8"))
        self._keys = [str(key).strip() for key in data.get("keys", []) if str(key).strip()]
        if not self._keys:
            raise ValueError(f"API key pool file has no keys: {self.pool_file}")
        self._max_per_key = max(1, int(data.get("max_per_key", 1)))
        self._lease_dir = Path(data.get("lease_dir") or (self.pool_file.parent / "key_leases"))
        self._lease_dir.mkdir(parents=True, exist_ok=True)
        self._poll_interval = max(0.05, float(data.get("poll_interval_seconds", 0.1)))
        self._stale_after_seconds = max(60.0, float(data.get("stale_after_seconds", 7200)))
        self._run_id = str(data.get("run_id", "unknown"))
        self._event_log = Path(data["event_log"]) if data.get("event_log") else None
        self._local = threading.local()
        self._lock = threading.Lock()
        self._cursor = (os.getpid() + threading.get_ident()) % (len(self._keys) * self._max_per_key)

    def acquire(self) -> str:
        slots = [(key_index, slot_index) for key_index in range(len(self._keys)) for slot_index in range(self._max_per_key)]
        while True:
            with self._lock:
                for offset in range(len(slots)):
                    index = (self._cursor + offset) % len(slots)
                    key_index, slot_index = slots[index]
                    lease_path = self._lease_dir / f"key_{key_index:03d}_slot_{slot_index:03d}.lease"
                    self._clear_stale_lease(lease_path)
                    try:
                        lease_path.mkdir()
                    except FileExistsError:
                        continue
                    except OSError:
                        continue
                    key = self._keys[key_index]
                    owner = {
                        "lease_id": uuid.uuid4().hex,
                        "pid": os.getpid(),
                        "thread": threading.get_ident(),
                        "run_id": self._run_id,
                        "key_id": self._key_id(key),
                        "key_index": key_index,
                        "slot_index": slot_index,
                        "acquired_at": time.time(),
                    }
                    try:
                        (lease_path / "owner.json").write_text(json.dumps(owner, ensure_ascii=False), encoding="utf-8")
                    except OSError:
                        pass
                    self._cursor = (index + 1) % len(slots)
                    self._held_leases().append({"key": key, "path": lease_path, "owner": owner})
                    self._write_event("acquire", owner)
                    return key
            time.sleep(self._poll_interval)

    def release(self, key: str) -> None:
        leases = self._held_leases()
        for index in range(len(leases) - 1, -1, -1):
            lease = leases[index]
            if lease["key"] != key:
                continue
            leases.pop(index)
            self._write_event("release", lease["owner"])
            self._remove_lease_dir(lease["path"])
            return

    def _held_leases(self) -> list[dict[str, Any]]:
        if not hasattr(self._local, "leases"):
            self._local.leases = []
        return self._local.leases

    def _clear_stale_lease(self, lease_path: Path) -> None:
        owner_path = lease_path / "owner.json"
        if not owner_path.exists():
            try:
                age = time.time() - lease_path.stat().st_mtime
            except OSError:
                return
            if age > self._stale_after_seconds:
                self._remove_lease_dir(lease_path)
            return
        try:
            owner = json.loads(owner_path.read_text(encoding="utf-8"))
            acquired_at = float(owner.get("acquired_at", 0))
        except Exception:
            acquired_at = 0
            owner = {}
        owner_pid = int(owner.get("pid", 0) or 0)
        if owner_pid and not self._pid_is_alive(owner_pid):
            self._remove_lease_dir(lease_path)
            return
        if time.time() - acquired_at > self._stale_after_seconds:
            self._remove_lease_dir(lease_path)

    @staticmethod
    def _pid_is_alive(pid: int) -> bool:
        if pid <= 0:
            return False
        try:
            os.kill(pid, 0)
        except ProcessLookupError:
            return False
        except PermissionError:
            return True
        except OSError:
            return False
        return True

    def _remove_lease_dir(self, lease_path: Path) -> None:
        for _attempt in range(10):
            shutil.rmtree(lease_path, ignore_errors=True)
            if not lease_path.exists():
                return
            time.sleep(0.02)

    def _write_event(self, event: str, owner: dict[str, Any]) -> None:
        if self._event_log is None:
            return
        row = {
            "event": event,
            "time": time.time(),
            "run_id": self._run_id,
            "pid": owner.get("pid"),
            "thread": owner.get("thread"),
            "key_id": owner.get("key_id"),
            "key_index": owner.get("key_index"),
            "slot_index": owner.get("slot_index"),
            "lease_id": owner.get("lease_id"),
        }
        try:
            self._event_log.parent.mkdir(parents=True, exist_ok=True)
            with self._event_log.open("a", encoding="utf-8") as fh:
                fh.write(json.dumps(row, ensure_ascii=False) + "\n")
        except OSError:
            pass

    def _key_id(self, key: str) -> str:
        return hashlib.sha256(key.encode("utf-8")).hexdigest()[:12]


@dataclass
class GenerationConfig:
    provider: str = "openai"
    model: str = "gpt-4o-2024-11-20"
    temperature: float = 0.0
    max_output_tokens: int = 4096
    api_key: str | None = None
    api_key_env: str = "OPENAI_API_KEY"
    base_url: str | None = None
    max_retries: int = 3
    retry_backoff_seconds: float = 2.0
    raw_http: bool = False
    timeout_seconds: int = 600
    # DeepSeek V4 defaults to thinking mode. Keep None for provider defaults;
    # structured-output experiments may opt into "disabled" explicitly.
    thinking: str | None = None
    # OpenAI-style reasoning effort (low/medium/high) for models such as gpt-5.x
    # that reject DeepSeek's ``thinking`` parameter. None leaves it unset.
    reasoning_effort: str | None = None
    # Optional key pool for dynamic key distribution across concurrent workers.
    api_keys: list[str] = field(default_factory=list)
    max_per_key: int = 5
    api_key_pool_file: str | None = None
    # Which stage this configuration drives: "builder" for the run that produces
    # SPL, "task" for the run that consumes it.  It selects which stage-specific
    # environment variables are consulted, and is empty when the config already
    # names its own keys.
    stage: str | None = None

    def resolve_key(self, key_pool: ApiKeyPool | FileApiKeyLeasePool | None = None) -> str:
        """Return the API key to use, preferring the pool if available."""
        if key_pool is not None:
            return key_pool.acquire()
        return self._keys_from_settings()[0]

    def _keys_from_settings(self) -> list[str]:
        """Every key this configuration can reach, config first, then env."""
        keys: list[str] = []
        if self.api_key:
            keys.append(self.api_key)
        for key in self.api_keys:
            if key and key not in keys:
                keys.append(key)
        for key in keys_from_env(self.stage):
            if key not in keys:
                keys.append(key)
        env_named = os.environ.get(self.api_key_env, "")
        if env_named and env_named not in keys:
            keys.append(env_named)
        return keys

    def get_key_pool(self) -> ApiKeyPool | FileApiKeyLeasePool | None:
        """Build a key pool when more than one key is available.

        A config may point at a key-pool file, but the pool directory is not
        shipped — it holds live credentials.  When the file is absent the
        configuration falls back to the keys in the environment instead of
        refusing to start, so a reader who supplies one key in ``.env`` can run
        the same config the paper's runs used.
        """
        if self.api_key_pool_file:
            pool_path = Path(_env.expand(self.api_key_pool_file))
            if pool_path.is_file():
                return FileApiKeyLeasePool(pool_path)
        keys = self._keys_from_settings()
        if len(keys) <= 1:
            return None
        return ApiKeyPool(keys, max_per_key=self.max_per_key)


# ── Result ───────────────────────────────────────────────────────────────
@dataclass
class GenerationResult:
    text: str
    provider: str
    model: str
    elapsed_seconds: float
    input_tokens: int | None = None
    output_tokens: int | None = None
    reasoning_tokens: int | None = None
    total_tokens: int | None = None
    raw_usage: dict[str, Any] | None = None

    def to_metadata(self) -> dict[str, Any]:
        data = asdict(self) | {"text": None}
        data["llm_elapsed_seconds"] = self.elapsed_seconds
        return data


# ── Client ───────────────────────────────────────────────────────────────
class ModelClient:
    def __init__(self, config: GenerationConfig):
        self.config = config
        self._key_pool = config.get_key_pool()

    def generate(self, prompt: str) -> str:
        return self.generate_with_metrics(prompt).text

    def generate_with_metrics(self, prompt: str) -> GenerationResult:
        provider = self.config.provider.lower()
        started = time.perf_counter()
        if provider == "mock":
            text = self._mock_response(prompt)
            return GenerationResult(
                text=text,
                provider=provider,
                model=self.config.model,
                elapsed_seconds=time.perf_counter() - started,
                input_tokens=self._rough_token_count(prompt),
                output_tokens=self._rough_token_count(text),
                reasoning_tokens=0,
                total_tokens=self._rough_token_count(prompt) + self._rough_token_count(text),
                raw_usage={"source": "rough_count_for_mock_provider"},
            )
        if provider == "openai":
            key = self._acquire_key()
            try:
                text, usage = self._openai_response(prompt, key)
            finally:
                self._release_key(key)
            elapsed = time.perf_counter() - started
            parsed_usage = self._parse_openai_usage(usage)
            return GenerationResult(
                text=text,
                provider=provider,
                model=self.config.model,
                elapsed_seconds=elapsed,
                **parsed_usage,
            )
        raise ValueError(
            f"Unsupported provider: {self.config.provider}. "
            "Only 'openai' and local smoke-test 'mock' are supported."
        )

    def _acquire_key(self) -> str:
        if self._key_pool is not None:
            return self._key_pool.acquire()
        keys = self.config._keys_from_settings()
        if not keys:
            raise RuntimeError(
                "OpenAI API key missing. Set OPENAI_API_KEY (or SPL_API_KEY) in "
                f"the environment or in .env, or set {self.config.api_key_env} / "
                "api_key / api_keys in the config."
            )
        return keys[0]

    def _release_key(self, key: str) -> None:
        if self._key_pool is not None:
            self._key_pool.release(key)

    def _mock_response(self, prompt: str) -> str:
        return "# MOCK_OUTPUT\n" + prompt[:500]

    def _openai_response(self, prompt: str, api_key: str) -> tuple[str, Any]:
        if self.config.raw_http:
            return self._openai_raw_http_response(prompt, api_key)

        try:
            from openai import OpenAI
        except ImportError as exc:
            raise RuntimeError("Install openai to use provider=openai") from exc

        import httpx

        client_kwargs = {"api_key": api_key}
        base_url = self._base_url()
        if base_url:
            client_kwargs["base_url"] = base_url
        timeout_seconds = int(self.config.timeout_seconds) if self.config.timeout_seconds else 600
        client_kwargs["timeout"] = httpx.Timeout(
            timeout_seconds, connect=min(10.0, timeout_seconds * 0.1)
        )
        client = OpenAI(**client_kwargs)
        _is_deepseek = ("deepseek" in (self.config.model or "").lower()
                        or "deepseek" in (base_url or "").lower())
        last_error: Exception | None = None
        for attempt in range(max(1, int(self.config.max_retries))):
            try:
                if not _is_deepseek:
                    try:
                        response = client.responses.create(
                            model=self.config.model,
                            input=prompt,
                            temperature=self.config.temperature,
                            max_output_tokens=self.config.max_output_tokens,
                        )
                        text = getattr(response, "output_text", None) or ""
                        return text, getattr(response, "usage", None)
                    except Exception:
                        pass  # fall through to chat.completions
                chat_kwargs: dict[str, Any] = {
                    "model": self.config.model,
                    "messages": [{"role": "user", "content": prompt}],
                    "temperature": self.config.temperature,
                    "max_tokens": completion_token_budget(
                        self.config.model,
                        self.config.base_url,
                        self.config.max_output_tokens,
                        self.config.thinking,
                    ),
                }
                if _is_deepseek and self.config.thinking in {"enabled", "disabled"}:
                    chat_kwargs["extra_body"] = {
                        "thinking": {"type": self.config.thinking},
                    }
                if self.config.reasoning_effort:
                    chat_kwargs["reasoning_effort"] = self.config.reasoning_effort
                response = client.chat.completions.create(**chat_kwargs)
                text = response.choices[0].message.content or ""
                return text, getattr(response, "usage", None)
            except Exception as exc:
                last_error = exc
                if attempt + 1 >= max(1, int(self.config.max_retries)):
                    break
                time.sleep(float(self.config.retry_backoff_seconds) * (2**attempt))
        raise RuntimeError(
            f"OpenAI request failed after {self.config.max_retries} attempts: {last_error}"
        ) from last_error

    def _base_url(self) -> str | None:
        """The endpoint for this configuration.

        The config's own ``base_url`` wins; otherwise the package-wide override
        from ``.env``.  Returning ``None`` lets the OpenAI client use its
        default, which is what a config that names no endpoint expects.
        """
        configured = _env.expand(self.config.base_url) if self.config.base_url else None
        return str(configured) if configured else base_url_from_env()

    def _openai_raw_http_response(self, prompt: str, api_key: str) -> tuple[str, Any]:
        base_url = (self._base_url() or "https://api.openai.com/v1").rstrip("/")
        url = f"{base_url}/chat/completions"
        payload = {
            "model": self.config.model,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": self.config.temperature,
            "max_tokens": self.config.max_output_tokens,
        }
        if self.config.thinking in {"enabled", "disabled"}:
            payload["thinking"] = {"type": self.config.thinking}
        if self.config.reasoning_effort:
            payload["reasoning_effort"] = self.config.reasoning_effort
        body = json.dumps(payload).encode("utf-8")
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "Accept-Encoding": "gzip, identity",
        }
        last_error: Exception | None = None
        for attempt in range(max(1, int(self.config.max_retries))):
            request = urllib.request.Request(url, data=body, headers=headers, method="POST")
            try:
                with urllib.request.urlopen(request, timeout=int(self.config.timeout_seconds)) as response:
                    raw_body = response.read()
                    if (response.headers.get("Content-Encoding", "").lower() == "gzip"
                            or raw_body.startswith(b"\x1f\x8b")):
                        raw_body = gzip.decompress(raw_body)
                    data = json.loads(raw_body.decode("utf-8", errors="replace"))
                choices = data.get("choices") or []
                text = ""
                if choices:
                    message = choices[0].get("message") or {}
                    text = message.get("content") or choices[0].get("text") or ""
                return text, data.get("usage")
            except urllib.error.HTTPError as exc:
                raw = exc.read().decode("utf-8", errors="replace")[:2000]
                last_error = RuntimeError(f"HTTP {exc.code}: {raw}")
            except Exception as exc:
                last_error = exc
            if attempt + 1 < max(1, int(self.config.max_retries)):
                time.sleep(float(self.config.retry_backoff_seconds) * (2**attempt))
        raise RuntimeError(
            f"OpenAI raw HTTP request failed after {self.config.max_retries} attempts: {last_error}"
        ) from last_error

    def _parse_openai_usage(self, usage: Any) -> dict[str, Any]:
        data = self._to_plain_dict(usage) if usage is not None else {}
        output_details = data.get("output_tokens_details") or data.get("completion_tokens_details") or {}
        reasoning_tokens = output_details.get("reasoning_tokens")
        input_tokens = data.get("input_tokens")
        if input_tokens is None:
            input_tokens = data.get("prompt_tokens")
        output_tokens = data.get("output_tokens")
        if output_tokens is None:
            output_tokens = data.get("completion_tokens")
        total_tokens = data.get("total_tokens")
        if total_tokens is None and input_tokens is not None and output_tokens is not None:
            total_tokens = input_tokens + output_tokens
        return {
            "input_tokens": input_tokens,
            "output_tokens": output_tokens,
            "reasoning_tokens": reasoning_tokens,
            "total_tokens": total_tokens,
            "raw_usage": data,
        }

    def _to_plain_dict(self, obj: Any) -> dict[str, Any]:
        if obj is None:
            return {}
        if isinstance(obj, dict):
            return obj
        if hasattr(obj, "model_dump"):
            return obj.model_dump()
        if hasattr(obj, "dict"):
            return obj.dict()
        return {
            key: getattr(obj, key)
            for key in dir(obj)
            if not key.startswith("_") and not callable(getattr(obj, key))
        }

    def _rough_token_count(self, text: str) -> int:
        return max(1, len(text) // 4) if text else 0
