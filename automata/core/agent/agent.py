from abc import ABC, abstractmethod
from typing import Optional, Tuple

from automata.core.base.openai import OpenAIChatMessage


class Agent(ABC):
    @abstractmethod
    def iter_task(self) -> Optional[Tuple[OpenAIChatMessage, OpenAIChatMessage]]:
        pass

    @abstractmethod
    def modify_last_instruction(self, new_instruction: str) -> None:
        pass

    @abstractmethod
    def replay_messages(self) -> str:
        pass

    @abstractmethod
    def run(self) -> str:
        pass
