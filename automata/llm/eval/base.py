import abc
import logging
from typing import Dict, List, NamedTuple

from automata.agent import Agent
from automata.config import AgentConfig
from automata.llm.foundation import LLMChatMessage

logger = logging.getLogger(__name__)


class Action(abc.ABC):
    """An arbitrary action to be taken by an LLM, like an OpenAI function call"""

    pass


class EvalResult(NamedTuple):
    """
    A class to represent the result of an eval.
    """

    full_match: bool
    match_result: Dict[Action, bool]
    extra_actions: List[Action]


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
        )

    @abc.abstractmethod
    def _build_and_run_agent(self, instructions: str) -> Agent:
        pass

    @abc.abstractmethod
    def _extract_action(self, message: LLMChatMessage) -> List[Action]:
        pass
