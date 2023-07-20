import json
from typing import Any, Dict, List, Optional

from automata.llm.eval.base import Action, Eval, logger
from automata.llm.foundation import LLMChatMessage


class CodeExecutionError(Exception):
    """Exception raised when there's an error executing the code."""

    pass


class VariableNotFoundError(CodeExecutionError):
    """Exception raised when the target variable is not found."""

    pass


class CodeWritingAction(Action):
    """An concrete action representing written code."""

    def __init__(
        self,
        object_types: str,
        object_value: Any = None,
        md_code_snippet: Optional[str] = None,
        object_variable_checks: Optional[List[str]] = None,
    ):
        if object_variable_checks is None:
            object_variable_checks = []

        self.md_code_snippet = md_code_snippet
        self.object_types = object_types
        self.object_value = object_value
        self.object_variable_checks = object_variable_checks

    def __eq__(self, other):
        if not isinstance(other, CodeWritingAction):
            return False

        if self.object_types != other.object_types:
            return False

        # Check for basic Python types
        basic_types = (int, float, str, list, dict, set, tuple, bool)
        if isinstance(self.object_value, basic_types):
            return self.object_value == other.object_value

        # If not a basic type, perform attribute checks
        return all(
            getattr(self.object_value, variable_check, None)
            == getattr(other.object_value, variable_check, None)
            for variable_check in self.object_variable_checks
        )

    def __hash__(self):
        return hash(
            (
                self.md_code_snippet,
                json.dumps(self.object_value),
                json.dumps(self.object_types),
            )
        )

    def __str__(self):
        return f"CodeWritingAction(md_code_snippet={self.md_code_snippet}, object_value={self.object_value}, object_types={self.object_types})"

    @staticmethod
    def _extract_snippet(
        snippet: str, expected_language: str = "python"
    ) -> str:
        """Extracts a code snippet from a markdown string."""
        return snippet.split(f"```{expected_language}")[1].replace("```", "")


class CodeWritingEval(Eval):
    """A class for evaluating an LLM's code writing ability."""

    def extract_action(self, message: LLMChatMessage) -> List[Action]:
        """Extracts the coding action explicitly"""
        actions: List[Action] = []

        if not message.content:
            return actions

        md_code_snippet = (
            message.content.split("```python")[1]
            if "```python" in message.content
            else None
        )

        # Parse the code snippet to extract set variables and their types
        parsed_snippets = self._parse_code_snippet(message.content)

        # Clean errors from parsed snippet
        for snippet in parsed_snippets:
            if "error" in snippet:
                logger.error(f"Error parsing code snippet: {snippet['error']}")
                parsed_snippets.remove(snippet)

            action = CodeWritingAction(
                md_code_snippet=md_code_snippet,
                object_value=snippet["value"],
                object_types=snippet["type"],
            )
            actions.append(action)
        return actions

    @staticmethod
    def _parse_code_snippet(
        raw_content, target_variables: List[str] = ["x"]
    ) -> List[Dict[str, Any]]:
        """Parses a code snippet and extracts the object value and type at the specified variable."""

        # Isolate the exec environment to a separate dictionary
        isolated_locals: Dict[str, Any] = {}

        try:
            code_snippet = CodeWritingAction._extract_snippet(raw_content)
            # Execute the code snippet
            exec(code_snippet, None, isolated_locals)
            target_values = [
                isolated_locals.get(target_variable)
                for target_variable in target_variables
            ]
            if target_values is None:
                raise VariableNotFoundError(
                    f"Variables '{target_variables}' not found in the executed code."
                )
            return [
                {"value": target_value, "type": type(target_value).__name__}
                for target_value in target_values
            ]

        except Exception as e:
            # If there's an error executing the code, return that.
            raise CodeExecutionError(f"Error executing code: {str(e)}")
