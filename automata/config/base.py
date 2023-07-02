import os
from abc import ABC, abstractmethod
from enum import Enum
from typing import Dict, Generic, List, Optional, TypeVar, Union

import yaml
from pydantic import BaseModel, PrivateAttr

from automata.core.tools.base import Tool
from automata.core.utils import convert_kebab_to_snake


class ConfigCategory(Enum):
    """
    A class to represent the different categories of configuration options
    Corresponds folders in automata/configs/*
    """

    AGENT = "agent"
    PROMPT = "prompt"
    SYMBOL = "symbol"
    INSTRUCTION = "instruction_configs"


class InstructionConfigVersion(Enum):
    """
    InstructionConfigVersion: Enum of instruction versions.
    Corresponds files in automata/configs/instruction_configs/*.yaml
    """

    AGENT_INTRODUCTION = "agent_introduction"


class AgentConfigName(Enum):
    """
    AgentConfigName: Enum of agent config names.
    Corresponds files in automata/config/agent/*.yaml
    """

    # Helper Configs
    DEFAULT = "default"
    TEST = "test"

    # Production Configs
    AUTOMATA_MAIN = "automata-main"


class LLMProvider(Enum):
    OPENAI = "openai"


class AgentConfig(ABC, BaseModel):
    config_name: AgentConfigName = AgentConfigName.DEFAULT
    tools: List[Tool] = []
    instructions: str = ""
    description: str = ""
    model: str = ""
    stream: bool = False
    verbose: bool = False
    max_iterations: int = 50
    temperature: float = 0.7
    session_id: Optional[str] = None

    class Config:
        arbitrary_types_allowed = True
        provider = LLMProvider.OPENAI

    @abstractmethod
    def setup(self) -> None:
        pass

    @abstractmethod
    def load(cls, config_name: AgentConfigName) -> "AgentConfig":
        """Loads the config for the agent."""
        pass

    @staticmethod
    @abstractmethod
    def get_llm_provider() -> LLMProvider:
        """Get the LLM provider for the agent."""
        pass

    @classmethod
    def _load_automata_yaml_config(cls, config_name: AgentConfigName) -> Dict:
        file_dir_path = os.path.dirname(os.path.abspath(__file__))
        # convert kebab to snake case to support file naming convention
        config_file_name = convert_kebab_to_snake(config_name.value)
        config_abs_path = os.path.join(
            file_dir_path,
            ConfigCategory.AGENT.value,
            cls.get_llm_provider().value,
            f"{config_file_name}.yaml",
        )

        if not os.path.isfile(config_abs_path):
            raise FileNotFoundError(f"Config file not found: {config_abs_path}")

        with open(config_abs_path, "r") as file:
            try:
                loaded_yaml = yaml.safe_load(file)
            except yaml.YAMLError as e:
                raise ValueError(f"Invalid YAML file: {config_abs_path}") from e

        if "config_name" in loaded_yaml:
            raise ValueError(
                "config_name already specified in YAML. Please remove this from the YAML file."
            )

        loaded_yaml["config_name"] = config_name
        return loaded_yaml


T = TypeVar("T", bound="AgentConfig")


class AgentConfigBuilder(Generic[T]):
    _config: T = PrivateAttr()

    def __init__(self, config: Optional[T] = None) -> None:
        self._config = config or self.create_config()

    def build(self) -> T:
        """Build and return an Agent instance with the current configuration."""
        self._config.setup()
        return self._config

    @staticmethod
    def create_config(config_name: Optional[AgentConfigName] = None) -> T:
        """Create the specific configuration object."""
        raise NotImplementedError

    @abstractmethod
    def with_model(self, model: str) -> "AgentConfigBuilder":
        pass

    def with_tools(self, tools: List[Tool]) -> "AgentConfigBuilder":
        self._config.tools = tools
        return self

    def with_stream(self, stream: bool) -> "AgentConfigBuilder":
        self._validate_type(stream, bool, "Stream")
        self._config.stream = stream
        return self

    def with_verbose(self, verbose: bool) -> "AgentConfigBuilder":
        self._validate_type(verbose, bool, "Verbose")
        self._config.verbose = verbose
        return self

    def with_max_iterations(self, max_iters: int) -> "AgentConfigBuilder":
        self._validate_type(max_iters, int, "Max iters")
        self._config.max_iterations = max_iters
        return self

    def with_temperature(self, temperature: float) -> "AgentConfigBuilder":
        self._validate_type(temperature, float, "Temperature")
        self._config.temperature = temperature
        return self

    def with_session_id(self, session_id: Optional[str]) -> "AgentConfigBuilder":
        if session_id:
            self._validate_type(session_id, str, "Session Id")
        self._config.session_id = session_id
        return self

    @classmethod
    def from_config(cls, config: T) -> "AgentConfigBuilder":
        """Create an AgentConfigBuilder instance using the provided configuration object."""
        return cls(config)

    @classmethod
    def from_name(cls, config_name: Union[str, AgentConfigName]) -> "AgentConfigBuilder":
        """Create an AgentConfigBuilder instance using the provided configuration object name."""
        if isinstance(config_name, str):
            try:
                config_name = AgentConfigName(config_name)
            except ValueError as e:
                raise ValueError(f"Invalid AgentConfigName value: {config_name}") from e

        return cls(cls.create_config(config_name))

    @staticmethod
    def _validate_type(value, expected_type, param_name: str) -> None:
        """Validate the type of the provided value and raise a ValueError if it doesn't match the expected type."""
        if not isinstance(value, expected_type):
            raise ValueError(f"{param_name} must be a {expected_type.__name__}.")
