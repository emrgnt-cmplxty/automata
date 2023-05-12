from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Optional, Tuple

from automata.core.base.openai import OpenAIChatMessage

if TYPE_CHECKING:
    from automata.core.coordinator.automata_coordinator import AutomataCoordinator


class Agent(ABC):
    @abstractmethod
    def set_coordinator(self, coordinator: "AutomataCoordinator"):
        pass

    @abstractmethod
    def iter_task(self) -> Optional[Tuple[OpenAIChatMessage, OpenAIChatMessage]]:
        pass

    @abstractmethod
    def run(self) -> str:
        pass
