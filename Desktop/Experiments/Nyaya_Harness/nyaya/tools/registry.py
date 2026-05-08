from nyaya.tools.base import Tool
from nyaya.tools.pratyaksha import (
    InspectState,
    ListDirectory,
    ReadFile,
    RunCommand,
    RunTest,
    SearchFiles,
    WriteFile,
)


class ToolRegistry:
    """Registry of available tools."""

    def __init__(self, workspace: str):
        self.workspace = workspace
        self._tools: dict[str, Tool] = {}
        self._register_defaults()

    def _register_defaults(self) -> None:
        for tool_cls in (
            ReadFile,
            WriteFile,
            RunCommand,
            ListDirectory,
            SearchFiles,
            RunTest,
            InspectState,
        ):
            tool = tool_cls(self.workspace)
            self._tools[f"{tool.category}.{tool.name}"] = tool

    def get(self, tool_name: str) -> Tool:
        if tool_name not in self._tools:
            raise KeyError(f"Unknown tool: {tool_name}")
        return self._tools[tool_name]

    def list_available(self) -> list[dict]:
        return [tool.to_llm_tool_spec() for tool in self._tools.values()]

    def list_by_category(self, category: str) -> list[Tool]:
        return [tool for tool in self._tools.values() if tool.category == category]
