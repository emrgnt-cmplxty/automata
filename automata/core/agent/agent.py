from abc import ABC, abstractmethod
from typing import Dict, Optional, Tuple


class Agent(ABC):
    @abstractmethod
    def iter_task(self) -> Optional[Tuple[Dict[str, str], Dict[str, str]]]:
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
