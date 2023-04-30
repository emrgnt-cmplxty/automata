from typing import Dict, Optional

from pydantic import BaseModel, PrivateAttr

from automata.configs.config_types import AutomataAgentConfig, InstructionConfigVersion
from automata.core.base.tool import Toolkit, ToolkitType

from .automata_agent import AutomataAgent


class AutomataAgentBuilder(BaseModel):
    _instance: AutomataAgent = PrivateAttr()

    def __init__(self, config: Optional[AutomataAgentConfig]):
        super().__init__()
        self._instance = AutomataAgent(config)

    def with_initial_payload(self, initial_payload: Dict[str, str]) -> "AutomataAgentBuilder":
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
        if model not in AutomataAgentConfig.Config.SUPPORTED_MDOELS:
            raise ValueError(f"Model {model} not found in Supported OpenAI list of models.")
        return self

    def with_stream(self, stream: bool) -> "AutomataAgentBuilder":
        if not isinstance(stream, bool):
            raise ValueError("Stream must be a boolean.")
        self._instance.stream = stream
        return self

    def with_verbose(self, verbose: bool) -> "AutomataAgentBuilder":
        if not isinstance(verbose, bool):
            raise ValueError("Verbose must be a boolean.")
        self._instance.verbose = verbose
        return self

    def with_max_iters(self, max_iters: int) -> "AutomataAgentBuilder":
        if not isinstance(max_iters, int):
            raise ValueError("Max iters must be an integer.")
        self._instance.max_iters = max_iters
        return self

    def with_temperature(self, temperature: float) -> "AutomataAgentBuilder":
        if not isinstance(temperature, float):
            raise ValueError("Temperature iters must be a float.")
        self._instance.temperature = temperature
        return self

    def with_session_id(self, session_id: Optional[str]) -> "AutomataAgentBuilder":
        if session_id and (not isinstance(session_id, str)):
            raise ValueError("Session Id must be a str.")
        self._instance.session_id = session_id
        return self

    def with_instruction_version(self, instruction_version: str) -> "AutomataAgentBuilder":
        if not isinstance(instruction_version, str):
            raise ValueError("Instruction version must be a str.")
        InstructionConfigVersion(instruction_version)
        self._instance.instruction_version = instruction_version
        return self

    def build(self) -> AutomataAgent:
        self._instance._setup()
        return self._instance
