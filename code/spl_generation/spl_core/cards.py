from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any


DEFAULT_SECTIONS = {
    "summary",
    "inputs",
    "outputs",
    "main_flow",
    "alternative_flows",
    "exceptions",
    "callees",
    "callers",
    "state_changes",
}


@dataclass
class SourceProvenance:
    file: str
    start_line: int
    end_line: int
    language: str
    content_hash: str
    revision: str


@dataclass
class SPLCard:
    symbol_id: str
    symbol: str
    source: SourceProvenance
    summary: str
    inputs: list[dict[str, Any]] = field(default_factory=list)
    outputs: list[dict[str, Any]] = field(default_factory=list)
    main_flow: list[str] = field(default_factory=list)
    alternative_flows: list[str] = field(default_factory=list)
    exception_flows: list[str] = field(default_factory=list)
    callees: list[str] = field(default_factory=list)
    callers: list[str] = field(default_factory=list)
    state_changes: list[str] = field(default_factory=list)
    spl_text: str = ""
    fresh: bool = True
    limitations: list[str] = field(default_factory=lambda: [
        "This card describes the currently indexed implementation.",
        "Verify the corresponding source before editing.",
    ])

    def to_dict(self, sections: list[str] | None = None) -> dict[str, Any]:
        data = asdict(self)
        data["source"] = asdict(self.source)
        if not sections:
            return data
        keep = {"symbol_id", "symbol", "source", "fresh", "limitations"} | set(sections)
        if "exceptions" in keep:
            keep.add("exception_flows")
        return {key: value for key, value in data.items() if key in keep}

