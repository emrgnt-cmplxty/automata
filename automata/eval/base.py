import json
import logging
import uuid
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Sequence, Union

from automata.llm.foundation import LLMChatMessage
from automata.tasks import AutomataTask, AutomataTaskExecutor

logger = logging.getLogger(__name__)

Payload = Dict[str, Union[List[str], str, Dict[str, str]]]


def parse_action_from_payload(payload: Payload) -> "Action":
    """Parses out the corresponding actiopn from a raw dictionary."""

    action_type = payload.pop("type")
    if action_type == "CodeWritingAction":
        from automata.eval.code_writing import CodeWritingAction

        return CodeWritingAction.from_payload(payload)
    elif action_type == "OpenAIFunctionCallAction":
        from automata.eval.eval_providers import OpenAIFunctionCallAction

        return OpenAIFunctionCallAction.from_payload(payload)

    else:
        raise ValueError(f"Unknown action type: {payload['type']}")


class Action(ABC):
    """An arbitrary action to be taken by an LLM, like an OpenAI function call"""

    @abstractmethod
    def to_payload(self) -> Payload:
        """Converts the Action to a dictionary."""
        pass

    @staticmethod
    @abstractmethod
    def from_payload(dct: Payload) -> "Action":
        """Creates an Action from a dictionary."""
        pass


class EvalResult(ABC):
    """An abstract class to represent the result of an evaluation."""

    def __init__(self, *args, **kwargs):
        # TODO - Add tests for run_id
        self.run_id = kwargs.get("run_id") or str(uuid.uuid4())
        if not isinstance(self.run_id, str):
            raise ValueError("run_id must be a string.")

    @property
    @abstractmethod
    def is_full_match(self) -> bool:
        """Indicates whether the evaluation was a full match."""

    @property
    @abstractmethod
    def is_partial_match(self) -> bool:
        """Indicates whether the evaluation was a partial match."""

    @abstractmethod
    def get_details(self) -> Dict[str, Any]:
        """Returns a dictionary with detailed information about the evaluation."""

    @abstractmethod
    def get_extra_info(self) -> Dict[str, Action]:
        """Returns a dictionary with extra information about the evaluation."""

    @abstractmethod
    def to_payload(self) -> Payload:
        """Converts the evaluation result to a dictionary (or other serializable format)."""

    @classmethod
    @abstractmethod
    def from_payload(cls, payload: Payload) -> "EvalResult":
        """Creates an evaluation result from a dictionary (or other serialized format)."""


class AgentEvalResult(EvalResult):
    """A concrete class to represent the result of an agent eval."""

    def __init__(
        self,
        match_results: Dict[Action, bool],
        extra_actions: List[Action],
        session_id: Optional[str],
        *args,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        self.match_results = match_results
        self.extra_actions = extra_actions
        self.session_id = session_id

    def __repr__(self) -> str:
        return f"AgentEvalResult(match_results={self.match_results}, extra_actions={self.extra_actions}, session_id={self.session_id}, run_id={self.run_id})"

    @property
    def is_full_match(self) -> bool:
        """Checks if the result is a full match."""
        return all(self.match_results.values())

    @property
    def is_partial_match(self) -> bool:
        """Checks if the result is a partial match."""
        return any(self.match_results.values())

    def get_details(self) -> Dict[str, Any]:
        """Gets the details of the result."""
        return {
            str(action): result
            for action, result in self.match_results.items()
        }

    def get_extra_info(self) -> Dict[str, Any]:
        """Gets the extra info of the result."""
        return {
            "extra_actions": [str(action) for action in self.extra_actions]
        }

    def to_payload(self) -> Payload:
        """Converts the result to a dictionary."""

        match_results = {
            json.dumps(action.to_payload()): str(result)
            for action, result in self.match_results.items()
        }
        extra_actions = [
            json.dumps(action.to_payload()) for action in self.extra_actions
        ]

        return {
            "match_results": match_results,
            "extra_actions": extra_actions,
        }

    @classmethod
    def from_payload(cls, payload: Payload) -> "AgentEvalResult":
        """Creates an evaluation result from a dictionary (or other serialized format)."""

        matches = payload["match_results"]
        if not isinstance(matches, dict) or not all(
            isinstance(item, str) for item in matches.keys()
        ):
            raise ValueError(
                f"An invalid match result was encountered in {matches}"
            )

        match_results = {
            parse_action_from_payload(json.loads(action)): result == "True"
            for action, result in matches.items()
        }

        extra_actions = [
            parse_action_from_payload(json.loads(action))
            for action in payload["extra_actions"]
        ]

        session_id = payload.get("session_id")
        if session_id is not None and not isinstance(session_id, str):
            raise ValueError(
                f"Invalid session_id ({session_id}) was observed."
            )
        run_id = payload.get("run_id")

        return cls(
            match_results=match_results,
            extra_actions=extra_actions,
            session_id=session_id,
            run_id=run_id,
        )


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


class Eval(ABC):
    """Abstract class for evaluating an LLMs performance."""

    @abstractmethod
    def __init__(
        self,
        *args,
        **kwargs,
    ):
        pass

    @abstractmethod
    def generate_eval_result(
        self,
        task: AutomataTask,
        expected_actions: List[Action],
        executor: Any,
        *args,
        **kwargs,
    ) -> EvalResult:
        """Generates an eval result for a given set of instructions and expected actions."""
        pass

    @abstractmethod
    def extract_action(self, message: LLMChatMessage) -> List[Action]:
        """Extracts a list of action from the given message."""
        pass

    @abstractmethod
    def _filter_actions(self, actions: List[Action]) -> List[Action]:
        """Filters a list of actions to only contain actions that are relevant to the eval."""
        pass


class AgentEval(Eval):
    """Abstract class for evaluating an LLMs performance."""

    def generate_eval_result(
        self,
        task: AutomataTask,
        expected_actions: List[Action],
        executor: AutomataTaskExecutor,
        *args,
        **kwargs,
    ) -> EvalResult:
        """Generates an eval result for a given set of instructions and expected actions."""

        agent = executor.execute(task)

        return self.process_result(
            expected_actions,
            agent.conversation.messages,
            session_id=agent.session_id,
        )

    def process_result(
        self,
        expected_actions: List[Action],
        process_input: Sequence[LLMChatMessage],
        *args,
        **kwargs,
    ) -> EvalResult:
        """Processes the result of an evaluation."""

        if "session_id" not in kwargs:
            raise ValueError("session_id must be provided.")

        session_id = kwargs["session_id"]
        run_id = kwargs.get("run_id")

        filtered_expected_actions = self._filter_actions(expected_actions)
        observed_actions: List[Action] = []
        for message in process_input:
            if extracted_actions := self.extract_action(message):
                observed_actions.extend(extracted_actions)

        match_results: Dict[Action, bool] = {
            action: action in observed_actions
            for action in filtered_expected_actions
        }

        extra_actions = [
            action
            for action in observed_actions
            if action not in filtered_expected_actions
        ]

        return AgentEvalResult(
            match_results=match_results,
            extra_actions=extra_actions,
            session_id=session_id,
            run_id=run_id,
        )


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
        # if len(expected_actions) == 0:
        # ...
        # elif len(expected_actions) == 1:
        # ...
        # else:
        # raise ValueError("Expected actions must be of length 0 or 1.")...
        # return ToolEvalResult(
        #     expected_action=expected_action,
        #     observed_action=observed_action,
        # )
        # TODO - Provide implementation
        raise NotImplementedError

    @abstractmethod
    def extract_action(self, message: LLMChatMessage) -> List[Action]:
        """Extracts a list of action from the given message."""
        pass

    def _filter_actions(self, actions: List[Action]) -> List[Action]:
        """In the context of ToolEval, there's only one action to be expected.
        Therefore, there's no need to filter actions."""
        return actions
