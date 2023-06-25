from abc import ABC, abstractmethod


import logging
from typing import Optional, Tuple

from automata.core.base.llm.llm_types import LLMCompletionResult

logger = logging.getLogger(__name__)


class Agent(ABC):
    """
    An agent is an autonomous entity that can perform actions and communicate with other agents.
    """

    @abstractmethod
    def iter_step(self) -> Optional[Tuple[LLMCompletionResult, LLMCompletionResult]]:
        pass

    @abstractmethod
    def run(self) -> str:
        pass

    @abstractmethod
    def setup(self) -> None:
        pass
