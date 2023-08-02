"""Implements an evaluation for code writing ability."""
import json
import logging
from typing import Any, Dict, List, Optional

from automata.core.base import AutomataError
from automata.eval.agent.agent_eval import AgentEval
from automata.eval.eval_base import Action, Payload, register_action
from automata.llm import LLMChatMessage

logger = logging.getLogger(__name__)


class CodeExecutionError(AutomataError):
    """Exception raised when there's an error executing the code."""

    pass


class VariableNotFoundError(AutomataError):
    """Exception raised when the target variable is not found."""

    pass


@register_action
class CodeWritingAction(Action):
    """An concrete action representing written code."""

    BACKWARD_LANGUAGE_MARKER_POSITION = 1
    FORWARD_LANGUAGE_MARKER_POSITION = 0

    # TODO - Consider adding variable name to the action,
    # e.g. if x = OpenAutomataAgent(),
    # and object_type = 'OpenAutomataAgent', object_value_repr = "OpenAutomataAgent(config = ...)",
    # then variable_name = 'x'
    def __init__(
        self,
        object_type: Optional[str],
        object_value_repr: Optional[str] = None,
        object_variable_checks: Optional[List[str]] = None,
        error: Optional[str] = None,
    ):  # sourcery skip: docstrings-for-functions
        if object_variable_checks is None:
            object_variable_checks = []

        self.object_type = object_type
        self.object_value_repr = object_value_repr
        self.object_variable_checks = object_variable_checks
        self.error = error

    def __eq__(self, other):  # sourcery skip: docstrings-for-functions
        if not isinstance(other, CodeWritingAction):
            return False

        if not self.object_type == other.object_type:
            return False

        """
        TODO - Improve __eq__ method to check for object equality
        The code below does not work since the object is a string representation
        The object needs to be parsed and loaded in order for the following below to work
        Check for basic Python types
        basic_types = (int, float, str, list, dict, set, tuple, bool)
        if isinstance(self.object_value_repr, basic_types):
            return self.object_value_repr == other.object_value_repr

        # If not a basic type, perform attribute checks
        return all(
            getattr(self.object_value_repr, variable_check, None)
            == getattr(other.object_value_repr, variable_check, None)
            for variable_check in self.object_variable_checks
        )
        """
        return True

    def __hash__(self):
        return hash(
            (
                json.dumps(self.object_value_repr),
                json.dumps(self.object_type),
            )
        )

    def __repr__(self):
        return f"CodeWritingAction(object_value_repr={self.object_value_repr}, object_type={self.object_type}, error={self.error})"

    def to_payload(self) -> Payload:
        """Converts a CodeWritingAction into a payload for storing."""

        return {
            "type": "CodeWritingAction",
            "object_value_repr": self.object_value_repr or "None",
            "object_type": self.object_type or "None",
            "error": self.error or "None",
        }

    @classmethod
    def from_payload(cls, payload: Payload) -> "CodeWritingAction":
        """Converts a payload CodeWritingAction into underlying payload."""

        object_type = payload["object_type"]
        if not isinstance(object_type, str):
            raise ValueError(
                f"Object types of type={type(object_type)} received, instead of str."
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

        error = payload.get("error")
        if error is not None and not isinstance(error, str):
            raise ValueError(
                f"Object types of type={type(error)} received, instead of str."
            )

        return cls(
            object_value_repr=object_value_repr,
            object_type=object_type,
            object_variable_checks=object_variable_checks,
            error=error,
        )

    @staticmethod
    def _extract_snippet(
        snippet: str, expected_language: str = "python"
    ) -> str:
        """Extracts a code snippet from a markdown string."""

        return snippet.split(f"```{expected_language}")[
            CodeWritingAction.BACKWARD_LANGUAGE_MARKER_POSITION
        ].split("```")[CodeWritingAction.FORWARD_LANGUAGE_MARKER_POSITION]


class CodeWritingEval(AgentEval):
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
            logger.debug(f"Failed to parse code snippet with {e}")
            parsed_snippets = []

        # Clean errors from parsed snippet
        for snippet in parsed_snippets:
            action = CodeWritingAction(
                object_value_repr=snippet.get("value"),
                object_type=snippet.get("type"),
                error=snippet.get("error"),
            )
            actions.append(action)
        return actions

    def _parse_code_snippet(self, raw_content: str) -> List[Dict[str, Any]]:
        """Parses a code snippet and extracts the object value and type at the specified variable."""

        if "```" not in raw_content:
            return []
        # Isolate the exec environment to a separate dictionary
        isolated_locals: Dict[str, Any] = {}
        try:
            code_snippet = CodeWritingAction._extract_snippet(raw_content)
            # Execute the code snippet
            try:
                exec(code_snippet, None, isolated_locals)
            except Exception as e:
                return [
                    {
                        "error": str(
                            CodeExecutionError(
                                f"Error executing code: {str(e)}"
                            )
                        ),
                    }
                ]

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
            raise CodeExecutionError(f"Error executing code: {str(e)}") from e

    def _filter_actions(self, actions: List[Action]) -> List[Action]:
        """Filters out non-CodeWritingActions."""

        return [
            action
            for action in actions
            if isinstance(action, CodeWritingAction)
        ]
