"""A script for running evaluations on LeetCode problems."""
import argparse
import logging
import os
from time import sleep

import numpy as np
import pandas as pd
from evalplus.data import write_jsonl
from leetcode_env.environment import LeetCodeEnv
from leetcode_env.leetcode_types import LeetCodeSubmission, ProgrammingLanguage

from zero_shot_replication.helpers.base import OUTPUT_FILE_NAME
from zero_shot_replication.helpers.utils import (
    extract_code,
    get_configured_logger,
    get_root_dir,
    load_file_or_raise,
    parse_arguments,
    prep_for_file_path,
)

USER_WAIT_TIME = 5  # seconds, per client
IP_WAIT_TIME = 5  # seconds, per IP
TIMEOUT_WAIT = 10


class SessionManager:
    sessions = os.environ["LEETCODE_SESSIONS"].split(",")

    SESSIONS = [f"SESSION_ID_{i}" for i in range(len(sessions))]

    def __init__(self):
        self.counter = 0
        self.envs = []
        for index in range(len(self.SESSIONS)):
            self.set_env(index)
            env = LeetCodeEnv(USER_WAIT_TIME)
            logging.info(
                f"Creating a LeetCodeEnv leetcode_session = {os.environ['LEETCODE_SESSION']}"
            )
            self.envs.append(env)

    def set_env(self, index: int) -> None:
        session_id = self.SESSIONS[index % len(self.SESSIONS)]
        logger.info(f"Setting session_id = {session_id}")
        os.environ["LEETCODE_SESSION"] = self.sessions[
            index % len(self.SESSIONS)
        ]

    def get_next_env(self) -> LeetCodeEnv:
        env = self.envs[self.counter % len(self.envs)]
        self.counter += 1
        return env


def read_existing_results(out_path: str) -> list[dict]:
    """Reads existing results from out_path if it exists, otherwise returns empty list"""
    return (
        load_file_or_raise(out_path).to_dict(orient="records")
        if os.path.exists(out_path)
        else []
    )


def _create_submission_result(
    solution: dict, extracted_code: str, status: str, reward: bool, done: str
) -> dict:
    return {
        "task_id": solution["task_id"],
        "status": status,
        "reward": int(reward),
        "done": done,
        "raw_completion": solution["raw_completion"],
        "extracted_code": extracted_code,
        "difficulty": solution["difficulty"],
    }


def process_submission(
    solution: dict,
    extracted_code: str,
    session_manager: SessionManager,
    logger: logging.Logger,
) -> dict:
    logger.info("Submitting code...")
    sub = LeetCodeSubmission(
        code=extracted_code,
        lang=ProgrammingLanguage.PYTHON3,
        question_id=str(int(solution["question_id"])),
        question_slug=solution["question_slug"],
        timeout=TIMEOUT_WAIT,
    )
    (
        status,
        reward,
        done,
        submission_result,
    ) = session_manager.get_next_env().step(sub)
    logger.info(
        f"Status:{status}, Reward:{reward}, Done:{done}, Result:{submission_result}"
    )
    logger.info("-" * 100)
    return _create_submission_result(
        solution, extracted_code, status, reward, done
    )


def process_answers(
    solutions: pd.DataFrame,
    logger: logging.Logger,
    out_path: str,
    session_manager: SessionManager,
) -> list[dict]:
    logger.info(f"Loding existing results from {out_path}...")
    new_results = read_existing_results(out_path)
    existing_frontend_ids = {result["task_id"] for result in new_results}

    logger.info(f"Loaded {len(new_results)} existing results")
    logger.info(f"Looping over {len(solutions)} generated solutions...")
    solutions = solutions.sort_values(by=["frontend_question_id"])[::-1]

    for loc in range(len(solutions)):
        try:
            solution = solutions.iloc[loc]
            extracted_code = extract_code(solution.raw_completion)

            if solution.task_id in existing_frontend_ids:
                logger.info(
                    f"Skipping {solution.task_id} because it already exists"
                )
                continue
            logger.info(f"Processing task {solution.task_id}...")

            logger.info(f"Actual prompt reads:\n{solution.actual_prompt}")
            logger.info("-" * 100)
            logger.info(f"Raw completion:\n{solution.raw_completion}")
            logger.info("-" * 100)

            processed_submission = process_submission(
                solution,
                extracted_code,
                session_manager,
                logger,
            )
            new_results.append(processed_submission)
            write_jsonl(out_path, new_results)

        except Exception as e:
            logger.error(f"Failed to process answer with {e}", exc_info=True)
            logger.info("Sleeping full downtime...")
            new_results.append(
                _create_submission_result(
                    solution,
                    extracted_code,
                    status="ERROR",
                    reward=False,
                    done="Complete.",
                )
            )
            sleep(IP_WAIT_TIME)  # TODO - Why can't we rely on client sleep?

        logger.info(f"Done processing task {solution.task_id}")
        write_jsonl(out_path, new_results)
    return new_results


def get_input_path(args: argparse.Namespace) -> str:
    """Get the output path for the given arguments."""
    input_dir = os.path.join(
        get_root_dir(),
        "results",
        prep_for_file_path(args.provider),
        prep_for_file_path(args.pset),
        prep_for_file_path(args.model),
    )

    if not os.path.exists(input_dir):
        os.makedirs(input_dir)

    return os.path.join(
        input_dir,
        args.input_file_name
        or OUTPUT_FILE_NAME.format(
            PROVIDER=prep_for_file_path(args.provider),
            pset=prep_for_file_path(args.pset),
            MODEL=prep_for_file_path(args.model),
            TEMPERATURE=prep_for_file_path(str(args.temperature)),
        ),
    )


def parse_results(results: list[dict]) -> dict:
    parsed_results: dict = {"easy": [], "medium": [], "hard": []}

    difficulty_map = {1: "easy", 2: "medium", 3: "hard"}

    for result in results:
        difficulty_key = difficulty_map.get(result["difficulty"])
        if difficulty_key:
            parsed_results[difficulty_key].append(result["reward"])

    return parsed_results


def display_parsed_results(parsed_results: dict) -> None:
    for difficulty, rewards in parsed_results.items():
        print(
            f"{difficulty.capitalize()} Results Count = {len(rewards)} Pass Rate = {100 * np.mean(rewards):.2f}%"
        )


if __name__ == "__main__":
    args = parse_arguments()
    args.pset = "leetcode"
    results_input_path = get_input_path(args)

    logger = get_configured_logger(__name__, "DEBUG")
    logger.info(f"Loading solutions from {results_input_path}")
    solutions = pd.DataFrame(load_file_or_raise(results_input_path))

    output_path = results_input_path.replace(".jsonl", "_eval_results.jsonl")

    logger.info(f"Saving results to {output_path}")

    session_manager = SessionManager()

    results = process_answers(
        solutions,
        logger,
        output_path,
        session_manager,
    )

    parsed = parse_results(results)
    display_parsed_results(parsed)
