from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List, Type


class LLMProvider(ABC):
    @abstractmethod
    def get_completion(self, prompt: str) -> str:
        pass


@dataclass
class ProviderConfig:
    name: str
    models: List[str]
    llm_class: Type[LLMProvider]
