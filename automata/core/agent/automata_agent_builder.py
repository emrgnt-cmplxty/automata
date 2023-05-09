from typing import Dict, Optional

from pydantic import BaseModel, PrivateAttr

from automata.configs.automata_agent_configs import AutomataAgentConfig, AutomataInstructionPayload
from automata.configs.config_enums import InstructionConfigVersion
from automata.core.base.tool import Toolkit, ToolkitType

from .automata_agent import AutomataAgent, MasterAutomataAgent


class AutomataAgentBuilder(BaseModel):
    """
    The AutomataAgentBuilder class is a builder for constructing instances of AutomataAgent and MasterAutomataAgent.
    It offers a flexible and easy-to-use interface for setting various properties of the agent before instantiation.
    """

    _instance: AutomataAgent = PrivateAttr()

    def __init__(self, config: Optional[AutomataAgentConfig]):
        """
        Initialize an AutomataAgentBuilder instance with the given config.

        Args:
            config (Optional[AutomataAgentConfig]): An optional configuration object for the AutomataAgent.
        """
        super().__init__()
        self._instance = AutomataAgent(config)

    @classmethod
    def from_config(cls, config: Optional[AutomataAgentConfig]) -> "AutomataAgentBuilder":
        """
        Create an AutomataAgentBuilder instance using the provided configuration object.

        Args:
            config (Optional[AutomataAgentConfig]): An optional configuration object for the AutomataAgent.

        Returns:
            AutomataAgentBuilder: A new AutomataAgentBuilder instance configured with the provided config.
        """
        instance = cls(config)
        return instance

    def with_instruction_payload(
        self, instruction_payload: AutomataInstructionPayload
    ) -> "AutomataAgentBuilder":
        """
        Set the initial payload for the AutomataAgent instance.

        Args:
            instruction_payload (AutomataInstructionPayload): A dictionary containing the initial payload for the AutomataAgent.

        Returns:
            AutomataAgentBuilder: The current AutomataAgentBuilder instance with the updated instruction_payload.
        """
        self._instance.instruction_payload = instruction_payload
        return self

    def with_llm_toolkits(
        self, llm_toolkits: Dict[ToolkitType, Toolkit]
    ) -> "AutomataAgentBuilder":
        """
        Set the low-level manipulation (LLM) toolkits for the AutomataAgent instance.

        Args:
            llm_toolkits (Dict[ToolkitType, Toolkit]): A dictionary containing the LLM toolkits for the AutomataAgent.

        Returns:
            AutomataAgentBuilder: The current AutomataAgentBuilder instance with the updated llm_toolkits.
        """
        self._instance.llm_toolkits = llm_toolkits
        return self

    def with_instructions(self, instructions: str) -> "AutomataAgentBuilder":
        """
        Set the instructions for the AutomataAgent instance.

        Args:
            instructions (str): A string containing the instructions for the AutomataAgent.

        Returns:
            AutomataAgentBuilder: The current AutomataAgentBuilder instance with the updated instructions.
        """
        self._instance.instructions = instructions
        return self

    def with_model(self, model: str) -> "AutomataAgentBuilder":
        """
        Set the model for the AutomataAgent instance and validate if it is supported.

        Args:
            model (str): A string containing the model name for the AutomataAgent.

        Raises:
            ValueError: If the provided model is not found in the list of supported models.

        Returns:
            AutomataAgentBuilder: The current AutomataAgentBuilder instance with the updated model.
        """
        self._instance.model = model
        if model not in AutomataAgentConfig.Config.SUPPORTED_MODELS:
            raise ValueError(f"Model {model} not found in Supported OpenAI list of models.")
        return self

    def with_stream(self, stream: bool) -> "AutomataAgentBuilder":
        """
        Set the stream flag for the AutomataAgent instance.

        Args:
            stream (bool): A boolean value indicating whether to use streaming mode for the AutomataAgent.

        Returns:
            AutomataAgentBuilder: The current AutomataAgentBuilder instance with the updated stream flag.
        """
        self._validate_type(stream, bool, "Stream")
        self._instance.stream = stream
        return self

    def with_verbose(self, verbose: bool) -> "AutomataAgentBuilder":
        """
        Set the verbose flag for the AutomataAgent instance.

        Args:
            verbose (bool): A boolean value indicating whether to use verbose mode for the AutomataAgent.

        Returns:
            AutomataAgentBuilder: The current AutomataAgentBuilder instance with the updated verbose flag.
        """
        self._validate_type(verbose, bool, "Verbose")
        self._instance.verbose = verbose
        return self

    def with_max_iters(self, max_iters: int) -> "AutomataAgentBuilder":
        """
        Set the maximum number of iterations for the AutomataAgent instance.

        Args:
            max_iters (int): An integer value representing the maximum number of iterations for the AutomataAgent.

        Returns:
            AutomataAgentBuilder: The current AutomataAgentBuilder instance with the updated max_iters value.
        """
        self._validate_type(max_iters, int, "Max iters")
        self._instance.max_iters = max_iters
        return self

    def with_temperature(self, temperature: float) -> "AutomataAgentBuilder":
        """
        Set the temperature for the AutomataAgent instance.

        Args:
            temperature (float): A float value representing the temperature for the AutomataAgent.

        Returns:
            AutomataAgentBuilder: The current AutomataAgentBuilder instance with the updated temperature value.
        """
        self._validate_type(temperature, float, "Temperature")
        self._instance.temperature = temperature
        return self

    def with_session_id(self, session_id: Optional[str]) -> "AutomataAgentBuilder":
        """
        Set the session ID for the AutomataAgent instance.

        Args:
            session_id (Optional[str]): An optional string representing the session ID for the AutomataAgent.

        Returns:
            AutomataAgentBuilder: The current AutomataAgentBuilder instance with the updated session ID.
        """
        if session_id:
            self._validate_type(session_id, str, "Session Id")
        self._instance.session_id = session_id
        return self

    def with_eval_mode(self, eval_mode: bool) -> "AutomataAgentBuilder":
        """
        Set the evaluation mode for the AutomataAgent instance.

        Args:
            eval_mode (bool): A boolean value indicating whether to use evaluation mode for the AutomataAgent.

        Returns:
            AutomataAgentBuilder: The current AutomataAgentBuilder instance with the updated eval_mode value.
        """
        self._validate_type(eval_mode, bool, "Eval mode")
        self._instance.eval_mode = eval_mode
        return self

    def with_instruction_version(self, instruction_version: str) -> "AutomataAgentBuilder":
        """
        Set the instruction version for the AutomataAgent instance.

        Args:
            instruction_version (str): A string representing the instruction version for the AutomataAgent.

        Returns:
            AutomataAgentBuilder: The current AutomataAgentBuilder instance with the updated instruction_version value.
        """
        self._validate_type(instruction_version, str, "Instruction version")
        InstructionConfigVersion(instruction_version)
        self._instance.instruction_version = instruction_version
        return self

    def build(self) -> AutomataAgent:
        """
        Build and return an AutomataAgent instance with the current configuration.

        Returns:
            AutomataAgent: An AutomataAgent instance with the current configuration.
        """
        self._instance._setup()
        return self._instance

    def build_master(self) -> MasterAutomataAgent:
        """
        Build and return an MasterAutomataAgent instance with the current configuration.

        Returns:
            MasterAutomataAgent: An MasterAutomataAgent instance with the current configuration.
        """
        self._instance._setup()
        return MasterAutomataAgent.from_agent(self._instance)

    @staticmethod
    def _validate_type(value, expected_type, param_name: str):
        """
        Validate the type of the provided value and raise a ValueError if it doesn't match the expected type.
        """
        if not isinstance(value, expected_type):
            raise ValueError(f"{param_name} must be a {expected_type.__name__}.")
