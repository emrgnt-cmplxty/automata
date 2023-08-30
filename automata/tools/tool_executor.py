from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Sequence

from automata.tools.tool_base import Tool

if TYPE_CHECKING:
    from automata.llm import FunctionCall


class IToolExecution(ABC):
    """Interface for executing tools."""

    @abstractmethod
    def execute(self, function_call: "FunctionCall") -> str:
        pass

    @abstractmethod
    def is_valid_tool(self, tool_name: str) -> bool:
        """Check if the tool name exists within the known tools."""
        pass


class ToolExecution(IToolExecution):
    """Class for executing tools."""

    def __init__(self, tools: Sequence[Tool]) -> None:
        self.tools = {tool.name: tool for tool in tools}

    def execute(self, function_call: "FunctionCall") -> str:
        if tool := self.tools.get(function_call.name):
            return tool.run(function_call.arguments)
        else:
            raise Exception(
                f"No tool found for function call: {function_call.name}"
            )

    def is_valid_tool(self, tool_name: str) -> bool:
        """Check if the tool name exists within the known tools."""
        return tool_name in self.tools


class ToolExecutor:
    """Class for using IToolExecution behavior to execute a tool."""

    def __init__(self, execution: IToolExecution) -> None:
        self.execution = execution

    def execute(self, function_call: "FunctionCall") -> str:
        return self.execution.execute(function_call)

    def is_valid_tool(self, tool_name: str) -> bool:
        """Forward the call to ToolExecution's is_valid_tool method."""
        return self.execution.is_valid_tool(tool_name)
