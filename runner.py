import argparse
import os

import dotenv
import openai
from evalplus.data import write_jsonl

from generators import ProblemGenerator, ProblemType
from llm_providers import OpenAIZeroShotProvider

dotenv.load_dotenv()


def parse_arguments() -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Parse Zero-Shot running commands"
    )
    parser.add_argument(
        "--temperature",
        type=float,
        default=0.7,
        help="Temperature parameter for OpenAI model.",
    )
    parser.add_argument(
        "--model",
        type=str,
        default="gpt-3.5-turbo",
        help="Model name for OpenAI.",
    )
    parser.add_argument(
        "--dataset", default="human-eval", help="Which dataset to run on?"
    )
    return parser.parse_args()


if __name__ == "__main__":
    openai.api_key = os.getenv("OPENAI_API_KEY", "")
    args = parse_arguments()

    openai_zero_shot_provider = OpenAIZeroShotProvider(
        model=args.model, temperature=args.temperature
    )
    problem_generator = ProblemGenerator(ProblemType(args.dataset))
    for task_id, problem in problem_generator.generator:
        print(f"\nTaskId:\n{task_id}\n\nProblem:\n{problem}\n")
        break
