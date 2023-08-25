"""Utility functions for evaluation scripts."""
import argparse
import os

from zero_shot_replication.helpers import OUTPUT_FILE_NAME
from zero_shot_replication.helpers.utils import (
    get_root_dir,
    load_file_or_raise,
    prep_for_file_path,
)


def read_existing_results(out_path: str) -> list[dict]:
    """Reads existing results from out_path if it exists, otherwise returns empty list"""
    return (
        load_file_or_raise(out_path).to_dict(orient="records")
        if os.path.exists(out_path)
        else []
    )


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
