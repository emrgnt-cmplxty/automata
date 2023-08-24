"""Run the zero-shot replication."""
import argparse
import os

import openai
from evalplus.data import write_jsonl

from zero_shot_replication.datasets import get_dataset
from zero_shot_replication.helpers import OUTPUT_FILE_NAME, ProblemType
from zero_shot_replication.helpers.utils import (
    extract_code,
    get_root_dir,
    load_existing_jsonl,
    parse_arguments,
    prep_for_file_path,
)
from zero_shot_replication.llm_providers import ProviderManager


def get_output_path(args: argparse.Namespace) -> str:
    """Get the output path for the given arguments."""
    output_dir = os.path.join(
        get_root_dir(),
        "results",
        prep_for_file_path(args.provider),
        prep_for_file_path(args.pset),
        prep_for_file_path(args.model),
    )

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    return os.path.join(
        output_dir,
        args.output_file_name
        or OUTPUT_FILE_NAME.format(
            PROVIDER=prep_for_file_path(args.provider),
            pset=prep_for_file_path(args.pset),
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
    llm_provider = ProviderManager.get_provider(args.provider, args.model)

    if not llm_provider:
        raise NotImplementedError(f"Provider '{args.provider}' not supported.")

    # Get the corresponding dataset
    dataset = get_dataset(ProblemType(args.pset))

    # Load existing results
    results = load_existing_jsonl(out_path)

    try:
        exising_task_ids = {result["task_id"] for result in results}
    except KeyError:
        exising_task_ids = {}
    # Run the experiment
    for task_id, problem in dataset.generator:
        if task_id in exising_task_ids:
            print(
                f"Continuing over existing task_id: {task_id} as it already exists."
            )
            continue

        prompt = dataset.get_formatted_prompt(problem)

        print(
            f"\n{'-'*200}\nTaskId:\n{task_id}\n\nProblem:\n{problem}\n\nPrompt:\n{prompt}\n"
        )

        try:
            raw_completion = llm_provider.get_completion(prompt)
            if args.pset in ["human-eval", "leetcode"]:
                # or other codegen
                completion = extract_code(raw_completion)
            else:
                completion = raw_completion

            print(f"Extracted Completion:\n{completion}\n")

            result = {
                **problem,
                "task_id": task_id,
                "completion": completion,
                "raw_completion": raw_completion,
                "actual_prompt": prompt,
            }
            results.append(result)
            write_jsonl(out_path, results)

        except (
            openai.error.OpenAIError,
            Exception,
        ) as e:  # Catch any OpenAI specific errors and general exceptions
            print(f"Error encountered for task_id {task_id}: {e}")
            continue
