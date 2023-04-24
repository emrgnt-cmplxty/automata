from abc import ABC, abstractmethod
from typing import Any


class BaseToolManager(ABC):
    def __init__(self, **kwargs):
        pass

    @abstractmethod
    def build_tools(self) -> Any:
        pass

    @abstractmethod
    def build_tools_with_automata(self) -> Any:
        pass
