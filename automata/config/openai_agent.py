import os
import uuid
from typing import Dict, List, Optional

import yaml
from pydantic import PrivateAttr

from automata.config.config_types import (
    AgentConfig,
    AgentConfigBuilder,
    AgentConfigName,
    ConfigCategory,
    InstructionConfigVersion,
)


class AutomataOpenAIAgentConfig(AgentConfig):
    class Config:
        SUPPORTED_MODELS = [
            "gpt-4",
            "gpt-3.5-turbo",
            "gpt-3.5-turbo-16k",
            "gpt-3.5-turbo-0613",
            "gpt-4-0613",
        ]
        arbitrary_types_allowed = True

    # System Template
    system_template: str = ""
    system_template_variables: List[str] = []
    system_template_formatter: Dict[str, str] = {}
    instruction_version: InstructionConfigVersion = InstructionConfigVersion.AGENT_INTRODUCTION
    system_instruction: Optional[str] = None

    class TemplateFormatter:
        @staticmethod
        def create_default_formatter(
            config: "AutomataOpenAIAgentConfig", max_default_overview_symbols: int = 100
        ) -> Dict[str, str]:
            """
            Create a default template formatter. The template formatter is used to format entries
            in the loaded agent template. These entries are denoted as {variable_name} in the template.

            Args:
                config (AutomataAgentConfig): The AutomataAgentConfig to use.

            Returns:
                Dict[str, str]: The default template formatter.

            Raises:
                NotImplementedError: If the config_name is not supported.

            TODO:
                - Consider how we might implement dependency injection across this call stack
                - Replace symbol_search with symbol_rank when it is implemented on DependencyFactory
            """
            formatter: Dict[str, str] = {}
            if config.config_name == AgentConfigName.AUTOMATA_MAIN:
                pass
            elif config.config_name == AgentConfigName.TEST:
                pass
            else:
                raise NotImplementedError("Automata does not have a default template formatter.")

            return formatter

    def setup(self) -> None:
        """Setup the agent."""
        if not self.session_id:
            self.session_id = str(uuid.uuid4())
        if not self.system_template_formatter:
            self.system_template_formatter = (
                AutomataOpenAIAgentConfig.TemplateFormatter.create_default_formatter(self)
            )
        if not self.system_instruction:
            self.system_instruction = self._formatted_instruction()

    @classmethod
    def load(cls, config_name: AgentConfigName) -> "AutomataOpenAIAgentConfig":
        """Loads the config for the agent."""
        if config_name == AgentConfigName.DEFAULT:
            return AutomataOpenAIAgentConfig()

        loaded_yaml = cls._load_automata_yaml_config(config_name)
        return AutomataOpenAIAgentConfig(**loaded_yaml)

    def _formatted_instruction(self) -> str:
        formatter_keys = set(self.system_template_formatter.keys())
        template_vars = set(self.system_template_variables)

        # Now check if the keys in formatter and template_vars match exactly
        if formatter_keys != template_vars:
            raise ValueError(
                f"Keys in system_template_formatter ({formatter_keys}) do not match system_template_variables ({template_vars})."
            )

        # Substitute variable placeholders in the system_template with their corresponding values
        formatted_instruction = self.system_template
        for variable, value in self.system_template_formatter.items():
            formatted_instruction = formatted_instruction.replace("{" + variable + "}", value)

        return formatted_instruction

    @classmethod
    def _load_automata_yaml_config(cls, config_name: AgentConfigName) -> Dict:
        file_dir_path = os.path.dirname(os.path.abspath(__file__))
        config_abs_path = os.path.join(
            file_dir_path, ConfigCategory.AGENT.value, f"{config_name.value}.yaml"
        )

        with open(config_abs_path, "r") as file:
            loaded_yaml = yaml.safe_load(file)
        loaded_yaml["config_name"] = config_name
        return loaded_yaml


class AutomataOpenAIAgentConfigBuilder(AgentConfigBuilder):
    """
    The AutomataAgentConfigBuilder class is a builder for constructing instances of AutomataAgents.
    It offers a flexible and easy-to-use interface for setting various properties of the agent before instantiation.
    """

    _config: AutomataOpenAIAgentConfig = PrivateAttr()

    @staticmethod
    def create_config(config_name: Optional[AgentConfigName]) -> AutomataOpenAIAgentConfig:  # type: ignore
        if config_name:
            return AutomataOpenAIAgentConfig.load(config_name)
        return AutomataOpenAIAgentConfig()

    def with_model(self, model: str) -> AgentConfigBuilder:
        if model not in AutomataOpenAIAgentConfig.Config.SUPPORTED_MODELS:
            raise ValueError(f"Model {model} not found in Supported OpenAI list of models.")
        self._config.model = model
        return self

    def with_system_template_formatter(
        self, system_template_formatter: Dict[str, str]
    ) -> "AutomataOpenAIAgentConfigBuilder":
        """
        Set the template formatter for the AutomataAgent instance and validate if it is supported.

        Args:
            model (str): A string containing the model name for the AutomataAgent.

        Raises:
            ValueError: If the provided model is not found in the list of supported models.
        """
        self._config.system_template_formatter = system_template_formatter
        for key, value in system_template_formatter.items():
            self._validate_type(key, str, "Template Formatter")
            self._validate_type(value, str, "Template Formatter")
        return self

    def with_instruction_version(
        self, instruction_version: str
    ) -> "AutomataOpenAIAgentConfigBuilder":
        self._validate_type(instruction_version, str, "Instruction version")
        self._config.instruction_version = InstructionConfigVersion(instruction_version)
        return self

    @staticmethod
    def create_from_args(*args, **kwargs) -> AutomataOpenAIAgentConfig:
        """
        Creates an AutomataAgentConfig instance from the provided arguments.

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            AutomataAgentConfig: An AutomataAgentConfig instance.
        """

        config_to_load = kwargs.get("config_to_load", None)
        config = kwargs.get("config", None)

        if not config_to_load and not config:
            raise ValueError("Config to load or config must be specified.")

        if config_to_load and config:
            raise ValueError("Config to load and config cannot both be specified.")

        if config_to_load:
            builder = AutomataOpenAIAgentConfigBuilder.from_name(
                config_name=AgentConfigName(config_to_load)
            )
        else:
            builder = AutomataOpenAIAgentConfigBuilder.from_config(config)  # type: ignore

        if "model" in kwargs:
            builder = builder.with_model(kwargs["model"])

        if "session_id" in kwargs:
            builder = builder.with_session_id(kwargs["session_id"])

        if "stream" in kwargs:
            builder = builder.with_stream(kwargs["stream"])

        if "verbose" in kwargs:
            builder = builder.with_verbose(kwargs["verbose"])

        if "max_iters" in kwargs:
            builder = builder.with_max_iterations(kwargs["max_iters"])

        if "tools" in kwargs:
            builder = builder.with_tools(kwargs["tools"])

        return builder.build()
