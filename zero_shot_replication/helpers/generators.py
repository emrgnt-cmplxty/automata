"""Generates problems to be run in the runner."""
import json
from typing import Any, Generator, Tuple

from evalplus.data import get_human_eval_plus

from zero_shot_replication.helpers.base import ProblemType

import os
import json
import random


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

    

    def _get_math_problems(self, level: str = None, randomize: bool = False) -> Generator[Tuple[str, Any], None, None]:
        base_path = "../datasets/inputs/MATH"
        
        all_files = []
        
        # Load all file paths into a list
        for category in os.listdir(base_path):
            category_path = os.path.join(base_path, category)
            if os.path.isdir(category_path):
                for file_name in os.listdir(category_path):
                    file_path = os.path.join(category_path, file_name)
                    all_files.append(file_path)
        
        # Shuffle the list if randomize is True
        if randomize:
            random.shuffle(all_files)
        
        # Iterate over the (potentially shuffled) list
        for file_path in all_files:
            # Load problems from the JSON file
            with open(file_path, 'r') as f:
                problem_details = json.load(f)

                if level is None or problem_details.get('level') == level:
                    yield (os.path.basename(file_path), problem_details)


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
            case ProblemType.MATH:
                # Fields on the yielded problem are ['problem', 'level', 'type', 'solution']
                yield from self._get_math_problems()
            case _:
                raise NotImplementedError(
                    f"Problem type not implemented for {self.problem_type}."
                )
