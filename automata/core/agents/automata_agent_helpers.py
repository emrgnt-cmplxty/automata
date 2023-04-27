import textwrap
from typing import Dict, Final, List, Optional, TypedDict, cast


def generate_user_observation_message(observations: Dict[str, str]) -> str:
    """Generate a message for the user based on the observations."""
    message = f"{ActionExtractor.ACTION_INDICATOR} observations\n"
    for observation_name in observations.keys():
        message += f"    {ActionExtractor.ACTION_INDICATOR}{observation_name}" + "\n"
        message += (
            f"      {ActionExtractor.ACTION_INDICATOR}{observations[observation_name]}" + "\n"
        )
    return message


def retrieve_completion_message(processed_inputs: Dict[str, str]) -> Optional[str]:
    """Check if the result is a return result indicator."""
    for processed_input in processed_inputs.keys():
        if ActionExtractor.RETURN_RESULT_INDICATOR in processed_input:
            return processed_inputs[processed_input]
    return None


class AutomataAction(TypedDict):
    """A dictionary containing an action and its inputs."""

    tool_name: str
    tool_query: str
    tool_args: List[str]


class ActionExtractor:
    """Class for extracting actions from an AutomataAgent string."""

    ACTION_INDICATOR: Final = "- "
    CODE_INDICATOR: Final = "```"
    TOOL_INDICATOR: Final = "tool_query"
    TOOL_NAME_FIELD: Final = "tool_name"
    TOOL_ARGS_FIELD: Final = "tool_args"
    TOOL_QUERY_FIELD: Final = "tool_query"
    RETURN_RESULT_INDICATOR: Final = "return_result"
    EXPECTED_CODING_LANGUAGES: Final = ["python"]

    TOOL_SPEC_LINES: Final = 3

    @classmethod
    def extract_actions(cls, text: str) -> List[AutomataAction]:
        """
        Extract actions from the given text.

        Args:
            text: A string containing actions formatted as nested lists.

        Returns:
            A list of dictionaries containing actions and their inputs.
        """
        lines = text.split("\n")
        actions: List[AutomataAction] = []
        action: Optional[AutomataAction] = None
        is_code = False
        skip_lines = 0
        # Iterate through the lines and extract actions
        for index, line in enumerate(lines):
            # We set "skip_next" when encountering accumulation phrases
            # e.g. "inputs"
            if skip_lines > 0:
                skip_lines -= 1
                continue
            if cls._is_new_tool_action(lines, index):
                if len(lines) <= index + cls.TOOL_SPEC_LINES - 1:
                    raise ValueError(f"Invalid action format: {line}")
                tool_query_line = lines[index]
                tool_name_line = lines[index + 2]
                action = cls._process_new_tool_action(
                    tool_query_line, tool_name_line, action, actions
                )
                skip_lines = cls.TOOL_SPEC_LINES
            elif cls._is_return_result_action(line):
                action = cls._process_new_return_result_action(line, action, actions)
            else:
                (is_code, skip_lines) = cls._process_action_input(
                    index, line, lines, action, is_code, skip_lines
                )
        # Add the last action if it exists
        if action is not None:
            actions.append(action)
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
        action: Optional[AutomataAction],
        actions: List[AutomataAction],
    ):
        """Process a new action."""
        if action is not None:
            actions.append(action)
        tool_query = tool_query_line.split(ActionExtractor.ACTION_INDICATOR)[1].strip()
        tool_name = tool_name_line.split(ActionExtractor.ACTION_INDICATOR)[1].strip()
        return AutomataAction(tool_name=tool_name, tool_query=tool_query, tool_args=[])

    @staticmethod
    def _is_return_result_action(line: str) -> bool:
        return line.strip().startswith(
            f"{ActionExtractor.ACTION_INDICATOR}{ActionExtractor.RETURN_RESULT_INDICATOR}"
        )

    @staticmethod
    def _process_new_return_result_action(
        line: str, action: Optional[AutomataAction], actions: List[AutomataAction]
    ):
        """Process a new return result action."""
        if action is not None:
            actions.append(action)
        return {
            ActionExtractor.TOOL_NAME_FIELD: line.strip()
            .split(ActionExtractor.ACTION_INDICATOR)[1]
            .split(ActionExtractor.ACTION_INDICATOR)[0]
            .strip(),
            ActionExtractor.TOOL_ARGS_FIELD: [],
            ActionExtractor.TOOL_QUERY_FIELD: "",
        }

    @staticmethod
    def _process_action_input(
        index: int,
        line: str,
        lines: List[str],
        action: Optional[AutomataAction],
        is_code: bool,
        skip_lines: int,
    ):
        """Process an action input."""
        if action is not None:
            inputs = cast(List[str], action[ActionExtractor.TOOL_ARGS_FIELD])
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
                inputs[-1] = textwrap.dedent(action[ActionExtractor.TOOL_ARGS_FIELD][-1])
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
