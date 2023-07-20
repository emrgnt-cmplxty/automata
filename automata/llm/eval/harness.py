from typing import List
from automata.llm.eval.base import Action, Eval
from automata.llm.eval.metrics import EvaluationMetrics


class EvaluationHarness:
    """A class to evaluate a list of instructions against a list of expected actions."""

    def __init__(self, eval_class, agent_config):
        self.eval_class = eval_class
        self.agent_config = agent_config

    def evaluate(
        self, instructions: List[str], expected_actions: List[List[Action]]
    ) -> EvaluationMetrics:
        results = []

        for instruction, actions in zip(instructions, expected_actions):
            eval_instance = self.eval_class(self.agent_config)
            result = eval_instance.generate_eval_result(instruction, actions)
            results.append(result)

        return EvaluationMetrics(results)
