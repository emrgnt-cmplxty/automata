import json
import logging
import os
from typing import Any, Dict, List, Optional, TypedDict, Union, cast

import yaml


def root_py_fpath() -> str:
    """
    Get the path to the root of the project python code

    Returns:
        str - A fpath object in string form

    """
    script_dir = os.path.dirname(os.path.realpath(__file__))
    data_folder = os.path.join(script_dir, "..")
    return data_folder


def root_fpath() -> str:
    """
    Returns the path to the root of the project directory.

    Returns:
        str - A fpath object in string form

    """
    data_folder = os.path.join(root_py_fpath(), "..")
    return data_folder


def config_fpath() -> str:
    """
    Get the path to the project config directory

    Returns:
        str - A fpath object in string form

    """
    data_folder = os.path.join(root_py_fpath(), "config")
    return data_folder


def load_config(
    config_name: str,
    file_name: str,
    config_type: str = "yaml",
    custom_decoder: Any = None,
) -> Any:
    """
    Loads a config file from the config directory

    Args:
        file_path (str): The path to the YAML file

    Returns:
        Any: The content of the YAML file as a Python object
    """
    with open(
        os.path.join(config_fpath(), config_name, f"{file_name}.{config_type}"),
        "r",
    ) as file:
        if config_type == "yaml":
            return yaml.safe_load(file)
        elif config_type == "json":
            samples_json_string = file.read()
            return json.loads(samples_json_string, object_hook=custom_decoder)


class HandlerDict(TypedDict):
    """A dictionary representing a logging handler"""

    class_: str
    formatter: str
    level: int
    filename: Optional[str]


class RootDict(TypedDict):
    """A dictionary representing the root logger"""

    handlers: List[str]
    level: int


class LoggingConfig(TypedDict, total=False):
    """A dictionary representing the logging configuration"""

    version: int
    disable_existing_loggers: bool
    formatters: dict
    handlers: dict[str, Union[HandlerDict, dict]]
    root: RootDict


def get_logging_config(
    log_level: int = logging.INFO, log_file: Optional[str] = None
) -> dict[str, Any]:
    """
    Returns logging configuration.

    Args:
        log_level (int): The log level.
        log_file (Optional[str]): The log file path.
    Returns
        dict[str, Any]: The logging configuration.
    """
    logging_config: LoggingConfig = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "standard": {  # a standard formatter for file handler
                "format": "%(asctime)s - %(levelname)s - %(name)s - %(message)s",
            },
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "formatter": "standard",
                "level": log_level,
            }
        },
        "root": {"handlers": ["console"], "level": log_level},
    }
    if log_file:  # if log_file is provided, add file handler
        logging_config["handlers"]["file"] = {
            "class": "logging.FileHandler",
            "filename": log_file,
            "formatter": "standard",
            "level": log_level,
        }
        logging_config["root"]["handlers"].append("file")  # add "file" to handlers

    return cast(dict[str, Any], logging_config)


def format_text(format_variables: Dict[str, str], input_text: str) -> str:
    """Format expected strings into the config."""
    for arg in format_variables:
        input_text = input_text.replace(f"{{{arg}}}", format_variables[arg])
    return input_text
