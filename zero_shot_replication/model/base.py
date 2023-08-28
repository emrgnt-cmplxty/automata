from abc import ABC, abstractmethod
from enum import Enum
from typing import Any


class ModelName(Enum):
    """An enum to hold the names of the models."""

    # OpenAI Models

    ## GPT-3.5
    GPT_3p5_TURBO_0301 = "gpt-3.5-turbo-0301"
    GPT_3p5_TURBO_0613 = "gpt-3.5-turbo-0613"
    GPT_3p5_TURBO = "gpt-3.5-turbo"

    ## GPT-4
    GPT_4_0314 = "gpt-4-0314"
    GPT_4_0613 = "gpt-4-0613"
    GPT_4 = "gpt-4"

    # Anthropic Models
    CLAUDE_INSTANT_1 = "claude-instant-1"
    CLAUDE_2 = "claude-2"

    # Meta Open Source Models
    LLAMA_2_7B_HF = "meta-llama/Llama-2-7b-hf"
    LLAMA_2_13B_HF = "meta-llama/Llama-2-13b-hf"
    LLAMA_2_70B_HF = "meta-llama/Llama-2-70b-hf"
    CODE_LLAMA_7B = "CodeLlama-7b-Python"
    CODE_LLAMA_13B = "CodeLlama-13b-Python"
    CODE_LLAMA_34B = "CodeLlama-34b-Python"

    META_MODELS = [
        LLAMA_2_7B_HF,
        LLAMA_2_13B_HF,
        LLAMA_2_70B_HF,
        CODE_LLAMA_7B,
        CODE_LLAMA_13B,
        CODE_LLAMA_34B,
    ]

    # Other HF Open Source Models
    WIZARD_LM_PYTHON_34B = "WizardLM/WizardCoder-Python-34B-V1.0"


class PromptMode(Enum):
    HUMAN_FEEDBACK = "human-feedback"
    COMPLETION = "completion"
    CLASSIFICATION = "classification"


class LargeLanguageModel(ABC):
    """An abstract class to provide a common interface for LLMs."""

    def __init__(
        self,
        model_name: ModelName,
        temperature: float,
        stream: bool,
        prompt_mode: PromptMode,
    ) -> None:
        self.model_name = model_name
        self.temperature = temperature
        self.stream = stream
        self.prompt_mode = prompt_mode

    @abstractmethod
    def get_completion(self, input: Any) -> str:
        pass
