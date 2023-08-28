import argparse
import json
import logging
import os

import pandas as pd


def load_file_or_raise(path: str):
    """Utility function to load a file or raise an error if not found."""
    try:
        file_extension = os.path.splitext(path)[-1].lower()
        if file_extension == ".csv":
            return pd.read_csv(path)
        elif file_extension == ".jsonl":
            with open(path, "r", encoding="utf-8") as file:
                return pd.DataFrame(
                    json.loads(line) for line in file if line.strip()
                )
        else:
            raise ValueError(f"Unsupported file format: {file_extension}")
    except FileNotFoundError as e:
        raise FileNotFoundError(
            f"Please check the expected data at {path}."
        ) from e


def get_root_dir() -> str:
    """Get the path to the root of the code repository."""

    script_dir = os.path.dirname(os.path.realpath(__file__))
    return os.path.join(script_dir, "..", "..")


def get_pset_inputs_dir() -> str:
    """Get the path to the psets directory."""

    pset_dir = os.path.dirname(os.path.realpath(__file__))
    return os.path.join(pset_dir, "..", "..", "psets")


def load_existing_jsonl(file_path: str) -> list[dict]:
    """Load existing results from a jsonl file."""

    if os.path.exists(file_path):
        with open(file_path, "r") as json_file:
            return [json.loads(line) for line in json_file]
    return []


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
        "--stream",
        type=bool,
        default=False,
        help="If supported, should the LLM stream completions?",
    )
    parser.add_argument(
        "--pset",
        type=str,
        default="human-eval",
        help="Which pset to run on?",
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
        default=None,
        help="Filename to override the default output file name with.",
    )
    parser.add_argument(
        "--input_file_name",
        default=None,
        help="Filename to override the default input file name with.",
    )
    parser.add_argument(
        "--solutions_file_path",
        default=None,
        help="Path to the solutions file to analyze",
    )

    return parser.parse_args()


def prep_for_file_path(in_path: str) -> str:
    """Prepare a string to be used in a file path."""

    return in_path.replace("-", "_").replace(".", "p").replace("/", "_")


def extract_code(raw_response: str) -> str:
    """Extract the code from a raw LLM response."""
    if "```python" in raw_response:
        cleaned_response = raw_response.split("```python")[1]
        return cleaned_response.split("```")[0]
    elif "```" in raw_response:
        cleaned_response = raw_response.split("```")[1]
        return cleaned_response.split("```")[0]
    else:
        return raw_response


def get_configured_logger(name: str, log_level: str) -> logging.Logger:
    log_level = getattr(logging, log_level.upper(), "INFO")
    logging.basicConfig(
        level=log_level, format="%(asctime)s - %(levelname)s - %(message)s"
    )
    return logging.getLogger(name)


def get_root_fpath() -> str:
    return os.path.dirname(os.path.abspath(__file__))
