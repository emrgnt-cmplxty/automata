from typing import Dict, Optional

from pydantic import BaseModel, PrivateAttr

from automata.config.config_types import (
    AgentConfigName,
    AutomataAgentConfig,
    InstructionConfigVersion,
)
from automata.core.agent.tools.tool_utils import build_llm_toolkits
from automata.core.base.tool import Toolkit, ToolkitType


class AutomataAgentConfigBuilder(BaseModel):
    """
    The AutomataAgentConfigBuilder class is a builder for constructing instances of AutomataAgents.
    It offers a flexible and easy-to-use interface for setting various properties of the agent before instantiation.
    """

    _config: AutomataAgentConfig = PrivateAttr()

    def __init__(self, config: Optional[AutomataAgentConfig] = None) -> None:
        super().__init__()
        self._config = config or AutomataAgentConfig()

    @classmethod
    def from_name(cls, config_name: AgentConfigName) -> "AutomataAgentConfigBuilder":
        """
        Create an AutomataAgentConfigBuilder instance using the provided configuration object name.

        Args:
            config_name (AgentConfigName): The name of the configuration object for the AutomataAgent.

        Returns:
            AutomataAgentConfigBuilder: A new AutomataAgentConfigBuilder instance
        """
        return cls(AutomataAgentConfig.load(config_name))

    @classmethod
    def from_config(cls, config: AutomataAgentConfig) -> "AutomataAgentConfigBuilder":
        """
        Create an AutomataAgentConfigBuilder instance using the provided configuration object.

        Args:
            config (AutomataAgentConfig): The provided configuration object for the AutomataAgent.

        Returns:
            AutomataAgentConfigBuilder: A new AutomataAgentConfigBuilder instance
        """
        return cls(config)

    def with_llm_toolkits(
        self, llm_toolkits: Dict[ToolkitType, Toolkit]
    ) -> "AutomataAgentConfigBuilder":
        """
        Set the low-level manipulation (LLM) toolkits for the AutomataAgent instance.

        Args:
            llm_toolkits (Dict[ToolkitType, Toolkit]): A dictionary containing the LLM toolkits for the AutomataAgent.

        Returns:
            AutomataAgentConfigBuilder: The current AutomataAgentConfigBuilder instance with the updated llm_toolkits.
        """
        self._config.llm_toolkits = llm_toolkits
        return self

    def with_system_template_formatter(
        self, system_template_formatter: Dict[str, str]
    ) -> "AutomataAgentConfigBuilder":
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

    def with_model(self, model: str) -> "AutomataAgentConfigBuilder":
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
        if model not in AutomataAgentConfig.Config.SUPPORTED_MODELS:
            raise ValueError(f"Model {model} not found in Supported OpenAI list of models.")
        return self

    def with_stream(self, stream: bool) -> "AutomataAgentConfigBuilder":
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

    def with_verbose(self, verbose: bool) -> "AutomataAgentConfigBuilder":
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

    def with_max_iters(self, max_iters: int) -> "AutomataAgentConfigBuilder":
        """
        Set the maximum number of iterations for the AutomataAgent instance.

        Args:
            max_iters (int): An integer value representing the maximum number of iterations for the AutomataAgent.

        Returns:
            AutomataAgentConfigBuilder: The current AutomataAgentConfigBuilder instance with the updated max_iters value.
        """
        self._validate_type(max_iters, int, "Max iters")
        self._config.max_iters = max_iters
        return self

    def with_temperature(self, temperature: float) -> "AutomataAgentConfigBuilder":
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

    def with_session_id(self, session_id: Optional[str]) -> "AutomataAgentConfigBuilder":
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

    def with_instruction_version(self, instruction_version: str) -> "AutomataAgentConfigBuilder":
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

    def build(self) -> AutomataAgentConfig:
        """
        Build and return an AutomataAgent instance with the current configuration.

        Returns:
            AutomataAgent: An AutomataAgent instance with the current configuration.
        """
        self._config.setup()
        return self._config

    @staticmethod
    def _validate_type(value, expected_type, param_name: str) -> None:
        """
        Validate the type of the provided value and raise a ValueError if it doesn't match the expected type.
        """
        if not isinstance(value, expected_type):
            raise ValueError(f"{param_name} must be a {expected_type.__name__}.")


def build_agent_message(agent_configs: Dict[AgentConfigName, AutomataAgentConfig]) -> str:
    """
    Constructs a string message containing the configuration version and description
    of all managed agent instances.

    Returns:
        str: The generated message.
    """
    return "".join(
        [
            f"\n{main_config.config_name.value}: {main_config.description}\n"
            for main_config in agent_configs.values()
        ]
    )


class AutomataAgentConfigFactory:
    @staticmethod
    def create_config(*args, **kwargs) -> AutomataAgentConfig:
        """
        Creates an AutomataAgentConfig instance from the provided arguments.

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            AutomataAgentConfig: An AutomataAgentConfig instance.
        """
        from automata.config.agent_config_builder import AutomataAgentConfigBuilder

        main_config_name = kwargs.get("main_config_name", None)
        main_config = kwargs.get("main_config", None)

        if not main_config_name and not main_config:
            raise ValueError("Main config name or config must be specified.")

        if main_config_name and main_config:
            raise ValueError("Main config name abd config cannot both be specified.")

        if main_config_name:
            builder = AutomataAgentConfigBuilder.from_name(AgentConfigName(main_config_name))
        else:
            builder = AutomataAgentConfigBuilder.from_config(main_config)  # type: ignore

        if "model" in kwargs:
            builder = builder.with_model(kwargs["model"])

        if "session_id" in kwargs:
            builder = builder.with_session_id(kwargs["session_id"])

        if "stream" in kwargs:
            builder = builder.with_stream(kwargs["stream"])

        if "verbose" in kwargs:
            builder = builder.with_verbose(kwargs["verbose"])

        if "with_max_iters" in kwargs:
            builder = builder.with_max_iters(kwargs["with_max_iters"])

        if "llm_toolkits" in kwargs and kwargs["llm_toolkits"] != "":
            llm_toolkits = build_llm_toolkits(kwargs["llm_toolkits"].split(","))
            builder = builder.with_llm_toolkits(llm_toolkits)

        return builder.build()
