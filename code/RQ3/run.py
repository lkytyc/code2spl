from __future__ import annotations

import argparse
import ast
import base64
import json
import os
import re
import shutil
import subprocess
import sys
import time
from pathlib import Path
from typing import Any

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from common.paths import PROJECT_ROOT, ensure_dir, read_config, read_json, resolve_in_project, write_json, write_text
from common.providers import ApiKeyPool, FileApiKeyLeasePool
from common.run_utils import run_ordered, selected_items


#: The prompt text each condition ran with.  These were frozen before the runs
#: and are inputs in the same sense the configs are, so they ship under `data/`
#: with the run settings rather than here beside the code that reads them.
PROMPT_ROOT = PROJECT_ROOT / "data" / "RQ3" / "settings" / "central_prompts"
FROZEN_ORIGINAL_PROMPT_ROOT = (PROJECT_ROOT / "data" / "RQ3" / "settings"
                               / "frozen_original_prompts")

STOPWORDS = {
    "the", "and", "or", "not", "with", "from", "import", "this", "that", "what", "did",
    "you", "expect", "expected", "happened", "because", "below", "code", "example",
    "result", "results", "true", "false", "none", "into", "when", "where", "which",
    "there", "their", "they", "them", "your", "have", "has", "had", "does", "done",
    "using", "used", "use", "can", "cannot", "should", "would", "could", "will",
    "all", "any", "its", "for", "are", "was", "were", "been", "being", "but",
    "also", "same", "then", "than", "core", "python", "response", "version",
    "environment", "installed", "commit", "output", "traceback", "log", "details",
    "np", "xr", "ds", "pd", "data", "type",
}

SPL_IMPORTANT_TERMS = {
    "dtype", "int32", "int64", "multiindex", "index", "indexes", "coordinate",
    "coordinates", "stack", "cast", "casts", "i4", "i8", "array", "pandas",
    "level", "levels", "values", "exception", "return", "condition", "branch",
}

SPL_GENERIC_TERMS = {
    "parse", "format", "split", "value", "values", "string", "strings", "error",
    "validate", "get", "set", "put", "remove", "add", "make", "create",
    "build", "update", "check", "handle", "process", "return", "object",
    "data", "type", "item", "items", "list", "dict", "file", "line",
}

GENERIC_WORKER_NAMES = {
    "copy", "get", "set", "add", "remove", "update", "create", "make",
    "build", "handle", "process", "values", "items", "keys",
}

LEGACY_SPL_PROTOCOL = "spl_guarded_protocol"
# NEW (misleading-card guard): identical to the legacy tuned protocol, except
# every SPL card/checkpoint carries an explicit warning that it describes
# PRE-FIX (current, possibly buggy) behavior rather than a correctness spec.
# This is the only intended change over the frozen original; the frozen prompt
# files themselves are untouched.
GUARDED_LEGACY_SPL_PROTOCOL = "spl_guarded_protocol"
STRICT_SPL_PROTOCOL = "generic_stage_isolated_v1"
ROLE_CONDITIONED_SPL_PROTOCOL = "generic_role_conditioned_v2"
# Public alias for the current generic protocol used by new experiment configs.
GENERIC_SPL_PROTOCOL = ROLE_CONDITIONED_SPL_PROTOCOL
SUPPORTED_SPL_PROTOCOLS = {
    LEGACY_SPL_PROTOCOL,
    GUARDED_LEGACY_SPL_PROTOCOL,
    STRICT_SPL_PROTOCOL,
    ROLE_CONDITIONED_SPL_PROTOCOL,
}


def spl_protocol(config: dict[str, Any]) -> str:
    # Historical Exp6 configs predate this field, so an omitted protocol must
    # continue to reproduce the saved tuned workflow.
    protocol = str(config.get("mini_spl_protocol") or LEGACY_SPL_PROTOCOL)
    if protocol not in SUPPORTED_SPL_PROTOCOLS:
        raise ValueError(
            f"Unsupported mini_spl_protocol={protocol!r}; "
            f"expected one of {sorted(SUPPORTED_SPL_PROTOCOLS)}"
        )
    return protocol


def uses_legacy_tuned_protocol(config: dict[str, Any]) -> bool:
    # The guarded protocol is a strict superset of the legacy tuned workflow:
    # it routes through the same frozen prompts and legacy scoring/plan logic,
    # only adding the misleading-card guard text.
    return spl_protocol(config) in {LEGACY_SPL_PROTOCOL, GUARDED_LEGACY_SPL_PROTOCOL}


def uses_misleading_guard(config: dict[str, Any]) -> bool:
    return spl_protocol(config) == GUARDED_LEGACY_SPL_PROTOCOL


def uses_strict_stage_isolated_protocol(config: dict[str, Any]) -> bool:
    return spl_protocol(config) == STRICT_SPL_PROTOCOL


SPL_MISLEADING_GUARD = (
    "WARNING — SPL describes PRE-FIX behavior, not a spec: the "
    "[COMMAND]/[CONDITION]/[RETURN]/[THROW] checkpoints below were extracted "
    "from the CURRENT (possibly buggy) source, so they state what the code does "
    "right now, including the bug itself. Checkpoints are descriptive, not "
    "authoritative. In particular, a checkpoint about a condition expression "
    "(e.g. a comparison threshold) or a variable's lifecycle (initialization vs "
    "per-iteration reset/update) is a prime SUSPECT to fix — verify it against "
    "the visible current source and the issue's FAIL_TO_PASS intent, and correct "
    "it rather than preserving it as spec."
)


SPL_SEARCH_SCRIPT = r'''#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

INDEX_PATH = Path("/tmp/spl_tools/spl_index.json")
GENERIC = {
    "parse", "format", "split", "value", "string", "error", "validate",
    "get", "set", "put", "remove", "add", "make", "create", "return",
    "object", "data", "type", "item", "items", "list", "dict",
}


def tokenize(text: str) -> list[str]:
    return [t.lower() for t in re.findall(r"[A-Za-z_][A-Za-z0-9_]{2,}", text)]


def score_entry(entry: dict, query_terms: list[str]) -> tuple[float, list[str]]:
    file_name = str(entry.get("file") or "")
    worker = str(entry.get("worker_name") or "")
    summary = str(entry.get("summary") or "")
    spl = str(entry.get("spl") or "")
    hay = f"{file_name} {worker} {summary} {spl}".lower()
    worker_low = worker.lower()
    file_low = file_name.lower()
    matched: list[str] = []
    score = 0.0
    for term in query_terms:
        if term in GENERIC:
            weight = 0.15
        elif term in worker_low:
            weight = 4.0
        elif term in file_low:
            weight = 3.0
        elif term in summary.lower():
            weight = 1.5
        else:
            weight = 0.6
        count = hay.count(term)
        if count:
            matched.append(term)
            score += weight * min(count, 4)
    return score, matched


def checkpoints(spl: str, limit: int = 4) -> list[str]:
    out = []
    for raw in spl.splitlines():
        line = " ".join(raw.strip().split())
        if not line:
            continue
        if not any(tag in line for tag in ("[COMMAND", "[CONDITION", "[RETURN", "[THROW", "[EXCEPTION_FLOW", "[ALTERNATIVE_FLOW")):
            continue
        out.append(line[:220])
        if len(out) >= limit:
            break
    return out


def main() -> None:
    if not INDEX_PATH.exists():
        print("No SPL index is available at /tmp/spl_tools/spl_index.json")
        raise SystemExit(1)
    data = json.loads(INDEX_PATH.read_text(encoding="utf-8", errors="replace"))
    entries = data.get("entries") if isinstance(data, dict) else data
    if not isinstance(entries, list):
        entries = []
    query = " ".join(sys.argv[1:]).strip()
    terms = tokenize(query)
    if not terms:
        print("Usage: python /tmp/spl_tools/spl_search.py \"issue symptom behavior terms\"")
        raise SystemExit(2)
    ranked = []
    for entry in entries:
        if not isinstance(entry, dict):
            continue
        score, matched = score_entry(entry, terms)
        if score > 0:
            ranked.append((score, matched, entry))
    ranked.sort(key=lambda row: row[0], reverse=True)
    if not ranked:
        print("No SPL entries matched. Fall back to source search.")
        return
    best = ranked[0][0]
    for rank, (score, matched, entry) in enumerate(ranked[:8], start=1):
        non_generic = [term for term in matched if term not in GENERIC]
        if rank <= 2 and non_generic and score >= max(1.0, best * 0.55):
            role = "SOURCE_OWNER_CANDIDATE"
        elif score > 0:
            role = "SOURCE_BOUND_CONTEXT_CHECK"
        else:
            role = "WEAK_CONTEXT_ONLY"
        print(f"[{rank}] score={score:.2f} file={entry.get('file')} worker={entry.get('worker_name')}")
        print(f"role: {role}")
        print(f"matched_terms: {', '.join(matched[:12])}")
        print(f"summary: {entry.get('summary', '')}")
        print("source_check: map at least one checkpoint to real source before editing.")
        for item in checkpoints(str(entry.get("spl") or "")):
            print(f"checkpoint: {item}")
        print("---")


if __name__ == "__main__":
    main()
'''


SPL_SHOW_SCRIPT = r'''#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path

INDEX_PATH = Path("/tmp/spl_tools/spl_index.json")


def checkpoints(spl: str, limit: int = 4) -> list[str]:
    out = []
    for raw in spl.splitlines():
        line = " ".join(raw.strip().split())
        if not line:
            continue
        if not any(tag in line for tag in ("[COMMAND", "[CONDITION", "[RETURN", "[THROW", "[EXCEPTION_FLOW", "[ALTERNATIVE_FLOW")):
            continue
        out.append(line[:220])
        if len(out) >= limit:
            break
    return out


def main() -> None:
    if not INDEX_PATH.exists():
        print("No SPL index is available at /tmp/spl_tools/spl_index.json")
        raise SystemExit(1)
    pattern = " ".join(sys.argv[1:]).lower().strip()
    if not pattern:
        print("Usage: python /tmp/spl_tools/spl_show.py \"file.py function_name\"")
        raise SystemExit(2)
    data = json.loads(INDEX_PATH.read_text(encoding="utf-8", errors="replace"))
    entries = data.get("entries") if isinstance(data, dict) else data
    if not isinstance(entries, list):
        entries = []
    terms = [term for term in pattern.replace("::", " ").replace("/", " ").split() if term]
    matches = []
    for entry in entries:
        if not isinstance(entry, dict):
            continue
        hay = f"{entry.get('file', '')} {entry.get('worker_name', '')} {entry.get('summary', '')}".lower()
        if all(term in hay for term in terms) or pattern in hay:
            matches.append(entry)
    if not matches:
        print("No exact SPL card matched. Try spl_search.py with broader behavior terms.")
        return
    for idx, entry in enumerate(matches[:4], start=1):
        print(f"### SPL CARD {idx}")
        print(f"File: {entry.get('file')}")
        print(f"Function: {entry.get('worker_name')}")
        print(f"Summary: {entry.get('summary', '')}")
        print("Use: source-bound behavior checklist. Map checkpoints to visible source before editing.")
        for item in checkpoints(str(entry.get("spl") or "")):
            print(f"Checkpoint: {item}")
        print("")
        print(entry.get("spl", ""))
        print("--- END SPL CARD ---")


if __name__ == "__main__":
    main()
'''


FREE_SUMMARY_SEARCH_SCRIPT = r'''#!/usr/bin/env python3
from __future__ import annotations

import re
import sys
from pathlib import Path

SUMMARY_PATH = Path("/tmp/spl_tools/free_summary_context.txt")


def main() -> None:
    if not SUMMARY_PATH.exists():
        print("No free-summary context is available.")
        raise SystemExit(1)
    query = " ".join(sys.argv[1:]).lower().strip()
    if not query:
        print("Usage: python /tmp/spl_tools/free_summary_search.py \"issue keywords\"")
        raise SystemExit(2)
    terms = [t for t in re.findall(r"[A-Za-z_][A-Za-z0-9_]{2,}", query) if t]
    lines = SUMMARY_PATH.read_text(encoding="utf-8", errors="replace").splitlines()
    hits = []
    for idx, line in enumerate(lines):
        low = line.lower()
        score = sum(low.count(term) for term in terms)
        if score:
            start = max(0, idx - 2)
            end = min(len(lines), idx + 3)
            hits.append((score, start, end))
    hits.sort(key=lambda row: row[0], reverse=True)
    if not hits:
        print("No summary hits. Fall back to source search.")
        return
    seen = set()
    for rank, (_score, start, end) in enumerate(hits[:6], start=1):
        key = (start, end)
        if key in seen:
            continue
        seen.add(key)
        print(f"[{rank}] lines {start + 1}-{end}")
        print("\n".join(lines[start:end]))
        print("---")


if __name__ == "__main__":
    main()
'''


def load_prompt_addendum(mode: str, config: dict[str, Any] | None = None) -> str:
    if mode == "miniswe_original":
        return ""
    if "spl" in mode and (config is None or uses_legacy_tuned_protocol(config)):
        path = FROZEN_ORIGINAL_PROMPT_ROOT / f"{mode}.md"
        return path.read_text(encoding="utf-8", errors="replace").strip()
    path = PROMPT_ROOT / mode / "addendum.md"
    return path.read_text(encoding="utf-8", errors="replace").strip()


def normalize_api_base(value: Any) -> str | None:
    text = str(value or "").strip()
    return text or None


def trim_text(text: str, max_chars: int) -> str:
    if len(text) <= max_chars:
        return text
    return text[: max(0, max_chars)] + "\n...[truncated]\n"


def read_local_problem_statement(sample_dir: Path) -> str:
    jsonl = sample_dir / "swebench_instance.jsonl"
    if jsonl.exists():
        for line in jsonl.read_text(encoding="utf-8", errors="replace").splitlines():
            if line.strip():
                row = json.loads(line)
                return str(row.get("problem_statement") or "")
    fallback = sample_dir / "problem_statement.txt"
    if fallback.exists():
        return fallback.read_text(encoding="utf-8", errors="replace")
    return ""


def issue_core_text(problem_statement: str) -> str:
    return problem_statement.split("###", 1)[0]


def tokenize_for_spl(text: str) -> list[str]:
    tokens: list[str] = []
    for raw in re.findall(r"[A-Za-z_][A-Za-z0-9_]*|[0-9]+", text):
        token = raw.lower()
        if token in {"i4", "i8"} or token in SPL_IMPORTANT_TERMS:
            tokens.append(token)
        elif len(token) >= 4 and token not in STOPWORDS:
            tokens.append(token)
    return tokens


def split_identifier_terms(text: str) -> set[str]:
    spaced = re.sub(r"([a-z])([A-Z])", r"\1 \2", text).replace("_", " ").replace(".", " ")
    return set(tokenize_for_spl(spaced))


def spl_query_terms(problem_statement: str, config: dict[str, Any]) -> set[str]:
    terms = set(tokenize_for_spl(issue_core_text(problem_statement)))
    full_terms = set(tokenize_for_spl(problem_statement))
    terms |= SPL_IMPORTANT_TERMS & full_terms
    if uses_legacy_tuned_protocol(config):
        if {"int32", "int64", "i4", "i8", "dtype"} & terms:
            terms |= {"dtype", "index", "pandas", "values"}
        if {"stack", "multiindex", "indexes", "index"} & terms:
            terms |= {"multiindex", "index", "level", "levels"}
    return terms


def extract_traceback_functions(problem_statement: str) -> list[str]:
    patterns = (
        r'(?m)^\s*File\s+["\'][^"\']+\.py["\'],\s+line\s+\d+,\s+in\s+([A-Za-z_][A-Za-z0-9_]*)\s*$',
        r"(?m)(?:^|\s)[A-Za-z0-9_./\\-]+\.py:\d+(?::\d+)?:\s+in\s+([A-Za-z_][A-Za-z0-9_]*)\b",
    )
    functions: list[str] = []
    seen: set[str] = set()
    for pattern in patterns:
        for function_name in re.findall(pattern, problem_statement):
            if function_name in seen:
                continue
            seen.add(function_name)
            functions.append(function_name)
    return functions


def score_spl_entry(
    entry: dict[str, Any],
    terms: set[str],
    problem_statement: str = "",
    *,
    legacy_tuned: bool = False,
) -> tuple[float, list[str]]:
    file_name = str(entry.get("file") or "")
    worker = str(entry.get("worker_name") or "")
    summary = str(entry.get("summary") or "")
    spl = str(entry.get("spl") or "")
    issue_low = problem_statement.lower()
    file_norm = file_name.replace("\\", "/").lower()
    worker_low = worker.lower()
    worker_leaf = worker_low.split(".")[-1]
    worker_snake_leaf = re.sub(r"(?<!^)(?=[A-Z])", "_", worker.split(".")[-1]).lower()
    chunks = {
        "worker": worker_low,
        "file": file_norm,
        "summary": summary.lower(),
        "spl": spl.lower(),
    }
    matched: list[str] = []
    score = 0.0
    for term in terms:
        term_score = 0.0
        locations: list[str] = []
        for name, text in chunks.items():
            if term not in text:
                continue
            locations.append(name)
            count = min(text.count(term), 3)
            if name == "worker":
                weight = 6.0
            elif name == "file":
                weight = 3.0
            elif name == "summary":
                weight = 4.0
            else:
                weight = 1.0
            if term in SPL_IMPORTANT_TERMS:
                weight *= 2.0
            if term in SPL_GENERIC_TERMS:
                weight *= 0.25
            term_score += weight * count
        if term_score:
            matched.append(f"{term}:{'/'.join(locations)}")
            score += term_score

    # Strong source-visible signals from the issue should dominate broad SPL
    # keyword frequency. This prevents words like "value", "name", or "dtype"
    # from promoting nearby context over a stack-trace function or explicit
    # source owner named in the issue.
    if file_norm and file_norm in issue_low:
        score += 35.0
        matched.append("exact_file_in_issue:file")
    stack_functions = (
        re.findall(r"\bin\s+([A-Za-z_][A-Za-z0-9_]*)\b", problem_statement)
        if legacy_tuned
        else extract_traceback_functions(problem_statement)
    )
    stack_function_lows = {function_name.lower() for function_name in stack_functions}
    for idx, function_name in enumerate(stack_functions):
        low = function_name.lower()
        if low and (low == worker_leaf or low == worker_snake_leaf):
            score += 55.0 + (idx * 14.0)
            matched.append(f"stack_function:{function_name}")
            break
    if (
        worker_leaf
        and worker_leaf not in GENERIC_WORKER_NAMES
        and not worker_leaf.startswith("__")
        and worker_leaf not in stack_function_lows
        and worker_leaf in issue_low
    ):
        score += 55.0
        matched.append(f"exact_worker_in_issue:{worker_leaf}")
    elif (
        worker_snake_leaf
        and worker_snake_leaf not in GENERIC_WORKER_NAMES
        and not worker_snake_leaf.startswith("__")
        and worker_snake_leaf not in stack_function_lows
        and worker_snake_leaf in issue_low
    ):
        score += 55.0
        matched.append(f"exact_worker_in_issue:{worker_snake_leaf}")

    if legacy_tuned and ("optim" in issue_low or "reduc" in issue_low) and "operation" in issue_low:
        if "reduce" in worker_low:
            score += 45.0
            matched.append("operation_reduce_owner:worker")
        if "migration_name_fragment" in worker_low and "fragment" not in issue_low:
            score *= 0.35
            matched.append("demote_name_fragment:worker")

    if legacy_tuned and {"dtype", "values"} & terms and {"dtype", "int32", "int64", "i4", "i8"} & terms:
        if "__array__" in worker_low or "values" in worker_leaf or "dtype" in worker_leaf:
            score += 70.0
            matched.append("dtype_output_owner:worker")
        elif is_constructor_worker(worker) and "constructor" not in issue_low and "initializ" not in issue_low:
            score *= 0.55
            matched.append("demote_constructor_context:worker")

    if legacy_tuned:
        summary_worker = f"{summary} {worker}".lower()
        if "dtype" in summary_worker and ("index" in summary_worker or "multiindex" in summary_worker):
            score += 25.0
        if "safe integer index" in summary_worker or "valid numpy dtype" in summary_worker:
            score += 35.0
    if is_constructor_worker(worker) and not any(
        item.split(":", 1)[0] in SPL_IMPORTANT_TERMS for item in matched
    ):
        score *= 0.4
    return score, matched


def is_constructor_worker(worker: str) -> bool:
    normalized = worker.lower().replace("-", "_")
    return "__init__" in normalized or normalized.endswith("_init") or normalized.endswith(".init")


def spl_card_role(rank: int, entry: dict[str, Any], best_score: float) -> str:
    score = float(entry.get("_spl_score") or 0.0)
    worker = str(entry.get("worker_name") or "")
    matched_terms = [str(item).split(":", 1)[0] for item in entry.get("_spl_matched_terms", [])]
    non_generic = [term for term in matched_terms if term not in SPL_GENERIC_TERMS]
    if is_constructor_worker(worker) and not any(term in SPL_IMPORTANT_TERMS for term in non_generic):
        return "SOURCE_BOUND_CONTEXT_CHECK"
    if rank == 1 and score > 0 and non_generic:
        return "PRIMARY_SOURCE_OWNER_CANDIDATE"
    if rank <= 3 and score > 0 and non_generic and score >= max(1.0, best_score * 0.55):
        return "SECONDARY_SOURCE_OWNER_CANDIDATE"
    if score > 0:
        return "SOURCE_BOUND_CONTEXT_CHECK"
    return "WEAK_CONTEXT_ONLY"


def extract_spl_checkpoints(spl: str, limit: int = 5, max_len: int = 180) -> list[str]:
    checkpoints: list[str] = []
    for raw_line in spl.splitlines():
        line = " ".join(raw_line.strip().split())
        if not line:
            continue
        if not any(tag in line for tag in ("[COMMAND", "[CONDITION", "[RETURN", "[THROW", "[EXCEPTION_FLOW", "[ALTERNATIVE_FLOW")):
            continue
        if len(line) > max_len:
            line = line[: max_len - 3].rstrip() + "..."
        checkpoints.append(line)
        if len(checkpoints) >= limit:
            break
    return checkpoints


def spl_controller_budget(mode: str, config: dict[str, Any]) -> tuple[int, int]:
    if mode == "miniswe_spl_both":
        return (
            max(1, int(config.get("mini_spl_both_controller_cards", 3))),
            max(200, int(config.get("mini_spl_both_controller_spl_chars", 600))),
        )
    return (
        max(1, int(config.get("mini_spl_controller_cards", 4))),
        max(200, int(config.get("mini_spl_controller_spl_chars", 750))),
    )


def ranked_spl_entries(sample_dir: Path, config: dict[str, Any]) -> list[dict[str, Any]]:
    path = sample_dir / "spl_index.json"
    if not path.exists():
        return []
    data = read_json(path)
    entries = data.get("entries") if isinstance(data, dict) else []
    if not isinstance(entries, list):
        return []
    problem_statement = read_local_problem_statement(sample_dir)
    terms = spl_query_terms(problem_statement, config)
    legacy_tuned = uses_legacy_tuned_protocol(config)
    ranked: list[tuple[float, int, list[str], dict[str, Any]]] = []
    for idx, entry in enumerate(entries):
        if not isinstance(entry, dict):
            continue
        score, matched = score_spl_entry(
            entry,
            terms,
            problem_statement,
            legacy_tuned=legacy_tuned,
        )
        copied = dict(entry)
        copied["_spl_score"] = round(score, 3)
        copied["_spl_matched_terms"] = matched[:12]
        ranked.append((score, idx, matched, copied))
    ranked.sort(key=lambda row: (row[0], -row[1]), reverse=True)
    positive = [entry for score, _idx, _matched, entry in ranked if score > 0]
    if positive:
        return positive
    return [entry for _score, _idx, _matched, entry in ranked]


def selected_spl_controller_cards(sample_dir: Path, mode: str, config: dict[str, Any]) -> list[tuple[str, dict[str, Any]]]:
    entries = ranked_spl_entries(sample_dir, config)
    if not entries:
        return []
    card_limit, _spl_chars = spl_controller_budget(mode, config)
    best_score = float(entries[0].get("_spl_score") or 0.0)
    primary_assigned = False
    selected: list[tuple[str, int, dict[str, Any]]] = []
    for rank, entry in enumerate(entries[:card_limit], start=1):
        role = spl_card_role(rank, entry, best_score)
        if role in {"PRIMARY_SOURCE_OWNER_CANDIDATE", "SECONDARY_SOURCE_OWNER_CANDIDATE"}:
            if not primary_assigned:
                role = "PRIMARY_SOURCE_OWNER_CANDIDATE"
                primary_assigned = True
            else:
                role = "SECONDARY_SOURCE_OWNER_CANDIDATE"
        selected.append((role, rank, entry))
    role_order = {
        "PRIMARY_SOURCE_OWNER_CANDIDATE": 0,
        "SECONDARY_SOURCE_OWNER_CANDIDATE": 1,
        "SOURCE_BOUND_CONTEXT_CHECK": 2,
        "WEAK_CONTEXT_ONLY": 3,
    }
    selected.sort(key=lambda row: (role_order.get(row[0], 99), row[1]))
    return [(role, entry) for role, _rank, entry in selected]


def source_bound_source_budget(mode: str, config: dict[str, Any]) -> int:
    if mode == "miniswe_spl_both":
        return max(400, int(config.get("mini_spl_both_source_bound_source_chars", 1200)))
    return max(400, int(config.get("mini_source_bound_source_chars", 1400)))


def prompt_card_limit(mode: str, config: dict[str, Any]) -> int:
    if mode == "miniswe_spl_both":
        return max(1, int(config.get("mini_spl_both_prompt_cards", 1)))
    return max(1, int(config.get("mini_spl_prompt_cards", 2)))


def worker_name_candidates(worker: str) -> tuple[list[str], list[str]]:
    parts = [part for part in str(worker or "").split(".") if part]
    owner_candidates = parts[:-1]
    raw_name = parts[-1] if parts else str(worker or "")
    function_candidates = [raw_name]
    snake_name = re.sub(r"(?<!^)(?=[A-Z])", "_", raw_name).lower()
    if snake_name and snake_name != raw_name:
        function_candidates.append(snake_name)

    dunder = re.search(r"__(\w+)__$", raw_name)
    if dunder:
        function_candidates.append(f"__{dunder.group(1)}__")
    if raw_name.endswith("__init__"):
        function_candidates.append("__init__")
    if raw_name.endswith("__new__"):
        function_candidates.append("__new__")
    if raw_name.endswith("__call__"):
        function_candidates.append("__call__")
    if raw_name.startswith("Print") and len(raw_name) > len("Print"):
        # SymPy printer methods are often represented in SPL as PrintFoo,
        # while the real source owner is _print_Foo.
        function_candidates.append(f"_print_{raw_name[len('Print'):]}")

    # Some SPL builders encode constructors as ClassAlias__init__ while the
    # real Python method is simply __init__ inside the class from owner_candidates.
    prefix = raw_name.split("__", 1)[0]
    if prefix and prefix != raw_name:
        owner_candidates.append(prefix)

    # Preserve order while removing duplicates.
    owners = list(dict.fromkeys(owner_candidates))
    funcs = list(dict.fromkeys(function_candidates))
    return owners, funcs


def node_source_excerpt(source_lines: list[str], node: ast.AST, max_chars: int) -> dict[str, Any]:
    start = int(getattr(node, "lineno", 1) or 1)
    end = int(getattr(node, "end_lineno", start) or start)
    code = "".join(source_lines[start - 1:end])
    return {
        "start_line": start,
        "end_line": end,
        "code": trim_text(code.rstrip(), max_chars),
    }


def extract_python_source_excerpts(source_text: str, worker: str, max_chars: int) -> tuple[str, list[dict[str, Any]]]:
    try:
        tree = ast.parse(source_text)
    except SyntaxError:
        return "UNRESOLVED_SOURCE_ANCHOR", []
    lines = source_text.splitlines(keepends=True)
    owner_candidates, function_candidates = worker_name_candidates(worker)
    excerpts: list[dict[str, Any]] = []

    class_nodes = [
        node for node in ast.walk(tree)
        if isinstance(node, ast.ClassDef) and (not owner_candidates or node.name in owner_candidates)
    ]
    for class_node in class_nodes:
        if function_candidates and class_node.name in function_candidates:
            excerpts.append(node_source_excerpt(lines, class_node, max_chars))
            continue
        for child in class_node.body:
            if isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef)) and child.name in function_candidates:
                excerpts.append(node_source_excerpt(lines, child, max_chars))

    if not excerpts:
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)) and node.name in function_candidates:
                excerpts.append(node_source_excerpt(lines, node, max_chars))

    if not excerpts:
        return "UNRESOLVED_SOURCE_ANCHOR", []
    status = "SOURCE_ANCHOR_UNIQUE" if len(excerpts) == 1 else "SOURCE_ANCHOR_MULTIPLE_SAME_OWNER"
    return status, excerpts[:4]


def fallback_source_excerpts(source_text: str, worker: str, max_chars: int) -> tuple[str, list[dict[str, Any]]]:
    _owners, function_candidates = worker_name_candidates(worker)
    lines = source_text.splitlines()
    for idx, line in enumerate(lines):
        stripped = line.strip()
        if not any(re.match(rf"(def|class)\s+{re.escape(name)}\b", stripped) for name in function_candidates):
            continue
        indent = len(line) - len(line.lstrip())
        end = idx + 1
        for j in range(idx + 1, len(lines)):
            other = lines[j]
            other_stripped = other.strip()
            if not other_stripped:
                continue
            other_indent = len(other) - len(other.lstrip())
            if other_indent <= indent and re.match(r"(def|class)\s+\w+", other_stripped):
                break
            end = j + 1
        code = "\n".join(lines[idx:end])
        return "SOURCE_ANCHOR_FALLBACK", [{
            "start_line": idx + 1,
            "end_line": end,
            "code": trim_text(code.rstrip(), max_chars),
        }]
    return "UNRESOLVED_SOURCE_ANCHOR", []


def source_excerpts_for_spl_entry(sample_dir: Path, entry: dict[str, Any], mode: str, config: dict[str, Any]) -> dict[str, Any]:
    rel_file = str(entry.get("file") or "").replace("\\", "/").strip("/")
    source_path = sample_dir / "source_files" / Path(rel_file)
    result: dict[str, Any] = {
        "status": "UNRESOLVED_SOURCE_ANCHOR",
        "repo_file": rel_file,
        "path": str(source_path),
        "excerpts": [],
    }
    if not rel_file or not source_path.exists():
        return result
    source_text = source_path.read_text(encoding="utf-8", errors="replace")
    max_chars = source_bound_source_budget(mode, config)
    if source_path.suffix == ".py":
        status, excerpts = extract_python_source_excerpts(source_text, str(entry.get("worker_name") or ""), max_chars)
    else:
        status, excerpts = fallback_source_excerpts(source_text, str(entry.get("worker_name") or ""), max_chars)
    result["status"] = status
    result["excerpts"] = excerpts
    return result


def likely_edit_focus(entry: dict[str, Any]) -> str:
    text = " ".join([
        str(entry.get("worker_name") or ""),
        str(entry.get("summary") or ""),
        str(entry.get("spl") or ""),
        " ".join(str(item) for item in entry.get("_spl_matched_terms", [])),
    ]).lower()
    if re.search(
        r"(?<![A-Za-z0-9_])(?:dtype|int32|int64|i4|i8|cast|casting|downcast|upcast|astype)(?![A-Za-z0-9_])",
        text,
    ):
        return "data-flow or return-value handling that preserves dtype/casting semantics"
    if any(term in text for term in ("exception", "[throw", "[exception_flow", "raise")):
        return "exception path, guard condition, or error construction"
    if any(term in text for term in ("parse", "format", "serialize", "deserialize", "regex", "escape", "unescape")):
        return "parser/formatter rule, literal, regex, or output-construction expression"
    if "[condition" in text or "branch" in text or " if " in text:
        return "condition, guard branch, or alternative-flow decision"
    if "[return" in text or "return" in text:
        return "return expression or returned object/value"
    if any(term in text for term in ("assign", "result", "append", "remove", "update", "set ")):
        return "assignment, mutation, or result/data-flow edge"
    return "smallest visible expression, branch, assignment, call, or return that conflicts with the issue"


def source_open_command(entry: dict[str, Any], bound: dict[str, Any]) -> str:
    repo_file = str(bound.get("repo_file") or entry.get("file") or "").replace("\\", "/").strip("/")
    excerpts = bound.get("excerpts") or []
    if repo_file and excerpts:
        first = excerpts[0]
        start = max(1, int(first.get("start_line") or 1))
        end = max(start, int(first.get("end_line") or start))
        return f"cd /testbed && sed -n '{start},{end}p' {repo_file}"
    worker = str(entry.get("worker_name") or "")
    _owners, function_candidates = worker_name_candidates(worker)
    names = [name for name in function_candidates if name]
    if repo_file and names:
        pattern = "\\|".join(f"def {name}\\|class {name}" for name in names[:3])
        return f"cd /testbed && grep -n \"{pattern}\" {repo_file} | head -20"
    if repo_file:
        return f"cd /testbed && sed -n '1,220p' {repo_file}"
    return "cd /testbed && python /tmp/spl_tools/spl_search.py \"issue behavior\""


def issue_specific_source_command(sample_dir: Path, entry: dict[str, Any], bound: dict[str, Any]) -> str | None:
    issue = read_local_problem_statement(sample_dir).lower()
    repo_file = str(bound.get("repo_file") or entry.get("file") or "").replace("\\", "/").strip("/")
    if not repo_file:
        return None
    if ("dtype" in issue or "int32" in issue or "int64" in issue or "'i4'" in issue or "'i8'" in issue) and "stack" in issue:
        return f"cd /testbed && grep -n \"def __array__\\|def dtype\\|def values\" {repo_file} | head -60"
    if "mathematica_code" in issue and ("max(" in issue or "min(" in issue or "max[" in issue or "min[" in issue):
        return f"cd /testbed && grep -n \"def _print_Max\\|def _print_Min\\|def _print_Function\\|def _print_\\|known_functions\" {repo_file} | head -100"
    if ("lognorm" in issue or "invalid vmin" in issue or "invalid vmax" in issue or "test_huge_range_log" in issue) and repo_file.endswith("image.py"):
        return f"cd /testbed && grep -n \"s_vmin\\|s_vmax\\|LogNorm\\|vrange\\|vmin\\|vmax\" {repo_file} | head -100"
    if "structured" in issue and "ndarray" in issue and ("column" in issue or "ndarraymixin" in issue):
        return f"cd /testbed && grep -n \"Structured ndarray\\|NdarrayMixin\\|len(data.dtype)\\|data_is_mixin\\|Column\" {repo_file} | head -100"
    if ("optim" in issue or "reduc" in issue) and "operation" in issue:
        return f"cd /testbed && grep -n \"def reduce\\|class .*Together\\|Alter.*Together\\|DeleteModel\" {repo_file} | head -100"
    return None


def patch_creation_command(entry: dict[str, Any], bound: dict[str, Any]) -> str:
    repo_file = str(bound.get("repo_file") or entry.get("file") or "").replace("\\", "/").strip("/")
    if repo_file:
        return f"git diff -- {repo_file} > patch.txt && sed -n '1,220p' patch.txt"
    return "git diff -- '*.py' > patch.txt && sed -n '1,220p' patch.txt"


def sibling_source_command(
    sample_dir: Path,
    entry: dict[str, Any],
    bound: dict[str, Any],
    *,
    legacy_tuned: bool = False,
) -> str | None:
    issue = read_local_problem_statement(sample_dir).lower()
    repo_file = str(bound.get("repo_file") or entry.get("file") or "").replace("\\", "/").strip("/")
    if not repo_file:
        return None
    worker = str(entry.get("worker_name") or "").lower()
    if legacy_tuned and (
        "dtype" in issue or "int32" in issue or "int64" in issue or "'i4'" in issue or "'i8'" in issue
    ) and "values" in issue:
        return f"cd /testbed && grep -n \"def __array__\\|def dtype\\|def values\" {repo_file} | head -40"
    if legacy_tuned and ("optim" in issue or "reduc" in issue) and "operation" in issue:
        return f"cd /testbed && grep -n \"def reduce\\|class .*Together\\|Alter.*Together\" {repo_file} | head -60"
    stack_functions = (
        [
            fn
            for fn in re.findall(
                r"\bin\s+([A-Za-z_][A-Za-z0-9_]*)\b",
                issue,
            )
            if len(fn) > 2
            and fn.lower() not in STOPWORDS
            and fn.lower() not in SPL_GENERIC_TERMS
        ]
        if legacy_tuned
        else extract_traceback_functions(read_local_problem_statement(sample_dir))
    )
    if stack_functions:
        pattern = "\\|".join(f"def {fn}" for fn in stack_functions[:4])
        return f"cd /testbed && grep -n \"{pattern}\" {repo_file} | head -40"
    if legacy_tuned and "mathematica_code" in issue and (
        "max(" in issue or "min(" in issue or "max[" in issue or "min[" in issue
    ):
        return f"cd /testbed && grep -n \"def _print_\\|known_functions\\|Max\\|Min\" {repo_file} | head -80"
    if legacy_tuned and (is_constructor_worker(worker) or "migration_name_fragment" in worker):
        return f"cd /testbed && grep -n \"def reduce\\|def __array__\\|def _print_\\|def make_image\\|def _make_image\" {repo_file} | head -60"
    return None


def repair_acceleration_hint(sample_dir: Path, entry: dict[str, Any]) -> str | None:
    issue = read_local_problem_statement(sample_dir).lower()
    worker = str(entry.get("worker_name") or "").lower()
    if "referenced before assignment" in issue or "unboundlocalerror" in issue or "unboundlocal" in issue:
        return (
            "For a variable-lifecycle bug ('referenced before assignment' / UnboundLocalError, "
            "where a variable is only assigned inside a loop that may not run): ADD a new "
            "`var = <default>` initialization line immediately BEFORE the loop. Do NOT move or "
            "remove the existing assignment inside the loop — that per-iteration reset must stay. "
            "The correct diff is a pure addition: exactly one '+' line and no '-' lines."
        )
    if ("dtype" in issue or "int32" in issue or "int64" in issue or "'i4'" in issue or "'i8'" in issue) and "stack" in issue:
        return "For stack/dtype issues, preserve any explicit dtype argument: use the requested dtype when provided, otherwise the stored/source dtype. Once the issue MVCE preserves dtype, do not run an edge-case sweep; create patch.txt immediately."
    if "mathematica_code" in issue and ("max(" in issue or "min(" in issue or "max[" in issue or "min[" in issue):
        return "For printer fallback issues, if no narrow _print_Max/_print_Min handler exists, add only the missing narrow handlers near existing _print_* methods. Do not add broad fallback handlers such as _print_LatticeOp."
    if ("lognorm" in issue or "invalid vmin" in issue or "invalid vmax" in issue or "test_huge_range_log" in issue) and "image.py" in str(entry.get("file") or "").lower():
        return "For LogNorm invalid vmin/vmax issues, inspect the _make_image s_vmin/s_vmax clamp first. Prefer the smallest condition/value-boundary change there before inspecting Normalize, _setattr_cm, or transform internals."
    if "structured" in issue and "ndarray" in issue and ("column" in issue or "ndarraymixin" in issue):
        return "For structured-ndarray Table issues, fix the source behavior that converts/views structured arrays. Do not submit a warning-only patch if the issue requires the resulting column type/behavior to change."
    if ("optim" in issue or "reduc" in issue) and "operation" in issue:
        return "For migration-operation optimization issues, prefer a narrow reduce() rule on the shared operation owner; avoid editing name/fragment helpers."
    if re.search(r"\.py:\d+:\s+in\s+", issue):
        return "For traceback issues, prioritize the deepest stack-frame source owner in this file and patch that path before wrappers."
    if "migration_name_fragment" in worker:
        return "This owner is probably naming context, not behavior ownership; use it only if the issue is explicitly about generated names."
    return None


def render_spl_patch_production_plan(
    sample_dir: Path,
    mode: str,
    config: dict[str, Any],
    selected_cards: list[tuple[str, dict[str, Any]]],
) -> list[str]:
    owner_cards = [
        (role, entry)
        for role, entry in selected_cards
        if role in {"PRIMARY_SOURCE_OWNER_CANDIDATE", "SECONDARY_SOURCE_OWNER_CANDIDATE"}
    ]
    if not owner_cards:
        owner_cards = selected_cards[:1]
    if not owner_cards:
        return []
    primary_role, primary = owner_cards[0]
    secondary = owner_cards[1][1] if len(owner_cards) > 1 else None
    bound = source_excerpts_for_spl_entry(sample_dir, primary, mode, config)
    legacy_tuned = uses_legacy_tuned_protocol(config)
    localization_only = mode == "miniswe_spl_localization" and not legacy_tuned
    repair_emphasis = (
        mode == "miniswe_spl_repair"
        and spl_protocol(config) == ROLE_CONDITIONED_SPL_PROTOCOL
    )
    sibling_command = sibling_source_command(
        sample_dir,
        primary,
        bound,
        legacy_tuned=legacy_tuned,
    )
    issue = read_local_problem_statement(sample_dir).lower()
    first_command = (
        issue_specific_source_command(sample_dir, primary, bound) if legacy_tuned else None
    ) or source_open_command(primary, bound)
    checkpoints = extract_spl_checkpoints(str(primary.get("spl") or ""), limit=3, max_len=150)
    lines = [
        (
            "## SPL Localization Plan"
            if localization_only
            else "## SPL Repair Plan"
            if repair_emphasis
            else "## SPL Patch Production Plan"
        ),
        "",
    ]
    if not legacy_tuned:
        lines.append(f"Controller protocol: {spl_protocol(config)}")
    lines.extend([
        (
            "Purpose: use SPL only to identify and verify a likely source owner."
            if localization_only
            else "Purpose: start from the shared localization handoff and use source-bound SPL to constrain a safe repair."
            if repair_emphasis
            else "Purpose: use SPL to reduce search steps and produce a patch within the fixed step limit."
        ),
        (
            "After localization, derive the repair from the issue, current source, and runtime evidence without further SPL guidance."
            if localization_only
            else "The owner is a stage input, not a repair claim. Verify it against current source, then use SPL behavior and preservation checkpoints while editing."
            if repair_emphasis
            else "Use this plan before any broad repository search. It is source-bound: patch only real files in /testbed."
        ),
        "",
        "Primary owner:",
        f"- Role: {primary_role}",
        f"- File: {primary.get('file')}",
        f"- Function: {primary.get('worker_name')}",
        f"- Source anchor: {bound.get('status')}",
    ])
    if legacy_tuned:
        lines.extend([
            f"- Likely edit focus: {likely_edit_focus(primary)}",
            f"- First source command to run: {first_command}",
            "- Completion trigger: after one issue-specific sanity check passes, stop searching and submit a source-only patch.",
            "- Owner-width guard: prefer a narrow named owner/expression over a broad fallback, dispatcher, constructor, wrapper, or semantic neighbor.",
        ])
    else:
        lines.extend([
            f"- First source command to run: {first_command}",
            "- Owner-width guard: prefer a narrow named owner/expression over a broad fallback, dispatcher, constructor, wrapper, or semantic neighbor.",
        ])
        if not localization_only:
            lines.extend([
                f"- Likely edit focus: {likely_edit_focus(primary)}",
                "- Completion trigger: submit only after a focused check exercises the reported behavior and passes.",
                "- Validation contract: prefer an official FAIL_TO_PASS test; otherwise use a faithful minimal reproducer. Import, syntax, and unrelated smoke checks do not qualify.",
            ])
    if not localization_only and not any(term in issue for term in ("warn", "warning", "deprecat", "message")):
        lines.append("- Side-effect guard: do not add warnings, logging, or user-facing messages unless the issue explicitly asks for them.")
    if sibling_command:
        lines.append(f"- Narrow sibling command if the first source is only context: {sibling_command}")
    hint = repair_acceleration_hint(sample_dir, primary) if legacy_tuned else None
    if hint:
        lines.append(f"- Repair acceleration hint: {hint}")
    if uses_misleading_guard(config):
        lines.append(
            "- Guard: SPL checkpoints describe PRE-FIX (current, possibly buggy) behavior. "
            "A condition/threshold or variable-lifecycle (init/reset/update) checkpoint is a "
            "fix candidate, not a spec to preserve; verify it against current source and the "
            "FAIL_TO_PASS intent before relying on it."
        )
    if checkpoints:
        lines.append("- SPL checkpoints to map onto source:")
        lines.extend([f"  - {item}" for item in checkpoints])
    if secondary is not None:
        lines.extend([
            "Secondary owner, only if the primary source visibly cannot control the issue:",
            f"- File: {secondary.get('file')}",
            f"- Function: {secondary.get('worker_name')}",
            (
                "- Use: source-owner verification only"
                if localization_only
                else f"- Focus: {likely_edit_focus(secondary)}"
            ),
        ])
    if localization_only:
        lines.extend([
            "",
            "Localization handoff:",
            "Step 1: Run the first source command and verify whether the visible source controls the reported behavior.",
            "Step 2: If it does not, inspect only the listed secondary owner before using native repository search.",
            "Step 3: Once an owner is confirmed, stop using SPL. Choose and validate the repair from current source and runtime evidence.",
            "Format rule: every response must still contain exactly one mswea_bash_command block; never answer with analysis text only.",
        ])
        return lines
    routine_heading = "Repair-stage routine:" if repair_emphasis else "Patch-production routine:"
    step_1 = (
        "Step 1: Treat the primary owner as the localization handoff. Run the first source command and verify that the visible source controls the issue behavior."
        if repair_emphasis
        else "Step 1: Run the first source command above, then decide whether that visible source owns the issue behavior."
    )
    legacy_validation_steps = [
        "Step 3: Use at most one cheap issue-specific sanity check after editing. If that check passes, do not run broad tests or edge-case sweeps; stop exploring.",
        f"Step 4: Create and inspect the patch with this command: {patch_creation_command(primary, bound)}",
        "Step 5: In the very next action submit exactly: echo COMPLETE_TASK_AND_SUBMIT_FINAL_OUTPUT && cat patch.txt",
    ]
    current_validation_steps = [
        "Step 3: Use at most two cheap focused checks after editing: the reported behavior first, then the nearest regression only if needed. Do not run broad suites or edge-case sweeps.",
        f"Step 4: Create and inspect the patch with this command: {patch_creation_command(primary, bound)}",
        "Step 5: After a qualifying behavior check passes and patch.txt is non-empty and plausible, submit exactly: echo COMPLETE_TASK_AND_SUBMIT_FINAL_OUTPUT && cat patch.txt",
    ]
    guarded_validation_steps = [
        "Step 3: Use at most two cheap focused checks after editing: (a) a minimal reproducer of the reported FAIL_TO_PASS behavior, and (b) one narrow regression check that neighboring behavior still holds (the normal non-degenerate case, not just the failing edge case). Do not run broad suites.",
        f"Step 4: Create the patch with this command: {patch_creation_command(primary, bound)}. Then inspect it and explicitly restate every line you ADDED (starts with '+') and every line you REMOVED (starts with '-'). If you only meant to ADD an initialization or guard, the diff must be a pure addition with no '-' lines; a '-' line right next to a '+' means you moved a line instead of adding a fallback — restore the removed line.",
        "Step 5: After both checks pass and the diff shows only your intended change, submit exactly: echo COMPLETE_TASK_AND_SUBMIT_FINAL_OUTPUT && cat patch.txt",
    ]
    if uses_misleading_guard(config):
        validation_steps = guarded_validation_steps
    elif legacy_tuned:
        validation_steps = legacy_validation_steps
    else:
        validation_steps = current_validation_steps
    lines.extend([
        "",
        routine_heading,
        step_1,
        "Step 2: If it owns the behavior, edit the smallest source construct in that file/function. Do not inspect unrelated SPL cards.",
        *validation_steps,
        "Budget rule: after a source owner maps to the issue, do not spend more than two additional search/read commands before editing.",
        "Format rule: every response must still contain exactly one mswea_bash_command block; never answer with analysis text only.",
    ])
    return lines


def render_source_bound_card_lines(
    sample_dir: Path,
    mode: str,
    config: dict[str, Any],
    *,
    card_number: int,
    role: str,
    entry: dict[str, Any],
    spl_chars: int,
) -> list[str]:
    bound = source_excerpts_for_spl_entry(sample_dir, entry, mode, config)
    checkpoints = extract_spl_checkpoints(str(entry.get("spl") or ""), limit=4)
    lines = [
        "",
        f"### SPL Controller Card {card_number}",
        f"Role: {role}",
        f"File: {entry.get('file')}",
        f"Function: {entry.get('worker_name')}",
        f"Source anchor: {bound['status']}",
        f"SPL score: {entry.get('_spl_score')}",
        "Matched terms: " + ", ".join(entry.get("_spl_matched_terms", [])[:10]),
        "Summary: " + str(entry.get("summary") or ""),
        "Use this card as: real source owner + SPL behavior checklist. Patch only the source excerpt/file, never the SPL text.",
    ]
    if uses_misleading_guard(config):
        lines.append(SPL_MISLEADING_GUARD)
    excerpts = bound.get("excerpts") or []
    if excerpts:
        for idx, excerpt in enumerate(excerpts, start=1):
            lines.extend([
                f"Editable source excerpt {idx}: {bound['repo_file']}:{excerpt['start_line']}-{excerpt['end_line']}",
                "```python",
                str(excerpt.get("code") or ""),
                "```",
            ])
    else:
        lines.extend([
            "Editable source excerpt: UNRESOLVED. Open the real file and map this SPL card to source before editing.",
        ])
    lines.extend([
        "SPL checkpoints:",
        *([f"- {item}" for item in checkpoints] if checkpoints else ["- No compact checkpoint extracted; use the summary only as a source-inspection hint."]),
        "SPL checklist excerpt:",
        "```",
        trim_text(str(entry.get("spl") or ""), spl_chars),
        "```",
    ])
    return lines


def load_trimmed_spl_index(sample_dir: Path, config: dict[str, Any]) -> dict[str, Any] | None:
    path = sample_dir / "spl_index.json"
    if not path.exists():
        return None
    entries = ranked_spl_entries(sample_dir, config)
    limit = max(1, int(config.get("mini_spl_tool_entry_limit", 80)))
    max_chars = max(200, int(config.get("mini_spl_entry_max_chars", 1400)))
    trimmed_entries: list[dict[str, Any]] = []
    for entry in entries[:limit]:
        if not isinstance(entry, dict):
            continue
        trimmed_entries.append({
            "file": entry.get("file"),
            "worker_name": entry.get("worker_name"),
            "summary": entry.get("summary"),
            "spl_score": entry.get("_spl_score"),
            "matched_terms": entry.get("_spl_matched_terms", []),
            "spl": trim_text(str(entry.get("spl") or ""), max_chars),
        })
    data = read_json(path)
    return {
        "instance_id": data.get("instance_id") if isinstance(data, dict) else None,
        "entries": trimmed_entries,
        "entry_count": len(trimmed_entries),
        "note": "Issue-ranked source-derived SPL entries for mini-SWE-agent tool use.",
    }


def build_spl_controller_block(sample_dir: Path, mode: str, config: dict[str, Any]) -> str:
    if "spl" not in mode:
        return ""
    if mode == "miniswe_spl_repair" and uses_strict_stage_isolated_protocol(config):
        if not (sample_dir / "spl_index.json").exists():
            return ""
        return "\n".join([
            "## SPL Repair Access",
            "",
            f"Controller protocol: {spl_protocol(config)}",
            "Localize the failing source owner with native repository tools first.",
            "Do not use SPL to choose a file or function.",
            "After current source evidence identifies an owner, query only that owner with:",
            '`python /tmp/spl_tools/spl_search.py "<repo file> <function or class>"`',
            "Use the returned SPL checkpoint only for repair impact/preservation analysis.",
            "Verify every SPL-derived claim against current source before editing.",
            "If SPL does not match the source owner, ignore it and continue natively.",
        ])
    selected_cards = selected_spl_controller_cards(sample_dir, mode, config)
    if not selected_cards:
        return ""
    _card_limit, spl_chars = spl_controller_budget(mode, config)
    localization_only = (
        mode == "miniswe_spl_localization"
        and not uses_legacy_tuned_protocol(config)
    )
    repair_emphasis = (
        mode == "miniswe_spl_repair"
        and spl_protocol(config) == ROLE_CONDITIONED_SPL_PROTOCOL
    )
    lines = [
        "## SPL Controller Cards",
        "",
        "These source-bound cards were selected from the full SPL index using the issue text and bound to real source excerpts when possible.",
        (
            "SPL is used only for source-owner localization in this condition."
            if localization_only
            else "This condition receives a shared owner handoff and uses SPL for source-bound repair reasoning and preservation checks."
            if repair_emphasis
            else "SPL is a structured natural-language view of source behavior. Here it is used to shorten the path to a patch, not to add broad extra context."
        ),
        "A full copy of these cards is available at `/tmp/spl_tools/source_bound_cards.md`, but do not open it unless the embedded plan is insufficient.",
        "",
        "Workflow:",
    ]
    if localization_only:
        lines.extend([
            "Step 1: Follow the SPL Localization Plan and inspect its first real source owner.",
            "Step 2: Map one SPL checkpoint to visible source only to verify ownership.",
            "Step 3: Once ownership is confirmed, stop using SPL and repair using the issue, current source, and runtime evidence.",
            "",
        ])
    elif repair_emphasis:
        lines.extend([
            "Step 1: Start from the embedded owner handoff and verify it against the visible current source.",
            "Step 2: Map SPL behavior and preservation checkpoints onto that owner; use them to choose the smallest safe edit.",
            "Step 3: If the handoff is visibly wrong, fall back to native search and record that the owner handoff failed.",
            "Step 4: After editing, run a focused check that exercises the reported behavior; use at most one additional narrow regression check, then create and inspect patch.txt.",
            "",
        ])
    else:
        if uses_legacy_tuned_protocol(config):
            lines.extend([
                "Step 1: Follow the SPL Patch Production Plan first. Run its first source command before broad repository search.",
                "Step 2: Map one SPL checkpoint to visible source. If it maps, edit the smallest source construct that conflicts with the issue.",
                "Step 3: Use secondary/context cards only if the primary source visibly cannot control the issue.",
                "Step 4: After editing, run at most one issue-specific sanity check. If it passes, do not run edge-case sweeps; create patch.txt and inspect it.",
                "Step 5: Submit in the next action after patch.txt looks plausible. Do not spend extra steps reprinting, re-searching, re-testing, or tracing internals unless the patch just failed.",
                "",
            ])
        else:
            lines.extend([
                "Step 1: Follow the SPL Patch Production Plan first. Run its first source command before broad repository search.",
                "Step 2: Map one SPL checkpoint to visible source. If it maps, edit the smallest source construct that conflicts with the issue.",
                "Step 3: Use secondary/context cards only if the primary source visibly cannot control the issue.",
                "Step 4: After editing, run a focused check that exercises the reported behavior. Import, syntax, and unrelated smoke checks do not qualify; use at most one additional narrow regression check.",
                "Step 5: Submit after the qualifying check passes and patch.txt looks plausible. Do not spend extra steps reprinting, broad-searching, or tracing unrelated internals.",
                "",
            ])
    lines.extend([
        "Card roles:",
        "- PRIMARY_SOURCE_OWNER_CANDIDATE / SECONDARY_SOURCE_OWNER_CANDIDATE: inspect this real source owner first.",
        "- SOURCE_BOUND_CONTEXT_CHECK: use only to preserve nearby behavior or inspect a narrow sibling after source evidence.",
        "- WEAK_CONTEXT_ONLY: ignore for owner choice; use only if source search independently reaches it.",
        "",
    ])
    plan_lines = render_spl_patch_production_plan(sample_dir, mode, config, selected_cards)
    if plan_lines:
        lines.extend(plan_lines)
        lines.append("")
    lines.extend([
        "Selected cards:",
    ])
    visible_cards = selected_cards[: prompt_card_limit(mode, config)]
    for card_number, (role, entry) in enumerate(visible_cards, start=1):
        lines.extend(render_source_bound_card_lines(
            sample_dir,
            mode,
            config,
            card_number=card_number,
            role=role,
            entry=entry,
            spl_chars=spl_chars,
        ))
    hidden_count = max(0, len(selected_cards) - len(visible_cards))
    if hidden_count:
        lines.extend([
            "",
            f"{hidden_count} additional context card(s) are available in /tmp/spl_tools/source_bound_cards.md.",
            "Open them only if the primary and secondary source owners are visibly wrong.",
        ])
    return "\n".join(lines).strip()


def build_source_bound_cards_document(sample_dir: Path, mode: str, config: dict[str, Any]) -> str:
    if "spl" not in mode:
        return ""
    if mode == "miniswe_spl_repair" and uses_strict_stage_isolated_protocol(config):
        return ""
    selected_cards = selected_spl_controller_cards(sample_dir, mode, config)
    if not selected_cards:
        return ""
    _card_limit, spl_chars = spl_controller_budget(mode, config)
    lines = [
        "# Source-Bound SPL Cards",
        "",
        "Each card binds one issue-ranked SPL entry to the corresponding real source excerpt when the source anchor can be resolved.",
        "Use these cards to navigate and check behavior, but patch only real files in `/testbed`.",
        "",
    ]
    plan_lines = render_spl_patch_production_plan(sample_dir, mode, config, selected_cards)
    if plan_lines:
        lines.extend(plan_lines)
        lines.append("")
    for card_number, (role, entry) in enumerate(selected_cards, start=1):
        lines.extend(render_source_bound_card_lines(
            sample_dir,
            mode,
            config,
            card_number=card_number,
            role=role,
            entry=entry,
            spl_chars=spl_chars,
        ))
    return "\n".join(lines).strip() + "\n"


def build_payload_files(sample_dir: Path, mode: str, config: dict[str, Any]) -> dict[str, str]:
    files: dict[str, str] = {
        "/tmp/spl_tools/spl_search.py": SPL_SEARCH_SCRIPT,
        "/tmp/spl_tools/spl_show.py": SPL_SHOW_SCRIPT,
        "/tmp/spl_tools/free_summary_search.py": FREE_SUMMARY_SEARCH_SCRIPT,
    }
    if "spl" in mode:
        spl_index = load_trimmed_spl_index(sample_dir, config)
        if spl_index:
            files["/tmp/spl_tools/spl_index.json"] = json.dumps(spl_index, ensure_ascii=False, indent=2)
        bound_cards = build_source_bound_cards_document(sample_dir, mode, config)
        if bound_cards:
            files["/tmp/spl_tools/source_bound_cards.md"] = bound_cards
            if mode != "miniswe_spl_repair" or not uses_strict_stage_isolated_protocol(config):
                plan_text = "\n".join(
                    render_spl_patch_production_plan(
                        sample_dir,
                        mode,
                        config,
                        selected_spl_controller_cards(sample_dir, mode, config),
                    )
                ).strip()
                if plan_text:
                    files["/tmp/spl_tools/patch_plan.md"] = plan_text + "\n"
        spl_context = sample_dir / "spl_context.txt"
        if spl_context.exists():
            files["/tmp/spl_tools/spl_context.txt"] = trim_text(
                spl_context.read_text(encoding="utf-8", errors="replace"),
                int(config.get("mini_spl_entry_limit", 8)) * int(config.get("mini_spl_entry_max_chars", 1800)),
            )
    if "free_summary" in mode:
        summary_path = sample_dir / "free_summary_context.txt"
        if summary_path.exists():
            files["/tmp/spl_tools/free_summary_context.txt"] = trim_text(
                summary_path.read_text(encoding="utf-8", errors="replace"),
                int(config.get("mini_free_summary_max_chars", 12000)),
            )
    return files


def build_startup_command(sample_dir: Path, mode: str, config: dict[str, Any]) -> str | None:
    if "spl" not in mode and "free_summary" not in mode:
        return None
    payload = []
    for path, text in build_payload_files(sample_dir, mode, config).items():
        payload.append({
            "path": path,
            "b64": base64.b64encode(text.encode("utf-8")).decode("ascii"),
            "executable": path.endswith(".py"),
        })
    payload_json = json.dumps(payload, ensure_ascii=True)
    return (
        "python - <<'PY'\n"
        "import base64, json, os\n"
        "from pathlib import Path\n"
        f"payload = json.loads({payload_json!r})\n"
        "for item in payload:\n"
        "    path = Path(item['path'])\n"
        "    path.parent.mkdir(parents=True, exist_ok=True)\n"
        "    path.write_bytes(base64.b64decode(item['b64']))\n"
        "    if item.get('executable'):\n"
        "        os.chmod(path, 0o755)\n"
        "print('Installed mini-SWE-agent auxiliary context in /tmp/spl_tools')\n"
        "PY"
    )


def materialize_payload_dir(sample_dir: Path, mode: str, config: dict[str, Any], out_dir: Path) -> Path | None:
    if "spl" not in mode and "free_summary" not in mode:
        return None
    payload_dir = out_dir / "payload_tools"
    if payload_dir.exists():
        shutil.rmtree(payload_dir)
    payload_dir.mkdir(parents=True, exist_ok=True)
    for container_path, text in build_payload_files(sample_dir, mode, config).items():
        rel_name = container_path.replace("\\", "/").split("/tmp/spl_tools/", 1)[-1]
        target = payload_dir / rel_name
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(text, encoding="utf-8", newline="\n")
    return payload_dir


def load_base_mini_config(config: dict[str, Any]) -> dict[str, Any]:
    repo = resolve_in_project(config.get("mini_swe_agent_repo", "code/third_party/mini_swe_agent/repo"))
    base_name = str(config.get("mini_base_config", "swebench_backticks.yaml"))
    base_path = repo / "src" / "minisweagent" / "config" / "benchmarks" / base_name
    if not base_path.exists():
        raise FileNotFoundError(f"mini-SWE-agent base config not found: {base_path}")
    return yaml.safe_load(base_path.read_text(encoding="utf-8"))


def build_mini_config(
    *,
    config: dict[str, Any],
    sample_dir: Path,
    out_dir: Path,
    mode: str,
    api_key: str | None,
) -> Path:
    mini_config = load_base_mini_config(config)
    addendum = load_prompt_addendum(mode, config)
    agent = mini_config.setdefault("agent", {})
    if addendum:
        agent["instance_template"] = str(agent.get("instance_template", "")).rstrip() + "\n\n" + addendum + "\n"
    controller_block = build_spl_controller_block(sample_dir, mode, config)
    if controller_block:
        agent["instance_template"] = str(agent.get("instance_template", "")).rstrip() + "\n\n" + controller_block + "\n"
        model = mini_config.setdefault("model", {})
        if uses_legacy_tuned_protocol(config):
            progress_rule = """
<spl_progress_rule>
If this is an SPL variant and you have already edited source code:
- after one issue-specific sanity check passes, your next command must create and inspect patch.txt;
- after a non-empty patch.txt has been inspected, your next command must be exactly `echo COMPLETE_TASK_AND_SUBMIT_FINAL_OUTPUT && cat patch.txt`;
- do not start a new broad search, dispatcher investigation, or edge-case sweep after a passing issue-specific check.
</spl_progress_rule>
"""
        else:
            progress_rule = """
<spl_progress_rule>
If this is an SPL variant and you have already edited source code:
- a qualifying check must execute the reported behavior, preferably the official FAIL_TO_PASS test or a faithful minimal reproducer;
- import, syntax, and unrelated smoke checks do not qualify as behavioral validation;
- after a qualifying focused check passes, create and inspect patch.txt without starting a new broad search or edge-case sweep;
- after a non-empty plausible patch.txt has been inspected, submit with `echo COMPLETE_TASK_AND_SUBMIT_FINAL_OUTPUT && cat patch.txt`.
</spl_progress_rule>
"""
        model["observation_template"] = str(model.get("observation_template", "")).rstrip() + "\n" + progress_rule + "\n"
    agent["step_limit"] = int(config.get("mini_step_limit", agent.get("step_limit", 36)))
    agent["cost_limit"] = float(config.get("mini_cost_limit", agent.get("cost_limit", 0)))
    agent["wall_time_limit_seconds"] = int(
        config.get("mini_wall_time_limit_seconds", agent.get("wall_time_limit_seconds", 1800) or 1800)
    )
    agent["confirm_exit"] = False

    environment = mini_config.setdefault("environment", {})
    environment["timeout"] = int(config.get("mini_environment_timeout_seconds", environment.get("timeout", 60)))
    environment["pull_timeout"] = int(
        config.get(
            "mini_docker_pull_timeout_seconds",
            config.get("mini_environment_timeout_seconds", environment.get("pull_timeout", 120)),
        )
    )
    environment["container_timeout"] = str(config.get("mini_container_timeout", environment.get("container_timeout", "2h")))
    environment["environment_class"] = "docker"
    if bool(config.get("mini_activate_testbed_conda", True)):
        conda_env = str(config.get("mini_conda_env_name", "testbed"))
        environment["interpreter"] = [
            "bash",
            "-lc",
            f"source /opt/miniconda3/bin/activate {conda_env} >/dev/null 2>&1 && eval \"$1\"",
            "mini_cmd",
        ]

    model_name = str(config.get("mini_model_name") or config.get("model") or "gpt-4o-mini")
    model = mini_config.setdefault("model", {})
    model["model_name"] = model_name
    model["model_class"] = str(config.get("mini_model_class", "litellm_textbased"))
    model["cost_tracking"] = "ignore_errors"
    model_kwargs = dict(model.get("model_kwargs") or {})
    model_kwargs["temperature"] = float(config.get("temperature", 0))
    model_kwargs["drop_params"] = True
    model_kwargs["custom_llm_provider"] = str(config.get("mini_custom_llm_provider", "openai"))
    api_base = normalize_api_base(config.get("base_url"))
    if api_base:
        model_kwargs["api_base"] = api_base
    if config.get("openai_timeout_seconds") is not None:
        model_kwargs["timeout"] = int(config.get("openai_timeout_seconds"))
    model["model_kwargs"] = model_kwargs

    config_path = out_dir / "mini_config.yaml"
    config_path.write_text(yaml.safe_dump(mini_config, sort_keys=False, allow_unicode=False), encoding="utf-8", newline="\n")
    return config_path


def extract_submission_from_traj(path: Path) -> tuple[str, dict[str, Any]]:
    if not path.exists():
        return "", {}
    data = read_json(path)
    info = data.get("info") if isinstance(data, dict) else {}
    submission = str((info or {}).get("submission") or "")
    return submission, data if isinstance(data, dict) else {}


def extract_usage_from_traj(data: dict[str, Any]) -> dict[str, Any]:
    prompt_tokens = completion_tokens = total_tokens = 0
    calls = 0
    for message in data.get("messages", []) if isinstance(data, dict) else []:
        extra = message.get("extra") if isinstance(message, dict) else None
        response = (extra or {}).get("response") if isinstance(extra, dict) else None
        usage = response.get("usage") if isinstance(response, dict) else None
        if not isinstance(usage, dict):
            continue
        calls += 1
        prompt_tokens += int(usage.get("prompt_tokens") or usage.get("input_tokens") or 0)
        completion_tokens += int(usage.get("completion_tokens") or usage.get("output_tokens") or 0)
        total_tokens += int(usage.get("total_tokens") or 0)
    if total_tokens == 0:
        total_tokens = prompt_tokens + completion_tokens
    model_stats = ((data.get("info") or {}).get("model_stats") or {}) if isinstance(data, dict) else {}
    return {
        "calls": calls or int(model_stats.get("api_calls") or 0),
        "input_tokens": prompt_tokens,
        "output_tokens": completion_tokens,
        "reasoning_tokens": 0,
        "total_tokens": total_tokens,
        "raw_usage": {"model_stats": model_stats},
    }


def parse_stdout_submission(stdout: str) -> str:
    marker = "COMPLETE_TASK_AND_SUBMIT_FINAL_OUTPUT"
    idx = stdout.find(marker)
    if idx < 0:
        return ""
    return stdout[idx + len(marker):].lstrip()


def clean_output_dir(out_dir: Path, run_dir: Path) -> None:
    if not out_dir.exists():
        return
    resolved_out = out_dir.resolve()
    resolved_run = run_dir.resolve()
    if resolved_run == resolved_out or resolved_run not in resolved_out.parents:
        raise ValueError(f"Refusing to clean output path outside run_dir: {resolved_out}")
    # Keep the caller's short/junction path for the filesystem operation on
    # Windows. The resolved path above is used only for the containment check;
    # resolving it here reintroduces the legacy MAX_PATH failure.
    shutil.rmtree(out_dir)


def condition_output_complete(out_dir: Path, mode: str, expected_spl_protocol: str) -> bool:
    required = [
        out_dir / "baseline_status.json",
        out_dir / "call_metadata.json",
        out_dir / "patch.diff",
        out_dir / "condition_complete.json",
    ]
    if not all(path.exists() for path in required):
        return False
    try:
        marker = read_json(out_dir / "condition_complete.json")
        status = read_json(out_dir / "baseline_status.json")
        read_json(out_dir / "call_metadata.json")
    except Exception:
        return False
    if marker.get("complete") is not True or marker.get("mode") != mode or status.get("mode") != mode:
        return False
    if "spl" in mode:
        # Artifacts written before protocol versioning are historical legacy-v0
        # outputs. Never resume them into a differently versioned SPL protocol.
        recorded_protocol = str(marker.get("spl_protocol") or LEGACY_SPL_PROTOCOL)
        if recorded_protocol != expected_spl_protocol:
            return False
    return True


def run_mode(
    config: dict[str, Any],
    item: dict[str, Any],
    mode: str,
    key_pool: ApiKeyPool | FileApiKeyLeasePool | None = None,
) -> str:
    short_root_value = (
        config.get("windows_short_project_root")
        or os.environ.get("EXP6_WINDOWS_SHORT_PROJECT_ROOT")
    ) if os.name == "nt" else None
    short_root = Path(str(short_root_value)) if short_root_value else None

    def work_path(path: Path) -> Path:
        if short_root is None:
            return path
        relative = path.resolve().relative_to(PROJECT_ROOT.resolve())
        return short_root / relative

    sample_dir = work_path(resolve_in_project(item["sample_dir"]))
    run_dir = work_path(ensure_dir(resolve_in_project(config["run_dir"])))
    safe_id = str(item["instance_id"]).replace("/", "__")
    out_dir = run_dir / safe_id / mode
    protocol = spl_protocol(config)
    if config.get("resume_existing_conditions", False) and condition_output_complete(out_dir, mode, protocol):
        return mode
    clean_output_dir(out_dir, run_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    write_text(out_dir / "mode.txt", mode)
    write_json(
        out_dir / "handoff.json",
        {
            "item": item,
            "sample_dir": str(sample_dir),
            "mode": mode,
            "spl_protocol": protocol if "spl" in mode else None,
        },
    )

    acquired_key: str | None = None
    if key_pool is not None:
        acquired_key = key_pool.acquire()
    elif config.get("api_key"):
        acquired_key = str(config.get("api_key"))
    elif config.get("api_key_env") and os.environ.get(str(config.get("api_key_env"))):
        acquired_key = os.environ[str(config.get("api_key_env"))]

    started = time.perf_counter()
    mini_config_path = build_mini_config(
        config=config,
        sample_dir=sample_dir,
        out_dir=out_dir,
        mode=mode,
        api_key=acquired_key,
    )
    payload_dir = materialize_payload_dir(sample_dir, mode, config, out_dir)

    repo = work_path(resolve_in_project(config.get("mini_swe_agent_repo", "code/third_party/mini_swe_agent/repo")))
    traj_path = out_dir / f"{safe_id}.traj.json"
    instance_jsonl = sample_dir / "swebench_instance.jsonl"
    if not instance_jsonl.exists():
        raise FileNotFoundError(f"Missing sanitized SWE-bench instance JSONL: {instance_jsonl}")
    def child_path(path: Path) -> str:
        if short_root is None:
            return str(path)
        try:
            path.relative_to(short_root)
            return str(path)
        except ValueError:
            pass
        relative = path.relative_to(PROJECT_ROOT)
        return str(short_root / relative)

    command = [
        sys.executable,
        child_path(Path(__file__).resolve().parent / "mini_runner.py"),
        "--mini-src",
        child_path(repo / "src"),
        "--mini-config",
        child_path(mini_config_path),
        "--instance-jsonl",
        child_path(instance_jsonl),
        "--output",
        child_path(traj_path),
    ]
    if payload_dir is not None:
        command.extend(["--tool-dir", child_path(payload_dir)])
    write_text(out_dir / "command_00.txt", " ".join(command))

    env = os.environ.copy()
    env["PYTHONPATH"] = child_path(repo / "src") + os.pathsep + env.get("PYTHONPATH", "")
    env.setdefault("PYTHONUTF8", "1")
    env.setdefault("PYTHONIOENCODING", "utf-8")
    env.setdefault("PYTHONUNBUFFERED", "1")
    if acquired_key:
        env["OPENAI_API_KEY"] = acquired_key
    if config.get("base_url"):
        env["OPENAI_API_BASE"] = str(config["base_url"])
        env["OPENAI_BASE_URL"] = str(config["base_url"])
    if config.get("hf_home"):
        env["HF_HOME"] = str(resolve_in_project(config["hf_home"]))
    if config.get("hf_datasets_cache"):
        env["HF_DATASETS_CACHE"] = str(resolve_in_project(config["hf_datasets_cache"]))
    if config.get("hf_offline", False):
        env["HF_DATASETS_OFFLINE"] = "1"
        env["HF_HUB_OFFLINE"] = "1"
        env["TRANSFORMERS_OFFLINE"] = "1"
    env["MSWEA_COST_TRACKING"] = "ignore_errors"

    try:
        result = subprocess.run(
            command,
            cwd=str(short_root or PROJECT_ROOT),
            env=env,
            text=True,
            capture_output=True,
            encoding="utf-8",
            errors="replace",
            timeout=int(config.get("mini_command_timeout_seconds", 7200)),
        )
        returncode = result.returncode
        stdout = result.stdout or ""
        stderr = result.stderr or ""
    except subprocess.TimeoutExpired as exc:
        returncode = None
        stdout = exc.stdout if isinstance(exc.stdout, str) else ""
        stderr = exc.stderr if isinstance(exc.stderr, str) else ""
        stderr += f"\nTIMEOUT after {int(config.get('mini_command_timeout_seconds', 7200))} seconds"
    finally:
        if acquired_key is not None and key_pool is not None:
            key_pool.release(acquired_key)

    elapsed = time.perf_counter() - started
    write_text(out_dir / "stdout_00.txt", stdout[-60000:])
    write_text(out_dir / "stderr_00.txt", stderr[-60000:])

    patch, traj_data = extract_submission_from_traj(traj_path)
    if not patch:
        patch = parse_stdout_submission(stdout)
    write_text(out_dir / "patch.diff", patch)

    usage = extract_usage_from_traj(traj_data)
    exit_status = ((traj_data.get("info") or {}).get("exit_status") if isinstance(traj_data, dict) else None) or ""
    available = bool(patch.strip()) and returncode == 0
    status = {
        "available": available,
        "mode": mode,
        "spl_protocol": protocol if "spl" in mode else None,
        "source": "mini_swe_agent_v2",
        "mini_config": str(mini_config_path),
        "trajectory": str(traj_path),
        "commands": [{"index": 0, "stage": "mini_swe_agent", "command": " ".join(command), "returncode": returncode}],
        "exit_status": exit_status,
        "elapsed_seconds": elapsed,
        "failure": None if available else {
            "stage": "mini_swe_agent",
            "returncode": returncode,
            "exit_status": exit_status,
            "stderr_tail": stderr[-4000:],
            "stdout_tail": stdout[-2000:],
        },
        "note": "Experiment 6 runs mini-SWE-agent v2. SPL/free-summary variants copy auxiliary files/tools into /tmp/spl_tools inside the mini container; the original condition does not.",
    }
    write_json(out_dir / "baseline_status.json", status)
    write_json(
        out_dir / "call_metadata.json",
        {
            "role": "swebench_miniswe",
            "condition": mode,
            "provider": "mini_swe_agent_v2",
            "model": config.get("mini_model_name") or config.get("model"),
            "spl_protocol": protocol if "spl" in mode else None,
            "elapsed_seconds": elapsed,
            "llm_elapsed_seconds": elapsed,
            **usage,
        },
    )
    write_json(
        out_dir / "condition_complete.json",
        {
            "complete": True,
            "instance_id": item["instance_id"],
            "mode": mode,
            "spl_protocol": protocol if "spl" in mode else None,
            "patch_chars": len(patch),
            "available": available,
            "elapsed_seconds": elapsed,
        },
    )
    return mode


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", required=True)
    args = parser.parse_args()
    config = read_config(resolve_in_project(args.config))
    if os.environ.get("EXP6_RECOVERY_MAX_WORKERS"):
        config["max_workers"] = int(os.environ["EXP6_RECOVERY_MAX_WORKERS"])
    if os.environ.get("EXP6_RECOVERY_ENVIRONMENT_TIMEOUT_SECONDS"):
        timeout_value = int(os.environ["EXP6_RECOVERY_ENVIRONMENT_TIMEOUT_SECONDS"])
        config["mini_environment_timeout_seconds"] = timeout_value
        config["mini_docker_pull_timeout_seconds"] = timeout_value
    if os.environ.get("EXP6_FORCE_RESUME_EXISTING_CONDITIONS") == "1":
        config["resume_existing_conditions"] = True

    artifact_dir = resolve_in_project(config["artifact_dir"])
    manifest = selected_items(read_json(artifact_dir / "manifest.json"), config)
    modes = list(config.get("conditions", []))
    work_items = [{"item": item, "mode": mode} for item in manifest for mode in modes]

    keys = [str(key).strip() for key in config.get("api_keys", []) if str(key).strip()]
    if config.get("api_key") and str(config["api_key"]).strip() not in keys:
        keys.insert(0, str(config["api_key"]).strip())
    pool_path = resolve_in_project(config["api_key_pool_file"]) if config.get("api_key_pool_file") else None
    if pool_path is not None and pool_path.is_file():
        key_pool = FileApiKeyLeasePool(pool_path)
    else:
        # The pool directory is not shipped — it holds live credentials.  Fall
        # back to the keys in the environment, as `ModelClient.get_key_pool`
        # does, so one key in `.env` is enough to run the shipped configs.
        key_pool = ApiKeyPool(keys, max_per_key=int(config.get("max_per_key", 1))) if len(keys) > 1 else None

    def work(row: dict[str, Any]) -> str:
        return run_mode(config, row["item"], row["mode"], key_pool)

    _results, errors = run_ordered(
        work_items,
        work,
        int(config.get("max_workers", 1)),
        bool(config.get("continue_on_error", True)),
    )
    run_dir = ensure_dir(resolve_in_project(config["run_dir"]))
    if errors:
        write_json(run_dir / "run_errors.json", errors)
    print(f"Wrote SWE-bench Verified mini-SWE-agent runs to {run_dir}")


if __name__ == "__main__":
    main()
