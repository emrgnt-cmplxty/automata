"""Implements an evaluation for code writing ability."""
import logging
from typing import Any, Dict, List, Optional

import jsonpickle

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
        print("self.py_object = ", self.py_object)
        print("other.py_object = ", other.py_object)
        print(
            "self.py_object == other.py_object = ",
            self.py_object == other.py_object,
        )
        print(
            "stringified self.py_object == other.py_object = ",
            str(self.py_object) == str(other.py_object),
        )

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

        print("payload = ", payload)
        if not isinstance(payload["py_object"], (str, dict)):
            raise ValueError(
                f"Object types of type={type(object)} received, instead of str."
            )
        print("payload = ", payload["py_object"])
        print("payload = ", type(payload["py_object"]))
        py_object = jsonpickle.decode(payload["py_object"])
        print("success...")
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

        if not message.content:
            return actions

        # Parse the code snippet to extract set variables and their types
        try:
            parsed_snippets = self._parse_code_snippet(message.content)
            print("parsed_snippets = ", parsed_snippets)
        except Exception as e:
            logger.debug(f"Failed to parse code snippet with {e}")
            parsed_snippets = []

        # Clean errors from parsed snippet
        for snippet in parsed_snippets:
            action = CodeWritingAction(
                py_object=snippet.get("py_object"),
                error=snippet.get("error"),
            )
            actions.append(action)
        print(f"returning actions = {actions}")
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

            targets = [
                isolated_locals.get(target_variable)
                for target_variable in self.target_variables
                if target_variable in isolated_locals
            ]
            if not targets:
                raise VariableNotFoundError(
                    f"Variables '{self.target_variables}' not found in the executed code."
                )
            return [{"py_object": py_object} for py_object in targets]

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
