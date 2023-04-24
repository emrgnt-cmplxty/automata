import os
from enum import Enum
from typing import Any, Dict, List, Optional

import yaml
from pydantic import BaseModel


class AutomataConfigVersion(Enum):
    DEFAULT = "default"
    TEST = "test"

    AUTOMATA_MASTER_V1 = "automata_master_v1"
    AUTOMATA_INDEXER_V1 = "automata_indexer_v1"
    AUTOMATA_WRITER_V1 = "automata_writer_v1"

    AUTOMATA_MASTER_V2 = "automata_master_v2"
    AUTOMATA_INDEXER_V2 = "automata_indexer_v2"
    AUTOMATA_WRITER_V2 = "automata_writer_v2"

    AUTOMATA_MASTER_V3 = "automata_master_v3"

    AUTOMATA_DOCSTRING_MANAGER_V1 = "automata_docstring_manager_v1"


class AutomataAgentConfig(BaseModel):

    """
    Args:
        config_version (AutomataConfigVersion): The config_version of the agent to use.
        initial_payload (Dict[str, str]): Initial payload to send to the agent.
        llm_toolkits (Dict[ToolkitType, Toolkit]): A dictionary of toolkits to use.
        instructions (str): A string of instructions to execute.
        instruction_template (str): A string of instructions to execute.
        instruction_input_variables (List[str]): A list of input variables for the instruction template.
        model (str): The model to use for the agent.
        stream (bool): Whether to stream the results back to the master.
        verbose (bool): Whether to print the results to stdout.
        max_iters (int): The maximum number of iterations to run.
        temperature (float): The temperature to use for the agent.
        session_id (Optional[str]): The session ID to use for the agent.
    """

    class Config:
        SUPPORTED_MDOELS = ["gpt-4", "gpt-3.5-turbo"]
        arbitrary_types_allowed = True

    config_version: str = "default"
    initial_payload: Dict[str, str] = {}
    llm_toolkits: Dict[
        Any, Any
    ] = {}  # Dict[ToolkitType, Toolkit], not specified due to circular import
    instructions: str = ""
    instruction_template: str = ""
    instruction_input_variables: List[str] = []
    model: str = "gpt-4"
    stream: bool = False
    verbose: bool = False
    max_iters: int = 1_000_000
    temperature: float = 0.7
    session_id: Optional[str] = None

    @classmethod
    def load(cls, config_version: AutomataConfigVersion) -> "AutomataAgentConfig":
        if config_version == AutomataConfigVersion.DEFAULT:
            return AutomataAgentConfig()
        file_dir_path = os.path.dirname(os.path.abspath(__file__))
        config_abs_path = os.path.join(file_dir_path, f"{config_version.value}.yaml")
        with open(config_abs_path, "r") as file:
            loaded_yaml = yaml.safe_load(file)
            return AutomataAgentConfig(**loaded_yaml)
