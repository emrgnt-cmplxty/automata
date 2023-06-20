from abc import ABC, abstractmethod
from typing import Any


class AgentTool(ABC):
    """AgentTool is an abstract class for building tools for agents."""

    def __init__(self, **kwargs) -> None:
        pass

    @abstractmethod
    def build(self) -> Any:
        pass
