import argparse
import os
from typing import Optional


def get_root_dir() -> str:
    """Get the path to the root of the Automata python code directory."""

    script_dir = os.path.dirname(os.path.realpath(__file__))
    return os.path.join(script_dir, "..")


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
        default=None,
        help="Filename to override the default output file name with.",
    )

    return parser.parse_args()


def prep_for_file_path(in_path: str) -> str:
    """Prepare a string to be used in a file path."""
    return in_path.replace("-", "_").replace(".", "p")
