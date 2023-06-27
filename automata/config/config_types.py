from abc import ABC, abstractmethod
from enum import Enum
from typing import Optional

from pydantic import BaseModel, PrivateAttr


class ConfigCategory(Enum):
    """
    A class to represent the different categories of configuration options
    """

    AGENT = "agent"
    PROMPT = "prompt"
    SYMBOL = "symbol"
    INSTRUCTION = "instruction_configs"


class InstructionConfigVersion(Enum):
    """
    InstructionConfigVersion: Enum of instruction versions.
    Corresponds to the name of the yaml file in automata/configs/instruction_configs.
    """

    AGENT_INTRODUCTION = "agent_introduction"


class AgentConfigName(Enum):
    """
    AgentConfigName: Enum of agent config names.
    Corresponds to the name of the yaml file in automata/config/agent/
    """

    # Helper Configs
    DEFAULT = "default"
    TEST = "test"

    # Production Configs
    AUTOMATA_MAIN = "automata_main"


class AgentConfig(ABC, BaseModel):
    class Config:
        arbitrary_types_allowed = True

    @abstractmethod
    def setup(self) -> None:
        """Setup the agent."""
        pass

    @abstractmethod
    def load(cls, config_name: AgentConfigName) -> "AgentConfig":
        """Loads the config for the agent."""
        pass


class AgentConfigBuilder(BaseModel):
    _config: AgentConfig = PrivateAttr()

    def __init__(self, config: Optional[AgentConfig] = None) -> None:
        self._config = config or self.create_config()

    @staticmethod
    def create_config(config_name: Optional[AgentConfigName] = None) -> AgentConfig:
        """Create the specific configuration object"""
        raise NotImplementedError

    def build(self) -> AgentConfig:
        """Build and return an Agent instance with the current configuration."""
        self._config.setup()
        return self._config

    @classmethod
    def from_config(cls, config: AgentConfig) -> "AgentConfigBuilder":
        """Create an AgentConfigBuilder instance using the provided configuration object."""
        return cls(config)

    @classmethod
    def from_name(cls, config_name: AgentConfigName) -> "AgentConfigBuilder":
        """Create an AgentConfigBuilder instance using the provided configuration object name."""
        return cls(cls.create_config(config_name))

    @staticmethod
    def _validate_type(value, expected_type, param_name: str) -> None:
        """Validate the type of the provided value and raise a ValueError if it doesn't match the expected type."""
        if not isinstance(value, expected_type):
            raise ValueError(f"{param_name} must be a {expected_type.__name__}.")
