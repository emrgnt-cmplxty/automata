import logging
import os

import torch
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    GenerationConfig,
    LlamaForCausalLM,
    LlamaTokenizer,
    StoppingCriteria,
    StoppingCriteriaList,
)

from zero_shot_replication.llm_providers.base import LargeLanguageModelProvider

logger = logging.getLogger(__name__)


class HuggingFaceZeroShotProvider(LargeLanguageModelProvider):
    """A class to provide zero-shot completions from the HuggingFace API."""

    def __init__(
        self,
        model: str = "meta-llama/Llama-2-7b-hf",
        temperature: float = 0.7,
        stream: bool = False,
    ) -> None:
        self.stream = stream
        self.hf_token = os.getenv("HF_TOKEN", "")
        if model in [
            "codellama/CodeLlama-7b-Python-hf",
            "codellama/CodeLlama-7b-hf",
            "codellama/CodeLlama-13b-hf",
            "codellama/CodeLlama-13b-Python-hf",
        ]:
            self.instruct_based = False
            self.loaded_model = LocalCodeLLamaModel(
                model, temperature, self.hf_token
            )
        elif model in ["CodeLlama-7b-Python", "CodeLlama-13b-Python"]:
            self.instruct_based = False
            self.loaded_model = CodeLlama(model, temperature)
        else:
            self.loaded_model = LocalLLamaModel(
                model, temperature, self.hf_token
            )

    def get_completion(self, prompt: str) -> str:
        """Get a completion from the Anthropic API based on the provided prompt."""
        # TODO - Consider more intelligent placing the '###Response:' string
        # This was added to match WizardCoder approach exactly.
        # Luckily, it is naturally aligned with the structure of our prompt.
        if self.instruct_based:
            prompt = f"{prompt}\n### Response:\n"
            completion = self.loaded_model.get_completion(prompt)
            if prompt in completion:
                completion = completion.split(prompt)[1]
        else:
            completion = self.loaded_model.get_completion(prompt)
        logger.info(f"Found a completion {completion}")
        return completion
