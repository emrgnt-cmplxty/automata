import json
import logging
from typing import Any, Dict, List, Optional

from automata.eval import Action, Eval, Payload
from automata.llm.foundation import LLMChatMessage

logger = logging.getLogger(__name__)


class CodeExecutionError(Exception):
    """Exception raised when there's an error executing the code."""

    pass


class VariableNotFoundError(CodeExecutionError):
    """Exception raised when the target variable is not found."""

    pass


class CodeWritingAction(Action):
    """An concrete action representing written code."""

    LANGUAGE_MARKER_POSITION = 1

    # TODO - Consider adding variable name to the action,
    # e.g. if x = OpenAutomataAgent(),
    # and object_types = 'OpenAutomataAgent', object_value_repr = "OpenAutomataAgent(config = ...)",
    # then variable_name = 'x'
    def __init__(
        self,
        object_types: str,
        object_value_repr: Optional[str] = None,
        object_variable_checks: Optional[List[str]] = None,
    ):
        if object_variable_checks is None:
            object_variable_checks = []

        self.object_types = object_types
        self.object_value_repr = object_value_repr
        self.object_variable_checks = object_variable_checks

    def __eq__(self, other):
        if not isinstance(other, CodeWritingAction):
            return False

        if self.object_types != other.object_types:
            return False

        # Check for basic Python types
        basic_types = (int, float, str, list, dict, set, tuple, bool)
        if isinstance(self.object_value_repr, basic_types):
            return self.object_value_repr == other.object_value_repr

        # If not a basic type, perform attribute checks
        return all(
            getattr(self.object_value_repr, variable_check, None)
            == getattr(other.object_value_repr, variable_check, None)
            for variable_check in self.object_variable_checks
        )

    def __hash__(self):
        return hash(
            (
                json.dumps(self.object_value_repr),
                json.dumps(self.object_types),
            )
        )

    def __repr__(self):
        return f"CodeWritingAction(object_value_repr={self.object_value_repr}, object_types={self.object_types})"

    def to_payload(self) -> Payload:
        """Converts a CodeWritingAction into a payload for storing."""

        return {
            "type": "CodeWritingAction",
            "object_value_repr": self.object_value_repr or "None",
            "object_types": self.object_types,
        }

    @classmethod
    def from_payload(cls, payload: Payload) -> "CodeWritingAction":
        """Converts a payload CodeWritingAction into underlying payload."""

        object_types = payload["object_types"]
        if not isinstance(object_types, str):
            raise ValueError(
                f"Object types of type={type(object_types)} received, instead of str."
            )

        object_value_repr = payload["object_value_repr"]
        if not isinstance(object_value_repr, str):
            raise ValueError(
                f"Object representation of type={type(object_value_repr)} received, instead of str."
            )

        object_variable_checks = payload.get("object_variable_checks")
        if object_variable_checks is not None and not isinstance(
            object_variable_checks, list
        ):
            raise ValueError(
                f"Object variable checks ({object_variable_checks}) was not of type list."
            )

        return cls(
            object_value_repr=object_value_repr,
            object_types=object_types,
            object_variable_checks=object_variable_checks,
        )

    @staticmethod
    def _extract_snippet(
        snippet: str, expected_language: str = "python"
    ) -> str:
        """Extracts a code snippet from a markdown string."""

        return snippet.split(f"```{expected_language}")[
            CodeWritingAction.LANGUAGE_MARKER_POSITION
        ].replace("```", "")


class CodeWritingEval(Eval):
    """A class for evaluating an LLM's code writing ability."""

    def __init__(
        self,
        target_variables: List[str] = ["x"],
        *args,
        **kwargs,
    ):
        self.target_variables = target_variables

    def extract_action(self, message: LLMChatMessage) -> List[Action]:
        """Extracts the coding action explicitly"""

        actions: List[Action] = []

        if not message.content:
            return actions

        # Parse the code snippet to extract set variables and their types
        try:
            parsed_snippets = self._parse_code_snippet(message.content)
        except Exception as e:
            logger.info(f"Failed to parse code snippet with {e}")
            parsed_snippets = []

        # Clean errors from parsed snippet
        for snippet in parsed_snippets:
            if "error" in snippet:
                logger.error(f"Error parsing code snippet: {snippet['error']}")
                parsed_snippets.remove(snippet)

            action = CodeWritingAction(
                object_value_repr=snippet["value"],
                object_types=snippet["type"],
            )
            actions.append(action)
        return actions

    def _parse_code_snippet(self, raw_content) -> List[Dict[str, Any]]:
        """Parses a code snippet and extracts the object value and type at the specified variable."""

        # Isolate the exec environment to a separate dictionary
        isolated_locals: Dict[str, Any] = {}

        try:
            code_snippet = CodeWritingAction._extract_snippet(raw_content)
            # Execute the code snippet
            exec(code_snippet, None, isolated_locals)
            target_values = [
                isolated_locals.get(target_variable)
                for target_variable in self.target_variables
                if target_variable in isolated_locals
            ]
            if target_values is None:
                raise VariableNotFoundError(
                    f"Variables '{self.target_variables}' not found in the executed code."
                )
            return [
                {
                    "value": str(target_value),
                    "type": type(target_value).__name__,
                }
                for target_value in target_values
            ]

        except Exception as e:
            # If there's an error executing the code, return that.
            raise CodeExecutionError(f"Error executing code: {str(e)}")

    def _filter_actions(self, actions: List[Action]) -> List[Action]:
        """Filters out non-CodeWritingActions."""

        return [
            action
            for action in actions
            if isinstance(action, CodeWritingAction)
        ]
