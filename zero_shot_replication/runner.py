import argparse
import os
from typing import Optional

import dotenv
import openai
from evalplus.data import write_jsonl

from zero_shot_replication.generators import ProblemGenerator, ProblemType
from zero_shot_replication.llm_providers import OpenAIZeroShotProvider
from zero_shot_replication.utils import get_root_dir

dotenv.load_dotenv()

OUTPUT_FILE_NAME = "{PROVIDER}_{DATASET}__model_eq_{MODEL}__temperature_eq_{TEMPERATURE}.jsonl"


def parse_arguments() -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Parse Zero-Shot running commands"
    )
    parser.add_argument(
        "--provider",
        type=str,
        default="openai",
        help="Which provider to use for zero-shot completions?",
    )
    parser.add_argument(
        "--dataset",
        type=str,
        default="human-eval",
        help="Which dataset to run on?",
    )
    parser.add_argument(
        "--model",
        type=str,
        default="gpt-3.5-turbo",
        help="Model name to load from the provider.",
    )
    parser.add_argument(
        "--temperature",
        type=float,
        default=0.7,
        help="Temperature parameter for provided model.",
    )
    parser.add_argument(
        "--output_file_name",
        type=Optional[str],
        default=None,
        help="Filename to override the default output file name with.",
    )

    return parser.parse_args()


def prep_for_file_path(in_path: str):
    return in_path.replace("-", "_").replace(".", "p")


def get_output_path(args: argparse.Namespace) -> str:
    output_dir = os.path.join(
        get_root_dir(),
        "results",
        prep_for_file_path(args.provider),
        prep_for_file_path(args.dataset),
        prep_for_file_path(args.model),
    )

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    return os.path.join(
        output_dir,
        args.output_file_name
        or OUTPUT_FILE_NAME.format(
            PROVIDER=prep_for_file_path(args.provider),
            DATASET=prep_for_file_path(args.dataset),
            MODEL=prep_for_file_path(args.model),
            TEMPERATURE=prep_for_file_path(str(args.temperature)),
        ),
    )


if __name__ == "__main__":
    """Run the zero-shot replication."""
    openai.api_key = os.getenv("OPENAI_API_KEY", "")
    args = parse_arguments()

    # Get the output path
    out_path = get_output_path(args)

    # Build an LLM provider instance
    llm_provider = OpenAIZeroShotProvider(
        model=args.model, temperature=args.temperature
    )

    # Build a problem generator instance
    problem_generator = ProblemGenerator(ProblemType(args.dataset))

    for task_id, problem in problem_generator.generator:
        completion = "A Test completion"
        prompt = "A test prompt."
        print(f"\nTaskId:\n{task_id}\n\nProblem:\n{problem}\n")
        result = {**problem, "completion": completion, "actual_prompt": prompt}
        write_jsonl(out_path, [result])
        break
