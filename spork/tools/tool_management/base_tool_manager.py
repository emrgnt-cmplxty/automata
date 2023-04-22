from abc import ABC, abstractmethod
from typing import List

from spork.core.base.tool import Tool


class BaseToolManager(ABC):
    def __init__(self, code_processor):
        self.code_processor = code_processor

    @abstractmethod
    def build_tools(self) -> List[Tool]:
        pass

    @abstractmethod
    def build_tools_with_meeseeks(self) -> List[Tool]:
        pass
