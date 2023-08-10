"""Implements an evaluation for code writing ability."""
import logging
import logging.config
from typing import Any, Dict, List, Optional

import jsonpickle

from automata.core.base import AutomataError
from automata.core.utils import get_logging_config
from automata.eval.agent.agent_eval import AgentEval
from automata.eval.eval_base import Action, Payload, register_action
from automata.llm import LLMChatMessage, OpenAIChatMessage

logger = logging.getLogger(__name__)
logging.config.dictConfig(get_logging_config())


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

    def __init__(
        self,
        py_object: Optional[Any],
        error: Optional[str] = None,
    ):  # sourcery skip: docstrings-for-functions
        self.py_object = py_object
        self.error = error

    def __eq__(self, other):  # sourcery skip: docstrings-for-functions
        if not isinstance(other, CodeWritingAction):
            return False
        return self.py_object == other.py_object

    def __hash__(self):
        return hash((jsonpickle.dumps(self.py_object),))

    def __repr__(self):
        return f"CodeWritingAction(py_object={self.py_object}, error={self.error})"

    def to_payload(self) -> Payload:
        """Converts a CodeWritingAction into a payload for storing."""

        return {
            "type": "CodeWritingAction",
            "py_object": str(jsonpickle.encode(self.py_object)),
            "error": self.error or "None",
        }

    @classmethod
    def from_payload(cls, payload: Payload) -> "CodeWritingAction":
        """Converts a payload CodeWritingAction into underlying payload."""

        if not isinstance(payload["py_object"], (str, dict)):
            raise ValueError(
                f"Object types of type={type(object)} received, instead of str."
            )
        # Extract the string from the payload
        json_string = payload["py_object"]

        if not isinstance(json_string, str):
            raise ValueError(
                "Expected a string, but received a non-string object."
            )

        # Replace single quotes with double quotes
        json_string_with_double_quotes = json_string.replace("'", '"')

        # Replace None with null
        json_string_with_double_quotes = (
            json_string_with_double_quotes.replace("None", "null")
        )

        # Decode the corrected JSON string using jsonpickle
        py_object = jsonpickle.decode(json_string_with_double_quotes)

        error = payload.get("error")
        if error is not None and not isinstance(error, str):
            raise ValueError(
                f"Object types of type={type(error)} received, instead of str."
            )

        return cls(
            py_object=py_object,
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

        if (
            not isinstance(message, OpenAIChatMessage)
            or not message.function_call
            or message.function_call.name != "call_termination"
        ):
            return actions

        arguments = message.function_call.arguments

        if "result" not in arguments:
            return actions

        parsed_snippets = self._parse_code_snippet(arguments["result"])

        for snippet in parsed_snippets:
            action = CodeWritingAction(
                py_object=snippet.get("py_object"),
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

            if targets := [
                isolated_locals.get(target_variable)
                for target_variable in self.target_variables
                if target_variable in isolated_locals
            ]:
                return [{"py_object": py_object} for py_object in targets]

            else:
                raise VariableNotFoundError(
                    f"Variables '{self.target_variables}' not found in the executed code."
                )
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
