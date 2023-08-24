"""Generates problems to be run in the runner."""
from typing import Any, Generator, Tuple

from evalplus.data import get_human_eval_plus

from zero_shot_replication.base import ProblemType


class ProblemGenerator:
    """A class for generating problems for the runner."""

    def __init__(self, problem_type: ProblemType) -> None:
        self.problem_type = problem_type

    @property
    def generator(self) -> Generator[Tuple[str, Any], None, None]:
        """
        Get a generator over the given problems

        Returns events of the form should be of the form:
            Generator[task_id: str, problem: dict
            problem: dict

        """
        if self.problem_type == ProblemType.HUMAN_EVAL:
            #  Fields on the yielded problem are ['task_id', 'prompt', 'entry_point', 'canonical_solution', 'test', 'contract', 'base_input', 'atol', 'plus_input']
            yield from get_human_eval_plus().items()
        else:
            raise NotImplementedError("Problem type not implemented.")
