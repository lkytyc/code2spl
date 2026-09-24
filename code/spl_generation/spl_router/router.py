from __future__ import annotations

import json
import time
from dataclasses import asdict
from pathlib import Path
from typing import Any

from spl_core.dependencies import build_dependency_graph
from spl_core.hashing import sha256_text
from spl_core.symbols import SourceSymbol, extract_symbols_from_file, iter_source_files

from .generator_adapter import ExistingSPLGeneratorAdapter


ROUTER_VERSION = 1
DEFAULT_MAX_CANDIDATES = 5
DEFAULT_GENERATION_BUDGET = 3
DEFAULT_SCOPE_PATHS = ["."]


class SPLRouter:
    """On-demand SPL orchestration for Codex-facing tools.

    Static indexing is deliberately LLM-free. SPL generation happens only for
    task-selected function/method candidates within a bounded budget.
    """

    def __init__(
        self,
        repository_path: str | Path,
        index_dir: str | Path | None = None,
        config: dict[str, Any] | None = None,
        event_log: str | Path | None = None,
    ):
        self.repository_path = Path(repository_path).resolve()
        self.index_dir = Path(index_dir).resolve() if index_dir else self.repository_path / ".spl_router"
        self.index_path = self.index_dir / "static_index.json"
        self.cache_path = self.index_dir / "spl_cache.json"
        self.config = config or {}
        self.event_log = Path(event_log).resolve() if event_log else None

    def understand(
        self,
        task: str,
        scope_paths: list[str] | None = None,
        max_candidates: int = DEFAULT_MAX_CANDIDATES,
        generation_budget: int = DEFAULT_GENERATION_BUDGET,
        include_patterns: list[str] | None = None,
        exclude_patterns: list[str] | None = None,
        instance_id: str | None = None,
        condition: str | None = None,
    ) -> dict[str, Any]:
        started = time.perf_counter()
        index = self._load_or_build_index(include_patterns, exclude_patterns)
        cache = self._load_cache()
        max_candidates = _bounded_int(max_candidates, 1, 8)
        generation_budget = _bounded_int(generation_budget, 0, 8)
        scope_paths = scope_paths or DEFAULT_SCOPE_PATHS
        terms = _terms(task)
        scored: list[tuple[float, list[str], dict[str, Any]]] = []
        for symbol in index.get("symbols", []):
            if not _in_scope(symbol["file"], scope_paths):
                continue
            haystack = " ".join([
                (symbol.get("symbol", "") + " ") * 4,
                (symbol.get("summary_hint", "") + " ") * 3,
                symbol.get("file", ""),
                _identifier_text(symbol.get("code", "")),
                " ".join(symbol.get("calls", [])),
                " ".join(symbol.get("state_changes", [])),
            ])
            score, hits = _score(terms, haystack)
            if score > 0:
                scored.append((score, hits, symbol))
        scored.sort(key=lambda row: row[0], reverse=True)

        generator = ExistingSPLGeneratorAdapter(self.config)
        candidates: list[dict[str, Any]] = []
        cache_hits = 0
        generated = 0
        budget_exhausted = False
        for score, hits, symbol in scored[:max_candidates]:
            cache_key = self._cache_key(symbol)
            cache_entry = cache.get("entries", {}).get(cache_key)
            status = "budget_exhausted"
            spl_text = ""
            spl_metadata: dict[str, Any] = {}
            if cache_entry:
                status = "cache_hit"
                cache_hits += 1
                spl_text = cache_entry.get("spl", "")
                spl_metadata = cache_entry.get("metadata", {})
            elif generated < generation_budget:
                generated_result = generator.generate(_symbol_from_dict(symbol))
                status = "generated"
                generated += 1
                spl_text = generated_result.text
                spl_metadata = generated_result.metadata
                cache.setdefault("entries", {})[cache_key] = {
                    "symbol_id": symbol["symbol_id"],
                    "source_hash": symbol["content_hash"],
                    "schema_version": self.config.get("spl_schema_version", "current"),
                    "prompt_version": self.config.get("spl_prompt_version", "existing"),
                    "generator_version": "common.spl_adapter",
                    "generated_at": time.time(),
                    "spl": spl_text,
                    "metadata": spl_metadata,
                }
            else:
                budget_exhausted = True

            candidates.append({
                "symbol_id": symbol["symbol_id"],
                "symbol": symbol["symbol"],
                "file_path": symbol["file"],
                "start_line": symbol["start_line"],
                "end_line": symbol["end_line"],
                "language": symbol["language"],
                "score": round(score, 4),
                "retrieval_reason": _reason(hits),
                "spl_status": status,
                "source_hash": symbol["content_hash"],
                "fresh": True,
                "spl": spl_text,
                "spl_metadata": _compact_metadata(spl_metadata),
            })

        self._save_cache(cache)
        duration_ms = int((time.perf_counter() - started) * 1000)
        result = {
            "task_hash": sha256_text(task),
            "repository_path": str(self.repository_path),
            "candidates": candidates,
            "generation_count": generated,
            "cache_hit_count": cache_hits,
            "budget_exhausted": budget_exhausted,
            "static_index_symbol_count": len(index.get("symbols", [])),
            "duration_ms": duration_ms,
            "limitations": [
                "SPL is generated only for selected functions, never for the whole repository.",
                "SPL Generator receives function source/static context only; task text is used only for retrieval.",
                "Verify every important SPL conclusion against current source before editing.",
            ],
        }
        self._log_event("spl_understand", {
            "instance_id": instance_id,
            "condition": condition,
            "query_hash": result["task_hash"],
            "max_candidates": max_candidates,
            "generation_budget": generation_budget,
            "candidates": [
                {
                    "symbol_id": item["symbol_id"],
                    "file_path": item["file_path"],
                    "start_line": item["start_line"],
                    "end_line": item["end_line"],
                    "score": item["score"],
                    "spl_status": item["spl_status"],
                }
                for item in candidates
            ],
            "cache_hits": cache_hits,
            "generated": generated,
            "budget_exhausted": budget_exhausted,
            "duration_ms": duration_ms,
            "generator_input_tokens": _sum_metadata(candidates, "input_tokens"),
            "generator_output_tokens": _sum_metadata(candidates, "output_tokens"),
        })
        return result

    def expand(
        self,
        symbol_id: str,
        direction: str = "both",
        depth: int = 1,
        generation_budget: int = 2,
        instance_id: str | None = None,
        condition: str | None = None,
    ) -> dict[str, Any]:
        started = time.perf_counter()
        index = self._load_or_build_index()
        symbols = index.get("symbols", [])
        by_id = {symbol["symbol_id"]: symbol for symbol in symbols}
        if symbol_id not in by_id:
            return {"error": "symbol_not_found", "symbol_id": symbol_id, "recoverable": True}

        graph = index.get("dependency_graph") or {"nodes": [], "edges": []}
        depth = _bounded_int(depth, 0, 2)
        selected = {symbol_id}
        selected_edges: list[dict[str, Any]] = []
        frontier = {symbol_id}
        for _ in range(depth):
            next_frontier: set[str] = set()
            for edge in graph.get("edges", []):
                forward = direction in {"both", "callees", "out"} and edge.get("source") in frontier
                backward = direction in {"both", "callers", "in"} and edge.get("target") in frontier
                if not forward and not backward:
                    continue
                selected_edges.append(edge)
                other = edge.get("target") if forward else edge.get("source")
                if other in by_id and other not in selected:
                    selected.add(other)
                    next_frontier.add(other)
            frontier = next_frontier
            if not frontier:
                break

        self._log_event("spl_expand", {
            "instance_id": instance_id,
            "condition": condition,
            "symbol_id": symbol_id,
            "direction": direction,
            "depth": depth,
            "node_count": len(selected),
            "edge_count": len(selected_edges),
            "generation_budget": generation_budget,
            "duration_ms": int((time.perf_counter() - started) * 1000),
        })
        return {
            "symbol_id": symbol_id,
            "direction": direction,
            "depth": depth,
            "nodes": [_public_symbol(by_id[item]) for item in selected if item in by_id],
            "edges": selected_edges[:80],
            "limitations": [
                "Dependency edges are static name-resolution evidence.",
                "Dynamic calls may be unresolved or missing.",
            ],
        }

    def control_plan(
        self,
        task: str,
        scope_paths: list[str] | None = None,
        max_candidates: int = DEFAULT_MAX_CANDIDATES,
        generation_budget: int = DEFAULT_GENERATION_BUDGET,
        include_patterns: list[str] | None = None,
        exclude_patterns: list[str] | None = None,
        instance_id: str | None = None,
        condition: str | None = None,
    ) -> dict[str, Any]:
        """Return SPL-derived control constraints for a Codex investigation.

        This deliberately avoids proposing a patch. It turns task-relevant SPL
        candidates into an action-control artifact: where to inspect first,
        when to stop broad search, what not to edit first, what behavior to
        preserve, and what to verify after editing.
        """
        started = time.perf_counter()
        understand = self.understand(
            task=task,
            scope_paths=scope_paths,
            max_candidates=max_candidates,
            generation_budget=generation_budget,
            include_patterns=include_patterns,
            exclude_patterns=exclude_patterns,
            instance_id=instance_id,
            condition=condition,
        )
        index = self._load_or_build_index(include_patterns, exclude_patterns)
        symbols = index.get("symbols", [])
        by_id = {symbol["symbol_id"]: symbol for symbol in symbols}
        graph = index.get("dependency_graph") or {"nodes": [], "edges": []}
        candidates = understand.get("candidates", [])
        inspection_order = []
        for priority, candidate in enumerate(candidates[:5], 1):
            symbol = by_id.get(candidate["symbol_id"], {})
            inspection_order.append(_control_inspection_entry(priority, candidate, symbol, graph))

        likely_owner = inspection_order[0] if inspection_order else None
        avoid = _control_avoid_entries(candidates, by_id)
        edit_constraints = _control_edit_constraints(likely_owner, by_id, graph)
        verification_targets = _control_verification_targets(task, likely_owner, by_id, graph)
        duration_ms = int((time.perf_counter() - started) * 1000)
        result = {
            "task_hash": understand.get("task_hash"),
            "repository_path": str(self.repository_path),
            "control_level": "Level 3: SPL as control constraints",
            "inspection_order": inspection_order,
            "avoid_until_needed": avoid,
            "likely_edit_owner": _likely_owner(likely_owner),
            "edit_constraints": edit_constraints,
            "source_verification_checklist": _source_verification_checklist(inspection_order),
            "post_edit_verification_targets": verification_targets,
            "budget": {
                "max_candidates": max_candidates,
                "generation_budget": generation_budget,
                "generation_count": understand.get("generation_count", 0),
                "cache_hit_count": understand.get("cache_hit_count", 0),
                "budget_exhausted": understand.get("budget_exhausted", False),
            },
            "control_rules": [
                "Follow inspection_order before broad search unless current source contradicts it.",
                "Do not edit from SPL alone; open the source range and verify the branch/state behavior first.",
                "Treat likely_edit_owner as a hypothesis for the smallest responsible unit, not as proof.",
                "Avoid low-priority candidates until priority 1-2 fail to explain the issue.",
                "Before finalizing a patch, check edit_constraints and post_edit_verification_targets.",
            ],
            "limitations": [
                "SPL-Control constrains investigation and editing; it does not provide a fix.",
                "Control constraints are derived from static index and selected function-level SPL only.",
                "When SPL-Control conflicts with current source or tests, source/tests win.",
            ],
            "duration_ms": duration_ms,
        }
        self._log_event("spl_control_plan", {
            "instance_id": instance_id,
            "condition": condition,
            "query_hash": result["task_hash"],
            "max_candidates": max_candidates,
            "generation_budget": generation_budget,
            "inspection_count": len(inspection_order),
            "avoid_count": len(avoid),
            "likely_edit_owner": result["likely_edit_owner"].get("symbol_id") if result["likely_edit_owner"] else None,
            "duration_ms": duration_ms,
            "generator_input_tokens": _sum_metadata(candidates, "input_tokens"),
            "generator_output_tokens": _sum_metadata(candidates, "output_tokens"),
        })
        return result

    def refresh(
        self,
        changed_files: list[str],
        regenerate_used_symbols: bool = True,
        instance_id: str | None = None,
        condition: str | None = None,
    ) -> dict[str, Any]:
        started = time.perf_counter()
        self._load_or_build_index()
        old_cache = self._load_cache()
        old_index = self._load_index()
        changed = {Path(item).as_posix() for item in changed_files}
        invalidated: list[str] = []
        kept_entries: dict[str, Any] = {}
        for key, entry in old_cache.get("entries", {}).items():
            symbol_id = str(entry.get("symbol_id", ""))
            file_path = symbol_id.split("::", 1)[0]
            if file_path in changed:
                invalidated.append(symbol_id)
            else:
                kept_entries[key] = entry
        cache = {"version": ROUTER_VERSION, "entries": kept_entries}

        for rel in changed:
            old_index["symbols"] = [symbol for symbol in old_index.get("symbols", []) if symbol.get("file") != rel]
            path = self.repository_path / rel
            if path.exists():
                symbols, _warnings = extract_symbols_from_file(path, self.repository_path)
                old_index.setdefault("symbols", []).extend(asdict(symbol) for symbol in symbols)
        old_index["dependency_graph"] = _graph_from_symbol_dicts(old_index.get("symbols", []))
        self._save_index(old_index)
        self._save_cache(cache)
        result = {
            "changed_files": sorted(changed),
            "invalidated_symbols": sorted(set(invalidated)),
            "regenerated_symbols": [],
            "cache_entries_kept": len(kept_entries),
            "refresh_scope": "changed_files_only",
            "duration_ms": int((time.perf_counter() - started) * 1000),
        }
        self._log_event("spl_refresh", {
            "instance_id": instance_id,
            "condition": condition,
            "changed_files": sorted(changed),
            "invalidated_symbols": result["invalidated_symbols"],
            "regenerate_used_symbols": regenerate_used_symbols,
            "duration_ms": result["duration_ms"],
        })
        return result

    def _load_or_build_index(
        self,
        include_patterns: list[str] | None = None,
        exclude_patterns: list[str] | None = None,
    ) -> dict[str, Any]:
        if self.index_path.exists():
            return self._load_index()
        symbols: list[SourceSymbol] = []
        warnings: list[str] = []
        for path in iter_source_files(self.repository_path, include_patterns, exclude_patterns):
            extracted, file_warnings = extract_symbols_from_file(path, self.repository_path)
            symbols.extend(extracted)
            warnings.extend(file_warnings)
        index = {
            "version": ROUTER_VERSION,
            "repository_path": str(self.repository_path),
            "built_at": time.time(),
            "index_kind": "static_no_llm",
            "symbols": [asdict(symbol) for symbol in symbols],
            "dependency_graph": _graph_from_symbol_dicts([asdict(symbol) for symbol in symbols]),
            "warnings": warnings,
        }
        self._save_index(index)
        return index

    def _load_index(self) -> dict[str, Any]:
        return json.loads(self.index_path.read_text(encoding="utf-8"))

    def _save_index(self, index: dict[str, Any]) -> None:
        self.index_dir.mkdir(parents=True, exist_ok=True)
        self.index_path.write_text(json.dumps(index, ensure_ascii=False, indent=2), encoding="utf-8")

    def _load_cache(self) -> dict[str, Any]:
        if not self.cache_path.exists():
            return {"version": ROUTER_VERSION, "entries": {}}
        return json.loads(self.cache_path.read_text(encoding="utf-8"))

    def _save_cache(self, cache: dict[str, Any]) -> None:
        self.index_dir.mkdir(parents=True, exist_ok=True)
        self.cache_path.write_text(json.dumps(cache, ensure_ascii=False, indent=2), encoding="utf-8")

    def _cache_key(self, symbol: dict[str, Any]) -> str:
        raw = "|".join([
            str(self.repository_path),
            symbol["file"],
            symbol["symbol"],
            symbol["content_hash"],
            str(self.config.get("spl_schema_version", "current")),
            str(self.config.get("spl_prompt_version", "existing")),
            "common.spl_adapter",
            str(ROUTER_VERSION),
        ])
        return sha256_text(raw)

    def _log_event(self, event: str, payload: dict[str, Any]) -> None:
        if not self.event_log:
            return
        self.event_log.parent.mkdir(parents=True, exist_ok=True)
        row = {"timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "event": event}
        row.update({k: v for k, v in payload.items() if v is not None})
        with self.event_log.open("a", encoding="utf-8", newline="\n") as f:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")


def _symbol_from_dict(data: dict[str, Any]) -> SourceSymbol:
    return SourceSymbol(
        symbol_id=data["symbol_id"],
        symbol=data["symbol"],
        file=data["file"],
        start_line=int(data["start_line"]),
        end_line=int(data["end_line"]),
        language=data["language"],
        code=data["code"],
        content_hash=data["content_hash"],
        calls=list(data.get("calls", [])),
        state_changes=list(data.get("state_changes", [])),
        summary_hint=data.get("summary_hint", ""),
    )


def _graph_from_symbol_dicts(symbols: list[dict[str, Any]]) -> dict[str, Any]:
    graph = build_dependency_graph([_symbol_from_dict(symbol) for symbol in symbols])
    return {"nodes": graph.nodes, "edges": graph.edges}


def _public_symbol(symbol: dict[str, Any]) -> dict[str, Any]:
    return {
        "symbol_id": symbol["symbol_id"],
        "symbol": symbol["symbol"],
        "file_path": symbol["file"],
        "start_line": symbol["start_line"],
        "end_line": symbol["end_line"],
        "language": symbol["language"],
        "source_hash": symbol["content_hash"],
        "summary_hint": symbol.get("summary_hint", ""),
    }


def _in_scope(file_path: str, scope_paths: list[str]) -> bool:
    if not scope_paths:
        return True
    normalized = Path(file_path).as_posix()
    for raw in scope_paths:
        scope = Path(raw).as_posix().strip("/")
        if scope in {"", "."}:
            return True
        if normalized == scope or normalized.startswith(scope + "/"):
            return True
    return False


def _terms(text: str) -> list[str]:
    import re

    tokens = []
    for token in re.findall(r"[A-Za-z_][A-Za-z0-9_]+", text):
        normalized = token.lower()
        if len(normalized) <= 2 or normalized in STOPWORDS:
            continue
        tokens.append(TYPE_SYNONYMS.get(normalized, normalized))
    return tokens


def _identifier_text(code: str) -> str:
    import re

    words = re.findall(r"[A-Za-z_][A-Za-z0-9_]+", code)
    return " ".join(word for word in words if word.lower() not in STOPWORDS)


def _score(query_terms: list[str], haystack: str) -> tuple[float, list[str]]:
    hay = haystack.lower()
    hits = []
    score = 0.0
    for term in query_terms:
        if term in hay:
            hits.append(term)
            score += 1.0 + min(hay.count(term), 4) * 0.1
    return score / max(len(query_terms), 1), hits


def _reason(hits: list[str]) -> str:
    if hits:
        return "Static index matched task terms: " + ", ".join(hits[:8])
    return "Selected by static symbol/path similarity."


def _bounded_int(value: Any, lower: int, upper: int) -> int:
    try:
        number = int(value)
    except Exception:
        number = lower
    return max(lower, min(number, upper))


def _compact_metadata(metadata: dict[str, Any]) -> dict[str, Any]:
    keys = [
        "provider",
        "model",
        "elapsed_seconds",
        "input_tokens",
        "output_tokens",
        "total_tokens",
        "calls",
        "generator_adapter",
        "issue_text_visible_to_generator",
    ]
    return {key: metadata.get(key) for key in keys if key in metadata}


def _sum_metadata(candidates: list[dict[str, Any]], key: str) -> int:
    total = 0
    for item in candidates:
        value = item.get("spl_metadata", {}).get(key)
        if isinstance(value, int):
            total += value
    return total


def _control_inspection_entry(
    priority: int,
    candidate: dict[str, Any],
    symbol: dict[str, Any],
    graph: dict[str, Any],
) -> dict[str, Any]:
    symbol_id = candidate["symbol_id"]
    code = symbol.get("code", "")
    line_count = max(1, int(candidate.get("end_line", 0)) - int(candidate.get("start_line", 0)) + 1)
    callers = _neighbor_ids(graph, symbol_id, "callers")
    callees = _neighbor_ids(graph, symbol_id, "callees")
    risk_tags = _risk_tags(symbol)
    return {
        "priority": priority,
        "symbol_id": symbol_id,
        "symbol": candidate.get("symbol"),
        "file_path": candidate.get("file_path"),
        "start_line": candidate.get("start_line"),
        "end_line": candidate.get("end_line"),
        "score": candidate.get("score"),
        "why_first": _why_first(candidate, symbol, callers, callees),
        "what_to_verify_in_source": _what_to_verify(code, candidate, risk_tags),
        "stop_condition": (
            "If this source range owns the failing input-to-output behavior, "
            "stop broad repository search and inspect only its direct callers/callees."
        ),
        "expand_if": (
            "Expand one hop only if this function delegates the behavior, mutates shared state, "
            "or the failing symptom is produced by a direct callee."
        ),
        "risk_tags": risk_tags,
        "caller_count": len(callers),
        "callee_count": len(callees),
        "line_count": line_count,
        "spl_status": candidate.get("spl_status"),
        "source_hash": candidate.get("source_hash"),
    }


def _control_avoid_entries(candidates: list[dict[str, Any]], by_id: dict[str, dict[str, Any]]) -> list[dict[str, Any]]:
    avoid = []
    for candidate in candidates[3:]:
        symbol = by_id.get(candidate["symbol_id"], {})
        reason = "Lower-ranked semantic overlap; inspect only if priority 1-3 fail in source verification."
        if _looks_like_wrapper_or_formatter(symbol):
            reason = "Looks like wrapper/formatter/helper behavior; do not edit before verifying the owning transformation."
        avoid.append({
            "symbol_id": candidate["symbol_id"],
            "file_path": candidate.get("file_path"),
            "start_line": candidate.get("start_line"),
            "end_line": candidate.get("end_line"),
            "reason": reason,
        })
    return avoid[:5]


def _control_edit_constraints(
    likely_owner: dict[str, Any] | None,
    by_id: dict[str, dict[str, Any]],
    graph: dict[str, Any],
) -> list[str]:
    constraints = [
        "Preserve the public function signature unless the verified source shows the bug is the signature itself.",
        "Make the smallest source edit inside the verified responsibility owner.",
        "Do not edit tests or unrelated helpers to force a pass.",
        "If SPL-Control is stale or contradicted by source, follow current source.",
    ]
    if not likely_owner:
        return constraints
    symbol = by_id.get(likely_owner["symbol_id"], {})
    code = symbol.get("code", "")
    if "return " in code:
        constraints.append("Preserve existing return shape/type for unaffected branches.")
    if "raise " in code:
        constraints.append("Preserve existing exception type and message behavior for unaffected invalid inputs.")
    if "except " in code or "finally:" in code:
        constraints.append("Do not bypass existing exception/finally control flow without source evidence.")
    if symbol.get("state_changes"):
        constraints.append("Preserve state mutations not directly tied to the reported symptom.")
    callers = _neighbor_ids(graph, likely_owner["symbol_id"], "callers")
    if callers:
        constraints.append("Check direct callers before changing the owner contract.")
    return constraints


def _control_verification_targets(
    task: str,
    likely_owner: dict[str, Any] | None,
    by_id: dict[str, dict[str, Any]],
    graph: dict[str, Any],
) -> list[dict[str, Any]]:
    if not likely_owner:
        return [{"target": "Run the narrowest relevant test or reproduce the issue after editing.", "source": "fallback"}]
    symbol = by_id.get(likely_owner["symbol_id"], {})
    code = symbol.get("code", "")
    targets = [
        {
            "target": "Re-run or inspect the failing behavior described by the problem statement.",
            "source": "problem_statement",
        },
        {
            "target": f"Re-check `{likely_owner['symbol_id']}` lines {likely_owner['start_line']}-{likely_owner['end_line']} after editing.",
            "source": "likely_edit_owner",
        },
    ]
    if "if " in code:
        targets.append({"target": "Exercise both the changed branch and at least one unchanged branch.", "source": "branch_structure"})
    if "return " in code:
        targets.append({"target": "Confirm unaffected return values keep their previous shape/type.", "source": "return_contract"})
    callers = _neighbor_ids(graph, likely_owner["symbol_id"], "callers")[:3]
    for caller in callers:
        targets.append({"target": f"Inspect direct caller contract: `{caller}`.", "source": "static_dependency"})
    if any(term in task.lower() for term in ["exception", "error", "raise", "warning"]):
        targets.append({"target": "Verify exception/warning behavior, not only the nominal path.", "source": "task_terms"})
    return targets[:8]


def _source_verification_checklist(inspection_order: list[dict[str, Any]]) -> list[dict[str, Any]]:
    checklist = []
    for item in inspection_order[:3]:
        checklist.append({
            "symbol_id": item["symbol_id"],
            "file_path": item["file_path"],
            "lines": f"{item['start_line']}-{item['end_line']}",
            "must_verify": item["what_to_verify_in_source"],
        })
    return checklist


def _likely_owner(entry: dict[str, Any] | None) -> dict[str, Any] | None:
    if not entry:
        return None
    confidence = 0.58
    if "branching" in entry.get("risk_tags", []):
        confidence += 0.08
    if "returns_value" in entry.get("risk_tags", []):
        confidence += 0.06
    if entry.get("caller_count", 0) or entry.get("callee_count", 0):
        confidence += 0.04
    return {
        "symbol_id": entry["symbol_id"],
        "file_path": entry["file_path"],
        "start_line": entry["start_line"],
        "end_line": entry["end_line"],
        "confidence": round(min(confidence, 0.82), 2),
        "reason": "Top-ranked semantic candidate with source range suitable for minimal responsibility verification.",
    }


def _neighbor_ids(graph: dict[str, Any], symbol_id: str, direction: str) -> list[str]:
    out = []
    for edge in graph.get("edges", []):
        if direction == "callees" and edge.get("source") == symbol_id and "::" in str(edge.get("target")):
            out.append(edge["target"])
        elif direction == "callers" and edge.get("target") == symbol_id and "::" in str(edge.get("source")):
            out.append(edge["source"])
    return sorted(set(out))


def _risk_tags(symbol: dict[str, Any]) -> list[str]:
    code = symbol.get("code", "")
    tags = []
    if "if " in code or "elif " in code:
        tags.append("branching")
    if "return " in code:
        tags.append("returns_value")
    if "raise " in code:
        tags.append("exception_path")
    if "except " in code or "finally:" in code:
        tags.append("exception_handling")
    if symbol.get("state_changes"):
        tags.append("state_mutation")
    if len(code.splitlines()) > 80:
        tags.append("long_function")
    if _looks_like_wrapper_or_formatter(symbol):
        tags.append("wrapper_or_formatter")
    return tags or ["simple_flow"]


def _looks_like_wrapper_or_formatter(symbol: dict[str, Any]) -> bool:
    name = str(symbol.get("symbol", "")).lower()
    summary = str(symbol.get("summary_hint", "")).lower()
    words = ["format", "print", "render", "repr", "str", "wrapper", "proxy", "show"]
    return any(word in name or word in summary for word in words)


def _why_first(candidate: dict[str, Any], symbol: dict[str, Any], callers: list[str], callees: list[str]) -> str:
    parts = [str(candidate.get("retrieval_reason", "Selected by SPL-Control ranking."))]
    if symbol.get("state_changes"):
        parts.append("It mutates state relevant to behavior ownership.")
    if callers:
        parts.append("It has direct static callers, so contract changes may propagate.")
    if callees:
        parts.append("It delegates to direct callees; expand only if source shows delegation owns the symptom.")
    return " ".join(parts)


def _what_to_verify(code: str, candidate: dict[str, Any], risk_tags: list[str]) -> str:
    checks = [
        f"Open `{candidate.get('file_path')}` lines {candidate.get('start_line')}-{candidate.get('end_line')}.",
        "Confirm the matched terms correspond to executable behavior, not comments or incidental names.",
    ]
    if "branching" in risk_tags:
        checks.append("Identify the exact branch that handles the reported symptom.")
    if "returns_value" in risk_tags:
        checks.append("Trace how inputs are transformed into the returned value.")
    if "exception_path" in risk_tags or "exception_handling" in risk_tags:
        checks.append("Check exception/warning paths before editing.")
    if "state_mutation" in risk_tags:
        checks.append("Check whether state changes are required by callers.")
    if "long_function" in risk_tags:
        checks.append("Read only the relevant branch first; avoid scanning unrelated blocks.")
    return " ".join(checks)


STOPWORDS = {
    "about",
    "above",
    "after",
    "again",
    "against",
    "also",
    "and",
    "any",
    "are",
    "because",
    "been",
    "but",
    "can",
    "cannot",
    "contains",
    "could",
    "def",
    "describe",
    "docs",
    "does",
    "doesn",
    "don",
    "expected",
    "for",
    "from",
    "has",
    "have",
    "html",
    "https",
    "info",
    "instead",
    "into",
    "its",
    "last",
    "line",
    "lines",
    "not",
    "note",
    "now",
    "one",
    "only",
    "org",
    "out",
    "put",
    "regardless",
    "related",
    "rerun",
    "return",
    "returns",
    "see",
    "set",
    "should",
    "sphinx",
    "steps",
    "that",
    "the",
    "then",
    "there",
    "this",
    "title",
    "using",
    "was",
    "when",
    "whether",
    "will",
    "with",
    "you",
}


TYPE_SYNONYMS = {
    "autodoc_typehints": "annotation",
    "hint": "annotation",
    "hints": "annotation",
    "typehint": "annotation",
    "typehints": "annotation",
}
