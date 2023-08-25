import logging

import openai

from zero_shot_replication.llm_providers.base import LLMProvider

logger = logging.getLogger(__name__)


class OpenAIZeroShotProvider(LLMProvider):
    """A class to provide zero-shot completions from the OpenAI API."""

    def __init__(
        self,
        model: str = "gpt-4-0613",
        temperature: float = 0.7,
        stream: bool = False,
    ) -> None:
        self.model = model
        self.temperature = temperature
        self.stream = stream

    def get_completion(self, prompt: str) -> str:
        """Get a completion from the OpenAI API based on the provided prompt."""
        logger.info(
            f"Getting completion from OpenAI API for model={self.model}"
        )
        response = openai.ChatCompletion.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt},
            ],
            # functions=[],  # no functions for zero-shot
            temperature=self.temperature,
            stream=self.stream,
        )

        return response.choices[0].message["content"]
