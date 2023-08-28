from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum
from typing import List, Type

from zero_shot_replication.model.base import LargeLanguageModel, ModelName


class ProviderName(Enum):
    OPENAI = "openai"
    ANTHROPIC = "anthropic"
    HUGGING_FACE = "hugging-face"


class LargeLanguageModelProvider(ABC):
    """An abstract class to provide a common interface for LLM providers."""

    @abstractmethod
    def __init__(self, model_name: ModelName, temperature: float) -> None:
        pass

    @abstractmethod
    def get_completion(self, prompt: str) -> str:
        pass

    @property
    @abstractmethod
    def model(self) -> LargeLanguageModel:
        """Property to get the instance of LargeLanguageModel."""

        pass


@dataclass
class ProviderConfig:
    """A dataclass to hold the configuration for a provider."""

    name: ProviderName
    models: List[ModelName]
    llm_class: Type[LargeLanguageModelProvider]


MODEL_SETS = {
    ProviderName.OPENAI: [
        ModelName.GPT_3p5_TURBO_0301,
        ModelName.GPT_3p5_TURBO_0613,
        ModelName.GPT_3p5_TURBO,
        ModelName.GPT_4_0314,
        ModelName.GPT_4_0613,
        ModelName.GPT_4,
    ],
    ProviderName.ANTHROPIC: [
        ModelName.CLAUDE_INSTANT_1,
        ModelName.CLAUDE_2,
    ],
    ProviderName.HUGGING_FACE: [
        ModelName.LLAMA_2_7B_HF,
        ModelName.LLAMA_2_13B_HF,
        ModelName.LLAMA_2_70B_HF,
        ModelName.CODE_LLAMA_7B,
        ModelName.CODE_LLAMA_13B,
        ModelName.CODE_LLAMA_34B,
        ModelName.WIZARD_LM_PYTHON_34B,
    ],
}
