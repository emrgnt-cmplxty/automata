from abc import ABC, abstractmethod
from typing import List, Optional

from langchain.agents import Tool

from ..utils import PassThroughBuffer


class BaseToolManager(ABC):
    def __init__(self, code_processor, logger: Optional[PassThroughBuffer] = None):
        self.code_processor = code_processor
        self.logger = logger

    @abstractmethod
    def build_tools(self) -> List[Tool]:
        pass
