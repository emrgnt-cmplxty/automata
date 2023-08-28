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
from zero_shot_replication.llm_providers.automata import AutomataZeroShotProvider


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
                "WizardLM/WizardCoder-Python-34B-V1.0",
                "meta-llama/Llama-2-7b-hf",
                "meta-llama/Llama-2-13b-hf",
                "meta-llama/Llama-2-70b-hf",
                "codellama/CodeLlama-7b-Python-hf",
                "codellama/CodeLlama-13b-Python-hf",
                "codellama/CodeLlama-7b-hf",
                "codellama/CodeLlama-13b-hf",
                "CodeLlama-7b-Python",
                "CodeLlama-13b-Python",
            ],
            HuggingFaceZeroShotProvider,
        ),
        ProviderConfig(
            "automata",
            [
                "gpt-4-0314",
            ],
            AutomataZeroShotProvider,
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
