# Here's a basic implementation of a class to evaluate detailed metrics from an EvalResult.
# For the sake of simplicity, this implementation only includes some basic metrics.
# In a real-world scenario, you would likely want to include more complex metrics,
# and you would probably want to use a library to calculate some of them.

from collections import Counter
from typing import List

from automata.llm.eval.base import EvalResult


class EvaluationMetrics:
    """A class to evaluate detailed metrics from a sequence of EvalResults."""

    def __init__(self, results: List[EvalResult]):
        self.results = results

    def total_actions(self) -> int:
        return sum(len(result.match_result) for result in self.results)

    def total_successful_actions(self) -> int:
        return sum(
            action
            for result in self.results
            for action in result.match_result.values()
        )

    def action_success_rate(self) -> float:
        total_actions = self.total_actions()
        if total_actions == 0:
            return 0
        else:
            return self.total_successful_actions() / total_actions

    def total_extra_actions(self) -> int:
        return sum(len(result.extra_actions) for result in self.results)

    def extra_action_frequency(self) -> Counter:
        all_extra_actions = [
            str(action)
            for result in self.results
            for action in result.extra_actions
        ]
        return Counter(all_extra_actions)

    def successful_actions_frequency(self) -> Counter:
        all_successful_actions = [
            str(action)
            for result in self.results
            for action, success in result.match_result.items()
            if success
        ]
        return Counter(all_successful_actions)

    def failed_actions_frequency(self) -> Counter:
        all_failed_actions = [
            str(action)
            for result in self.results
            for action, success in result.match_result.items()
            if not success
        ]
        return Counter(all_failed_actions)
