import argparse
import json
import os
import re

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
    return os.path.join(pset_dir, "..", "..", "psets", "inputs")


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

    return parser.parse_args()


def prep_for_file_path(in_path: str) -> str:
    """Prepare a string to be used in a file path."""

    return in_path.replace("-", "_").replace(".", "p")


def extract_code(raw_response: str) -> str:
    """Extract the code from a raw LLM response."""

    def _extract_unformatted(raw_response):
        # Extract the class definition as before
        class_definition_match = re.search(
            r"class\s\S*:\s*.*?(?=\n\n|$)", raw_response, re.DOTALL
        )
        class_definition = (
            class_definition_match[0] if class_definition_match else None
        )

        # Find the position of the class definition in the raw_response
        class_position = (
            class_definition_match.start() if class_definition_match else -1
        )

        # Extract the lines before the class definition
        lines_before_class = raw_response[:class_position].strip().splitlines()

        # Extract the import statements by filtering lines that start with 'import' or 'from'
        import_statements = [
            line
            for line in lines_before_class
            if line.startswith(("import", "from"))
        ]

        # Combine the import statements and the class definition
        return "\n".join(import_statements + [class_definition])

    if "```python" in raw_response:
        cleaned_response = raw_response.split("```python")[1]
        return cleaned_response.split("```")[0]
    elif "```" in raw_response:
        cleaned_response = raw_response.split("```")[1]
        return cleaned_response.split("```")[0]
    else:
        try:
            return _extract_unformatted(raw_response)
        except Exception as e:
            print("Error extracting code from response: ", e)
            return raw_response
