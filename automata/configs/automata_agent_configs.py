import os
from dataclasses import dataclass
from typing import Dict, List, Optional

import yaml
from pydantic import BaseModel

from automata.core.base.tool import Toolkit, ToolkitType

from .config_enums import AgentConfigVersion, ConfigCategory, InstructionConfigVersion


@dataclass
class AutomataInstructionPayload:
    """
    The AutomataInstructionPayload class is used to store the payload for formatting the introduction instruction.
    Fields on this class are used to format the introduction instruction.
    """

    agents_message: Optional[str] = None
    overview: Optional[str] = None
    tools: Optional[str] = None

    def validate_fields(self, required_fields: List[str]):
        initialized_fields = {field for field, value in self.__dict__.items() if value is not None}
        missing_fields = set(required_fields) - set(initialized_fields)

        if missing_fields:
            raise ValueError(f"Missing fields in AutomataInstructionPayload: {missing_fields}")


class AutomataAgentConfig(BaseModel):
    """
    Args:
        config_name (AgentConfigVersion): The config_name of the agent to use.
        instruction_payload (AutomataInstructionPayload): Initial payload to format input instructions.
        llm_toolkits (Dict[ToolkitType, Toolkit]): A dictionary of toolkits to use.
        instructions (str): A string of instructions to execute.
        system_instruction_template (str): A string of instructions to execute.
        instruction_input_variables (List[str]): A list of input variables for the instruction template.
        model (str): The model to use for the agent.
        stream (bool): Whether to stream the results back to the main.
        verbose (bool): Whether to print the results to stdout.
        max_iters (int): The maximum number of iterations to run.
        temperature (float): The temperature to use for the agent.
        session_id (Optional[str]): The session ID to use for the agent.
        instruction_version (InstructionConfigVersion): Config version of the introduction instruction.
    """

    class Config:
        SUPPORTED_MODELS = ["gpt-4", "gpt-3.5-turbo"]
        arbitrary_types_allowed = True

    config_name: AgentConfigVersion = AgentConfigVersion.AUTOMATA_INDEXER_DEV
    instruction_payload: AutomataInstructionPayload = AutomataInstructionPayload()
    llm_toolkits: Dict[ToolkitType, Toolkit] = {}
    instructions: str = ""
    description: str = ""
    system_instruction_template: str = ""
    instruction_input_variables: List[str] = []
    model: str = "gpt-4"
    stream: bool = False
    verbose: bool = False
    max_iters: int = 1_000_000
    temperature: float = 0.7
    session_id: Optional[str] = None
    instruction_version: InstructionConfigVersion = (
        InstructionConfigVersion.AGENT_INTRODUCTION_PROD
    )
    name: str = "Automata"

    @classmethod
    def load_automata_yaml_config(cls, config_name: AgentConfigVersion) -> Dict:
        """Loads the automata.yaml config file."""
        from automata.tool_management.tool_management_utils import build_llm_toolkits

        file_dir_path = os.path.dirname(os.path.abspath(__file__))
        config_abs_path = os.path.join(
            file_dir_path, ConfigCategory.AGENT.value, f"{config_name.value}.yaml"
        )

        with open(config_abs_path, "r") as file:
            loaded_yaml = yaml.safe_load(file)

        if "tools" in loaded_yaml:
            tools = loaded_yaml["tools"].split(",")
            loaded_yaml["llm_toolkits"] = build_llm_toolkits(tools)

        loaded_yaml["config_name"] = config_name
        return loaded_yaml

    @classmethod
    def add_overview_to_instruction_payload(cls, config: "AutomataAgentConfig") -> None:
        """Handles the overview input for the agent."""
        from automata.core.utils import root_py_path
        from automata.tools.python_tools.python_indexer import PythonIndexer

        if "overview" in config.instruction_input_variables:
            config.instruction_payload.overview = PythonIndexer.build_overview(root_py_path())

    @classmethod
    def load(cls, config_name: AgentConfigVersion) -> "AutomataAgentConfig":
        """Loads the config for the agent."""
        if config_name == AgentConfigVersion.DEFAULT:
            return AutomataAgentConfig()

        loaded_yaml = cls.load_automata_yaml_config(config_name)
        config = AutomataAgentConfig(**loaded_yaml)
        cls.add_overview_to_instruction_payload(config)

        return config
