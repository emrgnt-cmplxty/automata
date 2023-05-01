import os
from enum import Enum
from typing import Dict, List, Optional

import yaml
from pydantic import BaseModel

from automata.core.base.tool import Toolkit, ToolkitType
from .config_enums import AgentConfigVersion, ConfigCategory, InstructionConfigVersion


class AutomataAgentConfig(BaseModel):

    """
    Args:
        config_version (AgentConfigVersion): The config_version of the agent to use.
        initial_payload (Dict[str, str]): Initial payload to send to the agent.
        llm_toolkits (Dict[ToolkitType, Toolkit]): A dictionary of toolkits to use.
        instructions (str): A string of instructions to execute.
        system_instruction_template (str): A string of instructions to execute.
        instruction_input_variables (List[str]): A list of input variables for the instruction template.
        model (str): The model to use for the agent.
        stream (bool): Whether to stream the results back to the master.
        verbose (bool): Whether to print the results to stdout.
        max_iters (int): The maximum number of iterations to run.
        temperature (float): The temperature to use for the agent.
        session_id (Optional[str]): The session ID to use for the agent.
        instruction_version (InstructionConfigVersion): Config version of the introduction instruction.
    """

    class Config:
        SUPPORTED_MODELS = ["gpt-4", "gpt-3.5-turbo"]
        arbitrary_types_allowed = True

    config_version: AgentConfigVersion = AgentConfigVersion.AUTOMATA_INDEXER_DEV
    initial_payload: Dict[str, str] = {}
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
    instruction_version: str = InstructionConfigVersion.AGENT_INTRODUCTION_PROD.value

    @classmethod
    def load_automata_yaml_config(cls, config_version: AgentConfigVersion) -> Dict:
        from automata.tool_management.tool_management_utils import build_llm_toolkits

        file_dir_path = os.path.dirname(os.path.abspath(__file__))
        config_abs_path = os.path.join(
            file_dir_path, ConfigCategory.AGENT.value, f"{config_version.value}.yaml"
        )

        with open(config_abs_path, "r") as file:
            loaded_yaml = yaml.safe_load(file)

        if "tools" in loaded_yaml:
            tools = loaded_yaml["tools"].split(",")
            loaded_yaml["llm_toolkits"] = build_llm_toolkits(tools)

        loaded_yaml["config_version"] = config_version
        return loaded_yaml

    @classmethod
    def handle_overview_input(cls, config: "AutomataAgentConfig") -> None:
        from automata.core.utils import root_py_path
        from automata.tools.python_tools.python_indexer import PythonIndexer

        if "overview" in config.instruction_input_variables:
            indexer = PythonIndexer(root_py_path())
            config.initial_payload["overview"] = indexer.get_overview()

    @classmethod
    def load(cls, config_version: AgentConfigVersion) -> "AutomataAgentConfig":
        if config_version == AgentConfigVersion.DEFAULT:
            return AutomataAgentConfig()

        loaded_yaml = cls.load_automata_yaml_config(config_version)
        config = AutomataAgentConfig(**loaded_yaml)
        cls.handle_overview_input(config)

        return config
