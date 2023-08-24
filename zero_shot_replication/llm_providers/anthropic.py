from anthropic import AI_PROMPT, HUMAN_PROMPT, Anthropic

from zero_shot_replication.llm_providers.base import LLMProvider


class AnthropicZeroShotProvider(LLMProvider):
    """A class to provide zero-shot completions from the Anthropic API."""

    MAX_TOKENS_TO_SAMPLE = (
        4_096  # This is a large value, we should check if it makes sense
    )

    def __init__(
        self,
        model: str = "claude-2",
        temperature: float = 0.7,
        stream: bool = False,
    ) -> None:
        self.model = model
        self.temperature = temperature
        self.stream = stream
        self.anthropic = Anthropic()

    def get_completion(self, prompt: str) -> str:
        """Get a completion from the Anthropic API based on the provided prompt."""

        formatted_prompt = f"{HUMAN_PROMPT} {prompt} {AI_PROMPT}"
        completion = self.anthropic.completions.create(
            model="claude-2",
            max_tokens_to_sample=AnthropicZeroShotProvider.MAX_TOKENS_TO_SAMPLE,
            stream=self.stream,
            prompt=formatted_prompt,
            temperature=self.temperature,
        )  # type: ignore
        return completion.completion
