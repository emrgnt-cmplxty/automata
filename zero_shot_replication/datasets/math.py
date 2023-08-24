import textwrap
from typing import Any, Generator, List, Tuple

from zero_shot_replication.helpers import BaseDataset


class MATHDataset(BaseDataset):
    """A concrete class to provide MATH problems for the runner."""

    INPUT_FILE = "randomly_sampled_problems.csv"

    MATH_EVAL_TEMPLATE = textwrap.dedent(
        """
    ```markdown
    ### Instruction:
    Solve the following mathematical problem:
    {TASK_PROMPT}

    Ensure your solution is presented in BOXED LATEX format, e.g. `$\\boxed{{YOUR_SOLUTION}}$`.
    """
    )

    @property
    def raw_prompt(self) -> str:
        """Concrete method to get the raw prompt for LeetCode problems."""
        return MATHDataset.MATH_EVAL_TEMPLATE

    @property
    def input_paths(self) -> List[str]:
        """Concrete method to get a list over the LeetCode dataset paths"""
        raise NotImplementedError(
            "MATHDataset input paths needs implementation (probably via glob.glob(*))."
        )

    @property
    def generator(self) -> Generator[Tuple[str, Any], None, None]:
        """Concrete method to get a generator over the MATH problems"""
        raise NotImplementedError(
            "MATHDataset generator needs implementation."
        )

    def get_formatted_prompt(self, problem: dict) -> str:
        """Concrete method the formatted prompt for MATH problems."""
        return self.raw_prompt.format(TASK_PROMPT=problem["problem"])
