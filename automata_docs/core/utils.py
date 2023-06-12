import json
import logging
import os
from typing import Any, Dict, List, Optional, TypedDict, Union, cast

import numpy as np
import openai
import yaml


def format_text(format_variables: Dict[str, str], input_text: str) -> str:
    """Format expected strings into the config."""
    for arg in format_variables:
        input_text = input_text.replace(f"{{{arg}}}", format_variables[arg])
    return input_text


def root_py_path() -> str:
    """
    Returns the path to the root of the project python code.

    Returns:
    - A path object in string form

    """
    script_dir = os.path.dirname(os.path.realpath(__file__))
    data_folder = os.path.join(script_dir, "..")
    return data_folder


def config_path() -> str:
    """
    Returns the path to the project config directory

    Returns:
    - A path object in string form

    """
    script_dir = os.path.dirname(os.path.realpath(__file__))
    data_folder = os.path.join(script_dir, "..", "configs")
    return data_folder


def load_config(
    config_name: str,
    file_name: str,
    config_type: str = "yaml",
    custom_decoder: Any = None,
) -> Any:
    """
    Loads a config file.

    Args:
        file_path (str): The path to the YAML file.

    Returns:
        Any: The content of the YAML file as a Python object.
    """
    with open(
        os.path.join(config_path(), config_name, f"{file_name}.{config_type}"),
        "r",
    ) as file:
        if config_type == "yaml":
            return yaml.safe_load(file)
        elif config_type == "json":
            samples_json_string = file.read()
            return json.loads(samples_json_string, object_hook=custom_decoder)


def root_path() -> str:
    """
    Returns the path to the root of the project directory.

    Returns:
    - A path object in string form

    """
    script_dir = os.path.dirname(os.path.realpath(__file__))
    data_folder = os.path.join(script_dir, "..", "..")
    return data_folder


class HandlerDict(TypedDict):
    class_: str
    formatter: str
    level: int
    filename: Optional[str]


class RootDict(TypedDict):
    handlers: List[str]
    level: int


class LoggingConfig(TypedDict, total=False):
    version: int
    disable_existing_loggers: bool
    formatters: dict
    handlers: dict[str, Union[HandlerDict, dict]]
    root: RootDict


def get_logging_config(
    log_level: int = logging.INFO, log_file: Optional[str] = None
) -> dict[str, Any]:
    """Returns logging configuration."""
    color_scheme = {
        "DEBUG": "cyan",
        "INFO": "green",
        "WARNING": "yellow",
        "ERROR": "red",
        "CRITICAL": "bold_red",
    }
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
                "formatter": "colored",
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


def calculate_similarity(
    content_a: str, content_b: str, engine: str = "text-embedding-ada-002"
) -> float:
    """Calculate the similarity between two strings."""
    resp = openai.Embedding.create(input=[content_a, content_b], engine=engine)
    embedding_a = resp["data"][0]["embedding"]
    embedding_b = resp["data"][1]["embedding"]
    dot_product = np.dot(embedding_a, embedding_b)
    magnitude_a = np.sqrt(np.dot(embedding_a, embedding_a))
    magnitude_b = np.sqrt(np.dot(embedding_b, embedding_b))
    return dot_product / (magnitude_a * magnitude_b)
