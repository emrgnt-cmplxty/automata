import textwrap
from abc import ABC, abstractmethod
from typing import List, Optional, Tuple, Union

from automata.config.config_types import AgentConfigName

from .agent_enums import (
    SUPPORTED_CODING_LANGUAGES,
    ActionIndicator,
    AgentField,
    ResultField,
    ToolField,
)


class Action(ABC):
    @abstractmethod
    def __str__(self) -> str:
        """
        Returns a string representation of the Action instance.
        """
        pass

    @classmethod
    @abstractmethod
    def from_lines(cls, lines: List[str], index: int) -> "Action":
        """
        A method to create an instance of an Action subclass from a list of lines and an index.

        Args:
            lines (List[str]): A list of strings containing the lines of the AutomataActions configuration.
            index (int): The current line index being processed from the configuration.

        Returns:
            An instance of an Action subclass.
        """
        pass


class ToolAction(Action):
    def __init__(self, tool_name: str, tool_query: str, tool_args: List[str]) -> None:
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

    def __str__(self) -> str:
        """
        Returns a string representation of the ToolAction instance.

        Returns:
            str: A string representation of the ToolAction instance.
        """
        return f"ToolAction(name={self.tool_name}, query={self.tool_query}, args={self.tool_args})"

    @classmethod
    def from_lines(cls, lines: List[str], index: int) -> "ToolAction":
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


class AgentAction(Action):
    def __init__(
        self,
        agent_version: AgentConfigName,
        agent_query: str,
        agent_instruction: List[str],
    ) -> None:
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

    def __str__(self) -> str:
        """
        Returns a string representation of the AgentAction instance.

        Returns:
            str: A string representation of the AgentAction instance.
        """
        return f"AgentAction(version={self.agent_version}, query={self.agent_query}, instruction={self.agent_instruction})"

    @classmethod
    def from_lines(cls, lines: List[str], index: int) -> "AgentAction":
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


class ResultAction(Action):
    def __init__(self, result_name: str, result_outputs: List[str]) -> None:
        """
        Initialize a ResultAction instance.

        Args:
            result_name (str): The name of the result.
            result_outputs (List[str]): A list of result outputs.
        """
        self.result_name = result_name
        self.result_outputs = result_outputs

    def __str__(self) -> str:
        """
        Returns a string representation of the ResultAction instance.

        Returns:
            str: A string representation of the ResultAction instance.
        """
        return f"ResultAction(name={self.result_name}, outputs={self.result_outputs})"

    @classmethod
    def from_lines(cls, lines: List[str], index: int) -> "ResultAction":
        """
        Create a ResultAction instance from a list of lines and an index.

        Args:
            lines (List[str]): A list of strings containing the lines of the AutomataActions configuration.
            index (int): The current line index being processed from the configuration.

        Returns:
            ResultAction: An instance of the ResultAction class.
        """
        result_name = lines[index].split(ActionIndicator.ACTION.value)[1].strip()
        result_outputs = lines[index + 1].split(ActionIndicator.ACTION.value)[
            1
        ].strip() + "\n".join(lines[index + 2 :])
        return cls(result_name, [result_outputs])


ActionTypes = Union[ToolAction, AgentAction, ResultAction]


class AutomataActionExtractor:
    @classmethod
    def extract_actions(cls, text: str) -> List[ActionTypes]:
        """
        Extract the actions from the given text.

        Args:
            text (str): The input text containing actions.

        Returns:
            List[ActionTypes]: A list of extracted actions.
        """
        lines = text.split("\n")
        actions: List[ActionTypes] = []
        action: Optional[ActionTypes] = None
        is_code = False
        skip_lines = 0
        for index, line in enumerate(lines):
            if skip_lines > 0:
                skip_lines -= 1
                continue

            if cls._is_new_tool_action(lines, index):
                action = ToolAction.from_lines(lines, index)
                actions.append(action)  # type: ignore
                skip_lines = ToolField.SPEC_LINES.value

            elif cls._is_new_agent_action(lines, index):
                action = AgentAction.from_lines(lines, index)
                actions.append(action)  # type: ignore
                skip_lines = AgentField.SPEC_LINES.value

            elif cls._is_return_result_action(line):
                action = ResultAction.from_lines(lines, index)
                actions.append(action)  # type: ignore
                skip_lines = ResultField.SPEC_LINES.value

            else:
                (is_code, skip_lines) = cls._process_action_input(
                    index, line, lines, action, is_code, skip_lines
                )

        return actions

    @staticmethod
    def _is_new_tool_action(lines, index) -> bool:
        """
        Check if the current line represents the start of a new tool action.

        Args:
            lines (List[str]): The list of lines in the input text.
            index (int): The index of the current line.

        Returns:
            bool: True if the line is a new tool action, False otherwise.
        """
        return (
            len(lines) > index + 1
            and f"{ActionIndicator.ACTION.value}{ToolField.INDICATOR.value}" in lines[index]
            and f"{ActionIndicator.ACTION.value}{ToolField.NAME.value}" in lines[index + 1]
        )

    @staticmethod
    def _is_new_agent_action(lines, index) -> bool:
        """
        Check if the current line represents the start of a new agent action.

        Args:
            lines (List[str]): The list of lines in the input text.
            index (int): The index of the current line.

        Returns:
            bool: True if the line is a new agent action, False otherwise.
        """
        return (
            len(lines) > index + 1
            and f"{ActionIndicator.ACTION.value}{AgentField.INDICATOR.value}" in lines[index]
            and f"{ActionIndicator.ACTION.value}{AgentField.NAME.value}" in lines[index + 1]
        )

    @staticmethod
    def _is_return_result_action(line: str) -> bool:
        """
        Check if the current line represents a return result action.

        Args:
            line (str): The current line of the input text.

        Returns:
            bool: True if the line is a return result action, False otherwise.
        """
        return line.strip().startswith(
            f"{ActionIndicator.ACTION.value}{ResultField.INDICATOR.value}"
        )

    @staticmethod
    def _is_code_start(
        index: int,
        lines: List[str],
    ) -> bool:
        """
        Check if the current line represents the start of a code block.

        Args:
            index (int): The index of the current line in the input text.
            lines (List[str]): The list of lines in the input text.

        Returns:
            bool: True if the line is the start of a code block, False otherwise.
        """
        return len(lines) > index + 1 and ActionIndicator.CODE.value in lines[index + 1]

    @staticmethod
    def _is_code_end(line: str) -> bool:
        """
        Check if the current line represents the end of a code block.

        Args:
            line (str): The current line of the input text.

        Returns:
            bool: True if the line is the end of a code block, False otherwise.
        """
        return ActionIndicator.CODE.value in line

    @staticmethod
    def _is_code_indicator(line: str) -> bool:
        """
        Check if the current line is a code indicator.

        Args:
            line (str): The current line of the input text.

        Returns:
            bool: True if the line is a code indicator, False otherwise.
        """
        contains_indicator = line.strip() == ActionIndicator.CODE.value
        for language in SUPPORTED_CODING_LANGUAGES:
            contains_indicator = (
                contains_indicator
                or "%s%s" % (ActionIndicator.CODE.value, language) in line.strip()
            )

        return contains_indicator

    @staticmethod
    def _process_action_input(
        index: int,
        line: str,
        lines: List[str],
        action: Optional[ActionTypes],
        is_code: bool,
        skip_lines: int,
    ) -> Tuple[bool, int]:
        """
        Process the action input, handling code blocks and appending input to the current action.

        Args:
            index (int): The index of the current line in the input text.
            line (str): The current line of the input text.
            lines (List[str]): The list of lines in the input text.
            action (Optional[ActionTypes]): The current action being processed.
            is_code (bool): Indicates if the current line is part of a code block.
            skip_lines (int): The number of lines to skip for the current action.

        Returns:
            Tuple[bool, int]: A tuple containing the updated is_code and skip_lines values.
        """
        if action is not None:
            if isinstance(action, AgentAction):
                inputs = action.agent_instruction
            elif isinstance(action, ToolAction):
                inputs = action.tool_args
            elif isinstance(action, ResultAction):
                #     inputs = action.result_outputs
                return (is_code, skip_lines)

            if AutomataActionExtractor._is_code_start(index, lines) and (not is_code):
                is_code = True
                contains_language_definition = False
                for language in SUPPORTED_CODING_LANGUAGES:
                    if language in line:
                        contains_language_definition = True
                if contains_language_definition:
                    inputs.append("")
                else:
                    inputs.append(line + "\n")
                skip_lines = 1
            elif not AutomataActionExtractor._is_code_indicator(line) and is_code:
                if len(inputs) > 0:
                    inputs[-1] += line + "\n"
                else:
                    inputs.append(line + "\n")
            elif AutomataActionExtractor._is_code_end(line) and is_code:
                is_code = False
                inputs[-1] = textwrap.dedent(inputs[-1])
            elif ActionIndicator.ACTION.value in line:
                clean_line = line.split(ActionIndicator.ACTION.value)[1].strip()
                inputs.append(clean_line)
        return (is_code, skip_lines)
