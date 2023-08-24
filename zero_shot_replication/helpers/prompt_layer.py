"""Turns problems into prompts for the LLM Completion impl."""
from zero_shot_replication.helpers.base import HUMAN_EVAL_TEMPLATE, MATH_TEMPLATE, ProblemType


class PromptLayer:
    """A class to turn given problems into prompts for the LLM."""

    def __init__(self, problem_type: ProblemType) -> None:
        self.problem_type = problem_type

    def get_prompt(self, problem: dict) -> str:
        """Get a prompt for the given problem."""
        match self.problem_type:
            case ProblemType.HUMAN_EVAL:
                return self._get_human_eval_prompt(problem)
            case ProblemType.GSM8K:
                return self._get_GSM8K_prompt(problem)
            case ProblemType.MATH:
                return self._get_math_prompt(problem)
            case _:
                raise NotImplementedError("Problem type not implemented.")

    @staticmethod
    def _get_human_eval_prompt(problem: dict) -> str:
        """Get a prompt for a human eval problem."""
        return HUMAN_EVAL_TEMPLATE.format(CODE_PROMPT=problem["prompt"])    

    @staticmethod
    def _get_GSM8K_prompt(problem: dict) -> str:
        # do zero shot
        return problem.get("question", None)

    @staticmethod
    def _get_math_prompt(problem: dict) -> str:
        return MATH_TEMPLATE.format(TASK_PROMPT=problem["problem"])