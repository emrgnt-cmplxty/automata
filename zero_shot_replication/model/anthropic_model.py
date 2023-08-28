from anthropic import AI_PROMPT, HUMAN_PROMPT, Anthropic

from zero_shot_replication.model.base import (
    LargeLanguageModel,
    ModelName,
    PromptMode,
)


class AnthropicModel(LargeLanguageModel):
    """A concrete class for creating Anthropic models."""

    def __init__(
        self,
        model_name: ModelName,
        temperature: float,
        stream: bool,
        max_tokens_to_sample: int,
    ) -> None:
        super().__init__(
            model_name,
            temperature,
            stream,
            prompt_mode=PromptMode.HUMAN_FEEDBACK,
        )
        self.anthropic = Anthropic()
        self.max_tokens_to_sample = max_tokens_to_sample

    def get_completion(self, prompt: str) -> str:
        """Get a completion from the Anthropic API based on the provided messages."""

        formatted_prompt = f"{HUMAN_PROMPT} {prompt} {AI_PROMPT}"

        completion = self.anthropic.completions.create(
            model=self.model_name.value,
            max_tokens_to_sample=self.max_tokens_to_sample,
            stream=self.stream,
            prompt=formatted_prompt,
            temperature=self.temperature,
        )  # type: ignore
        return completion.completion
