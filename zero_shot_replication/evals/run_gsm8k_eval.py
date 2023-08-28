"""Load and process math problems and solutions."""
import argparse
import logging

import pandas as pd
from evalplus.data import write_jsonl

from zero_shot_replication.core import (
    is_equiv,
    last_boxed_only_string,
    remove_boxed,
)
from zero_shot_replication.core.utils import (
    load_file_or_raise,
    parse_arguments,
)
from zero_shot_replication.evals.eval_utils import (
    get_input_path,
    read_existing_results,
)


def process_problems_solutions(args: argparse.Namespace) -> None:
    args = parse_arguments()
    args.pset = "gsm8k"

    input_file_path = args.solutions_file_path or get_input_path(args)
    solutions = pd.DataFrame(load_file_or_raise(input_file_path))

    output_path = input_file_path.replace(".jsonl", "_eval_results.jsonl")

    print(f"Loading solutions from: {input_file_path}")

    new_results = read_existing_results(output_path)
    existing_task_ids = {result["task_id"] for result in new_results}

    rewards = 0
    for loc in range(len(solutions)):
        solution = solutions.iloc[loc]

        if solution["task_id"] in existing_task_ids:
            print(
                f"Skipping task_id {solution['task_id']} as it has already been processed."
            )
            continue

        answer = solution["answer"].split("####")[1].strip()
        ### Extra help for Claude-2
        attempt = remove_boxed(last_boxed_only_string(solution["completion"]))
        if not answer or not attempt:
            is_equivalent = False
        else:
            if "=" in attempt:
                attempt = attempt.split("=")[-1].strip()
            attempt = attempt.replace(",", "")
            attempt = attempt.replace("$", "")
            attempt = attempt.replace("""\\""", "")
            attempt = attempt.replace("'\\/'", "")
            attempt = attempt.split(" ")[0]
            attempt = attempt.split("\n")[0]

            is_equivalent = is_equiv(answer, attempt) or is_equiv(
                answer, attempt[::-1] if attempt else ""
            )
        print(f"is_equivalent = {is_equivalent}")

        print(
            f"task_id={solution['task_id']}, answer={answer}, attempt={attempt}"
        )

        new_results.append({**solution, "reward": is_equivalent})

    rewards = sum(entry["reward"] for entry in new_results)
    print(
        "\nEvaluating %s\nAccuracy %.2f percent\n"
        % (input_file_path, 100 * rewards / float(len(new_results)))
    )
    write_jsonl(output_path, new_results)


def main():
    args = parse_arguments()
    process_problems_solutions(args)


if __name__ == "__main__":
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    main()
