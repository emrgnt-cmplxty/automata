"""Load and process math problems and solutions."""
import argparse
import logging

import pandas as pd
from evalplus.data import write_jsonl

from zero_shot_replication.evals.eval_utils import (
    get_input_path,
    read_existing_results,
)
from zero_shot_replication.helpers.math_helpers import (
    is_equiv,
    last_boxed_only_string,
    remove_boxed,
)
from zero_shot_replication.helpers.utils import (
    load_file_or_raise,
    parse_arguments,
)


def process_problems_solutions(args: argparse.Namespace) -> None:
    args = parse_arguments()

    input_file_path = args.solutions_file_path or get_input_path(args)
    solutions = pd.DataFrame(load_file_or_raise(input_file_path))

    output_path = input_file_path.replace(".jsonl", "_eval_results.jsonl")

    print(f"Loading solutions from: {input_file_path}")

    new_results = read_existing_results(output_path)
    ## Uncomment after updating output files...
    # existing_task_ids = {result["task_id"] for result in new_results}

    rewards = 0
    for loc in range(len(solutions)):
        solution = solutions.iloc[loc]

        ## Uncomment after updating output files...
        # if solution["task_id"] in existing_task_ids:
        #     print(
        #         f"Skipping task_id {solution['task_id']} as it has already been processed."
        #     )
        #     continue

        answer = remove_boxed(last_boxed_only_string(solution["solution"]))
        attempt = remove_boxed(last_boxed_only_string(solution["completion"]))
        if not answer or not attempt:
            is_equivalent = False
        else:
            is_equivalent = is_equiv(answer, attempt) or is_equiv(
                answer, attempt[::-1] if attempt else ""
            )

        ## Uncomment after updating output files...
        # print(
        #     f"task_id={solution['task_id']}, answer={answer}, attempt={attempt}"
        # )

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


# """Load and process math problems and solutions."""
# import argparse
# import logging

# import pandas as pd

# from zero_shot_replication.evals.eval_utils import (
#     get_input_path,
#     read_existing_results,
# )
# from zero_shot_replication.helpers.math_helpers import (
#     is_equiv,
#     last_boxed_only_string,
#     remove_boxed,
# )
# from zero_shot_replication.helpers.utils import (
#     load_file_or_raise,
#     parse_arguments,
# )


# def process_problems_solutions(args: argparse.Namespace) -> None:
#     args = parse_arguments()

#     input_file_path = args.solutions_file_path or get_input_path(args)
#     solutions = pd.DataFrame(load_file_or_raise(input_file_path))

#     output_path = input_file_path.replace(".jsonl", "_eval_results.jsonl")

#     print(f"Loading solutions from: {input_file_path}")

#     new_results = read_existing_results(output_path)
#     existing_task_ids = {result["task_id"] for result in new_results}

#     rewards = 0
#     for loc in range(len(solutions)):
#         solution = solutions.iloc[loc]

#         if solution["task_id"] in existing_task_ids:
#             print(
#                 f"Skipping task_id {solution['task_id']} as it has already been processed."
#             )
#             continue
#         print(solution)

#         answer = remove_boxed(last_boxed_only_string(solution["answer"]))
#         attempt = remove_boxed(last_boxed_only_string(solution["completion"]))
#         print(f"answer={answer}, attempt={attempt}")

#         is_equivalent = is_equiv(answer, attempt) or is_equiv(
#             answer, attempt[::-1] if attempt else ""
#         )
#         rewards += float(is_equivalent)
#         print(f"is_equiv={is_equivalent}")
#         print(f"acc={rewards/(loc+1)}")
#         print(f"counter={loc}")


# def main():
#     args = parse_arguments()
#     process_problems_solutions(args)


# if __name__ == "__main__":
#     logger = logging.getLogger(__name__)
#     logger.setLevel(logging.INFO)
#     main()
