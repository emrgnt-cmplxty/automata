import abc
import logging
from typing import Dict, List, NamedTuple, Type

from automata.agent import AgentProvider
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
        self.agent_provider = agent_provider

    def generate_eval_result(
        self, instructions: str, expected_actions: List[Action]
    ) -> EvalResult:
        """Generates an eval result for a given set of instructions and expected actions."""

        filtered_expected_actions = self._filter_actions(expected_actions)

        agent = self.agent_provider.build_and_run_agent(instructions)
        observed_actions: List[Action] = []

        for message in agent.conversation.messages:
            if extracted_actions := self.extract_action(message):
                observed_actions.extend(extracted_actions)

        match_result: Dict[Action, bool] = {
            action: action in observed_actions
            for action in filtered_expected_actions
        }

        full_match = all(match_result.values())
        extra_actions = [
            action
            for action in observed_actions
            if action not in filtered_expected_actions
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

    @abc.abstractmethod
    def _filter_actions(self, actions: List[Action]) -> List[Action]:
        """Filters a list of actions to only contain actions that are relevant to the eval."""
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
    ) -> EvalResult:
        results = []
        for evaluator_class in self.evaluators:
            evaluator = evaluator_class(self.agent_provider)
            results.append(
                evaluator.generate_eval_result(instructions, expected_actions)
            )
        self.results: List[EvalResult] = results
        return CompositeEval.aggregate_result(results)

    @staticmethod
    def aggregate_result(results: List[EvalResult]) -> EvalResult:
        """Aggregates a list of EvalResult objects into a single result."""

        if not results:
            raise ValueError("No results to aggregate.")

        # Check conversations match across results
        if any(
            result.conversation != results[0].conversation
            for result in results
        ):
            raise ValueError("All conversations must match.")

        # Perform an 'and' operation over all full_match values
        aggregated_full_match = all(result.full_match for result in results)

        # Merge all match_result dictionaries
        aggregated_match_result = {}
        for result in results:
            aggregated_match_result |= result.match_result

        # Concatenate all extra_actions lists
        aggregated_extra_actions = []
        for result in results:
            aggregated_extra_actions.extend(result.extra_actions)

        # Return a new EvalResult object with the aggregated results
        return EvalResult(
            full_match=aggregated_full_match,
            match_result=aggregated_match_result,
            extra_actions=aggregated_extra_actions,
            conversation=results[0].conversation,
        )

    def extract_action(self, message: LLMChatMessage) -> List[Action]:
        """Extracts a list of action from the given message."""
        actions = []
        for evaluator in self.evaluators:
            actions.extend(
                evaluator(self.agent_provider).extract_action(message)
            )
        return actions

    def _filter_actions(self, actions: List[Action]) -> List[Action]:
        raise NotImplementedError(
            "The composite evaluator does not filter actions."
        )
