import os
import textwrap
from typing import Any, Generator, List, Tuple

import pandas as pd

from zero_shot_replication.helpers import BaseDataset, ProblemType
from zero_shot_replication.helpers.utils import (
    get_pset_inputs_dir,
    load_file_or_raise,
)


class MATHDataset(BaseDataset):
    """A concrete class to provide MATH problems for the runner."""

    INPUT_FILE = "../../psets/MATH/MATH_dataset_full_testing.csv"

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
        """Concrete method to get the raw prompt for MATH problems."""
        return MATHDataset.MATH_EVAL_TEMPLATE

    @property
    def input_paths(self) -> List[str]:
        """Concrete method to get a list over the MATH dataset paths."""
        return [
            os.path.join(
                get_pset_inputs_dir(),
                ProblemType.MATH.value.upper(),
                MATHDataset.INPUT_FILE,
            )
        ]

    @property
    def generator(self) -> Generator[Tuple[str, Any], None, None]:
        """Concrete method to get a generator over the MATH problems."""
        # Load the dataset using the utility function
        problems = load_file_or_raise(self.input_paths[0])

        # Iterate over each row in the dataframe
        for index, problem in problems.iterrows():
            # Convert the row to a dictionary and yield
            yield f"MATH/{int(index)}", problem.to_dict()

    def get_formatted_prompt(self, problem: dict) -> str:
        """Concrete method to get the formatted prompt for MATH problems."""
        return self.raw_prompt.format(TASK_PROMPT=problem["problem"])
