from __future__ import annotations

from pathlib import Path
from typing import Any

from spl_index.store import SPLIndex
from spl_router import SPLRouter


TOOL_SCHEMAS: list[dict[str, Any]] = [
    {
        "name": "spl_understand",
        "description": (
            "On-demand SPL-assisted code understanding. Builds a static no-LLM index, "
            "retrieves task-relevant functions, reuses fresh SPL cache, and generates "
            "SPL only for selected function candidates within budget."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {
                "repository_path": {"type": "string"},
                "task": {"type": "string"},
                "scope_paths": {"type": "array", "items": {"type": "string"}},
                "max_candidates": {"type": "integer"},
                "generation_budget": {"type": "integer"},
                "include_patterns": {"type": "array", "items": {"type": "string"}},
                "exclude_patterns": {"type": "array", "items": {"type": "string"}},
                "index_dir": {"type": "string"},
                "event_log": {"type": "string"},
                "config": {"type": "object"},
                "instance_id": {"type": "string"},
                "condition": {"type": "string"},
            },
            "required": ["repository_path", "task"],
        },
    },
    {
        "name": "spl_expand",
        "description": "Expand one SPL candidate by static callers/callees without expanding the whole graph.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "repository_path": {"type": "string"},
                "symbol_id": {"type": "string"},
                "direction": {"type": "string"},
                "depth": {"type": "integer"},
                "generation_budget": {"type": "integer"},
                "index_dir": {"type": "string"},
                "event_log": {"type": "string"},
                "config": {"type": "object"},
                "instance_id": {"type": "string"},
                "condition": {"type": "string"},
            },
            "required": ["repository_path", "symbol_id"],
        },
    },
    {
        "name": "spl_control_plan",
        "description": (
            "Return Level-3 SPL control constraints for Codex: inspection priority, "
            "avoid-until-needed regions, likely edit owner, edit constraints, and "
            "post-edit verification targets. This does not generate a patch."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {
                "repository_path": {"type": "string"},
                "task": {"type": "string"},
                "scope_paths": {"type": "array", "items": {"type": "string"}},
                "max_candidates": {"type": "integer"},
                "generation_budget": {"type": "integer"},
                "include_patterns": {"type": "array", "items": {"type": "string"}},
                "exclude_patterns": {"type": "array", "items": {"type": "string"}},
                "index_dir": {"type": "string"},
                "event_log": {"type": "string"},
                "config": {"type": "object"},
                "instance_id": {"type": "string"},
                "condition": {"type": "string"},
            },
            "required": ["repository_path", "task"],
        },
    },
    {
        "name": "spl_prepare_repository",
        "description": "Initialize or incrementally update a repository SPL index.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "repository_path": {"type": "string"},
                "include_patterns": {"type": "array", "items": {"type": "string"}},
                "exclude_patterns": {"type": "array", "items": {"type": "string"}},
                "incremental": {"type": "boolean"},
                "index_dir": {"type": "string"},
            },
            "required": ["repository_path"],
        },
    },
    {
        "name": "spl_search",
        "description": "Retrieve source-bound candidate functions/files by semantic query.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "repository_path": {"type": "string"},
                "query": {"type": "string"},
                "task_type": {"type": "string"},
                "top_k": {"type": "integer"},
                "scope": {"type": "object"},
                "index_dir": {"type": "string"},
            },
            "required": ["repository_path", "query"],
        },
    },
    {
        "name": "spl_get_card",
        "description": "Return selected sections of a structured SPL card for one symbol.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "repository_path": {"type": "string"},
                "symbol_id": {"type": "string"},
                "sections": {"type": "array", "items": {"type": "string"}},
                "index_dir": {"type": "string"},
            },
            "required": ["repository_path", "symbol_id"],
        },
    },
    {
        "name": "spl_trace_dependencies",
        "description": "Trace static caller/callee and unresolved dependency edges.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "repository_path": {"type": "string"},
                "symbol_id": {"type": "string"},
                "direction": {"type": "string"},
                "depth": {"type": "integer"},
                "include_external": {"type": "boolean"},
                "index_dir": {"type": "string"},
            },
            "required": ["repository_path", "symbol_id"],
        },
    },
    {
        "name": "spl_explain_region",
        "description": "Explain the SPL semantics covering a source file line range.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "repository_path": {"type": "string"},
                "file": {"type": "string"},
                "start_line": {"type": "integer"},
                "end_line": {"type": "integer"},
                "index_dir": {"type": "string"},
            },
            "required": ["repository_path", "file", "start_line", "end_line"],
        },
    },
    {
        "name": "spl_validate",
        "description": "Check whether an SPL card still matches the current source content hash.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "repository_path": {"type": "string"},
                "symbol_id": {"type": "string"},
                "index_dir": {"type": "string"},
            },
            "required": ["repository_path", "symbol_id"],
        },
    },
    {
        "name": "spl_refresh",
        "description": (
            "Incrementally invalidate or refresh SPL for modified files. Use changed_files "
            "for the on-demand router path; legacy files is still accepted for the older index path."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {
                "repository_path": {"type": "string"},
                "changed_files": {"type": "array", "items": {"type": "string"}},
                "regenerate_used_symbols": {"type": "boolean"},
                "files": {"type": "array", "items": {"type": "string"}},
                "refresh_dependents": {"type": "boolean"},
                "index_dir": {"type": "string"},
                "event_log": {"type": "string"},
                "config": {"type": "object"},
                "instance_id": {"type": "string"},
                "condition": {"type": "string"},
            },
            "required": ["repository_path"],
        },
    },
]


def handle_tool(name: str, arguments: dict[str, Any]) -> dict[str, Any]:
    repo = arguments.get("repository_path")
    if not repo:
        return {"error": "missing_repository_path", "recoverable": True}
    if name == "spl_understand":
        router = SPLRouter(
            repo,
            index_dir=arguments.get("index_dir"),
            config=arguments.get("config") or {},
            event_log=arguments.get("event_log"),
        )
        return router.understand(
            task=arguments.get("task", ""),
            scope_paths=arguments.get("scope_paths"),
            max_candidates=arguments.get("max_candidates", 5),
            generation_budget=arguments.get("generation_budget", 3),
            include_patterns=arguments.get("include_patterns"),
            exclude_patterns=arguments.get("exclude_patterns"),
            instance_id=arguments.get("instance_id"),
            condition=arguments.get("condition"),
        )
    if name == "spl_expand":
        router = SPLRouter(
            repo,
            index_dir=arguments.get("index_dir"),
            config=arguments.get("config") or {},
            event_log=arguments.get("event_log"),
        )
        return router.expand(
            symbol_id=arguments.get("symbol_id", ""),
            direction=arguments.get("direction", "both"),
            depth=arguments.get("depth", 1),
            generation_budget=arguments.get("generation_budget", 2),
            instance_id=arguments.get("instance_id"),
            condition=arguments.get("condition"),
        )
    if name == "spl_control_plan":
        router = SPLRouter(
            repo,
            index_dir=arguments.get("index_dir"),
            config=arguments.get("config") or {},
            event_log=arguments.get("event_log"),
        )
        return router.control_plan(
            task=arguments.get("task", ""),
            scope_paths=arguments.get("scope_paths"),
            max_candidates=arguments.get("max_candidates", 5),
            generation_budget=arguments.get("generation_budget", 3),
            include_patterns=arguments.get("include_patterns"),
            exclude_patterns=arguments.get("exclude_patterns"),
            instance_id=arguments.get("instance_id"),
            condition=arguments.get("condition"),
        )
    if name == "spl_refresh" and "changed_files" in arguments:
        router = SPLRouter(
            repo,
            index_dir=arguments.get("index_dir"),
            config=arguments.get("config") or {},
            event_log=arguments.get("event_log"),
        )
        return router.refresh(
            changed_files=arguments.get("changed_files", []),
            regenerate_used_symbols=arguments.get("regenerate_used_symbols", True),
            instance_id=arguments.get("instance_id"),
            condition=arguments.get("condition"),
        )
    index = SPLIndex(repo, arguments.get("index_dir")).load()
    if name == "spl_prepare_repository":
        return index.prepare(
            include_patterns=arguments.get("include_patterns"),
            exclude_patterns=arguments.get("exclude_patterns"),
            incremental=arguments.get("incremental", True),
        )
    if name == "spl_search":
        return index.search(
            query=arguments.get("query", ""),
            task_type=arguments.get("task_type", "code_understanding"),
            top_k=arguments.get("top_k", 8),
            scope=arguments.get("scope") or {},
        )
    if name == "spl_get_card":
        return index.get_card(arguments.get("symbol_id", ""), arguments.get("sections"))
    if name == "spl_trace_dependencies":
        return index.trace_dependencies(
            arguments.get("symbol_id", ""),
            direction=arguments.get("direction", "both"),
            depth=arguments.get("depth", 2),
            include_external=arguments.get("include_external", False),
        )
    if name == "spl_explain_region":
        return index.explain_region(
            file=arguments.get("file", ""),
            start_line=int(arguments.get("start_line", 1)),
            end_line=int(arguments.get("end_line", arguments.get("start_line", 1))),
        )
    if name == "spl_validate":
        return index.validate(arguments.get("symbol_id", ""))
    if name == "spl_refresh":
        return index.refresh(arguments.get("files", []), arguments.get("refresh_dependents", True))
    return {"error": "unknown_tool", "tool": name, "recoverable": True}


def list_tools() -> dict[str, Any]:
    return {"tools": TOOL_SCHEMAS}
