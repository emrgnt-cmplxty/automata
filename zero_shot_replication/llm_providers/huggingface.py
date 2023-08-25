import torch
import transformers
from transformers import AutoTokenizer

from zero_shot_replication.llm_providers.base import LLMProvider


class HuggingFaceZeroShotProvider(LLMProvider):
    """A class to provide zero-shot completions from the Anthropic API."""

    MAX_TOKENS_TO_SAMPLE = (
        4_096  # This is a large value, we should check if it makes sense
    )

    def __init__(
        self,
        model: str = "facebook/opt-125m",
        temperature: float = 0.7,
        stream: bool = False,
    ) -> None:
        print("model = ", model)
        self.model = model
        self.temperature = temperature
        self.stream = stream
        self.tokenizer = AutoTokenizer.from_pretrained(self.model)

        self.pipeline = transformers.pipeline(
            "text-generation",
            model=self.model,
            torch_dtype=torch.float16,
            device_map="auto",
        )

    def get_completion(self, prompt: str) -> str:
        """Get a completion from the Anthropic API based on the provided prompt."""

        sequences = self.pipeline(
            'I liked "Breaking Bad" and "Band of Brothers". Do you have any recommendations of other shows I might like?\n',
            do_sample=True,
            top_k=10,
            num_return_sequences=1,
            eos_token_id=self.tokenizer.eos_token_id,
            max_length=200,
        )
        for seq in sequences:
            print(f"Result: {seq['generated_text']}")
        raise NotImplementedError(
            "HuggingFaceZeroShotProvider not implemented."
        )
