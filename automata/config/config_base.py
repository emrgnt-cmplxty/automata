"""
Base classes for configuration options.
"""
from abc import ABC
from dataclasses import dataclass
from enum import Enum
from typing import List

from pydantic import BaseModel

from automata.core.utils import convert_kebab_to_snake_case
from automata.tools.tool_base import Tool


class PathEnum(Enum):

    """A base class for enums that represent paths."""

    def to_path(self) -> str:
        return convert_kebab_to_snake_case(self.value)


class InstructionConfigVersion(PathEnum):
    """
    InstructionConfigVersion: Enum of instruction versions.
    Corresponds files in automata/configs/instruction_configs/*.yaml
    """

    AGENT_INTRODUCTION = "agent-introduction"
    PLUMB_BOT = "bad-introduction"


class LLMProvider(PathEnum):
    OPENAI = "openai"


@dataclass
class ModelInformation:
    """A class to represent the model information"""

    prompt_token_cost: float
    completion_token_cost: float
    abs_max_tokens: int


class AgentConfig(ABC, BaseModel):
    """An abstract class to represent the configuration of an agent."""

    tools: List[Tool] = []
    instructions: str = ""
    description: str = ""
    system_template: str = ""
    model: str = "gpt-4"
    stream: bool = False
    verbose: bool = False
    max_iterations: int = 50
    abs_max_tokens: int = 8192
    max_token_percentage: float = 0.9
    max_tokens = int(0.9 * 8192)
    temperature: float = 0.7

    class Config:
        arbitrary_types_allowed = True
        provider = LLMProvider.OPENAI
