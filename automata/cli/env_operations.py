import logging
from typing import Dict

from dotenv import load_dotenv

from automata.cli.cli_output_logger import CLI_OUTPUT_LEVEL, CustomLogger

logging.setLoggerClass(CustomLogger)
logger = logging.getLogger(__name__)
logger.setLevel(CLI_OUTPUT_LEVEL)


def log_cli_output(message):
    """An override to log cli output messages"""

    logger.log(CLI_OUTPUT_LEVEL, message)


def get_key(dotenv_path: str, key_to_get: str):
    """Get an existing key from a .env file."""

    with open(dotenv_path, "r") as file:
        lines = file.readlines()

    for line in lines:
        key, _, value = line.partition("=")
        if key == key_to_get:
            return value.rstrip()


def replace_key(dotenv_path: str, key_to_set: str, value_to_set: str):
    """Replace an existing key in a .env file."""

    with open(dotenv_path, "r") as file:
        lines = file.readlines()

    for i, line in enumerate(lines):
        key, _, _ = line.partition("=")
        if key == key_to_set:
            lines[i] = f"{key_to_set}={value_to_set}\n"

    with open(dotenv_path, "w") as file:
        file.writelines(lines)


def load_env_vars(dotenv_path: str, default_keys: Dict[str, str]):
    """Loads the env variables into the local env."""
    load_dotenv()

    for key, default_value in default_keys.items():
        current_value = get_key(dotenv_path, key)
        if (
            current_value is None
            and key == "GRAPH_TYPE"
            or current_value is not None
            and (not current_value or current_value == default_value)
            and key == "GRAPH_TYPE"
        ):
            new_value = "dynamic"
        elif current_value is None:
            raise ValueError(f"Key {key} not found in the .env file")
        elif not current_value or current_value == default_value:
            new_value = input(
                f"{key} is not configured. Please enter your key: "
            )
        else:
            new_value = current_value
        replace_key(dotenv_path, key, new_value)


def show_key_value(dotenv_path: str, key: str):
    """Shows the key value to the user."""

    value = get_key(dotenv_path, key)
    log_cli_output(f"The value of {key} is: {value}")


def update_key_value(dotenv_path: str, key: str):
    """Updates the key value in the local environment."""

    new_value = input(f"Enter new value for {key}: ")
    replace_key(dotenv_path, key, new_value)
    log_cli_output(f"The value of {key} has been updated.")


def update_graph_type(dotenv_path: str, type: str):
    """Updates the type in the local environment."""

    replace_key(dotenv_path, "GRAPH_TYPE", type)
    log_cli_output(f"The graph type has been updated to {type}.")


def delete_key_value(dotenv_path: str, key: str):
    """Deletes the key from the local environment."""

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
