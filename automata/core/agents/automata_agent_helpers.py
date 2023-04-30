import textwrap
from abc import ABC, abstractmethod
from typing import Dict, Final, List, Optional, Tuple, Union, cast


def generate_user_observation_message(observations: Dict[str, str], include_prefix=True) -> str:
    """Generate a message for the user based on the observations."""
    message = ""
    if include_prefix:
        message += f"{ActionExtractor.ACTION_INDICATOR} observations\n"
    for observation_name in observations.keys():
        message = append_observation_message(observation_name, observations, message)
    return message


def append_observation_message(observation_name: str, observations: Dict[str, str], message: str):
    new_message = ""
    new_message += f"    {ActionExtractor.ACTION_INDICATOR}{observation_name}" + "\n"
    new_message += (
        f"      {ActionExtractor.ACTION_INDICATOR}{observations[observation_name]}" + "\n"
    )
    return message + new_message


def retrieve_completion_message(processed_inputs: Dict[str, str]) -> Optional[str]:
    """Check if the result is a return result indicator."""
    for processed_input in processed_inputs.keys():
        if ActionExtractor.RETURN_RESULT_INDICATOR in processed_input:
            return processed_inputs[processed_input]
    return None


class Action(ABC):
    @classmethod
    @abstractmethod
    def from_lines(cls, lines: List[str], index: int):
        pass


class ToolAction(Action):
    """A dictionary containing an action and its inputs."""

    def __init__(self, tool_name: str, tool_query: str, tool_args: List[str]):
        self.tool_name = tool_name
        self.tool_query = tool_query
        self.tool_args = tool_args

    @classmethod
    def from_lines(cls, lines: List[str], index: int):
        tool_query = lines[index].split(ActionExtractor.ACTION_INDICATOR)[1].strip()
        tool_name = lines[index + 2].split(ActionExtractor.ACTION_INDICATOR)[1].strip()
        return cls(tool_name, tool_query, [])


class AgentAction(Action):
    def __init__(self, agent_name: str, agent_query: str, agent_instruction: List[str]):
        self.agent_name = agent_name
        self.agent_query = agent_query
        self.agent_instruction = agent_instruction

    @classmethod
    def from_lines(cls, lines: List[str], index: int):
        agent_query = lines[index].split(ActionExtractor.ACTION_INDICATOR)[1].strip()
        agent_name = lines[index + 2].split(ActionExtractor.ACTION_INDICATOR)[1].strip()
        return cls(agent_name, agent_query, [])


class ResultAction(Action):
    def __init__(self, result_name: str, result_outputs: List[str]):
        self.result_name = result_name
        self.result_outputs = result_outputs

    @classmethod
    def from_lines(cls, lines: List[str], index: int):
        result_name = lines[index].split(ActionExtractor.ACTION_INDICATOR)[1].strip()
        # TODO - Generalize from_lines to work with multiple lines
        result_outputs = lines[index + 1].split(ActionExtractor.ACTION_INDICATOR)[1].strip()
        return cls(result_name, [result_outputs])


ActionTypes = Union[ToolAction, AgentAction, ResultAction]


class ActionExtractor:
    """Class for extracting actions from an AutomataAgent string."""

    ACTION_INDICATOR: Final = "- "
    CODE_INDICATOR: Final = "```"

    EXPECTED_CODING_LANGUAGES: Final = ["python"]

    # Tool indicatation variables
    TOOL_INDICATOR: Final = "tool_query"
    TOOL_NAME_FIELD: Final = "tool_name"
    TOOL_ARGS_FIELD: Final = "tool_args"
    TOOL_QUERY_FIELD: Final = "tool_query"
    TOOL_SPEC_LINES: Final = 3

    # Agent indicatation variables
    AGENT_INDICATOR: Final = "agent_query"
    AGENT_NAME_FIELD: Final = "agent_name"
    AGENT_ARGS_FIELD: Final = "agent_instruction"
    AGENT_QUERY_FIELD: Final = "agent_query"
    ACTION_SPEC_LINES: Final = 3

    # Result indicatation variables
    RETURN_RESULT_INDICATOR: Final = "return_result"
    RESULT_SPEC_LINES: Final = 2

    @classmethod
    def extract_actions(cls, text: str) -> List[ActionTypes]:
        lines = text.split("\n")
        actions: List[ActionTypes] = []
        action: Optional[ActionTypes] = None
        is_code = False
        skip_lines = 0

        # Iterate through the lines and extract actions
        for index, line in enumerate(lines):
            if skip_lines > 0:
                skip_lines -= 1
                continue

            if cls._is_new_tool_action(lines, index):
                action = ToolAction.from_lines(lines, index)
                actions.append(action)  # type: ignore
                skip_lines = cls.TOOL_SPEC_LINES

            elif cls._is_new_agent_action(lines, index):
                action = AgentAction.from_lines(lines, index)
                actions.append(action)  # type: ignore
                skip_lines = cls.ACTION_SPEC_LINES

            elif cls._is_return_result_action(line):
                action = ResultAction.from_lines(lines, index)
                actions.append(action)  # type: ignore
                skip_lines = cls.RESULT_SPEC_LINES

            else:
                (is_code, skip_lines) = cls._process_action_input(
                    index, line, lines, action, is_code, skip_lines
                )
        return actions

    @staticmethod
    def _is_new_tool_action(lines, index):
        """Check if the current line is a new action."""
        return (
            len(lines) > index + 1
            and f"{ActionExtractor.ACTION_INDICATOR}{ActionExtractor.TOOL_INDICATOR}"
            in lines[index]
            and f"{ActionExtractor.ACTION_INDICATOR}{ActionExtractor.TOOL_NAME_FIELD}"
            in lines[index + 1]
        )

    @staticmethod
    def _process_new_tool_action(
        tool_query_line: str,
        tool_name_line: str,
        action: Optional[ToolAction],
        actions: List[ActionTypes],
    ):
        """Process a new action."""
        if action is not None:
            actions.append(action)
        tool_query = tool_query_line.split(ActionExtractor.ACTION_INDICATOR)[1].strip()
        tool_name = tool_name_line.split(ActionExtractor.ACTION_INDICATOR)[1].strip()
        return ToolAction(tool_name=tool_name, tool_query=tool_query, tool_args=[])

    @staticmethod
    def _is_new_agent_action(lines, index):
        """Check if the current line is a new agent action."""
        return (
            len(lines) > index + 1
            and f"{ActionExtractor.ACTION_INDICATOR}{ActionExtractor.AGENT_INDICATOR}"
            in lines[index]
            and f"{ActionExtractor.ACTION_INDICATOR}{ActionExtractor.AGENT_NAME_FIELD}"
            in lines[index + 1]
        )

    @staticmethod
    def _process_new_agent_action(
        agent_query_line: str,
        agent_name_line: str,
        action: Optional[ActionTypes],
        actions: List[ActionTypes],
    ):
        """Process a new agent action."""
        if action is not None:
            actions.append(action)
        agent_query = agent_query_line.split(ActionExtractor.ACTION_INDICATOR)[1].strip()
        agent_name = agent_name_line.split(ActionExtractor.ACTION_INDICATOR)[1].strip()
        return AgentAction(agent_name=agent_name, agent_query=agent_query, agent_instruction=[])

    @staticmethod
    def _is_return_result_action(line: str) -> bool:
        """Check if the current line is a new return result action."""
        return line.strip().startswith(
            f"{ActionExtractor.ACTION_INDICATOR}{ActionExtractor.RETURN_RESULT_INDICATOR}"
        )

    @staticmethod
    def _process_new_return_result_action(
        line: str, action: Optional[ResultAction], actions: List[ActionTypes]
    ):
        """Process a new return result action."""
        if action is not None:
            actions.append(action)
        name = (
            line.strip()
            .split(ActionExtractor.ACTION_INDICATOR)[1]
            .split(ActionExtractor.ACTION_INDICATOR)[0]
        )
        return ResultAction(result_name=name, result_outputs=[])

    @staticmethod
    def _process_action_input(
        index: int,
        line: str,
        lines: List[str],
        action: Optional[Action],
        is_code: bool,
        skip_lines: int,
    ) -> Tuple[bool, int]:
        """Process an action input."""
        if action is not None:
            if isinstance(action, AgentAction):
                inputs = cast(List[str], action.agent_instruction)
            elif isinstance(action, ToolAction):
                inputs = cast(List[str], action.tool_args)
            elif isinstance(action, ResultAction):
                inputs = cast(List[str], action.result_outputs)

            if ActionExtractor._is_code_start(index, lines) and (not is_code):
                is_code = True
                contains_language_definition = False
                for language in ActionExtractor.EXPECTED_CODING_LANGUAGES:
                    if language in line:
                        contains_language_definition = True
                if contains_language_definition:
                    inputs.append("")
                else:
                    inputs.append(line + "\n")
                skip_lines = 1
            elif not ActionExtractor._is_code_indicator(line) and is_code:
                inputs[-1] += line + "\n"
            elif ActionExtractor._is_code_end(line) and (not is_code):
                count = line.count("`")
                if count != 6:
                    raise ValueError(f"Invalid action format: {line}")
            elif ActionExtractor._is_code_end(line) and is_code:
                is_code = False
                inputs[-1] = textwrap.dedent(inputs[-1])
            elif ActionExtractor.ACTION_INDICATOR in line:
                clean_line = line.split(ActionExtractor.ACTION_INDICATOR)[1].strip()
                inputs.append(clean_line)
        return (is_code, skip_lines)

    @staticmethod
    def _is_code_start(
        index: int,
        lines: List[str],
    ):
        """Check if the current line is the start of a code block."""
        return len(lines) > index + 1 and ActionExtractor.CODE_INDICATOR in lines[index + 1]

    @staticmethod
    def _is_code_end(line: str) -> bool:
        """Check if the current line is the end of a code block."""
        return ActionExtractor.CODE_INDICATOR in line

    @staticmethod
    def _is_code_indicator(line: str) -> bool:
        """Check if the current line is a code indicator."""
        return line.strip() == ActionExtractor.CODE_INDICATOR
