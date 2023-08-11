# sourcery skip: avoid-global-variables, no-relative-imports, require-parameter-annotation, require-return-annotation
# flake8: noqa
"""Study the dataset."""
import argparse
import logging
import os
import sys

from evalplus.data import write_jsonl
from leetcode_constants import LEETCODE_PROBLEMS_PATH
from leetcode_problem_solver import LeetCodeSolver
from leetcode_problems_loader import LeetCodeLoader

from automata.config import DATA_ROOT_PATH, EmbeddingDataCategory
from automata.core.utils import get_root_fpath

# Get the absolute path of the leetcode directory
leetcode_gym_location = os.path.join(
    get_root_fpath(), "research", "leetcode_hard_gym"  # , "leetcode_env"
)

# Add the parent directory to the PYTHONPATH
sys.path.append(leetcode_gym_location)

# Now we can import any Python file from the parent directory
from leetcode_env.environment import LeetCodeEnv  # type: ignore
from leetcode_env.leetcode_types import (  # type: ignore
    LeetCodeSubmission,
    ProgrammingLanguage,
)

# Get the absolute path of the parent directory
agency_location = os.path.join(
    get_root_fpath(), "research", "study_agency_0614"  # , "local agency"
)

# Add the parent directory to the PYTHONPATH
sys.path.append(agency_location)
from completion_provider import CompletionProvider, RunMode

logger = logging.getLogger(__name__)


def prep_for_leetcode(code: str) -> str:
    lines = code.split("\n")
    modified_lines = ["class Solution():"]
    for line in lines:
        if line.startswith("def "):
            line = "def " + line[4:].replace("(", "(self, ", 1)
        modified_lines.append(f"  {line}")
    return "\n".join(modified_lines)


LEETCODE_SOLUTIONS_FILE_NAME = "test_leetcode_model_eq_{MODEL}_temp_eq_{TEMPERATURE}_run_mode_eq_{RUN_MODE}_solutions.jsonl"
LEETCODE_SOLUTIONS_OUTPUT_PATH = os.path.join(
    get_root_fpath(),
    DATA_ROOT_PATH,
    EmbeddingDataCategory.RESEARCH.value,
    "leetcode_results",
    LEETCODE_SOLUTIONS_FILE_NAME,
)


def main():  # sourcery skip: docstrings-for-functions
    # Argument parsing setup
    parser = argparse.ArgumentParser(
        description="Find similar solutions to LeetCode problems using OpenAI."
    )
    parser.add_argument(
        "--problems_data_path",
        default=LEETCODE_PROBLEMS_PATH,
        help="Path to the LeetCode problems data.",
    )
    parser.add_argument(
        "--solutions_output_data_path",
        default=LEETCODE_SOLUTIONS_OUTPUT_PATH,
        help="Path to the solutions JSON file.",
    )
    parser.add_argument("--temperature", type=float, default=0.7, help="")
    parser.add_argument("--run_mode", type=str, default="vanilla", help="")
    parser.add_argument(
        "--model", type=str, default="gpt-3.5-turbo-0613", help=""
    )

    args = parser.parse_args()
    print(f"Loading problem data from {args.problems_data_path}")
    loader = LeetCodeLoader(args.problems_data_path)
    num_examples = len(loader.data)
    print(f"Number of examples to run = {num_examples}")

    solver = LeetCodeSolver(num_examples)

    completion_provider = CompletionProvider(
        run_mode=RunMode(args.run_mode),
        model=args.model,
        temperature=args.temperature,
    )

    output_path = args.solutions_output_data_path.format(
        MODEL=args.model, TEMPERATURE=args.temperature, RUN_MODE=args.run_mode
    )
    env = LeetCodeEnv()

    completion_seqs = []
    for index in solver.indices:
        problem_context = loader.get_problem_context(index)

        print(
            f"Running w/ problem at index {index} and context:\n\n{problem_context}"
        )

        try:
            (
                raw_completion,
                clean_completion,
            ) = completion_provider.get_raw_and_cleaned_completions(
                problem_context
            )

            sub = LeetCodeSubmission(
                code=prep_for_leetcode(clean_completion),
                lang=ProgrammingLanguage.PYTHON3,
                question_id=loader.get_backend_problem_id(index),
                question_slug=loader.get_problem_slug(index),
            )

            status, reward, done, submission_result = env.step(sub)
            print(status, reward, done, submission_result)
            solver.log_result(index, reward)

            completion_seqs.append(
                {
                    "task_id": f"LeetCode-Hard/{index}",
                    "completion": clean_completion,
                    "raw_completion": raw_completion,
                }
            )
            print(f"Writing output to {output_path}")
            write_jsonl(output_path, completion_seqs)

        except Exception:
            write_jsonl(output_path, completion_seqs)
            solver.log_result(index, False)


if __name__ == "__main__":
    from automata.cli.commands import configure_logging

    configure_logging("DEBUG")
    main()
