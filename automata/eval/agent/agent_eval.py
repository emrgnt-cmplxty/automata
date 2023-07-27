import json
from typing import Any, Dict, List, Optional, Sequence

from automata.eval.eval_base import (
    Action,
    Eval,
    EvalResult,
    Payload,
    parse_action_from_payload,
)
from automata.llm.llm_base import LLMChatMessage
from automata.tasks import AutomataTask, AutomataTaskExecutor


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
