from __future__ import annotations

import json
import os
import sys
import time
import uuid
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .paths import ARTIFACTS_ROOT, CODE_SPL_ROOT, ensure_dir, ensure_under_project
from .providers import GenerationConfig, GenerationResult, ModelClient
from .usage import UsageTotals


if str(CODE_SPL_ROOT) not in sys.path:
    sys.path.insert(0, str(CODE_SPL_ROOT))

from language_support import analyze_specific_method_ast, detect_language, extract_source_members  # noqa: E402


@dataclass
class SPLConfig:
    mode: str = "openai"
    model: str = "gpt-4o-2024-11-20"
    max_output_tokens: int = 2048
    api_key: str | None = None
    api_key_env: str = "OPENAI_API_KEY"
    base_url: str | None = None
    raw_http: bool = False
    timeout_seconds: int = 600
    max_retries: int = 3
    api_keys: list[str] | None = None
    max_per_key: int = 1
    api_key_pool_file: str | None = None
    thinking: str | None = None
    temp_source_dir: Path = ARTIFACTS_ROOT / "tmp_sources"
    decompose_max_depth: int = 2
    decompose_size_threshold: int = 30


@dataclass
class SPLBuildResult:
    text: str
    metadata: dict[str, Any]


class SPLGenerator:
    def __init__(self, config: SPLConfig | None = None):
        self.config = config or SPLConfig()
        self._usage_totals = UsageTotals()
        self._call_metadata: list[dict[str, Any]] = []
        # Use a unique temp subdirectory per generator instance so that
        # concurrent experiments never clash on temp file writes.
        unique_tag = f"{os.getpid()}_{uuid.uuid4().hex[:8]}"
        self.config.temp_source_dir = self.config.temp_source_dir / unique_tag
        if self.config.mode == "mock":
            self.decomposer = None
            self.llm = None
            self.recursive = None
        elif self.config.mode == "openai":
            from method_analyzer import ASTDecomposer, LLMAnalyzer, RecursiveAnalyzer  # noqa: E402

            self.decomposer = ASTDecomposer()
            self.llm = LLMAnalyzer()
            self._client = ModelClient(
                GenerationConfig(
                    provider="openai",
                    model=self.config.model,
                    temperature=0.0,
                    max_output_tokens=self.config.max_output_tokens,
                    api_key=self.config.api_key,
                    api_key_env=self.config.api_key_env,
                    base_url=self.config.base_url,
                    raw_http=self.config.raw_http,
                    timeout_seconds=self.config.timeout_seconds,
                    max_retries=self.config.max_retries,
                    api_keys=list(self.config.api_keys or []),
                    max_per_key=int(self.config.max_per_key),
                    api_key_pool_file=self.config.api_key_pool_file,
                    thinking=self.config.thinking,
                )
            )
            self.llm._call_llm = self._openai_llm
            self.recursive = RecursiveAnalyzer(self.llm)
        else:
            raise ValueError(f"Unsupported SPL mode: {self.config.mode}")

    def generate_for_code(self, code: str, language: str, stem: str) -> str:
        return self.generate_for_code_with_metrics(code, language, stem).text

    def generate_for_code_with_metrics(self, code: str, language: str, stem: str) -> SPLBuildResult:
        result, _spl_by_method = self.generate_for_code_with_metrics_and_map(code, language, stem)
        return result

    def generate_for_code_with_metrics_and_map(
        self, code: str, language: str, stem: str
    ) -> tuple[SPLBuildResult, dict[str, str]]:
        suffix = {"python": ".py", "java": ".java", "cpp": ".cpp"}.get(language, ".txt")
        temp_dir = ensure_dir(self.config.temp_source_dir)
        temp_path = temp_dir / f"{stem}{suffix}"
        ensure_under_project(temp_path)
        temp_path.write_text(code, encoding="utf-8")
        return self.generate_for_file_with_metrics_and_map(temp_path)

    def generate_for_file(self, file_path: str | Path) -> str:
        return self.generate_for_file_with_metrics(file_path).text

    def generate_for_file_with_metrics(self, file_path: str | Path) -> SPLBuildResult:
        result, _spl_by_method = self.generate_for_file_with_metrics_and_map(file_path)
        return result

    def generate_for_file_with_metrics_and_map(
        self, file_path: str | Path
    ) -> tuple[SPLBuildResult, dict[str, str]]:
        """Generate SPL for all methods in a file and return (result, spl_by_method).

        *spl_by_method* maps ``ClassName.method_name`` (or ``method_name`` for
        global functions) to the cleaned SPL block text for that method.
        """
        self._reset_usage()
        started = time.perf_counter()
        path = ensure_under_project(file_path)
        language = detect_language(path)
        classes, global_methods = extract_source_members(path)
        parts: list[str] = []
        method_count = 0
        spl_by_method: dict[str, str] = {}

        for class_name, methods in classes.items():
            parts.append(f"# CLASS {class_name}")
            for method in methods:
                method_count += 1
                spl_block = self._generate_method_spl(method, language, class_name)
                key = f"{class_name}.{method['name']}"
                spl_by_method[key] = self._cleanup_spl_tags(spl_block)
                parts.append(spl_block)

        for method in global_methods:
            method_count += 1
            spl_block = self._generate_method_spl(method, language, None)
            spl_by_method[method["name"]] = self._cleanup_spl_tags(spl_block)
            parts.append(spl_block)

        text = "\n\n".join(part for part in parts if part.strip())
        text = self._cleanup_spl_tags(text)
        totals = self._usage_totals.to_dict()
        elapsed = time.perf_counter() - started
        metadata = {
            "role": "spl_build",
            "provider": self.config.mode,
            "model": self.config.model,
            "language": language,
            "method_count": method_count,
            "elapsed_seconds": elapsed,
            "spl_build_elapsed_seconds": elapsed,
            "llm_call_totals": totals,
            "input_tokens": totals["input_tokens"],
            "output_tokens": totals["output_tokens"],
            "reasoning_tokens": totals["reasoning_tokens"],
            "total_tokens": totals["total_tokens"],
            "calls": totals["calls"],
            "calls_detail": self._call_metadata,
        }
        return SPLBuildResult(text=text, metadata=metadata), spl_by_method

    def _generate_method_spl(self, method: dict[str, Any], language: str, class_name: str | None) -> str:
        if self.config.mode == "mock":
            return self._generate_mock_method_spl(method, language, class_name)
        ast_data = analyze_specific_method_ast(method["code"], method["name"], language, class_name)
        self.decomposer.size_threshold = self.config.decompose_size_threshold
        subcodes = self.decomposer.decompose_from_ast_data(ast_data, max_depth=self.config.decompose_max_depth)
        analyzed = self.recursive.analyze_subcodes(subcodes)
        flat_analyses = self._flatten_analyses(analyzed)
        return self.llm.convert_to_template("", method["code"], flat_analyses)

    def _generate_mock_method_spl(self, method: dict[str, Any], language: str, class_name: str | None) -> str:
        started = time.perf_counter()
        method_name = str(method.get("name") or "unknown")
        owner = f"{class_name}." if class_name else ""
        text = (
            f'[DEFINE_WORKER: "Mock SPL for {owner}{method_name}." {method_name}]\n'
            "    [INPUTS]\n"
            "    [END_INPUTS]\n\n"
            "    [OUTPUTS]\n"
            "    [END_OUTPUTS]\n\n"
            "    [MAIN_FLOW]\n"
            "        [SEQUENTIAL_BLOCK]\n"
            f"            [COMMAND Represent the {language} method body for smoke-test validation. RESULT mock_semantics]\n"
            "        [END_SEQUENTIAL_BLOCK]\n"
            "    [END_MAIN_FLOW]\n"
            "[END_WORKER]"
        )
        result = GenerationResult(
            text=text,
            provider="mock",
            model=self.config.model,
            elapsed_seconds=time.perf_counter() - started,
            input_tokens=max(1, len(str(method.get("code", ""))) // 4),
            output_tokens=max(1, len(text) // 4),
            reasoning_tokens=0,
            total_tokens=max(1, len(str(method.get("code", ""))) // 4) + max(1, len(text) // 4),
            raw_usage={"source": "rough_count_for_mock_spl"},
        )
        self._record_call(result)
        return text

    @staticmethod
    def _flatten_analyses(analyzed_subcodes: list[dict[str, Any]]) -> list[dict[str, Any]]:
        flat: list[dict[str, Any]] = []

        def walk(items):
            for item in items:
                flat.append({
                    'type': item.get('type', ''),
                    'analyzer_type': item.get('analyzer_type', ''),
                    'depth': item.get('depth', 0),
                    'code': item.get('original_code', item.get('code', '')),
                    'analysis': item.get('analysis', ''),
                    'lineno': item.get('lineno', 0),
                })
                if 'children' in item:
                    walk(item['children'])

        walk(analyzed_subcodes)
        return flat

    @staticmethod
    def _cleanup_spl_tags(spl_text: str) -> str:
        """Remove <SPL> tags that reference functions without a [DEFINE_WORKER] block.

        The LLM always emits <SPL>name</SPL> when it sees a function call.
        This post-pass extracts the set of valid worker names from the generated
        SPL and strips <SPL> wrappers that reference non-existent workers,
        keeping only the bare function name.
        """
        import re as _re
        workers: set[str] = set()
        for m in _re.finditer(r'\[DEFINE_WORKER:\s*"[^"]*"\s+([^\]]+)\]', spl_text):
            workers.add(m.group(1).strip())

        def _replace_tag(match: _re.Match) -> str:
            name = match.group(1).strip()
            if name in workers:
                return match.group(0)  # keep <SPL> tag
            return name  # strip wrapper, keep bare name

        return _re.sub(r'<SPL>\s*(.+?)\s*</SPL>', _replace_tag, spl_text)

    def _mock_llm(self, prompt: str) -> str:
        started = time.perf_counter()
        text = json.dumps(
            {
                "worker_name": "MockWorker",
                "brief_description": "Mock SPL generated for pipeline validation.",
                "inputs": [],
                "outputs": [],
                "main_flow": [{"command": "Analyze code bundle", "result": "SPL view"}],
                "alternative_flows": [],
                "exception_flows": [],
            },
            ensure_ascii=False,
        )
        result = GenerationResult(
            text=text,
            provider="mock",
            model=self.config.model,
            elapsed_seconds=time.perf_counter() - started,
            input_tokens=max(1, len(prompt) // 4) if prompt else 0,
            output_tokens=max(1, len(text) // 4),
            reasoning_tokens=0,
            total_tokens=(max(1, len(prompt) // 4) if prompt else 0) + max(1, len(text) // 4),
            raw_usage={"source": "rough_count_for_mock_spl"},
        )
        self._record_call(result)
        return text

    def _openai_llm(self, prompt: str) -> str:
        result = self._client.generate_with_metrics(prompt)
        self._record_call(result)
        return result.text

    def _record_call(self, result: GenerationResult) -> None:
        metadata = result.to_metadata()
        metadata["calls"] = 1
        self._usage_totals.add(metadata)
        self._call_metadata.append(metadata)

    def _reset_usage(self) -> None:
        self._usage_totals = UsageTotals()
        self._call_metadata = []


# ── Shared inline-SPL-card formatter ────────────────────────────────────────
# Used by exp1 and exp2 run.py to build per-function cards that pair source
# code (raw, skeleton, or scaffold) with the matching SPL block, so the LLM
# sees each function's code and behaviour together rather than as two separate
# blocks.

_SPL_INLINE_DISCLAIMER = (
    "source-derived behavior checkpoints for this function; map them back to source before using them"
)


def _extract_function_blocks(code: str, language: str) -> list[dict]:
    """Parse source/skeleton code into per-function blocks.

    Returns a list of dicts with keys: name, code, start_line, end_line.
    Handles Python, Java, and C++ method/function signatures.
    """
    if not code.strip():
        return []

    lines = code.splitlines()
    blocks: list[dict] = []
    current_name: str | None = None
    current_start: int | None = None
    current_lines: list[str] = []

    # Regex patterns for function/method signatures
    py_func = r'^\s*(?:async\s+)?def\s+(\w+)\s*\('
    java_func = r'^\s*(?:public|private|protected|static|\s)+[\w<>\[\],\s]+\s+(\w+)\s*\([^)]*\)\s*(?:throws\s+[\w\s,]+)?\s*\{?'
    cpp_func = r'^\s*(?:virtual\s+|static\s+|inline\s+|explicit\s+)*(?:[\w:<>*&,\s]+)\s+(\w+)\s*\([^)]*\)\s*(?:const\s*)?(?:\{|$)'

    if language == "python":
        sig_pattern = py_func
    elif language == "java":
        sig_pattern = java_func
    else:
        sig_pattern = cpp_func

    import re as _re
    indent_level: int | None = None

    def _finalize():
        nonlocal current_name, current_start, current_lines, indent_level
        if current_name is not None and current_lines:
            blocks.append({
                "name": current_name,
                "code": "\n".join(current_lines),
                "start_line": current_start if current_start is not None else 0,
                "end_line": (current_start if current_start is not None else 0) + len(current_lines) - 1,
            })
        current_name = None
        current_start = None
        current_lines = []
        indent_level = None

    for i, line in enumerate(lines):
        m = _re.match(sig_pattern, line)
        if m:
            _finalize()
            current_name = m.group(1)
            current_start = i
            current_lines = [line]
            # determine indentation for this function
            stripped = line.lstrip()
            indent_level = len(line) - len(stripped)
            # Check if this is a single-line function body (e.g. Java `{ ... }`)
            if language != "python" and "{" in line and "}" in line:
                # single-line body already captured
                pass
            continue

        if current_name is not None:
            # In Python skeleton mode, `...` or `pass` may be placeholders;
            # check if we've left the function via a less-indented non-empty line
            if language == "python":
                stripped = line.strip()
                if stripped and not stripped.startswith("#"):
                    line_indent = len(line) - len(line.lstrip())
                    if line_indent <= indent_level:
                        _finalize()
                        continue
            current_lines.append(line)

    _finalize()
    return blocks


def _match_spl_key(func_name: str, spl_by_method: dict) -> str | None:
    """Find the SPL block for a function name, trying various key formats."""
    if func_name in spl_by_method:
        return spl_by_method[func_name]
    # Try matching class.method format
    for key, value in spl_by_method.items():
        if key.endswith("." + func_name) or key == func_name:
            return value
    return None


def build_spl_method_index(spl_by_method: dict[str, str]) -> str:
    """Build a compact structured method index from SPL cards.

    Extracts method name, description, inputs, outputs, and calls from
    each SPL block and presents them as a compact table BEFORE the raw
    SPL cards.  This gives the model a quick overview without removing
    the precision of raw SPL tags.
    """
    import re as _re

    if not spl_by_method:
        return ""

    lines = ["## Method Index"]
    for key, spl_text in spl_by_method.items():
        bare = key.split(".")[-1] if "." in key else key

        # Description
        desc_m = _re.search(r'\[DEFINE_WORKER:\s*"([^"]*)"\s*(\w+)\]', spl_text)
        desc = desc_m.group(1)[:100] if desc_m else ""

        # Inputs
        inputs_m = _re.search(r'\[INPUTS\](.*?)\[END_INPUTS\]', spl_text, _re.DOTALL)
        inputs = []
        if inputs_m:
            for m in _re.finditer(r'<REF>\s*(\w+)\s*</REF>\s*:?\s*(\S+)?', inputs_m.group(1)):
                inputs.append("{}:{}".format(m.group(1), (m.group(2) or "?")))

        # Outputs
        outputs_m = _re.search(r'\[OUTPUTS\](.*?)\[END_OUTPUTS\]', spl_text, _re.DOTALL)
        outputs = []
        if outputs_m:
            for m in _re.finditer(r'<REF>\s*(\w+)\s*</REF>\s*:?\s*(\S+)?', outputs_m.group(1)):
                outputs.append("{}:{}".format(m.group(1), (m.group(2) or "?")))

        # Calls
        calls = _re.findall(r'<SPL>\s*(\w+)\s*</SPL>', spl_text)
        # Also detect self.method() calls
        for m in _re.finditer(r'self\.(\w+)\s*\(', spl_text):
            if m.group(1) not in calls:
                calls.append(m.group(1))

        params = ", ".join(inputs) if inputs else "—"
        rets = ", ".join(outputs) if outputs else "—"
        callee_str = ", ".join(calls) if calls else "—"

        lines.append("| `{}` | {} | {} | {} | {} |".format(
            bare, desc[:80], params, rets, callee_str))

    # Add header row at the right position
    header = "| Method | Purpose | Inputs | Returns | Calls |"
    sep = "|---|---|---|---|---|"
    lines.insert(1, sep)
    lines.insert(1, header)

    # Field detection
    all_fields = set()
    for spl_text in spl_by_method.values():
        for m in _re.finditer(r'self\.(\w+)', spl_text):
            all_fields.add(m.group(1))
    # Filter out method names
    method_names = set()
    for key in spl_by_method:
        method_names.add(key.split(".")[-1] if "." in key else key)
    all_fields -= method_names
    if all_fields:
        lines.append("")
        lines.append("Fields: {}".format(", ".join(sorted(all_fields))))

    lines.append("")
    return "\n".join(lines)


_GENERIC_QUERY_TERMS = {
    "about", "after", "again", "against", "answer", "before", "being",
    "below", "between", "change", "class", "code", "could", "does",
    "each", "edit", "from", "function", "given", "have", "into", "method",
    "only", "other", "output", "program", "question", "result", "return",
    "should", "source", "than", "that", "their", "then", "there", "these",
    "this", "through", "using", "value", "what", "when", "where", "which",
    "with", "would",
}


def select_task_relevant_spl_methods(
    spl_by_method: dict[str, str],
    query: str,
    *,
    max_cards: int = 4,
) -> dict[str, str]:
    """Select a deterministic, query-relevant subset of function SPL cards.

    Exact method-name references dominate the ranking. Remaining identifier
    terms provide semantic recall over the card text. The original mapping
    order is the deterministic fallback when the query has no useful signal.
    """
    import re as _re

    if not spl_by_method or max_cards <= 0:
        return {}

    quoted = {
        token.lower()
        for span in _re.findall(r"`([^`]+)`|'([^']+)'|\"([^\"]+)\"", query or "")
        for part in span
        for token in _re.findall(r"[A-Za-z_][A-Za-z0-9_]*", part)
    }
    terms = {
        token.lower()
        for token in _re.findall(r"[A-Za-z_][A-Za-z0-9_]*", query or "")
        if len(token) >= 4 and token.lower() not in _GENERIC_QUERY_TERMS
    }
    terms.update(quoted)

    ranked: list[tuple[int, int, str, str]] = []
    for position, (key, spl_text) in enumerate(spl_by_method.items()):
        key_text = str(key)
        bare = key_text.rsplit(".", 1)[-1].lower()
        searchable = f"{key_text}\n{spl_text}".lower()
        score = 0
        for term in terms:
            if term == bare:
                score += 30
            elif term in bare or bare in term:
                score += 12
            matches = len(_re.findall(rf"\b{_re.escape(term)}\b", searchable))
            score += min(matches, 4) * (4 if term in quoted else 2)
        if score:
            ranked.append((-score, position, key_text, spl_text))

    if not ranked:
        return dict(list(spl_by_method.items())[:max_cards])

    ranked.sort()
    return {key: spl_text for _score, _position, key, spl_text in ranked[:max_cards]}


def recover_spl_by_worker(spl_text: str) -> dict[str, str]:
    """Recover a function-level SPL map from a concatenated SPL artifact.

    Older prepared artifacts sometimes contain ``spl.txt`` but no
    ``spl_by_method.json``.  Keeping that artifact usable is important for a
    fair rerun: an absent sidecar must not silently turn an SPL condition into
    a no-SPL condition.  Duplicate worker names are retained with a stable
    ``#N`` suffix; language-specific binders may disambiguate them further.
    """
    import re as _re

    blocks: dict[str, str] = {}
    counts: dict[str, int] = {}
    pattern = _re.compile(
        r'\[DEFINE_WORKER:\s*"[^"]*"\s*([^\]\s]+)\](.*?)\[END_WORKER\]',
        _re.DOTALL,
    )
    for match in pattern.finditer(str(spl_text or "")):
        worker = match.group(1).strip()
        counts[worker] = counts.get(worker, 0) + 1
        key = worker if counts[worker] == 1 else f"{worker}#{counts[worker]}"
        blocks[key] = match.group(0).strip()
    return blocks


def format_task_relevant_spl_cards(
    spl_by_method: dict[str, str],
    query: str,
    language: str = "python",
    *,
    max_cards: int = 4,
) -> str:
    """Render selected SPL without repeating source already in the prompt."""
    selected = select_task_relevant_spl_methods(
        spl_by_method,
        query,
        max_cards=max_cards,
    )
    return format_inline_spl_cards_generic(
        "",
        selected,
        language,
        include_source=False,
    )


def format_inline_spl_cards_generic(
    source_code: str,
    spl_by_method: dict[str, str],
    language: str = "python",
    *,
    source_code_label: str = "Source Code",
    include_source: bool = True,
) -> str:
    """Build per-function inline cards pairing source code with SPL.

    Args:
        source_code: Raw source, skeleton, or scaffold text.
        spl_by_method: Mapping of ``ClassName.method_name`` → SPL block.
        language: ``python``, ``java``, or ``cpp``.
        source_code_label: Heading label for the source code block
            (e.g. ``"Skeleton"`` for skeleton-based conditions).
        include_source: If False, generate SPL-only cards (for spl_only condition).

    Returns:
        Markdown string with per-function cards separated by ``---``.
    """
    if not spl_by_method:
        return ""

    func_blocks = _extract_function_blocks(source_code, language)
    cards: list[str] = []

    if func_blocks:
        for fb in func_blocks:
            name = fb["name"]
            spl_text = _match_spl_key(name, spl_by_method)
            if not spl_text:
                continue
            card = f"### Function: `{name}`\n\n"
            if include_source and fb["code"].strip():
                fence = "python" if language == "python" else ("java" if language == "java" else "cpp")
                card += f"**{source_code_label}:**\n```{fence}\n{fb['code']}\n```\n"
            card += f"\n**SPL ({_SPL_INLINE_DISCLAIMER}):**\n{spl_text}\n"
            cards.append(card)
    else:
        # Fallback: no function blocks extracted — use SPL keys directly
        for key, spl_text in spl_by_method.items():
            card = f"### Function: `{key}`\n\n"
            if include_source:
                card += f"**{source_code_label}:** *(see enclosing source)*\n\n"
            card += f"**SPL ({_SPL_INLINE_DISCLAIMER}):**\n{spl_text}\n"
            cards.append(card)

    if not cards:
        return ""

    return "\n\n---\n".join(cards) + "\n"
