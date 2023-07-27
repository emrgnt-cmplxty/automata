"""Generates a composite evaluator from a list of evaluators."""
from typing import Dict, List, Union

from automata.eval.agent.agent_eval import AgentEval, AgentEvalResult
from automata.eval.base import Action, Eval
from automata.eval.tool.tool_eval import ToolEval
from automata.llm.foundation import LLMChatMessage
from automata.tasks import AutomataTask, AutomataTaskExecutor


def aggregate_agent_result(results: List[AgentEvalResult]) -> AgentEvalResult:
    """Aggregates a list of EvalResult objects into a single result."""

    if not results:
        raise ValueError("No results to aggregate.")

    # Check conversations match across results
    if any(result.session_id != results[0].session_id for result in results):
        raise ValueError("All session ids must match.")

    if any(result.run_id != results[0].run_id for result in results):
        raise ValueError("All run ids must match.")

    # Merge all match_result dictionaries
    aggregated_match_results: Dict[Action, bool] = {}
    for result in results:
        aggregated_match_results |= result.match_results

    # Concatenate all extra_actions lists
    aggregated_extra_actions = []
    for result in results:
        aggregated_extra_actions.extend(result.extra_actions)

    # Return a new EvalResult object with the aggregated results
    return AgentEvalResult(
        match_results=aggregated_match_results,
        extra_actions=aggregated_extra_actions,
        session_id=results[0].session_id,
        run_id=results[0].run_id,
    )


def check_eval_uniqueness(
    evaluator_classes: Union[List[Eval], List[AgentEval], List[ToolEval]]
) -> bool:
    """Checks that all evaluators are of different types."""

    if len(evaluator_classes) != len(set(evaluator_classes)):
        raise ValueError("All evaluators must be of different types.")

    return True


class AgentEvalComposite(Eval):
    """Creates a composite evaluator from a list of evaluator classes."""

    def __init__(
        self,
        evaluators: List[AgentEval],
        *args,
        **kwargs,
    ):  # sourcery skip: docstrings-for-functions
        check_eval_uniqueness(evaluators)
        super().__init__(*args, **kwargs)

        self.agent_evaluators: List[AgentEval] = []
        for evaluator in evaluators:
            if not isinstance(evaluator, AgentEval):
                raise ValueError("Evaluators must be of type AgentEval.")
            self.agent_evaluators.append(evaluator)

    def generate_eval_result(
        self,
        task: AutomataTask,
        expected_actions: List[Action],
        executor: AutomataTaskExecutor,
        *args,
        **kwargs,
    ) -> AgentEvalResult:
        """Generates an eval result for a given set of instructions and expected actions."""

        agent = executor.execute(task)

        results: List[AgentEvalResult] = []
        for evaluator in self.agent_evaluators:
            result = evaluator.process_result(
                expected_actions,
                agent.conversation.messages,
                session_id=agent.session_id,
                run_id=kwargs.get("run_id"),
            )
            if not isinstance(result, AgentEvalResult):
                raise ValueError("Evaluators must return an AgentEvalResult.")
            results.append(result)
        return aggregate_agent_result(results)

    def extract_action(self, message: LLMChatMessage) -> List[Action]:
        """Extracts a list of action from the given message."""

        actions = []
        for evaluator in self.agent_evaluators:
            actions.extend(evaluator.extract_action(message))
        return actions

    def _filter_actions(self, actions: List[Action]) -> List[Action]:
        """Filters a list of actions to only contain actions that are relevant to the eval."""

        raise NotImplementedError(
            "The composite evaluator does not filter actions."
        )
