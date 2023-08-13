# sourcery skip: avoid-global-variables, no-relative-imports, require-parameter-annotation, require-return-annotation
# flake8: noqa
"""Study the dataset."""
import argparse
import json
import logging
import os
import sys

from agentified_solution_oracle import (
    AgentifiedSolutionOracleOpenAIToolkitBuilder,
)
from evalplus.data import write_jsonl
from leetcode_constants import LEETCODE_PROBLEMS_PATH, LEETCODE_SOLUTIONS_PATH
from leetcode_problem_solver import LeetCodeSolver
from leetcode_problems_loader import LeetCodeLoader
from leetcode_solutions_finder import LeetCodeSolutionsFinder

from automata.config import DATA_ROOT_PATH, EmbeddingDataCategory
from automata.core.utils import get_root_fpath
from automata.llm import OpenAIEmbeddingProvider

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


LEETCODE_SOLUTIONS_FILE_NAME = "test_leetcode_model_eq_{MODEL}_temp_eq_{TEMPERATURE}_run_mode_eq_{RUN_MODE}_solutions.jsonl"
LEETCODE_SOLUTIONS_OUTPUT_PATH = os.path.join(
    get_root_fpath(),
    DATA_ROOT_PATH,
    EmbeddingDataCategory.RESEARCH.value,
    "leetcode_results",
    LEETCODE_SOLUTIONS_FILE_NAME,
)


def prep_for_leetcode(code: str) -> str:
    lines = code.split("\n")
    modified_lines = ["class Solution():"]
    for line in lines:
        if line.startswith("def "):
            line = "def " + line[4:].replace("(", "(self, ", 1)
        modified_lines.append(f"  {line}")
    return "\n".join(modified_lines)


def load_existing_jsonl(file_path):
    if os.path.exists(file_path):
        with open(file_path, "r") as json_file:
            return [json.loads(line) for line in json_file]
    return []


def load_existing_task_ids(existing_data):
    return {entry["task_id"] for entry in existing_data}


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
    parser.add_argument("--overwrite", type=bool, default=False, help="")

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
    embedding_provider = OpenAIEmbeddingProvider()

    output_path = args.solutions_output_data_path.format(
        MODEL=args.model, TEMPERATURE=args.temperature, RUN_MODE=args.run_mode
    )
    print(f"Loading from {output_path}")
    existing_data = load_existing_jsonl(output_path)
    existing_task_ids = (
        set() if args.overwrite else load_existing_task_ids(existing_data)
    )

    completion_seqs = existing_data or []
    env = LeetCodeEnv()

    for index in solver.indices:
        task_id = f"LeetCode-Hard/{index}"

        if task_id in existing_task_ids and not args.overwrite:
            print(
                f"Skipping task_id {task_id} as it already exists in the output file."
            )
            continue
        problem_context = loader.get_problem_context(index)

        print(
            f"Running w/ problem at index {index} and context:\n\n{problem_context}"
        )

        try:
            tools = []
            if (
                args.run_mode
                == RunMode.ADVANCED_AGENT_WITH_INTERPRETER_AND_ORACLE.value
            ):
                solutions_finder = LeetCodeSolutionsFinder(
                    embedding_provider,
                    max_entry_id=loader.get_frontend_problem_id(
                        index
                    ),  # Solutions are indexed along frontend problem id
                    max_num_examples=1,
                    num_examples_to_screen=25,
                    solutions_data_path=LEETCODE_SOLUTIONS_PATH,
                    lowest_difficulty="Medium",
                )
                tools = AgentifiedSolutionOracleOpenAIToolkitBuilder(
                    leetcode_solution_finder=solutions_finder
                ).build_for_open_ai()  # type: ignore

            (
                raw_completion,
                clean_completion,
            ) = completion_provider.get_raw_and_cleaned_completions(
                problem_context, tools
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

        except Exception as e:
            print(f"Failed with exception {e}")
            write_jsonl(output_path, completion_seqs)
            solver.log_result(index, False)


if __name__ == "__main__":
    from automata.cli.commands import configure_logging

    configure_logging("DEBUG")
    main()
