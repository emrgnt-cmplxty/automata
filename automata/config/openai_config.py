"""A config for the OpenAI Automata Agent."""
from typing import Optional

from automata.config import (
    AgentConfig,
    ModelInformation,
)

SUPPORTED_MODEL_INFORMATION = {
    "gpt-4": ModelInformation(
        prompt_token_cost=0.03,
        completion_token_cost=0.06,
        abs_max_tokens=8_192,
    ),
    "gpt-4-32k": ModelInformation(
        prompt_token_cost=0.003,
        completion_token_cost=0.004,
        abs_max_tokens=32_768,
    ),
    "gpt-4-0613": ModelInformation(
        prompt_token_cost=0.03,
        completion_token_cost=0.06,
        abs_max_tokens=8_192,
    ),
    "gpt-3.5-turbo": ModelInformation(
        prompt_token_cost=0.0015,
        completion_token_cost=0.002,
        abs_max_tokens=4_096,
    ),
    "gpt-3.5-turbo-0613": ModelInformation(
        prompt_token_cost=0.0015,
        completion_token_cost=0.002,
        abs_max_tokens=4_096,
    ),
    "gpt-3.5-turbo-16k": ModelInformation(
        prompt_token_cost=0.003,
        completion_token_cost=0.004,
        abs_max_tokens=16_384,
    ),
}


class OpenAIAutomataAgentConfig(AgentConfig):
    """A class to hold the configuration for the Automata OpenAI Agent."""

    arbitrary_types_allowed = True
    system_instruction: Optional[str] = None
