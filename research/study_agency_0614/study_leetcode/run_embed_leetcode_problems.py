"""Prepares the dataset for agent evaluation"""
# sourcery skip: avoid-global-variables, no-relative-imports
import argparse
import logging
import logging.config
from typing import Any, Generator, List, Tuple

import pandas as pd
from leetcode_constants import LEETCODE_SOLUTIONS_PATH

from automata.core.utils import get_logging_config
from automata.llm import OpenAIEmbeddingProvider

# Specify the path to your JSON file
PROBLEM_CHUNK_SIZE = 512

logger = logging.getLogger(__name__)
logging.config.dictConfig(get_logging_config())


def chunks(lst: List, n: int) -> Generator[Tuple, Any, Any]:
    """Yield successive n-sized chunks from a `List` object lst."""
    for i in range(0, len(lst), n):
        yield i, lst[i : i + n]


def main(input_dataset_path: str, output_dataset_path: str) -> None:
    """
    Reads the dataset from the input path,
    adds embeddings, and writes the dataset to the output path.
    """
    logger.info(f"Loading input dataset from {input_dataset_path}")
    # Load the JSON file into a pandas DataFrame
    # Data sourced from HF
    # [https://huggingface.co/datasets/mhhmm/leetcode-solutions-python]
    # Schema:
    #   Index(['id', 'code_with_data', 'code_only', 'code_with_problem',
    #    'explanation_only', 'embedding'], dtype='object')
    df = pd.read_json(input_dataset_path)

    # code_with_data is the primary column,
    # print(df['code_with_data'][0])
    # ```bash
    # # two-sum
    # # Two Sum
    # # Easy
    # # Given an array of integers `nums` and an integer `target`, return _indices of the two numbers such that they add up to `target`_.

    # You may assume that each input would have **_exactly_ one solution**, and you may not use the _same_ element twice.

    # You can return the answer in any order.
    #
    # **Example 1:**
    # ...
    # ```

    # print(df['code_with_problem'][0])
    # ```bash
    # ... Repeat L29-42 above ...
    # ```python
    # def twoSum(nums, target):
    #     map = {}
    #     for i, num in enumerate(nums):
    #         complement = target - num
    #         if complement in map:
    #             return [map[complement], i]
    #         map[num] = i
    #     return []
    # ```

    logger.info("Cleaning problem statements")
    # Extract cleaned explanations by removing everything from `**Example 1:` and downwards
    # e.g. we move further examples, constraints, and follow-ups
    problem_statements_no_examples = [
        ele.split("**Example 1:")[0].strip()
        for ele in df["code_with_data"].values
    ]

    # Remove blob / difficulty-tag and format
    cleaned_problem_statements = []
    for entry in problem_statements_no_examples:
        split_entry = entry.split("#")
        title = split_entry[2]
        description = "#".join(split_entry[4:])
        cleaned_problem_statements.append(
            f"Title:{title}\n\nDescription:\n{description}"
        )
    logger.info("Producing embeddings")
    # Initialize the embedding provider
    embedding_provider = OpenAIEmbeddingProvider()

    # Loop through the cleaned_explanations and produce
    embedded_problem_statements = []
    for counter, data_chunk in chunks(
        cleaned_problem_statements, PROBLEM_CHUNK_SIZE
    ):
        logger.info(f"Running chunk {counter}")
        # Build embedding vectors for each chunk
        chunk_embeddings = embedding_provider.batch_build_embedding_vector(
            data_chunk
        )
        embedded_problem_statements.extend(chunk_embeddings)

    logger.info("Adding embeddings to the DataFrame")
    # Add the embeddings to the DataFrame as a new column
    df["embedding"] = embedded_problem_statements

    logger.info(f"Saving output to {output_dataset_path}")
    # Save the modified DataFrame back to the original JSON file
    df.to_json(output_dataset_path)


if __name__ == "__main__":
    # Argument parsing setup
    parser = argparse.ArgumentParser(
        description="Find similar solutions to LeetCode problems using OpenAI."
    )
    parser.add_argument(
        "--input_data_path",
        default=LEETCODE_SOLUTIONS_PATH,
        help="Path to read the LeetCode problems data from.",
    )

    parser.add_argument(
        "--output_data_path",
        default=LEETCODE_SOLUTIONS_PATH,
        help="Path to write the LeetCode problems data to.",
    )

    args = parser.parse_args()

    logger.setLevel(logging.INFO)

    main(args.input_data_path, args.output_data_path)
