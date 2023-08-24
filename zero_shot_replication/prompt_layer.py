"""Turns problems into prompts for the LLM Completion impl."""
from zero_shot_replication.base import ProblemType


class PromptLayer:
    """A class to turn given problems into prompts for the LLM."""

    def __init__(self, problem_type: ProblemType) -> None:
        self.problem_type = problem_type

    def get_prompt(self, problem: dict) -> str:
        """Get a prompt for the given problem."""
        if self.problem_type == ProblemType.HUMAN_EVAL:
            return self._get_human_eval_prompt(problem)
        else:
            raise NotImplementedError("Problem type not implemented.")

    @staticmethod
    def _get_human_eval_prompt(problem: dict) -> str:
        """Get a prompt for a human eval problem."""
        return "This is a test, Return True"
