"""A module for implementing evaluation metrics."""
from collections import Counter
from typing import List, Optional

from automata.eval.agent.agent_eval import AgentEvalResult


class AgentEvaluationMetrics:
    """A class to evaluate detailed metrics from a sequence of EvalResults."""

    def __init__(self, results: List[AgentEvalResult]):
        # sourcery skip: docstrings-for-functions
        self.results = results
        self._total_actions: Optional[int] = None
        self._total_successful_actions: Optional[int] = None
        self._total_full_matches: Optional[int] = None
        self._total_partial_matches: Optional[int] = None
        self._total_extra_actions: Optional[int] = None
        self._partial_match_success_rate: Optional[float] = None
        self._full_match_success_rate: Optional[float] = None
        self._action_success_rate: Optional[float] = None
        self._extra_action_frequency: Optional[Counter[str]] = None
        self._successful_actions_frequency: Optional[Counter[str]] = None
        self._failed_actions_frequency: Optional[Counter[str]] = None

    def __str__(self) -> str:
        return (
            f"Total Actions: {self.total_actions}\n"
            f"Successful Actions: {self.total_successful_actions}\n"
            f"Full Matches: {self.total_full_matches}\n"
            f"Partial Matches: {self.total_partial_matches}\n"
            f"Extra Actions: {self.total_extra_actions}\n"
            f"Partial Match Success Rate: {self.partial_match_rate}\n"
            f"Full Match Success Rate: {self.full_match_rate}\n"
            f"Action Success Rate: {self.action_success_rate}\n"
        )

    @property
    def total_full_matches(self) -> int:
        """Returns the total number of full matches."""

        if self._total_full_matches is None:
            self._total_full_matches = sum(
                result.is_full_match for result in self.results
            )
        return self._total_full_matches

    @property
    def total_partial_matches(self) -> int:
        """Returns the total number of full matches."""

        if self._total_partial_matches is None:
            self._total_partial_matches = sum(
                result.is_partial_match for result in self.results
            )
        return self._total_partial_matches

    @property
    def total_actions(self) -> int:
        """Returns the total number of actions."""

        if self._total_actions is None:
            self._total_actions = sum(
                len(result.match_results) for result in self.results
            )
        return self._total_actions

    @property
    def total_successful_actions(self) -> int:
        """Returns the total number of successful actions."""

        if self._total_successful_actions is None:
            self._total_successful_actions = sum(
                action
                for result in self.results
                for action in result.match_results.values()
            )
        return self._total_successful_actions

    @property
    def full_match_rate(self) -> float:
        """Returns the full match rate."""

        if self._full_match_success_rate is None:
            total_results = len(self.results)
            if total_results == 0:
                self._full_match_success_rate = 0
            else:
                self._full_match_success_rate = (
                    self.total_full_matches / total_results
                )
        return self._full_match_success_rate

    @property
    def partial_match_rate(self) -> float:
        """Returns the full match rate."""

        if self._partial_match_success_rate is None:
            total_results = len(self.results)
            if total_results == 0:
                self._partial_match_success_rate = 0
            else:
                self._partial_match_success_rate = (
                    self.total_partial_matches / total_results
                )
        return self._partial_match_success_rate

    @property
    def action_success_rate(self) -> float:
        """Returns the action success rate."""

        if self._action_success_rate is None:
            total_actions = self.total_actions
            if total_actions == 0:
                self._action_success_rate = 0
            else:
                self._action_success_rate = (
                    self.total_successful_actions / total_actions
                )
        return self._action_success_rate

    @property
    def total_extra_actions(self) -> int:
        """Returns the total number of extra actions."""

        if self._total_extra_actions is None:
            self._total_extra_actions = sum(
                len(result.extra_actions) for result in self.results
            )
        return self._total_extra_actions

    @property
    def extra_action_frequency(self) -> Counter:
        """Returns the frequency of extra actions."""

        if self._extra_action_frequency is None:
            all_extra_actions = [
                str(action)
                for result in self.results
                for action in result.extra_actions
            ]
            self._extra_action_frequency = Counter(all_extra_actions)
        return self._extra_action_frequency

    @property
    def successful_actions_frequency(self) -> Counter:
        """Returns the frequency of successful actions."""

        if self._successful_actions_frequency is None:
            all_successful_actions = [
                str(action)
                for result in self.results
                for action, success in result.match_results.items()
                if success
            ]
            self._successful_actions_frequency = Counter(
                all_successful_actions
            )
        return self._successful_actions_frequency

    @property
    def failed_actions_frequency(self) -> Counter:
        """Returns the frequency of failed actions."""

        if self._failed_actions_frequency is None:
            all_failed_actions = [
                str(action)
                for result in self.results
                for action, success in result.match_results.items()
                if not success
            ]
            self._failed_actions_frequency = Counter(all_failed_actions)
        return self._failed_actions_frequency
