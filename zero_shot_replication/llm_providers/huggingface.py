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

CHECKPOINT = "meta-llama/Llama-2-7b-hf"
DEFAULT_MAX_LENGTH = 128
DEFAULT_TOP_P = 0.95


class LocalLLamaModel:
    def __init__(self, hf_access_token: str) -> None:
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.tokenizer = None
        self.pipeline = None
        print("hf_access_token = ", hf_access_token)
        self.hf_access_token = hf_access_token

    def load(self):
        self.model = LlamaForCausalLM.from_pretrained(
            CHECKPOINT,
            use_auth_token=self.hf_access_token,
            torch_dtype=torch.float16,
            device_map="auto",
        )

        self.tokenizer = LlamaTokenizer.from_pretrained(
            CHECKPOINT,
            device_map="auto",
            torch_dtype=torch.float16,
            use_auth_token=self.hf_access_token,
        )

    def stream_model(self, prompt: str, *args, **kwargs):
        streamer = TextIteratorStreamer(self.tokenizer)

        with torch.no_grad():
            generation_config = GenerationConfig(
                **kwargs,
            )
            inputs = self.tokenizer(
                prompt,
                return_tensors="pt",
                max_length=DEFAULT_MAX_LENGTH,
                truncation=True,
                padding=True,
            )
            input_ids = inputs["input_ids"].to("cuda")
            generation_kwargs = {
                "input_ids": input_ids,
                "generation_config": generation_config,
                "return_dict_in_generate": True,
                "output_scores": True,
                "max_new_tokens": 1_024,  # generation_args["max_new_tokens"],
                "streamer": streamer,
            }
            thread = Thread(
                target=self.model.generate, kwargs=generation_kwargs
            )
            thread.start()

            def inner():
                yield from streamer
                thread.join()

        return inner()

    # def predict(self, request: Dict):

    #     if stream:
    #         return self.stream_model(request)

    #     with torch.no_grad():
    #         try:
    #             prompt = request.pop("prompt")
    #             input_ids = self.tokenizer(
    #                 prompt, return_tensors="pt"
    #             ).input_ids.cuda()
    #             output = self.model.generate(
    #                 inputs=input_ids, **request["generate_args"]
    #             )

    #             return self.tokenizer.decode(output[0])
    #         except Exception as exc:
    #             return {"status": "error", "data": None, "message": str(exc)}


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
        self.loaded_model = LocalLLamaModel(self.hf_token).load()

    def get_completion(self, prompt: str) -> str:
        """Get a completion from the Anthropic API based on the provided prompt."""
        return self.loaded_model.stream_model(prompt)
