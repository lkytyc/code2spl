from __future__ import annotations

from dataclasses import dataclass

from .symbols import SourceSymbol


@dataclass
class DependencyGraph:
    nodes: list[dict]
    edges: list[dict]


def build_dependency_graph(symbols: list[SourceSymbol]) -> DependencyGraph:
    by_short: dict[str, list[SourceSymbol]] = {}
    for symbol in symbols:
        by_short.setdefault(symbol.symbol.split(".")[-1], []).append(symbol)

    nodes = [
        {
            "id": symbol.symbol_id,
            "symbol": symbol.symbol,
            "file": symbol.file,
            "start_line": symbol.start_line,
            "end_line": symbol.end_line,
            "language": symbol.language,
        }
        for symbol in symbols
    ]
    edges: list[dict] = []
    for symbol in symbols:
        for call in symbol.calls:
            short = call.split(".")[-1]
            targets = by_short.get(short, [])
            if targets:
                for target in targets:
                    if target.symbol_id != symbol.symbol_id:
                        edges.append({
                            "source": symbol.symbol_id,
                            "target": target.symbol_id,
                            "type": "callee",
                            "confidence": "resolved_by_name",
                        })
            else:
                edges.append({
                    "source": symbol.symbol_id,
                    "target": call,
                    "type": "unresolved_reference",
                    "confidence": "unresolved",
                })
    return DependencyGraph(nodes=nodes, edges=edges)
