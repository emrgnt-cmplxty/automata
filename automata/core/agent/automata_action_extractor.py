import textwrap
from typing import List, Optional, Tuple

from .automata_actions import ActionTypes, AgentAction, ResultAction, ToolAction
from .automata_agent_utils import (
    SUPPORTED_CODING_LANGUAGES,
    ActionIndicator,
    AgentField,
    ResultField,
    ToolField,
)


class AutomataActionExtractor:
    @classmethod
    def extract_actions(cls, text: str) -> List[ActionTypes]:
        """Extract the actions from the text."""
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
        """Check if the line is a new tool action."""
        return (
            len(lines) > index + 1
            and f"{ActionIndicator.ACTION.value}{ToolField.INDICATOR.value}" in lines[index]
            and f"{ActionIndicator.ACTION.value}{ToolField.NAME.value}" in lines[index + 1]
        )

    @staticmethod
    def _is_new_agent_action(lines, index) -> bool:
        """Check if the line is a new agent action."""
        return (
            len(lines) > index + 1
            and f"{ActionIndicator.ACTION.value}{AgentField.INDICATOR.value}" in lines[index]
            and f"{ActionIndicator.ACTION.value}{AgentField.NAME.value}" in lines[index + 1]
        )

    @staticmethod
    def _is_return_result_action(line: str) -> bool:
        """Check if the line is a return result action."""
        return line.strip().startswith(
            f"{ActionIndicator.ACTION.value}{ResultField.INDICATOR.value}"
        )

    @staticmethod
    def _process_action_input(
        index: int,
        line: str,
        lines: List[str],
        action: Optional[ActionTypes],
        is_code: bool,
        skip_lines: int,
    ) -> Tuple[bool, int]:
        """Process the action input."""
        if action is not None:
            if isinstance(action, AgentAction):
                inputs = action.agent_instruction
            elif isinstance(action, ToolAction):
                inputs = action.tool_args
            elif isinstance(action, ResultAction):
                inputs = action.result_outputs

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
            elif AutomataActionExtractor._is_code_end(line) and (not is_code):
                count = line.count("`")
                if count != 6:
                    raise ValueError(f"Invalid action format: {line}")
            elif AutomataActionExtractor._is_code_end(line) and (not is_code):
                count = line.count("`")
                if count != 6:
                    raise ValueError(f"Invalid action format: {line}")
            elif AutomataActionExtractor._is_code_end(line) and is_code:
                is_code = False
                inputs[-1] = textwrap.dedent(inputs[-1])
            elif ActionIndicator.ACTION.value in line:
                clean_line = line.split(ActionIndicator.ACTION.value)[1].strip()
                inputs.append(clean_line)
        return (is_code, skip_lines)

    @staticmethod
    def _is_code_start(
        index: int,
        lines: List[str],
    ):
        """Check if the current line is the start of a code block."""
        return len(lines) > index + 1 and ActionIndicator.CODE.value in lines[index + 1]

    @staticmethod
    def _is_code_end(line: str) -> bool:
        """Check if the current line is the end of a code block."""
        return ActionIndicator.CODE.value in line

    @staticmethod
    def _is_code_indicator(line: str) -> bool:
        """Check if the current line is a code indicator."""
        return line.strip() == ActionIndicator.CODE.value
