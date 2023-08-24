"""Generates problems to be run in the runner."""
import json
from typing import Any, Generator, Tuple

from evalplus.data import get_human_eval_plus

from zero_shot_replication.helpers.base import ProblemType


class ProblemGenerator:
    """A class for generating problems for the runner."""

    def __init__(self, problem_type: ProblemType) -> None:
        self.problem_type = problem_type

    def _problem_with_task_id(self, problems: Generator[Any, None, None]) -> Generator[Tuple[str, Any], None, None]:
        """Yield problems with auto-incrementing task_id."""
        self.task_count = 0
        for problem in problems:
            yield (str(self.task_count), problem)
            self.task_count += 1

    @property
    def generator(self) -> Generator[Tuple[str, Any], None, None]:
        """
        Get a generator over the given problems

        Returns events of the form should be of the form:
            Generator[[task_id: str, problem: dict], None None]

        """
        match self.problem_type:
            case ProblemType.HUMAN_EVAL:
                #  Fields on the yielded problem are ['task_id', 'prompt', 'entry_point', 'canonical_solution', 'test', 'contract', 'base_input', 'atol', 'plus_input']
                yield from get_human_eval_plus().items()
            case ProblemType.GSM8K:
                #  Fields on the yielded problem are ['question', 'answer']
                filename = "datasets/inputs/GSM8K/all.jsonl"
                with open(filename, "r", encoding="utf-8") as file:
                    problems = (json.loads(line) for line in file if line)
                    yield from self._problem_with_task_id(problems)
            case _:
                raise NotImplementedError(
                    f"Problem type not implemented for {self.problem_type}."
                )
