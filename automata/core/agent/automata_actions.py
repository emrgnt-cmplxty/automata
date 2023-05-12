from abc import ABC, abstractmethod
from typing import List, Union

from automata.configs.config_enums import AgentConfigName

from .automata_agent_enums import ActionIndicator


class Action(ABC):
    @classmethod
    @abstractmethod
    def from_lines(cls, lines: List[str], index: int):
        """
        A factory method to create an instance of an Action subclass from a list of lines and an index.

        Args:
            lines (List[str]): A list of strings containing the lines of the AutomataActions configuration.
            index (int): The current line index being processed from the configuration.

        Returns:
            An instance of an Action subclass.
        """
        pass

    @abstractmethod
    def __str__(self):
        """
        Returns a string representation of the Action instance.

        Returns:
            str: A string representation of the Action instance.
        """
        pass


class ToolAction(Action):
    def __init__(self, tool_name: str, tool_query: str, tool_args: List[str]):
        """
        Initialize a ToolAction instance.

        Args:
            tool_name (str): The name of the tool.
            tool_query (str): The query to be executed by the tool.
            tool_args (List[str]): A list of arguments to be passed to the tool.
        """
        self.tool_name = tool_name
        self.tool_query = tool_query
        self.tool_args = tool_args

    @classmethod
    def from_lines(cls, lines: List[str], index: int):
        """
        Create a ToolAction instance from a list of lines and an index.

        Args:
            lines (List[str]): A list of strings containing the lines of the AutomataActions configuration.
            index (int): The current line index being processed from the configuration.

        Returns:
            ToolAction: An instance of the ToolAction class.
        """
        tool_query = lines[index].split(ActionIndicator.ACTION.value)[1].strip()
        tool_name = lines[index + 2].split(ActionIndicator.ACTION.value)[1].strip()
        return cls(tool_name, tool_query, [])

    def __str__(self):
        """
        Returns a string representation of the ToolAction instance.

        Returns:
            str: A string representation of the ToolAction instance.
        """
        return f"ToolAction(name={self.tool_name}, query={self.tool_query}, args={self.tool_args})"


class AgentAction(Action):
    def __init__(
        self,
        agent_version: AgentConfigName,
        agent_query: str,
        agent_instruction: List[str],
    ):
        """
        Initialize an AgentAction instance.

        Args:
            agent_version (AgentConfigName): The version of the agent configuration.
            agent_query (str): The query to be executed by the agent.
            agent_instruction (List[str]): A list of instructions for the agent.
        """
        self.agent_version = agent_version
        self.agent_query = agent_query
        self.agent_instruction = agent_instruction

    @classmethod
    def from_lines(cls, lines: List[str], index: int):
        """
        Create an AgentAction instance from a list of lines and an index.

        Args:
            lines (List[str]): A list of strings containing the lines of the AutomataActions configuration.
            index (int): The current line index being processed from the configuration.

        Returns:
            AgentAction: An instance of the AgentAction class.
        """
        agent_query = lines[index].split(ActionIndicator.ACTION.value)[1].strip()
        agent_version = AgentConfigName(
            lines[index + 2].split(ActionIndicator.ACTION.value)[1].strip()
        )
        return cls(agent_version, agent_query, [])

    def __str__(self):
        """
        Returns a string representation of the AgentAction instance.

        Returns:
            str: A string representation of the AgentAction instance.
        """
        return f"AgentAction(version={self.agent_version}, query={self.agent_query}, instruction={self.agent_instruction})"


class ResultAction(Action):
    def __init__(self, result_name: str, result_outputs: List[str]):
        """
        Initialize a ResultAction instance.

        Args:
            result_name (str): The name of the result.
            result_outputs (List[str]): A list of result outputs.
        """
        self.result_name = result_name
        self.result_outputs = result_outputs

    @classmethod
    def from_lines(cls, lines: List[str], index: int):
        """
        Create a ResultAction instance from a list of lines and an index.

        Args:
            lines (List[str]): A list of strings containing the lines of the AutomataActions configuration.
            index (int): The current line index being processed from the configuration.

        Returns:
            ResultAction: An instance of the ResultAction class.
        """
        result_name = lines[index].split(ActionIndicator.ACTION.value)[1].strip()
        result_outputs = lines[index + 1].split(ActionIndicator.ACTION.value)[1].strip()
        return cls(result_name, [result_outputs])

    def __str__(self):
        """
        Returns a string representation of the ResultAction instance.

        Returns:
            str: A string representation of the ResultAction instance.
        """
        return f"ResultAction(name={self.result_name}, outputs={self.result_outputs})"


ActionTypes = Union[ToolAction, AgentAction, ResultAction]
