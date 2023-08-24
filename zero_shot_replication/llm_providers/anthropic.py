from zero_shot_replication.llm_providers.base import LLMProvider


class AnthropicZeroShotProvider(LLMProvider):
    """A class to provide zero-shot completions from the Anthropic API."""

    def __init__(
        self,
        model: str = "claude-2",
        temperature: float = 0.7,
        stream: bool = False,
    ) -> None:
        self.model = model
        self.temperature = temperature
        self.stream = stream

    def get_completion(self, prompt: str) -> str:
        """Get a completion from the Anthropic API based on the provided prompt."""
        raise NotImplementedError(
            "AnthropicZeroShotProvider not implemented yet."
        )
