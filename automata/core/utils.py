import json
import logging
import os
from typing import Any, Dict, List, Optional, TypedDict, Union, cast

import colorlog
import numpy as np
import openai
import yaml

from automata.embedding.base import EmbeddingVectorProvider


def set_openai_api_key(override_key: Optional[str] = None) -> None:
    """Sets the OpenAI API key from the environment variable OPENAI_API_KEY"""
    if not openai.api_key:
        from automata.config import OPENAI_API_KEY

        openai.api_key = override_key or OPENAI_API_KEY


def get_root_py_fpath() -> str:
    """Get the path to the root of the Automata python code directory."""
    script_dir = os.path.dirname(os.path.realpath(__file__))
    return os.path.join(script_dir, "..")


def get_root_fpath() -> str:
    """Get the path to the root of the Automata directory."""
    return os.path.join(get_root_py_fpath(), "..")


def get_embedding_data_fpath() -> str:
    """Get the path to the root of the Automata config directory."""
    return os.path.join(get_root_fpath(), "automata-embedding-data")


def get_config_fpath() -> str:
    """Get the path to the root of the Automata config directory."""
    return os.path.join(get_root_py_fpath(), "config")


def load_config(
    config_name: str,
    file_name: str,
    config_type: str = "yaml",
    custom_decoder: Any = None,
) -> Any:
    """Loads a config file from the config directory"""
    with open(
        os.path.join(
            get_config_fpath(), config_name, f"{file_name}.{config_type}"
        ),
        "r",
    ) as file:
        if config_type == "yaml":
            return yaml.safe_load(file)
        elif config_type == "json":
            samples_json_string = file.read()
            return json.loads(samples_json_string, object_hook=custom_decoder)


def format_text(format_variables: Dict[str, str], input_text: str) -> str:
    """Format expected strings into the config."""
    for arg in format_variables:
        input_text = input_text.replace(f"{{{arg}}}", format_variables[arg])
    return input_text


def convert_kebab_to_snake_case(s: str) -> str:
    """Convert a kebab-case string to snake_case."""
    return s.replace("-", "_")


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
            "colored": {
                "()": colorlog.ColoredFormatter,
                "format": "%(log_color)s%(levelname)s:%(name)s:%(message)s",
                "log_colors": color_scheme,
            },
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
        logging_config["root"]["handlers"].append(
            "file"
        )  # add "file" to handlers

    return cast(dict[str, Any], logging_config)


def is_sorted(lst):
    return all(a <= b for a, b in zip(lst, lst[1:]))


def calculate_similarity(
    content_a: str, content_b: str, provider: EmbeddingVectorProvider
) -> float:
    """Calculate the similarity between two strings."""
    embedding_a = provider.build_embedding_vector(content_a)
    embedding_b = provider.build_embedding_vector(content_b)
    dot_product = np.dot(embedding_a, embedding_b)
    magnitude_a = np.sqrt(np.dot(embedding_a, embedding_a))
    magnitude_b = np.sqrt(np.dot(embedding_b, embedding_b))
    return dot_product / (magnitude_a * magnitude_b)
