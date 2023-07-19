import abc
import json
import logging
from typing import Any, Dict, List, NamedTuple, Optional

from automata.agent import Agent
from automata.config import AgentConfig
from automata.llm.foundation import LLMChatMessage, LLMConversation

logger = logging.getLogger(__name__)


class Action(abc.ABC):
    """An arbitrary action to be taken by an LLM, like an OpenAI function call"""

    pass


class CodeWritingAction(Action):
    """An action represented by writing a code snippet."""

    def __init__(
        self,
        object_type: str,
        object_value: Any = None,
        md_code_snippet: Optional[str] = None,
        object_variable_checks: Optional[List[str]] = None,
    ):
        if object_variable_checks is None:
            object_variable_checks = []

        self.md_code_snippet = md_code_snippet
        self.object_type = object_type
        self.object_value = object_value
        self.object_variable_checks = object_variable_checks

    def __eq__(self, other):
        if not isinstance(other, CodeWritingAction):
            return False

        if self.object_type != other.object_type:
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
                json.dumps(self.object_type),
            )
        )

    def __str__(self):
        return f"CodeWritingAction(md_code_snippet={self.md_code_snippet}, object_value={self.object_value}, object_type={self.object_type})"

    @staticmethod
    def _cleanup_snippet(snippet) -> str:
        return snippet.split("```python")[1].replace("```", "")


class EvalResult(NamedTuple):
    """
    A class to represent the result of an eval.
    """

    full_match: bool
    match_result: Dict[Action, bool]
    extra_actions: List[Action]
    conversation: LLMConversation


class Eval(abc.ABC):
    """Abstract class for evaluating an LLMs performance"""

    def __init__(self, config: AgentConfig, *args, **kwargs):
        self.config = config

    def generate_eval_result(
        self, instructions: str, expected_actions: List[Action]
    ) -> EvalResult:
        agent = self._build_and_run_agent(instructions)
        observed_actions: List[Action] = []

        for message in agent.conversation.messages:
            if extracted_actions := self._extract_action(message):
                observed_actions.extend(extracted_actions)

        match_result: Dict[Action, bool] = {
            action: action in observed_actions for action in expected_actions
        }

        full_match = all(match_result.values())
        extra_actions = [
            action
            for action in observed_actions
            if action not in expected_actions
        ]

        return EvalResult(
            full_match=full_match,
            match_result=match_result,
            extra_actions=extra_actions,
            conversation=agent.conversation,
        )

    @abc.abstractmethod
    def _build_and_run_agent(self, instructions: str) -> Agent:
        pass

    @abc.abstractmethod
    def _extract_action(self, message: LLMChatMessage) -> List[Action]:
        pass


class CodeWritingEval(Eval):
    """A class for evaluating an LLM's code writing ability."""

    def _extract_action(self, message: LLMChatMessage) -> List[Action]:
        """Extract the coding action"""
        # TODO - Think of a cleaner, more modular way to handle md snippet extraction
        # TODO - Think of a way to set target_variable more intelligently

        actions: List[Action] = []
        md_code_snippet = (
            message.content.split("```python")[1]
            if "```python" in message
            else None
        )

        # Parse the code snippet to extract set variables and their types
        parsed_snippet = self._parse_code_snippet(message.content)
        if "error" in parsed_snippet:
            logger.error(
                f"Error parsing code snippet: {parsed_snippet['error']}"
            )
            return actions

        action = CodeWritingAction(
            md_code_snippet=md_code_snippet,
            object_value=parsed_snippet["value"],
            object_type=parsed_snippet["type"],
        )
        actions.append(action)
        return actions

    @staticmethod
    def _parse_code_snippet(
        raw_content, target_variable="x"
    ) -> Dict[str, str]:
        """Parses a code snippet and extracts the object value and type at the specified variable."""

        # Isolate the exec environment to a separate dictionary
        isolated_locals: Dict[str, Any] = {}

        try:
            code_snippet = CodeWritingAction._cleanup_snippet(raw_content)
            # Execute the code snippet
            exec(code_snippet, None, isolated_locals)
            target_value = isolated_locals[target_variable]
            return {"value": target_value, "type": type(target_value).__name__}

        except Exception as e:
            # If there's an error executing the code, return that.
            return {"error": str(e)}
