import uuid
from typing import Dict, List, Optional

from pydantic import PrivateAttr

from automata.config.base import (
    AgentConfig,
    AgentConfigBuilder,
    AgentConfigName,
    InstructionConfigVersion,
    LLMProvider,
)
from automata.core.experimental.search.rank import SymbolRank
from automata.core.singletons.dependency_factory import dependency_factory


class OpenAIAutomataAgentConfig(AgentConfig):
    """A class to hold the configuration for the Automata OpenAI Agent."""

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
            config: "OpenAIAutomataAgentConfig",
            symbol_rank: SymbolRank,
            max_default_overview_symbols: int = 100,
        ) -> Dict[str, str]:
            """
            TODO:
                - Re-implement this method after the new instruction configs are finalized.
            """
            formatter: Dict[str, str] = {}
            if config.config_name == AgentConfigName.AUTOMATA_MAIN:
                top_symbols = symbol_rank.get_top_symbols(max_default_overview_symbols)
                formatter["symbol_rank_overview"] = "\n".join(
                    f"{symbol}"
                    for symbol, _ in sorted(top_symbols, key=lambda x: x[1], reverse=True)
                )
                formatter["max_iterations"] = str(config.max_iterations)
            elif config.config_name != AgentConfigName.TEST:
                raise NotImplementedError("Automata does not have a default template formatter.")

            return formatter

    def setup(self) -> None:
        if not self.session_id:
            self.session_id = str(uuid.uuid4())
        if not self.system_template_formatter:
            self.system_template_formatter = (
                OpenAIAutomataAgentConfig.TemplateFormatter.create_default_formatter(
                    self, dependency_factory.get("symbol_rank")
                )
            )
        if not self.system_instruction:
            self.system_instruction = self._formatted_instruction()

    @classmethod
    def load(cls, config_name: AgentConfigName) -> "OpenAIAutomataAgentConfig":
        """Loads the config for the agent."""
        if config_name == AgentConfigName.DEFAULT:
            return OpenAIAutomataAgentConfig()

        loaded_yaml = cls._load_automata_yaml_config(config_name)
        return OpenAIAutomataAgentConfig(**loaded_yaml)

    @staticmethod
    def get_llm_provider() -> LLMProvider:
        """Get the provider for the agent."""
        return LLMProvider.OPENAI

    def _formatted_instruction(self) -> str:
        """
        Formats the system template with the system template formatter
        to produce the system instruction.
        """
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


class OpenAIAutomataAgentConfigBuilder(AgentConfigBuilder):
    """
    The AutomataAgentConfigBuilder class is a builder for constructing instances of AutomataAgents.
    It offers a flexible and easy-to-use interface for setting various properties of the agent before instantiation.
    """

    _config: OpenAIAutomataAgentConfig = PrivateAttr()

    @staticmethod
    def create_config(config_name: Optional[AgentConfigName]) -> OpenAIAutomataAgentConfig:  # type: ignore
        if config_name:
            return OpenAIAutomataAgentConfig.load(config_name)
        return OpenAIAutomataAgentConfig()

    def with_model(self, model: str) -> AgentConfigBuilder:
        if model not in OpenAIAutomataAgentConfig.Config.SUPPORTED_MODELS:
            raise ValueError(f"Model {model} not found in Supported OpenAI list of models.")
        self._config.model = model
        return self

    def with_system_template_formatter(
        self, system_template_formatter: Dict[str, str]
    ) -> "OpenAIAutomataAgentConfigBuilder":
        """
        Set the template formatter for the AutomataAgent instance and validate if it is supported.

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
    ) -> "OpenAIAutomataAgentConfigBuilder":
        self._validate_type(instruction_version, str, "Instruction version")
        self._config.instruction_version = InstructionConfigVersion(instruction_version)
        return self

    @staticmethod
    def create_from_args(*args, **kwargs) -> OpenAIAutomataAgentConfig:
        """Creates an AutomataAgentConfig instance from the provided arguments."""

        config_to_load = kwargs.get("config_to_load", None)
        config = kwargs.get("config", None)

        if not config_to_load and not config:
            raise ValueError("Config to load or config must be specified.")

        if config_to_load and config:
            raise ValueError("Config to load and config cannot both be specified.")

        if config_to_load:
            builder = OpenAIAutomataAgentConfigBuilder.from_name(
                config_name=AgentConfigName(config_to_load)
            )
        else:
            builder = OpenAIAutomataAgentConfigBuilder.from_config(config)  # type: ignore

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
