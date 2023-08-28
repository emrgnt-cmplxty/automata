import logging
import os

import torch
from transformers import GenerationConfig, LlamaForCausalLM, LlamaTokenizer

from zero_shot_replication.model.base import (
    LargeLanguageModel,
    ModelName,
    PromptMode,
)

logger = logging.getLogger(__name__)


class HuggingFaceLlamaModel(LargeLanguageModel):
    """A class to provide zero-shot completions from a local Llama model."""

    # TODO - Make these upstream configurations
    MAX_OUTPUT_LENGTH = 2048
    TOP_K = 40
    TOP_P = 0.9
    NUM_BEAMS = 1

    def __init__(
        self,
        model_name: ModelName,
        temperature: float,
        stream: bool,
        max_output_length=None,
    ) -> None:
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        logger.info(f"Selecting device = {self.device}")

        super().__init__(
            model_name,
            temperature,
            stream,
            prompt_mode=PromptMode.HUMAN_FEEDBACK,
        )
        self.max_output_length = (
            max_output_length or HuggingFaceLlamaModel.MAX_OUTPUT_LENGTH
        )
        self.hf_access_token = os.getenv("HF_TOKEN", "")

        self.tokenizer = LlamaTokenizer.from_pretrained(
            model_name.value,
            torch_dtype=torch.float16,
            device_map="auto",
            use_auth_token=self.hf_access_token,
        )

        self.model = LlamaForCausalLM.from_pretrained(
            model_name.value,
            torch_dtype=torch.float16,
            device_map="auto",
            use_auth_token=self.hf_access_token,
        )
        self.temperature = temperature

    def get_completion(self, prompt: str) -> str:
        """Generate the completion from the local Llama model."""
        # TODO - Move all configurations upstream

        inputs = self.tokenizer(prompt, return_tensors="pt").to(self.device)

        generation_config = GenerationConfig(
            temperature=self.temperature,
            top_p=HuggingFaceLlamaModel.TOP_P,
            top_k=HuggingFaceLlamaModel.TOP_K,
            num_beams=HuggingFaceLlamaModel.NUM_BEAMS,
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
