from nyaya.schemas.pancavayava import PancavayavaStep
from nyaya.tools.registry import ToolRegistry


def execute_tool_calls(step: PancavayavaStep, tool_calls: list[dict], tools: ToolRegistry) -> None:
    applied = []
    for call in tool_calls:
        tool = tools.get(call["tool"])
        pramana_call = tool.call(used_for="upanaya", **call.get("args", {}))
        step.pramana_calls.append(pramana_call)
        applied.append(f"{pramana_call.tool}({pramana_call.input})")
    step.upanaya = "\n".join(applied) if applied else "No tool calls"
