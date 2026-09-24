from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

from .tools import handle_tool, list_tools


def _jsonrpc_result(request_id: Any, result: Any) -> dict[str, Any]:
    return {"jsonrpc": "2.0", "id": request_id, "result": result}


def _jsonrpc_error(request_id: Any, code: int, message: str, data: Any = None) -> dict[str, Any]:
    error = {"code": code, "message": message}
    if data is not None:
        error["data"] = data
    return {"jsonrpc": "2.0", "id": request_id, "error": error}


def dispatch(message: dict[str, Any]) -> dict[str, Any] | None:
    method = message.get("method")
    request_id = message.get("id")
    params = message.get("params") or {}
    try:
        if method == "initialize":
            return _jsonrpc_result(request_id, {
                "protocolVersion": "2024-11-05",
                "serverInfo": {"name": "spl-code-understanding", "version": "0.1.0"},
                "capabilities": {"tools": {}},
            })
        if method == "tools/list":
            return _jsonrpc_result(request_id, list_tools())
        if method == "tools/call":
            name = params.get("name", "")
            arguments = params.get("arguments") or {}
            result = handle_tool(name, arguments)
            return _jsonrpc_result(request_id, {"content": [{"type": "text", "text": json.dumps(result, ensure_ascii=False)}]})
        if method in {"notifications/initialized", "initialized"}:
            return None
        return _jsonrpc_error(request_id, -32601, f"Unknown method: {method}")
    except Exception as exc:
        return _jsonrpc_error(request_id, -32000, type(exc).__name__, {"message": str(exc)})


def serve_stdio() -> None:
    for line in sys.stdin:
        if not line.strip():
            continue
        try:
            message = json.loads(line)
        except json.JSONDecodeError as exc:
            print(json.dumps(_jsonrpc_error(None, -32700, "Parse error", str(exc))), flush=True)
            continue
        response = dispatch(message)
        if response is not None:
            print(json.dumps(response, ensure_ascii=False), flush=True)


def call_once(tool: str, arguments_json: str) -> None:
    arguments = json.loads(arguments_json) if arguments_json else {}
    print(json.dumps(handle_tool(tool, arguments), ensure_ascii=False, indent=2))


def main() -> None:
    parser = argparse.ArgumentParser(description="SPL code-understanding MCP-compatible server")
    parser.add_argument("--stdio", action="store_true", help="Run JSON-RPC stdio server")
    parser.add_argument("--call", help="Call one tool directly for smoke testing")
    parser.add_argument("--arguments", default="{}", help="JSON object for --call")
    parser.add_argument("--arguments-file", help="Read JSON object for --call from a file")
    args = parser.parse_args()
    if args.call:
        arguments = Path(args.arguments_file).read_text(encoding="utf-8") if args.arguments_file else args.arguments
        call_once(args.call, arguments)
        return
    serve_stdio()


if __name__ == "__main__":
    main()
