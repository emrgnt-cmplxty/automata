from zero_shot_replication.llm_providers.anthropic_provider import (
    AnthropicZeroShotProvider,
)
from zero_shot_replication.llm_providers.base import (
    MODEL_SETS,
    LargeLanguageModelProvider,
    ProviderConfig,
    ProviderName,
)

# from zero_shot_replication.llm_providers.hugging_face_provider import (
#     HuggingFaceZeroShotProvider,
# )
from zero_shot_replication.llm_providers.openai_provider import (
    OpenAIZeroShotProvider,
)
from zero_shot_replication.model import ModelName


class ProviderManager:
    PROVIDERS = [
        ProviderConfig(
            ProviderName.OPENAI,
            MODEL_SETS[ProviderName.OPENAI],
            OpenAIZeroShotProvider,
        ),
        ProviderConfig(
            ProviderName.ANTHROPIC,
            MODEL_SETS[ProviderName.ANTHROPIC],
            AnthropicZeroShotProvider,
        ),
        # ProviderConfig(
        #     "hugging-face",
        #     ,
        #     HuggingFaceZeroShotProvider,
        # ),
    ]

    @staticmethod
    def get_provider(
        provider_name: ProviderName, model_name: ModelName, *args, **kwargs
    ) -> LargeLanguageModelProvider:
        for provider in ProviderManager.PROVIDERS:
            if (
                provider.name == provider_name
                and model_name not in provider.models
            ):
                raise ValueError(
                    f"Model '{model_name}' not supported by provider '{provider_name}'."
                )
            elif provider.name == provider_name:
                return provider.llm_class(model_name, *args, **kwargs)

        raise ValueError(f"Provider '{provider_name}' not supported.")
