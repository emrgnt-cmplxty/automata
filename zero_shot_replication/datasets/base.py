from typing import Optional

from zero_shot_replication.helpers.base import BaseDataset, ProblemType


def get_dataset(problem_type: ProblemType) -> BaseDataset:
    """Get the dataset which corresponds to a problem type."""

    dataset: Optional[BaseDataset] = None

    match problem_type:
        case ProblemType.HUMAN_EVAL:
            from zero_shot_replication.datasets.human_eval import (
                HumanEvalDataset,
            )

            dataset = HumanEvalDataset()
        case ProblemType.LEETCODE:
            from zero_shot_replication.datasets.leetcode import LeetCodeDataset

            dataset = LeetCodeDataset()
        case ProblemType.LEETCODE_MSFT_SPARKS:
            from zero_shot_replication.datasets.leetcode_msft_sparks import (
                LeetCodeMSFTSparksDataset,
            )

            dataset = LeetCodeMSFTSparksDataset()
        case ProblemType.GSM8K:
            from zero_shot_replication.datasets.gsm8k import GSM8KDataset

            dataset = GSM8KDataset()
        case ProblemType.MATH:
            from zero_shot_replication.datasets.math import MATHDataset

            dataset = MATHDataset()
        case _:
            raise NotImplementedError(
                f"Problem type not implemented for {problem_type}."
            )
    return dataset
