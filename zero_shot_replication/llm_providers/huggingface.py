import os
from threading import Thread
from typing import Dict

import torch
from transformers import (
    GenerationConfig,
    LlamaForCausalLM,
    LlamaTokenizer,
    TextIteratorStreamer,
)


class LocalLLamaModel:
    """A class to provide zero-shot completions from a local Llama model."""

    DEFAULT_MAX_LENGTH = 128
    # DEFAULT_TOP_P = 0.95

    def __init__(
        self, model: str, hf_access_token: str, max_output_length=None
    ) -> None:
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.hf_access_token = hf_access_token
        self.max_output_length = (
            max_output_length or LocalLLamaModel.DEFAULT_MAX_LENGTH
        )
        self.tokenizer = LlamaTokenizer.from_pretrained(
            model,
            device_map="auto",
            torch_dtype=torch.float16,
            add_eos_token=True,
            use_auth_token=self.hf_access_token,
        )
        self.tokenizer.pad_token_id = self.tokenizer.eos_token_id

        self.model = LlamaForCausalLM.from_pretrained(
            model,
            torch_dtype=torch.float16,
            device_map="auto",
            use_auth_token=self.hf_access_token,
        )
        self.model.to(self.device)

    def get_completion(self, ipt: str, *args, **kwargs) -> str:
        template = (
            "The following is a conversation between a human and an AI assistant. "
            "The AI assistant gives helpful, detailed, and polite answers to the user's questions.\n"
            "[|Human|]: {instruction}\n\n[|AI|]:"
        )
        text = template.format_map(dict(instruction=ipt))
        inputs = self.tokenizer(text, return_tensors="pt").to(self.device)
        outputs = self.model.generate(
            **inputs,
            max_new_tokens=self.max_output_length,
            **kwargs,
        )
        batch_size, length = inputs.input_ids.shape
        return self.tokenizer.decode(
            outputs[0, length:], skip_special_tokens=True
        )


from zero_shot_replication.llm_providers.base import LLMProvider


class HuggingFaceZeroShotProvider(LLMProvider):
    """A class to provide zero-shot completions from the Anthropic API."""

    MAX_TOKENS_TO_SAMPLE = (
        4_096  # This is a large value, we should check if it makes sense
    )

    def __init__(
        self,
        model: str = "llama-2-13b",
        temperature: float = 0.7,
        stream: bool = False,
    ) -> None:
        self.model = model
        self.temperature = temperature
        self.stream = stream
        self.hf_token = os.getenv("HF_TOKEN", "")
        self.loaded_model = LocalLLamaModel(model, self.hf_token)

    def get_completion(self, prompt: str) -> str:
        """Get a completion from the Anthropic API based on the provided prompt."""
        return self.loaded_model.get_completion(prompt)
