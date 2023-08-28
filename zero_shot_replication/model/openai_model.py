import openai

from zero_shot_replication.model.base import (
    LargeLanguageModel,
    ModelName,
    PromptMode,
)


class OpenAIModel(LargeLanguageModel):
    """A concrete class for creating OpenAI models."""

    def __init__(
        self,
        model_name: ModelName = ModelName.GPT_4,
        temperature: float = 0.7,
        stream: bool = False,
    ) -> None:
        if stream:
            raise ValueError(
                "Stream is not supported for OpenAI in this framework."
            )
        super().__init__(
            model_name,
            temperature,
            stream,
            prompt_mode=PromptMode.HUMAN_FEEDBACK,
        )

    def get_completion(self, messages: list[dict]) -> str:
        """Get a completion from the OpenAI API based on the provided messages."""

        # TODO - Add support for functions.

        response = openai.ChatCompletion.create(
            model=self.model_name.value,
            messages=messages,
            temperature=self.temperature,
            stream=self.stream,
        )

        return response.choices[0].message["content"]
