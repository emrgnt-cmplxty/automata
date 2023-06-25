"""Interface for tools."""
from enum import Enum
from inspect import signature
from typing import Any, Awaitable, Callable, List, Optional, Tuple, Union

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

    def _run(self, tool_input: Tuple[Optional[str], ...]) -> str:
        """Use the tool."""
        return self.function(*tool_input)

    async def _arun(self, tool_input: Tuple[Optional[str], ...]) -> str:
        """Use the tool asynchronously."""
        if self.coroutine:
            return await self.coroutine(tool_input)
        raise NotImplementedError("Tool does not support async")

    # TODO: this is for backwards compatibility, remove in future
    def __init__(self, name: str, function: Callable[[str], str], description: str, **kwargs: Any):
        """Initialize tool."""
        super(Tool, self).__init__(name=name, function=function, description=description, **kwargs)  # type: ignore


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
