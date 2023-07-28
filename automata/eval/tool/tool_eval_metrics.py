from typing import List

from automata.eval.tool.tool_eval import ToolEvalResult


class ToolEvaluationMetrics:
    """A class to evaluate detailed metrics from a sequence of ToolEvalResults."""

    def __init__(self, results: List[ToolEvalResult]):
        self.results = results

    @property
    def total_evaluations(self) -> int:
        """Returns the total number of evaluations."""
        return len(self.results)

    @property
    def total_full_matches(self) -> int:
        """Returns the total number of full matches."""
        return sum(result.is_full_match for result in self.results)

    @property
    def total_partial_matches(self) -> int:
        """Returns the total number of partial matches."""
        return sum(result.is_partial_match for result in self.results)

    @property
    def full_match_rate(self) -> float:
        """Returns the full match rate."""
        return (
            self.total_full_matches / self.total_evaluations
            if self.total_evaluations
            else 0
        )

    @property
    def partial_match_rate(self) -> float:
        """Returns the partial match rate."""
        return (
            self.total_partial_matches / self.total_evaluations
            if self.total_evaluations
            else 0
        )

    def __str__(self) -> str:
        return (
            f"Total Evaluations: {self.total_evaluations}\n"
            f"Full Matches: {self.total_full_matches}\n"
            f"Partial Matches: {self.total_partial_matches}\n"
            f"Full Match Rate: {self.full_match_rate}\n"
            f"Partial Match Rate: {self.partial_match_rate}\n"
        )
