"""Load and process math problems and solutions."""
import argparse
import json
import logging
import os
from glob import glob

import dotenv
import numpy as np
import openai
import pandas as pd

from zero_shot_replication.helpers.math_helpers import is_equiv
from zero_shot_replication.helpers.utils import (
    get_root_fpath,
    load_existing_jsonl,
    parse_arguments,
)

# Constants
MATH_RESULTS_FILE_NAME = "math_results_{MODEL}_{TEMPERATURE}_{RUN_MODE}.jsonl"
MATH_RESULTS_DIR = os.path.join(
    get_root_fpath(), "..", "..", "results", "openai", "MATH", "gpt_4_0314"
)
NUM_SAMPLES_DEFAULT = 250
INPUTS = glob(os.path.join("data", "inputs", "MATH", "*", "*"))

dotenv.load_dotenv()
np.random.seed(4294967294)


def load_existing_problems(output_path: str) -> tuple[list[dict], set[str]]:
    existing_data = load_existing_jsonl(output_path)
    return existing_data, {entry["problem"] for entry in existing_data}


def load_inputs(existing_problems=None) -> pd.DataFrame:
    indices = list(range(len(INPUTS)))
    np.random.shuffle(indices)

    results = []
    for index in indices:
        with open(INPUTS[index], "r") as f:
            problem_data = json.loads(f.read())
            if (
                existing_problems
                and problem_data["problem"] in existing_problems
            ):
                continue  # Skip problems that have already been observed
            results.append(problem_data)

    return pd.DataFrame(results)


def remove_boxed(s) -> str:
    left = "oxed{"
    try:
        assert s[: len(left)] == left
        assert s[-1] == "}"
        return s[len(left) : -1]
    except Exception:
        return None


def last_boxed_only_string(string) -> str:
    idx = string.rfind("oxed{")
    if idx < 0:
        idx = string.rfind("\\fbox")
    if idx < 0:
        return None

    i = idx
    right_brace_idx = None
    num_left_braces_open = 0
    while i < len(string):
        if string[i] == "{":
            num_left_braces_open += 1
        if string[i] == "}":
            num_left_braces_open -= 1
            if num_left_braces_open == 0:
                right_brace_idx = i
                break
        i += 1

    return (
        None if right_brace_idx is None else string[idx : right_brace_idx + 1]
    )


def process_problems_solutions(args: argparse.Namespace) -> None:
    openai.api_key = os.getenv("OPENAI_API_KEY_LOCAL", "")

    solutions_output_path = args.solutions_file_path
    results, existing_problems = load_existing_problems(solutions_output_path)
    rewards = 0
    for counter, result in enumerate(results):
        print(result)

        answer = remove_boxed(last_boxed_only_string(result["solution"]))
        attempt = remove_boxed(last_boxed_only_string(result["completion"]))
        print(f"answer={answer}, attempt={attempt}")

        is_equivalent = is_equiv(answer, attempt) or is_equiv(
            answer, attempt[::-1] if attempt else ""
        )
        rewards += float(is_equivalent)
        print(f"is_equiv={is_equivalent}")
        print(f"acc={rewards/(counter+1)}")
        print(f"counter={counter}")


def main():
    args = parse_arguments()
    process_problems_solutions(args)


if __name__ == "__main__":
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    main()
