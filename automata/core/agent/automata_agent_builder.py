from typing import Dict, Optional

from pydantic import BaseModel, PrivateAttr

from automata.configs.automata_agent_configs import AutomataAgentConfig
from automata.configs.config_enums import InstructionConfigVersion
from automata.core.base.tool import Toolkit, ToolkitType

from .automata_agent import AutomataAgent


class AutomataAgentBuilder(BaseModel):
    """
    A builder class for constructing instances of AutomataAgent.
    """
    _instance: AutomataAgent = PrivateAttr()

    def __init__(self, config: Optional[AutomataAgentConfig]):
        super().__init__()
        self._instance = AutomataAgent(config)

    @classmethod
    def from_config(cls, config: Optional[AutomataAgentConfig]) -> "AutomataAgentBuilder":
        instance = cls(config)
        return instance

    def with_initial_payload(self, initial_payload: Dict[str, str]) -> "AutomataAgentBuilder":
        """
        Set the initial payload for the AutomataAgent instance.
        """
        self._instance.initial_payload = initial_payload
        return self

    def with_llm_toolkits(
        self, llm_toolkits: Dict[ToolkitType, Toolkit]
    ) -> "AutomataAgentBuilder":
        self._instance.llm_toolkits = llm_toolkits
        return self

    def with_instructions(self, instructions: str) -> "AutomataAgentBuilder":
        self._instance.instructions = instructions
        return self

    def with_model(self, model: str) -> "AutomataAgentBuilder":
        self._instance.model = model
        if model not in AutomataAgentConfig.Config.SUPPORTED_MODELS:
            raise ValueError(f"Model {model} not found in Supported OpenAI list of models.")
        return self

    def with_stream(self, stream: bool) -> "AutomataAgentBuilder":
        self._validate_type(stream, bool, "Stream")
        self._instance.stream = stream
        return self

    def with_verbose(self, verbose: bool) -> "AutomataAgentBuilder":
        self._validate_type(verbose, bool, "Verbose")
        self._instance.verbose = verbose
        return self

    def with_max_iters(self, max_iters: int) -> "AutomataAgentBuilder":
        self._validate_type(max_iters, int, "Max iters")
        self._instance.max_iters = max_iters
        return self

    def with_temperature(self, temperature: float) -> "AutomataAgentBuilder":
        self._validate_type(temperature, float, "Temperature")
        self._instance.temperature = temperature
        return self

    def with_session_id(self, session_id: Optional[str]) -> "AutomataAgentBuilder":
        if session_id:
            self._validate_type(session_id, str, "Session Id")
        self._instance.session_id = session_id
        return self

    def with_instruction_version(self, instruction_version: str) -> "AutomataAgentBuilder":
        self._validate_type(instruction_version, str, "Instruction version")
        InstructionConfigVersion(instruction_version)
        self._instance.instruction_version = instruction_version
        return self

    def build(self) -> AutomataAgent:
        self._instance._setup()
        return self._instance

    @staticmethod
    def _validate_type(value, expected_type, param_name: str):
        """
        Validate the type of the provided value and raise a ValueError if it doesn't match the expected type.
        """
        if not isinstance(value, expected_type):
            raise ValueError(f"{param_name} must be a {expected_type.__name__}.")
