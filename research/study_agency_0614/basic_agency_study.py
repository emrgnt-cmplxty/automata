"""Basic agency study, e.g. simple completion / agent generation"""
import argparse
import os

from completion_provider import CompletionProvider, RunMode
from evalplus.data import get_human_eval_plus, write_jsonl
from tqdm import tqdm

from automata.config import DATA_ROOT_PATH, EmbeddingDataCategory
from automata.core.utils import get_root_fpath

HUMANEVAL_SOLUTIONS_FILE_NAME = "test_human_eval_model_eq_{MODEL}_temp_eq_{TEMPERATURE}_run_mode_eq_{RUN_MODE}_solutions.jsonl"
HUMANEVAL_SOLUTIONS_PATH = os.path.join(
    get_root_fpath(),
    DATA_ROOT_PATH,
    EmbeddingDataCategory.RESEARCH.value,
    HUMANEVAL_SOLUTIONS_FILE_NAME,
)


def main() -> None:
    """Main function for generating human eval solutions"""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--model", type=str, default="gpt-3.5-turbo-0613", help=""
    )
    parser.add_argument("--overwrite", type=bool, default=False)
    parser.add_argument("--start_index", type=int, default=0, help="")
    parser.add_argument("--end_index", type=int, default=164, help="")
    parser.add_argument(
        "--output_fpath",
        type=str,
        default=HUMANEVAL_SOLUTIONS_PATH,
        help="",
    )
    parser.add_argument("--temperature", type=float, default=0.7, help="")
    parser.add_argument("--run_mode", type=str, default="vanilla", help="")

    args = parser.parse_args()

    if not RunMode(args.run_mode):
        raise ValueError(
            f"Invalid mode: {args.run_mode}, Available modes: {RunMode}"
        )

    completion_provider = CompletionProvider(
        run_mode=RunMode(args.run_mode),
        model=args.model,
        temperature=args.temperature,
    )
    problems = get_human_eval_plus()

    task_ids = sorted(problems.keys())[args.start_index : args.end_index]
    prompts = [problems[task_id]["prompt"] for task_id in task_ids]
    num_samples = len(prompts)
    print(f"Number of samples: {num_samples}")

    completion_seqs = []
    output_path = args.output_fpath.format(
        MODEL=args.model, TEMPERATURE=args.temperature, RUN_MODE=args.run_mode
    )
    if os.path.exists(output_path) and not args.overwrite:
        raise ValueError(f"Output path already exists: {output_path}")

    for i in tqdm(range(num_samples), ncols=0, total=num_samples):
        print(f"Loading sample i = {i}")

        raw_prompt = prompts[i]
        print(f"Passing raw prompt ={raw_prompt}")

        (
            raw_completion,
            clean_completion,
        ) = completion_provider.get_raw_and_cleaned_completions(raw_prompt)
        print(f"Found Raw Completion = {raw_completion}")

        completion_seqs.append(
            {
                "task_id": task_ids[i],
                "completion": clean_completion,
                "raw_completion": raw_completion,
            }
        )
        print(f"Writing output to {output_path}")
        write_jsonl(output_path, completion_seqs)


if __name__ == "__main__":
    main()
