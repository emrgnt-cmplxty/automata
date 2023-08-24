import os
import textwrap
from typing import Any, Generator, List, Tuple

from zero_shot_replication.helpers.base import BaseDataset, ProblemType
from zero_shot_replication.helpers.utils import (
    get_pset_inputs_dir,
    load_file_or_raise,
)


class LeetCodeDataset(BaseDataset):
    """A concrete class to provide LeetCode problems for the runner."""

    INPUT_FILE = "randomly_sampled_problems.csv"

    LEETCODE_EVAL_TEMPLATE = textwrap.dedent(
        """
    ### Instruction:
    Provide a response which completes the following Python coding task:
    {TASK_PROMPT} 


    Make sure your code aligns with the following snippet:

    ```python
    {CODE_SNIPPET}
    ```

    ### Notes: 
    Respond with the entire complete function definition, including a re-stated function definition.
    Use only built-in libraries and numpy, assume no additional imports other than those provided in the problem statement.
    Do not add any comments, be as concise in your code as possible.
    This is a competitive coding problem, pursue the most efficient algorithm possible.
    """
    )

    @property
    def raw_prompt(self) -> str:
        """Concrete method to get the raw prompt for LeetCode problems."""
        return LeetCodeDataset.LEETCODE_EVAL_TEMPLATE

    @property
    def input_paths(self) -> List[str]:
        """Concrete method to get a list over the LeetCode dataset paths"""
        return [
            os.path.join(
                get_pset_inputs_dir(),
                ProblemType.LEETCODE.value.upper(),
                LeetCodeDataset.INPUT_FILE,
            )
        ]

    @property
    def generator(self) -> Generator[Tuple[str, Any], None, None]:
        """Concrete method to get a generator over the LeetCode problems"""
        problems = load_file_or_raise(self.input_paths[0])
        problems.index = [
            f"LeetCode/{int(frontend_question_id)}"
            for frontend_question_id in problems.frontend_question_id.values
        ]

        #  Fields on the yielded problem are:
        # ['Unnamed: 0', 'question_slug', 'question_title', 'frontend_question_id',
        #    'question_id', 'raw_content', 'difficulty', 'paid_only', 'cpp_snippet',
        #    'java_snippet', 'python_snippet', 'python3_snippet', 'c_snippet',
        #    'csharp_snippet', 'javascript_snippet', 'ruby_snippet', 'swift_snippet',
        #    'golang_snippet', 'scala_snippet', 'kotlin_snippet', 'rust_snippet',
        #    'php_snippet', 'typescript_snippet', 'racket_snippet', 'erlang_snippet',
        #    'elixir_snippet', 'dart_snippet', 'react_snippet']
        yield from problems.iterrows()

    def get_formatted_prompt(self, problem: dict) -> str:
        """Concrete method for the formatted prompt for LeetCode problems."""
        return self.raw_prompt.format(
            TASK_PROMPT=problem["raw_content"],
            CODE_SNIPPET=problem["python3_snippet"],
        )
