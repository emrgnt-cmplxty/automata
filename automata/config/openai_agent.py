import os
import uuid
from typing import Dict, List, Optional

import yaml
from pydantic import BaseModel, PrivateAttr

from automata.config.config_types import (
    AgentConfigBuilder,
    AgentConfigName,
    ConfigCategory,
    InstructionConfigVersion,
)
from automata.core.base.tool import Tool


class AutomataOpenAIAgentConfig(BaseModel):
    """
    Args:
        config_name (AgentConfigName): The config_name of the agent to use.
        tools (List[Tool]): A list of tools available to the model.
        instructions (str): A string of instructions to execute.
        system_template (str): A string of instructions to execute.
        system_template_variables (List[str]): A list of required input variables for the instruction template.
        system_template_formatter (Dict[str, str]): A user provided dictionary of input variables and corresponding text.
        model (str): The model to use for the agent.
        stream (bool): Whether to stream the results back to the main.
        verbose (bool): Whether to print the results to stdout.
        max_iters (int): The maximum number of iterations to run.
        temperature (float): The temperature to use for the agent.
        session_id (Optional[str]): The session ID to use for the agent.
        instruction_version (InstructionConfigVersion): Config version of the introduction instruction.
    """

    class Config:
        SUPPORTED_MODELS = [
            "gpt-4",
            "gpt-3.5-turbo",
            "gpt-3.5-turbo-16k",
            "gpt-3.5-turbo-0613",
            "gpt-4-0613",
        ]
        arbitrary_types_allowed = True

    config_name: AgentConfigName = AgentConfigName.DEFAULT
    tools: List[Tool] = []
    instructions: str = ""
    description: str = ""
    model: str = "gpt-4-0613"
    stream: bool = False
    verbose: bool = False
    max_iterations: int = 50
    temperature: float = 0.7
    session_id: Optional[str] = None
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
            Create a default template formatter.

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
            # formatter: Dict[str, str] = {}
            if config.config_name == AgentConfigName.AUTOMATA_MAIN:
                pass
            elif config.config_name == AgentConfigName.TEST:
                pass
            else:
                raise NotImplementedError("Automata does not have a default template formatter.")

            return {}

    def setup(self) -> None:
        """Setup the agent."""
        if not self.session_id:
            self.session_id = str(uuid.uuid4())
        if not self.system_template_formatter:
            self.system_template_formatter = (
                AutomataOpenAIAgentConfig.TemplateFormatter.create_default_formatter(self)
            )
        if not self.system_instruction:
            self.system_instruction = self._formatted_prompt()

    @classmethod
    def load_automata_yaml_config(cls, config_name: AgentConfigName) -> Dict:
        """
        Loads the automata.yaml config file.

        Args:
            config_name (AgentConfigName): The config_name of the agent to use.

        Returns:
            Dict: The loaded yaml config.
        """
        file_dir_path = os.path.dirname(os.path.abspath(__file__))
        config_abs_path = os.path.join(
            file_dir_path, ConfigCategory.AGENT.value, f"{config_name.value}.yaml"
        )

        with open(config_abs_path, "r") as file:
            loaded_yaml = yaml.safe_load(file)
        loaded_yaml["config_name"] = config_name
        return loaded_yaml

    @classmethod
    def load(cls, config_name: AgentConfigName) -> "AutomataOpenAIAgentConfig":
        """Loads the config for the agent."""
        if config_name == AgentConfigName.DEFAULT:
            return AutomataOpenAIAgentConfig()

        loaded_yaml = cls.load_automata_yaml_config(config_name)
        return AutomataOpenAIAgentConfig(**loaded_yaml)

    def _formatted_prompt(self) -> str:
        """
        Format system_template with the entries in the system_template_formatter.

        Returns:
            str: Formatted system_template string.
        """
        formatter_keys = set(self.system_template_formatter.keys())
        template_vars = set(self.system_template_variables)

        # Now check if the keys in formatter and template_vars match exactly
        if formatter_keys != template_vars:
            raise ValueError(
                f"Keys in system_template_formatter ({formatter_keys}) do not match system_template_variables ({template_vars})."
            )

        # Substitute variable placeholders in the system_template with their corresponding values
        formatted_prompt = self.system_template
        for variable, value in self.system_template_formatter.items():
            formatted_prompt = formatted_prompt.replace("{" + variable + "}", value)

        return formatted_prompt


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

    def with_tools(self, tools: List[Tool]) -> "AutomataOpenAIAgentConfigBuilder":
        """
        Set the low-level manipulation (LLM) toolkits for the AutomataAgent instance.

        Args:
            tool_builders (List[Tool]]): A list of tools for use by the AutomataAgent.

        Returns:
            AutomataAgentConfigBuilder: The current AutomataAgentConfigBuilder instance with the updated tool_builders.
        """
        self._config.tools = tools
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

        Returns:
            AutomataAgentConfigBuilder: The current AutomataAgentConfigBuilder instance with the updated model.
        """
        self._config.system_template_formatter = system_template_formatter
        for key, value in system_template_formatter.items():
            self._validate_type(key, str, "Template Formatter")
            self._validate_type(value, str, "Template Formatter")
        return self

    def with_model(self, model: str) -> "AutomataOpenAIAgentConfigBuilder":
        """
        Set the model for the AutomataAgent instance and validate if it is supported.

        Args:
            model (str): A string containing the model name for the AutomataAgent.

        Raises:
            ValueError: If the provided model is not found in the list of supported models.

        Returns:
            AutomataAgentConfigBuilder: The current AutomataAgentConfigBuilder instance with the updated model.
        """
        self._config.model = model
        if model not in AutomataOpenAIAgentConfig.Config.SUPPORTED_MODELS:
            raise ValueError(f"Model {model} not found in Supported OpenAI list of models.")
        return self

    def with_stream(self, stream: bool) -> "AutomataOpenAIAgentConfigBuilder":
        """
        Set the stream flag for the AutomataAgent instance.

        Args:
            stream (bool): A boolean value indicating whether to use streaming mode for the AutomataAgent.

        Returns:
            AutomataAgentConfigBuilder: The current AutomataAgentConfigBuilder instance with the updated stream flag.
        """
        self._validate_type(stream, bool, "Stream")
        self._config.stream = stream
        return self

    def with_verbose(self, verbose: bool) -> "AutomataOpenAIAgentConfigBuilder":
        """
        Set the verbose flag for the AutomataAgent instance.

        Args:
            verbose (bool): A boolean value indicating whether to use verbose mode for the AutomataAgent.

        Returns:
            AutomataAgentConfigBuilder: The current AutomataAgentConfigBuilder instance with the updated verbose flag.
        """
        self._validate_type(verbose, bool, "Verbose")
        self._config.verbose = verbose
        return self

    def with_max_iterations(self, max_iters: int) -> "AutomataOpenAIAgentConfigBuilder":
        """
        Set the maximum number of iterations for the AutomataAgent instance.

        Args:
            max_iters (int): An integer value representing the maximum number of iterations for the AutomataAgent.

        Returns:
            AutomataAgentConfigBuilder: The current AutomataAgentConfigBuilder instance with the updated max_iters value.
        """
        self._validate_type(max_iters, int, "Max iters")
        self._config.max_iterations = max_iters
        return self

    def with_temperature(self, temperature: float) -> "AutomataOpenAIAgentConfigBuilder":
        """
        Set the temperature for the AutomataAgent instance.

        Args:
            temperature (float): A float value representing the temperature for the AutomataAgent.

        Returns:
            AutomataAgentConfigBuilder: The current AutomataAgentConfigBuilder instance with the updated temperature value.
        """
        self._validate_type(temperature, float, "Temperature")
        self._config.temperature = temperature
        return self

    def with_session_id(self, session_id: Optional[str]) -> "AutomataOpenAIAgentConfigBuilder":
        """
        Set the session ID for the AutomataAgent instance.

        Args:
            session_id (Optional[str]): An optional string representing the session ID for the AutomataAgent.

        Returns:
            AutomataAgentConfigBuilder: The current AutomataAgentConfigBuilder instance with the updated session ID.
        """
        if session_id:
            self._validate_type(session_id, str, "Session Id")
        self._config.session_id = session_id
        return self

    def with_instruction_version(
        self, instruction_version: str
    ) -> "AutomataOpenAIAgentConfigBuilder":
        """
        Set the instruction version for the AutomataAgent instance.

        Args:
            instruction_version (str): A string representing the instruction version for the AutomataAgent.

        Returns:
            AutomataAgentConfigBuilder: The current AutomataAgentConfigBuilder instance with the updated instruction_version value.
        """
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

        main_config_name = kwargs.get("main_config_name", None)
        main_config = kwargs.get("main_config", None)

        if not main_config_name and not main_config:
            raise ValueError("Main config name or config must be specified.")

        if main_config_name and main_config:
            raise ValueError("Main config name abd config cannot both be specified.")

        if main_config_name:
            builder = AutomataOpenAIAgentConfigBuilder.from_name(
                config_name=AgentConfigName(main_config_name)
            )
        else:
            builder = AutomataOpenAIAgentConfigBuilder.from_config(main_config)  # type: ignore

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
