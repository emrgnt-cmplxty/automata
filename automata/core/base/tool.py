"""Interface for tools."""
from enum import Enum
from inspect import signature
from typing import Any, Awaitable, Callable, Dict, List, Optional, Tuple, Union

from pydantic import BaseModel, Extra


class ToolNotFoundError(Exception):
    def __init__(self, tool_name) -> None:
        self.tool_name = tool_name
        super().__init__(f"Error: Tool '{tool_name}' not found.")


class Tool(BaseModel):
    """Tool that takes in function or coroutine directly."""

    class Config:
        """Configuration for this pydantic object."""

        extra = Extra.forbid
        arbitrary_types_allowed = True

    function: Callable[..., str]
    name: str = ""
    description: str = ""
    coroutine: Optional[Callable[..., Awaitable[str]]] = None

    def run(self, tool_input: Dict[str, str]) -> str:
        """Use the tool."""
        return self.function(**tool_input)
