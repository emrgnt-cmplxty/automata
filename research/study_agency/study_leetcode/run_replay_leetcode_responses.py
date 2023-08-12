# sourcery skip: avoid-global-variables, no-relative-imports, require-parameter-annotation, require-return-annotation
# flake8: noqa
"""Study the dataset."""
import argparse
import json
import logging
import os
import sys
import time

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
    get_root_fpath(),
    "research",
    "study_agency",
    "study_human_eval",  # , "local agency"
)

# Add the parent directory to the PYTHONPATH
sys.path.append(agency_location)
from completion_provider import CompletionProvider, RunMode

logger = logging.getLogger(__name__)


def load_existing_jsonl(file_path):
    if os.path.exists(file_path):
        with open(file_path, "r") as json_file:
            return [json.loads(line) for line in json_file]
    return []


def prep_for_leetcode(code: str) -> str:
    lines = code.split("\n")
    modified_lines = ["class Solution():"]
    for line in lines:
        if line.startswith("def "):
            line = "def " + line[4:].replace("(", "(self, ", 1)
        modified_lines.append(f"  {line}")
    return "\n".join(modified_lines)


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
        "--input_data_path",
        default=LEETCODE_PROBLEMS_PATH,
        help="Path to the LeetCode problems data.",
    )
    args = parser.parse_args()

    input_problems = load_existing_jsonl(args.input_data_path)
    loader = LeetCodeLoader(args.problems_data_path)
    env = LeetCodeEnv()

    correct = 0
    for counter, problem in enumerate(input_problems, start=1):
        completion = problem["completion"]
        print("raw completion = ", problem["raw_completion"])
        index = int(problem["task_id"].split("/")[1])

        print(
            f"Running task_id = {problem['task_id']}, with backend_problem_id={loader.get_backend_problem_id(index)}, and frontend_problem_id={loader.get_frontend_problem_id(index)}"
        )
        print(f"Inserting completion = {completion}")
        sub = LeetCodeSubmission(
            code=prep_for_leetcode(completion),
            lang=ProgrammingLanguage.PYTHON3,
            question_id=loader.get_backend_problem_id(index),
            question_slug=loader.get_problem_slug(index),
        )

        status, reward, done, submission_result = env.step(sub)
        print(status, reward, done)

        correct += int(reward)
        print(f"Fraction correct = {correct}/{counter}")
        time.sleep(10)


if __name__ == "__main__":
    from automata.cli.commands import configure_logging

    configure_logging("DEBUG")
    main()
