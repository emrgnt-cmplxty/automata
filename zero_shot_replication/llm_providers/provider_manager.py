from zero_shot_replication.llm_providers.anthropic import (
    AnthropicZeroShotProvider,
)
from zero_shot_replication.llm_providers.base import (
    LLMProvider,
    ProviderConfig,
)
from zero_shot_replication.llm_providers.huggingface import (
    HuggingFaceZeroShotProvider,
)
from zero_shot_replication.llm_providers.openai import OpenAIZeroShotProvider


class ProviderManager:
    PROVIDERS = [
        ProviderConfig(
            "openai",
            [
                "gpt-3.5-turbo-0301",
                "gpt-3.5-turbo-0613",
                "gpt-4-0314",
                "gpt-4-0613",
            ],
            OpenAIZeroShotProvider,
        ),
        ProviderConfig(
            "anthropic",
            ["claude-2", "claude-instant-1"],
            AnthropicZeroShotProvider,
        ),
        ProviderConfig(
            "huggingface",
            [
                "meta-llama/Llama-2-7b-hf",
                "meta-llama/Llama-2-13b-hf",
                "meta-llama/Llama-2-70b-hf",
            ],
            HuggingFaceZeroShotProvider,
        ),
    ]

    @staticmethod
    def get_provider(
        provider_name: str, model_name: str, temperature: float
    ) -> LLMProvider:
        for provider in ProviderManager.PROVIDERS:
            if provider.name == provider_name:
                if model_name in provider.models:
                    return provider.llm_class(
                        model=model_name, temperature=temperature
                    )
                raise ValueError(
                    f"Model '{model_name}' not supported by provider '{provider_name}'"
                )
        raise ValueError(f"Provider '{provider_name}' not supported.")
