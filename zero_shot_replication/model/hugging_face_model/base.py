from zero_shot_replication.model.base import (
    LargeLanguageModel,
    ModelName,
)
from zero_shot_replication.model.hugging_face_model.hf_llama import (
    HuggingFaceLlamaModel,
)


class HuggingFaceModel(LargeLanguageModel):
    """A concrete class for creating OpenAI models."""

    META_MODELS = [
        ModelName.LLAMA_2_7B_HF,
        ModelName.LLAMA_2_13B_HF,
        ModelName.LLAMA_2_70B_HF,
        ModelName.CODE_LLAMA_7B,
        ModelName.CODE_LLAMA_13B,
        ModelName.CODE_LLAMA_34B,
    ]

    def __init__(
        self,
        model_name: ModelName = ModelName.GPT_4,
        temperature: float = 0.7,
        stream: bool = False,
    ) -> None:
        if stream:
            raise ValueError(
                "Stream is not supported for HuggingFace in this framework."
            )
        if model_name in HuggingFaceModel.META_MODELS:
            raise NotImplementedError("Meta models are not supported yet.")
        else:
            self.model = HuggingFaceLlamaModel(
                model_name,
                temperature,
                stream,
            )

    def get_completion(self, prompt: str) -> str:
        """Get a completion from the OpenAI API based on the provided messages."""
        return self.model.get_completion(prompt)
