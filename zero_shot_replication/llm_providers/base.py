from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List, Type


class LLMProvider(ABC):
    """An abstract class to provide a common interface for LLM providers."""

    instruct_based = True  # default is instruction-based LLM

    @abstractmethod
    def __init__(self, model: str, temperature: float) -> None:
        pass

    @abstractmethod
    def get_completion(self, prompt: str) -> str:
        pass


@dataclass
class ProviderConfig:
    """A dataclass to hold the configuration for a provider."""

    name: str
    models: List[str]
    llm_class: Type[LLMProvider]
