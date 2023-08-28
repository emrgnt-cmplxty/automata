import os
from typing import Any, Generator, List, Tuple

import pandas as pd

from zero_shot_replication.core import BaseDataset, ProblemType
from zero_shot_replication.core.utils import (
    get_pset_inputs_dir,
    load_file_or_raise,
)
from zero_shot_replication.datasets.leetcode import LeetCodeDataset
from zero_shot_replication.model.base import PromptMode


class LeetCodeMSFTSparksDataset(BaseDataset):
    """A concrete class to provide LeetCode problems for the runner."""

    INPUT_FILE = "full_problems.csv"

    def __init__(self) -> None:
        self.leetcode_dataset = LeetCodeDataset()

    @property
    def raw_prompt(self) -> str:
        """Concrete method to get the raw prompt for LeetCode problems."""
        return self.leetcode_dataset.LEETCODE_EVAL_TEMPLATE

    @property
    def input_paths(self) -> List[str]:
        """Concrete method to get a list over the LeetCode dataset paths"""
        return [
            os.path.join(
                get_pset_inputs_dir(),
                ProblemType.LEETCODE.value.upper(),
                LeetCodeMSFTSparksDataset.INPUT_FILE,
            )
        ]

    @property
    def generator(self) -> Generator[Tuple[str, Any], None, None]:
        """Concrete method to get a generator over the LeetCode problems"""
        problems = load_file_or_raise(self.input_paths[0])
        problems = self.filter_problems_by_question_id(problems)

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

    def get_formatted_prompt(
        self,
        problem: dict,
        prompt_mode: PromptMode = PromptMode.HUMAN_FEEDBACK,
    ) -> str:
        """Concrete method for the formatted prompt for LeetCode problems."""
        return self.raw_prompt.format(
            TASK_PROMPT=problem["raw_content"],
            CODE_SNIPPET=problem["python3_snippet"],
        )

    @staticmethod
    def filter_problems_by_question_id(problems: pd.DataFrame) -> pd.DataFrame:
        """
        Filter the problems dataframe by difficulty and keep the top N_HARD, N_MEDIUM, and N_EASY problems.

        Args:
        - problems (pd.DataFrame): The dataframe containing all problems.

        Returns:
        - pd.DataFrame: A dataframe containing the filtered problems.
        """
        # TODO - Fetch from LC-MSFT dataset.
        id_list = {
            2432,
            2433,
            2434,
            2435,
            2437,
            2438,
            2439,
            2440,
            2441,
            2442,
            2443,
            2444,
            2446,
            2447,
            2448,
            2449,
            2451,
            2452,
            2453,
            2454,
            2455,
            2456,
            2457,
            2458,
            2460,
            2461,
            2462,
            2463,
            2465,
            2466,
            2467,
            2468,
            2469,
            2470,
            2471,
            2472,
            2475,
            2476,
            2477,
            2478,
            2481,
            2482,
            2483,
            2484,
            2485,
            2486,
            2487,
            2488,
            2490,
            2491,
            2492,
            2493,
            2496,
            2497,
            2498,
            2499,
            2500,
            2501,
            2502,
            2503,
            2506,
            2507,
            2508,
            2509,
            2511,
            2512,
            2513,
            2514,
            2515,
            2516,
            2517,
            2518,
            2520,
            2521,
            2522,
            2523,
            2525,
            2526,
            2527,
            2528,
            2529,
            2530,
            2531,
            2532,
        }

        return problems.iloc[
            [
                problem.frontend_question_id in id_list
                for _, problem in problems.iterrows()
            ]
        ]
