import abc
import logging
from typing import Dict, List, NamedTuple, Type, List

from automata.agent import Agent, AgentProvider
from automata.config import AgentConfig
from automata.llm.foundation import LLMChatMessage, LLMConversation

logger = logging.getLogger(__name__)


class Action(abc.ABC):
    """An arbitrary action to be taken by an LLM, like an OpenAI function call"""

    pass


class EvalResult(NamedTuple):
    """A concrete class to represent the result of an eval."""

    full_match: bool
    match_result: Dict[Action, bool]
    extra_actions: List[Action]
    conversation: LLMConversation


class Eval(abc.ABC):
    """Abstract class for evaluating an LLMs performance"""

    def __init__(
        self,
        agent_provider: AgentProvider,
        *args,
        **kwargs,
    ):
        self.config = config
        self.agent_provider = agent_provider

    def generate_eval_result(
        self, instructions: str, expected_actions: List[Action]
    ) -> EvalResult:
        """Generates an eval result for a given set of instructions and expected actions."""
        agent = self.agent_provider.build_and_run_agent(instructions)
        observed_actions: List[Action] = []

        for message in agent.conversation.messages:
            if extracted_actions := self.extract_action(message):
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
    def extract_action(self, message: LLMChatMessage) -> List[Action]:
        """Extracts a list of action from the given message."""
        pass


class CompositeEval(Eval):
    def __init__(
        self,
        agent_provider: AgentProvider,
        evaluators: List[Type[Eval]],
        *args,
        **kwargs,
    ):
        super().__init__(agent_provider, *args, **kwargs)
        self.evaluators = evaluators

    def generate_eval_results(
        self, instructions: str, expected_actions: List[Action]
    ) -> List[EvalResult]:
        results = []
        for evaluator_class in self.evaluators:
            evaluator = evaluator_class(self.agent_provider)
            results.append(
                evaluator.generate_eval_result(instructions, expected_actions)
            )
        return results

    def extract_action(self, message: LLMChatMessage) -> List[Action]:
        """Extracts a list of action from the given message."""
        actions = []
        for evaluator in self.evaluators:
            actions.extend(
                evaluator(self.config, self.agent_provider).extract_action(
                    message
                )
            )
        return actions
