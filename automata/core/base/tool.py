"""Interface for tools."""
from enum import Enum
from inspect import signature
from typing import Any, Awaitable, Callable, List, Optional, Tuple, Union, Dict

from automata.core.base.base_tool import BaseTool


class ToolNotFoundError(Exception):
    def __init__(self, tool_name) -> None:
        self.tool_name = tool_name
        super().__init__(f"Error: Tool '{tool_name}' not found.")


class Tool(BaseTool):
    """Tool that takes in function or coroutine directly."""

    function: Callable[..., str]
    name: str = ""
    description: str = ""
    coroutine: Optional[Callable[..., Awaitable[str]]] = None

    def run(self, tool_input: Dict[str, str]) -> str:
        """Use the tool."""
        return self.function(**tool_input)


class Toolkit:
    """A toolkit of tools."""

    def __init__(self, tools: List[Tool]):
        self.tools = tools

    def __repr__(self) -> str:
        return f"Toolkit(tools={self.tools})"


class ToolkitType(Enum):
    PY_READER = "py_reader"
    PY_WRITER = "py_writer"
    SYMBOL_SEARCH = "symbol_search"
    CONTEXT_ORACLE = "context_oracle"
