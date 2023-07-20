from typing import List, Type

from automata.llm.eval.base import Action, CompositeEval, Eval
from automata.llm.eval.metrics import EvaluationMetrics


class EvaluationHarness:
    """A class to evaluate a list of instructions against a list of expected actions."""

    def __init__(self, evals: List[Eval]):
        self.evals = evals

    def evaluate(
        self,
        instructions: List[str],
        expected_actions: List[List[Action]],
        aggregate=True,
    ) -> EvaluationMetrics:
        """Returns the evaluation metrics for the given instructions and expected actions."""
        results = []

        for eval, instruction, actions in zip(
            self.evals, instructions, expected_actions
        ):
            print("actions = ", actions)
            result = eval.generate_eval_result(instruction, actions)
            print("result = ", result)
            results.append(result)

        if aggregate:
            results = [CompositeEval.aggregate_result(results)]
        print("aggregate results = ", results)
        return EvaluationMetrics(results)
