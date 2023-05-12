from typing import Dict, Optional

from pydantic import BaseModel, PrivateAttr

from automata.configs.automata_agent_configs import AutomataAgentConfig, AutomataInstructionPayload
from automata.configs.config_enums import AgentConfigName, InstructionConfigVersion
from automata.core.base.tool import Toolkit, ToolkitType
from automata.tool_management.tool_management_utils import build_llm_toolkits


class AutomataAgentConfigBuilder(BaseModel):
    """
    The AutomataAgentConfigBuilder class is a builder for constructing instances of AutomataAgents.
    It offers a flexible and easy-to-use interface for setting various properties of the agent before instantiation.
    """

    _config: AutomataAgentConfig = PrivateAttr()

    def __init__(self, config: Optional[AutomataAgentConfig] = None):
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
        instance = cls(AutomataAgentConfig.load(config_name))
        return instance

    @classmethod
    def from_config(cls, config: AutomataAgentConfig) -> "AutomataAgentConfigBuilder":
        """
        Create an AutomataAgentConfigBuilder instance using the provided configuration object.

        Args:
            config (AutomataAgentConfig): The provided configuration object for the AutomataAgent.

        Returns:
            AutomataAgentConfigBuilder: A new AutomataAgentConfigBuilder instance
        """
        instance = cls(config)
        return instance

    def with_instruction_payload(
        self, instruction_payload: AutomataInstructionPayload
    ) -> "AutomataAgentConfigBuilder":
        """
        Set the initial payload for the AutomataAgent instance.

        Args:
            instruction_payload (AutomataInstructionPayload): A dictionary containing the initial payload for the AutomataAgent.

        Returns:
            AutomataAgentConfigBuilder: The current AutomataAgentConfigBuilder instance with the updated instruction_payload.
        """
        self._config.instruction_payload = instruction_payload
        return self

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

    def with_eval_mode(self, eval_mode: bool) -> "AutomataAgentConfigBuilder":
        """
        Set the evaluation mode for the AutomataAgent instance.

        Args:
            eval_mode (bool): A boolean value indicating whether to use evaluation mode for the AutomataAgent.

        Returns:
            AutomataAgentConfigBuilder: The current AutomataAgentConfigBuilder instance with the updated eval_mode value.
        """
        self._validate_type(eval_mode, bool, "Eval mode")
        self._config.eval_mode = eval_mode
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

    def with_helper_agent_configs(
        self, helper_agent_configs: Dict[AgentConfigName, AutomataAgentConfig]
    ) -> "AutomataAgentConfigBuilder":
        """
        Set the helper agent config list

        Args:
            instruction_version (str): A string representing the instruction version for the AutomataAgent.

        Returns:
            AutomataAgentConfigBuilder: The current AutomataAgentConfigBuilder instance with the updated instruction_version value.
        """
        self._validate_type(
            helper_agent_configs,
            Dict[AgentConfigName, AutomataAgentConfig],
            "Helper agent configs",
        )
        self.helper_agent_configs = helper_agent_configs
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
    def _validate_type(value, expected_type, param_name: str):
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
        from automata.configs.automata_agent_config_utils import AutomataAgentConfigBuilder

        print("kwargs = ", kwargs)
        main_config_name = kwargs.get("main_config_name", None)
        main_config = kwargs.get("main_config", None)

        if not main_config_name and not main_config:
            raise ValueError("Main config name or config must be specified.")
        if main_config_name:
            builder = AutomataAgentConfigBuilder.from_name(main_config_name)
        else:
            builder = AutomataAgentConfigBuilder.from_config(main_config)

        instruction_payload = kwargs.get("instruction_payload", {})

        if "helper_agent_configs" in kwargs:
            print("kwargs helper_agent_configs= ", kwargs["helper_agent_configs"])
            instruction_payload["agents_message"] = build_agent_message(
                kwargs["helper_agent_configs"]
            )
            builder = builder.with_helper_agent_configs(kwargs["helper_agent_configs"])

        if instruction_payload != {}:
            instruction_payload = AutomataInstructionPayload(**instruction_payload)
            builder = builder.with_instruction_payload(instruction_payload)

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

        if "eval_mode" in kwargs:
            builder = builder.with_eval_mode(kwargs["eval_mode"])

        return builder.build()
