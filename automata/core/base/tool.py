"""Interface for tools."""
from typing import Awaitable, Callable, Dict, Optional

from pydantic import BaseModel, Extra


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
