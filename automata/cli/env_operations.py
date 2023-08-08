"""
This module contains the functions to perform environment operations for the CLI.
"""

import logging
import os
import re
from typing import Dict, List, Optional

from dotenv import load_dotenv

from automata.cli.cli_output_logger import CLI_OUTPUT_LEVEL, CustomLogger
from automata.symbol.graph.symbol_graph_types import SymbolGraphType

logging.setLoggerClass(CustomLogger)
logger = logging.getLogger(__name__)
logger.setLevel(CLI_OUTPUT_LEVEL)


def log_cli_output(message: str) -> None:
    """An override to log cli output messages"""

    logger.log(CLI_OUTPUT_LEVEL, message)
    return None


def get_key(dotenv_path: str, key_to_get: str) -> Optional[str]:
    """Get an existing key from a .env file."""

    with open(dotenv_path, "r") as file:
        lines = file.readlines()

    for line in lines:
        key, _, value = line.partition("=")
        if key == key_to_get:
            return value.rstrip()

    return None


def replace_key(dotenv_path: str, key_to_set: str, value_to_set: str) -> None:
    """Replace an existing key in a .env file."""

    with open(dotenv_path, "r") as file:
        lines = file.readlines()

    for i, line in enumerate(lines):
        key, _, _ = line.partition("=")
        if key == key_to_set:
            lines[i] = f"{key_to_set}={value_to_set}\n"

    with open(dotenv_path, "w") as file:
        file.writelines(lines)


def load_env_vars(dotenv_path: str, default_keys: Dict[str, str]) -> None:
    """Loads the env variables into the local env."""

    load_dotenv()

    for key, default_value in default_keys.items():
        current_value = get_key(dotenv_path, key)
        if key == "GRAPH_TYPE":
            if current_value is None or current_value not in [
                e.value for e in SymbolGraphType
            ]:
                new_value = select_graph_type()
            else:
                new_value = current_value
        elif key == "DATA_ROOT_PATH":
            if current_value is None:
                choice = ask_choice(
                    f"Select {key} source", ["Default", "Custom"]
                )
                if choice == "Default":
                    new_value = default_value
                else:
                    new_value = input(f"Enter custom value for {key}: ")
            else:
                new_value = current_value
        elif current_value is None:
            # Check if the environment variable is set at the system level
            system_value = os.getenv(key)
            if system_value is not None:
                new_value = system_value
            else:
                raise ValueError(
                    f"Key {key} not found in the .env file and not set in system environment"
                )
        elif not current_value or current_value == default_value:
            new_value = input(
                f"{key} is not configured. Please enter your key: "
            )
        else:
            new_value = current_value
        replace_key(dotenv_path, key, new_value)


def ask_choice(prompt: str, choices: List[str]) -> str:
    """Prompt the user to select a choice from the given list."""

    while True:
        print(prompt)
        for i, choice in enumerate(choices, start=1):
            print(f"{i}. {choice}")
        try:
            choice_index = int(input("Enter the number of your choice: ")) - 1
            if 0 <= choice_index < len(choices):
                return choices[choice_index]
            else:
                print("Invalid choice. Please try again.")
        except ValueError:
            print("Invalid input. Please enter a number.")


def select_graph_type() -> str:
    """Prompt the user to select a graph type."""

    valid_options = [e.value for e in SymbolGraphType]
    valid_options = [re.escape(option) for option in valid_options]
    options_string = "".join(valid_options)

    prompt = f"Select graph type from {options_string}: "
    while True:
        user_input = input(prompt).strip().lower()
        if user_input in valid_options:
            return user_input
        else:
            print(f"Invalid choice. Please select from {options_string}")


def show_key_value(dotenv_path: str, key: str) -> None:
    """Shows the key value to the user."""

    value = get_key(dotenv_path, key)
    log_cli_output(f"The value of {key} is: {value}")


def update_key_value(dotenv_path: str, key: str) -> None:
    """Updates the key value in the local task_environment."""

    if key == "DATA_ROOT_PATH":
        choice = ask_choice(f"Select {key} source", ["Default", "Custom"])
        if choice == "Default":
            replace_key(
                dotenv_path,
                key,
                "automata-embedding-data",
            )
        else:
            new_value = input(f"Enter custom value for {key}: ")
            replace_key(dotenv_path, key, new_value)
    else:
        new_value = input(f"Enter new value for {key}: ")
        replace_key(dotenv_path, key, new_value)
    log_cli_output(f"The value of {key} has been updated.")


def update_graph_type(dotenv_path: str, graph_type: str) -> None:
    """Updates the type in the local environment."""

    replace_key(dotenv_path, "GRAPH_TYPE", graph_type)
    log_cli_output(f"The graph type has been updated to {graph_type}.")


def delete_key_value(dotenv_path: str, key: str) -> None:
    """Deletes the key from the local task_environment."""

    user_confirmation = input(
        f"Are you sure you want to delete the value of {key}? [y/n]: "
    )
    if user_confirmation.lower() == "y":
        replace_key(dotenv_path, key, "")
        log_cli_output(f"The value of {key} has been deleted.")
    else:
        log_cli_output(
            f"Operation cancelled. The value of {key} has not been deleted."
        )
