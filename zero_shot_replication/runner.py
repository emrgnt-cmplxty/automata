"""Run the zero-shot replication."""
import argparse
import os

import openai
from evalplus.data import write_jsonl

from zero_shot_replication.base import ProblemType
from zero_shot_replication.generators import ProblemGenerator
from zero_shot_replication.prompt_layer import PromptLayer
from zero_shot_replication.llm_providers import OpenAIZeroShotProvider
from zero_shot_replication.utils import (
    get_root_dir,
    parse_arguments,
    prep_for_file_path,
)

OUTPUT_FILE_NAME = "{PROVIDER}_{DATASET}__model_eq_{MODEL}__temperature_eq_{TEMPERATURE}.jsonl"


def get_output_path(args: argparse.Namespace) -> str:
    """Get the output path for the given arguments."""
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
    llm_provider = None
    if args.provider == "openai":
        llm_provider = OpenAIZeroShotProvider(
            model=args.model, temperature=args.temperature
        )
    else:
        raise NotImplementedError("Provider not implemented.")

    # Build a problem generator instance
    problem_generator = ProblemGenerator(ProblemType(args.dataset))

    # Build a prompt layer instance
    prompt_layer = PromptLayer(ProblemType(args.dataset))

    for task_id, problem in problem_generator.generator:
        prompt = prompt_layer.get_prompt(problem)

        print(
            f"\n{'-'*200}\nTaskId:\n{task_id}\n\nProblem:\n{problem}\n\nPrompt:\n{prompt}\n"
        )
        completion = llm_provider.get_completion(prompt)
        print(f"Completion:\n{completion}\n")

        result = {**problem, "completion": completion, "actual_prompt": prompt}
        write_jsonl(out_path, [result])
        if "1" in task_id:
            break
