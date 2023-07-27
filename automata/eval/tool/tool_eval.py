import json
from abc import abstractmethod
from typing import Any, Dict, List, Optional

from automata.eval.eval_base import (
    Action,
    Eval,
    EvalResult,
    Payload,
    parse_action_from_payload,
)
from automata.llm.llm_base import LLMChatMessage
from automata.tasks import AutomataTask


class ToolEval(Eval):
    """Abstract class for evaluating tools' performance."""

    def generate_eval_result(
        self,
        task: AutomataTask,
        expected_actions: List[Action],
        executor: Any,
        *args,
        **kwargs,
    ) -> EvalResult:
        """Generates an eval result for a given set of instructions and expected actions."""
        # TODO - Provide implementation
        raise NotImplementedError

    def process_result(
        self,
        expected_actions: List[Action],
        process_input: Any,
        *args,
        **kwargs,
    ) -> EvalResult:
        """Processes the result of an evaluation."""
        raise NotImplementedError

    @abstractmethod
    def extract_action(self, message: LLMChatMessage) -> List[Action]:
        """Extracts a list of action from the given message."""
        pass

    def _filter_actions(self, actions: List[Action]) -> List[Action]:
        """In the context of ToolEval, there's only one action to be expected.
        Therefore, there's no need to filter actions."""
        return actions


class ToolEvalResult(EvalResult):
    """A concrete class to represent the result of a tool eval."""

    def __init__(
        self,
        expected_action: Optional[Action],
        observed_action: Optional[Action],
        *args,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        self.expected_action = expected_action
        self.observed_action = observed_action

    @property
    def is_full_match(self) -> bool:
        """Checks if the result is a full match."""
        return self.expected_action == self.observed_action

    @property
    def is_partial_match(self) -> bool:
        """Checks if the result is a partial match."""
        return self.is_full_match or self.expected_action is None

    def is_match(self) -> bool:
        """Checks if the result is a match."""
        return self.expected_action == self.observed_action

    def get_details(self) -> Dict[str, Optional[Action]]:
        """Gets the details of the result."""
        return {
            "expected_action": self.expected_action,
            "observed_action": self.observed_action,
        }

    def get_extra_info(self) -> Dict[str, Any]:
        """Gets the extra info of the result."""
        return {}

    def to_payload(self) -> Payload:
        """Converts the evaluation result to a dictionary (or other serializable format)."""
        return {
            "expected_action": json.dumps(self.expected_action.to_payload())
            if self.expected_action
            else "None",
            "observed_action": json.dumps(self.observed_action.to_payload())
            if self.observed_action
            else "None",
        }

    @classmethod
    def from_payload(cls, payload: Payload) -> "ToolEvalResult":
        """Creates an evaluation result from a dictionary (or other serialized format)."""

        if not isinstance(payload["expected_action"], str):
            raise ValueError("Expected action must be a string.")

        if not isinstance(payload["observed_action"], str):
            raise ValueError("Observed action must be a string.")

        expected_action = parse_action_from_payload(
            json.loads(payload["expected_action"])
        )
        observed_action = parse_action_from_payload(
            json.loads(payload["observed_action"])
        )

        return cls(
            expected_action=expected_action, observed_action=observed_action
        )
