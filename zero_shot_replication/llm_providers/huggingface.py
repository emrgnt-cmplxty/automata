import logging
import os

import torch
from transformers import LlamaForCausalLM, LlamaTokenizer, GenerationConfig

from zero_shot_replication.llm_providers.base import LLMProvider

logger = logging.getLogger(__name__)


class LocalLLamaModel:
    """A class to provide zero-shot completions from a local Llama model."""

    # TODO - Make these upstream configurations
    MAX_OUTPUT_LENGTH = 2048
    TOP_K = 40
    TOP_P = 0.9
    NUM_BEAMS = 1

    def __init__(
        self,
        model: str,
        temperature: float,
        hf_access_token: str,
        max_output_length=None,
    ) -> None:
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        logger.info(f"Selecting device = {self.device}")

        self.hf_access_token = hf_access_token
        self.max_output_length = (
            max_output_length or LocalLLamaModel.MAX_OUTPUT_LENGTH
        )
        self.tokenizer = LlamaTokenizer.from_pretrained(
            model,
            device_map="auto",
            torch_dtype=torch.float16,
            use_auth_token=self.hf_access_token,
        )

        self.model = LlamaForCausalLM.from_pretrained(
            model,
            torch_dtype=torch.float16,
            device_map="auto",
            use_auth_token=self.hf_access_token,
        )
        self.temperature = temperature

    def get_completion(self, prompt: str, *args, **kwargs) -> str:
        inputs = self.tokenizer(prompt, return_tensors="pt").to(self.device)

        # TODO - Move to HF Configuration approach

        generation_config = GenerationConfig(
            temperature=self.temperature,
            top_p=LocalLLamaModel.TOP_P,
            top_k=LocalLLamaModel.TOP_K,
            num_beams=LocalLLamaModel.NUM_BEAMS,
            eos_token_id=self.tokenizer.eos_token_id,
            pad_token_id=self.tokenizer.pad_token_id,
            do_sample=True,
        )


        output = self.model.generate(
            inputs["input_ids"],
            generation_config=generation_config,
            do_sample=True,
            max_new_tokens=self.max_output_length,
        )

        output = output[0].to(self.device)
        return self.tokenizer.decode(output)


class HuggingFaceZeroShotProvider(LLMProvider):
    """A class to provide zero-shot completions from the Anthropic API."""

    def __init__(
        self,
        model: str = "meta-llama/Llama-2-7b-hf",
        temperature: float = 0.7,
        stream: bool = False,
    ) -> None:
        self.stream = stream
        self.hf_token = os.getenv("HF_TOKEN", "")
        self.loaded_model = LocalLLamaModel(model, temperature, self.hf_token)

    def get_completion(self, prompt: str) -> str:
        """Get a completion from the Anthropic API based on the provided prompt."""
        # TODO - Consider more intelligent place for the '###Response:' string
        # This was added to match WizardCoder approach exactly.
        prompt = f"{prompt}\n### Response:\n"
        completion = self.loaded_model.get_completion(prompt)
        if prompt in completion:
            completion = completion.split(prompt)[1]
        logger.info(f"Found a completion {completion}")
        return completion
