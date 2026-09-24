from __future__ import annotations

import json
import os
import re
import subprocess
import time
from dataclasses import asdict
from pathlib import Path
from typing import Any

from spl_core.cards import SPLCard, SourceProvenance
from spl_core.dependencies import build_dependency_graph
from spl_core.hashing import sha256_file, sha256_text
from spl_core.symbols import SourceSymbol, extract_symbols_from_file, iter_source_files


INDEX_VERSION = 1


def default_index_dir(repository_path: str | Path) -> Path:
    return Path(repository_path).resolve() / ".spl_index"


def repository_revision(repository_path: str | Path) -> str:
    root = Path(repository_path).resolve()
    try:
        result = subprocess.run(
            ["git", "-C", str(root), "rev-parse", "--short", "HEAD"],
            capture_output=True,
            text=True,
            timeout=3,
        )
        if result.returncode == 0:
            dirty = subprocess.run(
                ["git", "-C", str(root), "status", "--porcelain"],
                capture_output=True,
                text=True,
                timeout=3,
            )
            suffix = "+dirty" if dirty.stdout.strip() else ""
            return f"git:{result.stdout.strip()}{suffix}"
    except Exception:
        pass
    return "worktree:unknown"


class SPLIndex:
    def __init__(self, repository_path: str | Path, index_dir: str | Path | None = None):
        self.repository_path = Path(repository_path).resolve()
        self.index_dir = Path(index_dir).resolve() if index_dir else default_index_dir(self.repository_path)
        self.index_path = self.index_dir / "index.json"
        self.data: dict[str, Any] = {
            "version": INDEX_VERSION,
            "repository_path": str(self.repository_path),
            "repository_id": "repo-" + sha256_text(str(self.repository_path))[-12:],
            "revision": repository_revision(self.repository_path),
            "files": {},
            "symbols": {},
            "dependency_graph": {"nodes": [], "edges": []},
            "logs": [],
        }

    def load(self) -> "SPLIndex":
        if self.index_path.exists():
            self.data = json.loads(self.index_path.read_text(encoding="utf-8"))
        return self

    def save(self) -> None:
        self.index_dir.mkdir(parents=True, exist_ok=True)
        self.index_path.write_text(json.dumps(self.data, ensure_ascii=False, indent=2), encoding="utf-8")

    def prepare(
        self,
        include_patterns: list[str] | None = None,
        exclude_patterns: list[str] | None = None,
        incremental: bool = True,
        files: list[str] | None = None,
    ) -> dict[str, Any]:
        self.load()
        started = time.perf_counter()
        warnings: list[str] = []
        failed_files: list[dict[str, str]] = []
        updated_symbols = 0
        indexed_files = 0
        skipped_files = 0
        target_files = [self.repository_path / item for item in files] if files else list(
            iter_source_files(self.repository_path, include_patterns, exclude_patterns)
        )
        old_symbols = dict(self.data.get("symbols", {}))
        touched_files: set[str] = set()

        for path in target_files:
            try:
                resolved = path.resolve()
                rel = resolved.relative_to(self.repository_path).as_posix()
                file_hash = sha256_file(resolved)
                previous = self.data.get("files", {}).get(rel, {})
                if incremental and previous.get("content_hash") == file_hash:
                    skipped_files += 1
                    continue
                symbols, file_warnings = extract_symbols_from_file(resolved, self.repository_path)
                warnings.extend(file_warnings)
                self._remove_file_symbols(rel)
                self.data.setdefault("files", {})[rel] = {
                    "content_hash": file_hash,
                    "language": symbols[0].language if symbols else "unknown",
                    "symbol_count": len(symbols),
                    "updated_at": time.time(),
                }
                for symbol in symbols:
                    card = self._card_from_symbol(symbol)
                    self.data.setdefault("symbols", {})[symbol.symbol_id] = card.to_dict()
                    updated_symbols += 1 if old_symbols.get(symbol.symbol_id, {}).get("source", {}).get("content_hash") != symbol.content_hash else 0
                touched_files.add(rel)
                indexed_files += 1
            except Exception as exc:
                failed_files.append({"file": str(path), "error": type(exc).__name__, "message": str(exc)})

        all_symbols = [self._symbol_from_card(card) for card in self.data.get("symbols", {}).values()]
        graph = build_dependency_graph(all_symbols)
        self.data["dependency_graph"] = {"nodes": graph.nodes, "edges": graph.edges}
        self._refresh_callers_from_graph()
        self.data["revision"] = repository_revision(self.repository_path)
        self._log("spl_prepare_repository", started, {"files": len(target_files), "updated_symbols": updated_symbols})
        self.save()
        return {
            "repository_id": self.data["repository_id"],
            "revision": self.data["revision"],
            "indexed_files": indexed_files,
            "indexed_symbols": len(self.data.get("symbols", {})),
            "updated_symbols": updated_symbols,
            "skipped_files": skipped_files,
            "failed_files": failed_files,
            "warnings": warnings,
        }

    def search(self, query: str, task_type: str = "code_understanding", top_k: int = 8, scope: dict[str, Any] | None = None) -> dict[str, Any]:
        self.load()
        scope = scope or {}
        query_terms = _terms(query)
        path_filters = [Path(p).as_posix().rstrip("/") for p in scope.get("paths", [])]
        languages = set(scope.get("languages", []))
        candidates: list[dict[str, Any]] = []
        for symbol_id, card in self.data.get("symbols", {}).items():
            source = card.get("source", {})
            file_path = source.get("file", "")
            language = source.get("language", "")
            if path_filters and not any(file_path == p or file_path.startswith(p + "/") for p in path_filters):
                continue
            if languages and language not in languages:
                continue
            haystack = " ".join([
                card.get("symbol", ""),
                card.get("summary", ""),
                card.get("spl_text", ""),
                " ".join(card.get("main_flow", [])),
                " ".join(card.get("alternative_flows", [])),
            ])
            score, hits = _score(query_terms, haystack)
            if score <= 0:
                continue
            candidates.append({
                "symbol_id": symbol_id,
                "symbol": card.get("symbol"),
                "file": file_path,
                "start_line": source.get("start_line"),
                "end_line": source.get("end_line"),
                "responsibility": card.get("summary"),
                "relevance_reason": _reason(hits, task_type),
                "score": round(score, 4),
                "evidence_type": "semantic_match",
                "fresh": self.validate(symbol_id)["valid"],
            })
        candidates.sort(key=lambda item: item["score"], reverse=True)
        self._log("spl_search", time.perf_counter(), {"query": query, "returned": min(top_k, len(candidates))})
        self.save()
        return {"query": query, "task_type": task_type, "candidates": candidates[: max(1, min(int(top_k), 50))]}

    def get_card(self, symbol_id: str, sections: list[str] | None = None) -> dict[str, Any]:
        self.load()
        card = self.data.get("symbols", {}).get(symbol_id)
        if not card:
            return {"error": "symbol_not_found", "symbol_id": symbol_id, "recoverable": True}
        out = _filter_sections(dict(card), sections)
        out["fresh"] = self.validate(symbol_id)["valid"]
        return out

    def validate(self, symbol_id: str) -> dict[str, Any]:
        card = self.data.get("symbols", {}).get(symbol_id)
        if not card:
            return {"valid": False, "reason": "Symbol not found", "requires_refresh": True}
        source = card.get("source", {})
        path = self.repository_path / source.get("file", "")
        if not path.exists():
            return {"valid": False, "reason": "Source file missing", "indexed_hash": source.get("content_hash"), "current_hash": None, "requires_refresh": True}
        lines = path.read_text(encoding="utf-8").splitlines()
        start = max(1, int(source.get("start_line", 1)))
        end = min(len(lines), int(source.get("end_line", start)))
        current_hash = sha256_text("\n".join(lines[start - 1:end]))
        indexed_hash = source.get("content_hash")
        return {
            "valid": current_hash == indexed_hash,
            "reason": "fresh" if current_hash == indexed_hash else "Source content hash changed",
            "indexed_hash": indexed_hash,
            "current_hash": current_hash,
            "requires_refresh": current_hash != indexed_hash,
        }

    def trace_dependencies(self, symbol_id: str, direction: str = "both", depth: int = 2, include_external: bool = False) -> dict[str, Any]:
        self.load()
        max_depth = max(0, min(int(depth), 4))
        graph = self.data.get("dependency_graph", {"nodes": [], "edges": []})
        nodes_by_id = {node["id"]: node for node in graph.get("nodes", [])}
        selected_nodes = {symbol_id}
        selected_edges: list[dict[str, Any]] = []
        frontier = {symbol_id}
        for _ in range(max_depth):
            next_frontier: set[str] = set()
            for edge in graph.get("edges", []):
                forward = direction in {"both", "callees", "out"} and edge.get("source") in frontier
                backward = direction in {"both", "callers", "in"} and edge.get("target") in frontier
                if not forward and not backward:
                    continue
                target = edge.get("target") if forward else edge.get("source")
                if edge.get("type") == "unresolved_reference" and not include_external:
                    selected_edges.append(edge)
                    continue
                selected_edges.append(edge)
                if target in nodes_by_id and target not in selected_nodes:
                    selected_nodes.add(target)
                    next_frontier.add(target)
            frontier = next_frontier
            if not frontier:
                break
        return {
            "symbol_id": symbol_id,
            "direction": direction,
            "depth": max_depth,
            "nodes": [nodes_by_id[node_id] for node_id in selected_nodes if node_id in nodes_by_id],
            "edges": selected_edges[:100],
            "limitations": ["Dynamic calls may be unresolved.", "Edges are static name-resolution evidence, not runtime proof."],
        }

    def explain_region(self, file: str, start_line: int, end_line: int) -> dict[str, Any]:
        self.load()
        matches = []
        for symbol_id, card in self.data.get("symbols", {}).items():
            source = card.get("source", {})
            if source.get("file") != Path(file).as_posix():
                continue
            s = int(source.get("start_line", 0))
            e = int(source.get("end_line", 0))
            if s <= end_line and e >= start_line:
                matches.append({
                    "symbol_id": symbol_id,
                    "symbol": card.get("symbol"),
                    "source": source,
                    "summary": card.get("summary"),
                    "relevant_flow": _region_flow(card, start_line, end_line),
                    "fresh": self.validate(symbol_id)["valid"],
                })
        return {"file": file, "start_line": start_line, "end_line": end_line, "matches": matches}

    def refresh(self, files: list[str], refresh_dependents: bool = True) -> dict[str, Any]:
        self.load()
        before = set(self.data.get("symbols", {}))
        result = self.prepare(files=files, incremental=False)
        after = set(self.data.get("symbols", {}))
        invalidated_set = before - after
        invalidated = sorted(invalidated_set)
        normalized_files = {Path(file).as_posix() for file in files}
        refreshed_existing = {
            symbol_id
            for symbol_id, card in self.data.get("symbols", {}).items()
            if card.get("source", {}).get("file") in normalized_files
        }
        refreshed = sorted((after - (before - invalidated_set)) | refreshed_existing)
        if refresh_dependents:
            graph = self.data.get("dependency_graph", {})
            changed = set(refreshed) | set(invalidated)
            dependents = sorted({edge.get("source") for edge in graph.get("edges", []) if edge.get("target") in changed})
        else:
            dependents = []
        return {
            "refreshed_symbols": refreshed,
            "invalidated_symbols": invalidated,
            "dependent_symbols": dependents,
            "prepare_result": result,
        }

    def _card_from_symbol(self, symbol: SourceSymbol) -> SPLCard:
        revision = repository_revision(self.repository_path)
        spl_text = _mock_spl(symbol)
        return SPLCard(
            symbol_id=symbol.symbol_id,
            symbol=symbol.symbol,
            source=SourceProvenance(
                file=symbol.file,
                start_line=symbol.start_line,
                end_line=symbol.end_line,
                language=symbol.language,
                content_hash=symbol.content_hash,
                revision=revision,
            ),
            summary=symbol.summary_hint,
            inputs=[],
            outputs=[],
            main_flow=_extract_flow_lines(spl_text, "[COMMAND"),
            alternative_flows=_extract_flow_lines(spl_text, "[ALTERNATIVE_FLOW"),
            exception_flows=_extract_flow_lines(spl_text, "[EXCEPTION_FLOW"),
            callees=symbol.calls,
            state_changes=symbol.state_changes,
            spl_text=spl_text,
        )

    def _symbol_from_card(self, card: dict[str, Any]) -> SourceSymbol:
        source = card.get("source", {})
        return SourceSymbol(
            symbol_id=card.get("symbol_id", ""),
            symbol=card.get("symbol", ""),
            file=source.get("file", ""),
            start_line=int(source.get("start_line", 1)),
            end_line=int(source.get("end_line", 1)),
            language=source.get("language", "text"),
            code="",
            content_hash=source.get("content_hash", ""),
            calls=list(card.get("callees", [])),
            state_changes=list(card.get("state_changes", [])),
            summary_hint=card.get("summary", ""),
        )

    def _remove_file_symbols(self, rel: str) -> None:
        symbols = self.data.setdefault("symbols", {})
        for symbol_id, card in list(symbols.items()):
            if card.get("source", {}).get("file") == rel:
                del symbols[symbol_id]

    def _refresh_callers_from_graph(self) -> None:
        for card in self.data.get("symbols", {}).values():
            card["callers"] = []
        for edge in self.data.get("dependency_graph", {}).get("edges", []):
            if edge.get("type") != "callee":
                continue
            target = edge.get("target")
            source = edge.get("source")
            if target in self.data.get("symbols", {}):
                self.data["symbols"][target].setdefault("callers", []).append(source)

    def _log(self, tool_name: str, started: float, payload: dict[str, Any]) -> None:
        self.data.setdefault("logs", []).append({
            "tool": tool_name,
            "elapsed_seconds": max(0.0, time.perf_counter() - started),
            "payload": payload,
            "time": time.time(),
        })
        self.data["logs"] = self.data["logs"][-1000:]


def _mock_spl(symbol: SourceSymbol) -> str:
    calls = "\n".join(f"            [COMMAND Calls {callee}. RESULT call_dependency]" for callee in symbol.calls[:20])
    states = "\n".join(f"            [COMMAND Updates or assigns {state}. RESULT state_change]" for state in symbol.state_changes[:20])
    body = "\n".join(part for part in [calls, states] if part)
    if not body:
        body = "            [COMMAND Execute the current source implementation. RESULT current_behavior]"
    return (
        f'[DEFINE_WORKER: "{symbol.summary_hint}" {symbol.symbol}]\n'
        "    [INPUTS]\n"
        "    [END_INPUTS]\n\n"
        "    [OUTPUTS]\n"
        "    [END_OUTPUTS]\n\n"
        "    [MAIN_FLOW]\n"
        "        [SEQUENTIAL_BLOCK]\n"
        f"{body}\n"
        "        [END_SEQUENTIAL_BLOCK]\n"
        "    [END_MAIN_FLOW]\n"
        "[END_WORKER]"
    )


def _extract_flow_lines(spl_text: str, prefix: str) -> list[str]:
    return [line.strip() for line in spl_text.splitlines() if line.strip().startswith(prefix)]


STOP_TERMS = {
    "the", "and", "for", "with", "from", "this", "that", "function", "method",
    "responsible", "current", "implementation", "value", "return", "returns",
    "find", "code", "query",
}


def _terms(text: str) -> set[str]:
    raw = {token.lower() for token in re.findall(r"[A-Za-z_][A-Za-z0-9_]*", text or "") if len(token) > 2}
    expanded = set(raw)
    for token in raw:
        expanded.update(part.lower() for part in re.findall(r"[A-Z]?[a-z]+|[A-Z]+(?=[A-Z]|$)|[0-9]+", token) if len(part) > 2)
        if len(token) > 4 and token.endswith("ing"):
            expanded.add(token[:-3])
            expanded.add(token[:-3] + "e")
            if len(token) > 5 and token[-4] == token[-5]:
                expanded.add(token[:-4])
        if len(token) > 4 and token.endswith("s"):
            expanded.add(token[:-1])
    return {term for term in expanded if term not in STOP_TERMS}


def _score(query_terms: set[str], haystack: str) -> tuple[float, list[str]]:
    hay_terms = _terms(haystack)
    hits = sorted(query_terms & hay_terms)
    if not hits:
        return 0.0, []
    return min(1.0, len(hits) / max(1, len(query_terms)) + 0.05 * len(hits)), hits


def _reason(hits: list[str], task_type: str) -> str:
    if not hits:
        return f"Candidate matched the {task_type} query weakly."
    return f"Semantic terms matched for {task_type}: " + ", ".join(hits[:8])


def _filter_sections(card: dict[str, Any], sections: list[str] | None) -> dict[str, Any]:
    if not sections:
        return card
    keep = {"symbol_id", "symbol", "source", "fresh", "limitations"} | set(sections)
    if "exceptions" in keep:
        keep.add("exception_flows")
    return {key: value for key, value in card.items() if key in keep}


def _region_flow(card: dict[str, Any], start_line: int, end_line: int) -> list[str]:
    flows = list(card.get("main_flow", [])) + list(card.get("alternative_flows", [])) + list(card.get("exception_flows", []))
    return flows[:8] or [card.get("summary", "No SPL flow lines available for this region.")]
