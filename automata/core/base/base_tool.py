"""Base implementation for tools or skills."""

from abc import abstractmethod
from typing import Optional, Tuple

from pydantic import BaseModel, Extra


class BaseTool(BaseModel):
    """Class responsible for defining a tool or skill for an LLM."""

    name: str
    description: str
    return_direct: bool = False
    verbose: bool = False

    class Config:
        """Configuration for this pydantic object."""

        extra = Extra.forbid
        arbitrary_types_allowed = True

    @abstractmethod
    def _run(self, tool_input: Tuple[Optional[str], ...]) -> str:
        """Use the tool."""

    @abstractmethod
    async def _arun(self, tool_input: Tuple[Optional[str], ...]) -> str:
        """Use the tool asynchronously."""

    def __call__(self, tool_input: Tuple[Optional[str], ...]) -> str:
        """Make tools callable with str input."""
        return self.run(tool_input)

    def run(
        self,
        tool_input: Tuple[Optional[str], ...],
    ) -> str:
        """Run the tool."""
        try:
            observation = self._run(tool_input)
        except (Exception, KeyboardInterrupt) as e:
            raise e
        return observation

    async def arun(
        self,
        tool_input: Tuple[Optional[str], ...],
    ) -> str:
        """Run the tool asynchronously."""
        try:
            # We then call the tool on the tool input to get an observation
            observation = await self._arun(tool_input)
        except (Exception, KeyboardInterrupt) as e:
            raise e
        return observation
