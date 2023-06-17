from abc import ABC, abstractmethod
from typing import Any


class AgentTool(ABC):
    def __init__(self, **kwargs):
        pass

    @abstractmethod
    def build(self) -> Any:
        pass
