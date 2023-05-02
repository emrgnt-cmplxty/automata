from abc import ABC, abstractmethod
from typing import List, Union

from automata.configs.config_enums import AgentConfigVersion

from .automata_agent_utils import ActionIndicator


class Action(ABC):
    @classmethod
    @abstractmethod
    def from_lines(cls, lines: List[str], index: int):
        pass


class ToolAction(Action):
    def __init__(self, tool_name: str, tool_query: str, tool_args: List[str]):
        self.tool_name = tool_name
        self.tool_query = tool_query
        self.tool_args = tool_args

    @classmethod
    def from_lines(cls, lines: List[str], index: int):
        tool_query = lines[index].split(ActionIndicator.ACTION.value)[1].strip()
        tool_name = lines[index + 2].split(ActionIndicator.ACTION.value)[1].strip()
        return cls(tool_name, tool_query, [])


class AgentAction(Action):
    def __init__(
        self,
        agent_config_version: AgentConfigVersion,
        agent_query: str,
        agent_instruction: List[str],
    ):
        self.agent_config_version = agent_config_version
        self.agent_query = agent_query
        self.agent_instruction = agent_instruction

    @classmethod
    def from_lines(cls, lines: List[str], index: int):
        agent_query = lines[index].split(ActionIndicator.ACTION.value)[1].strip()
        agent_config_version = AgentConfigVersion(
            lines[index + 2].split(ActionIndicator.ACTION.value)[1].strip()
        )
        return cls(agent_config_version, agent_query, [])


class ResultAction(Action):
    def __init__(self, result_name: str, result_outputs: List[str]):
        self.result_name = result_name
        self.result_outputs = result_outputs

    @classmethod
    def from_lines(cls, lines: List[str], index: int):
        result_name = lines[index].split(ActionIndicator.ACTION.value)[1].strip()
        result_outputs = lines[index + 1].split(ActionIndicator.ACTION.value)[1].strip()
        return cls(result_name, [result_outputs])


ActionTypes = Union[ToolAction, AgentAction, ResultAction]
