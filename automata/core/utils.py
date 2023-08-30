"""
Utility functions for Automata.
"""
import json
import logging
import os
from typing import (
    TYPE_CHECKING,
    Any,
    Dict,
    List,
    Optional,
    Tuple,
    Type,
    TypedDict,
    Union,
    cast,
)

import colorlog
import numpy as np
import openai
import yaml
import time
from functools import wraps

from automata.cli.cli_output_logger import CLI_OUTPUT_LEVEL

if TYPE_CHECKING:
    from automata.embedding.embedding_base import EmbeddingVectorProvider


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


class LoggerDict(TypedDict):
    """A dictionary representing a specific logger configuration"""

    handlers: List[str]
    level: int
    propagate: bool


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
    loggers: dict[str, LoggerDict]
    root: RootDict


class ColorScheme(TypedDict):
    """A dictionary representing the color scheme for the CLI"""

    DEBUG: str
    INFO: str
    WARNING: str
    ERROR: str
    CRITICAL: str
    CLI_OUTPUT: str


class ColorConfig:
    """A class representing the color scheme for the CLI"""

    color_scheme: ColorScheme = {
        "DEBUG": "cyan",
        "INFO": "green",
        "WARNING": "yellow",
        "ERROR": "red",
        "CRITICAL": "bold_red",
        "CLI_OUTPUT": "bold_white",
    }


def ensure_stream_handler_for_root() -> None:
    """Ensure the root logger has a StreamHandler with colored formatting."""
    root_logger = logging.getLogger()
    if not any(
        isinstance(handler, logging.StreamHandler)
        for handler in root_logger.handlers
    ):
        stream_handler = logging.StreamHandler()
        colored_formatter = colorlog.ColoredFormatter(
            "%(log_color)s%(message)s",
            log_colors=cast(Dict[str, str], ColorConfig.color_scheme),
        )
        stream_handler.setFormatter(colored_formatter)
        root_logger.addHandler(stream_handler)


def get_logging_config(
    log_level: int = logging.DEBUG, log_file: Optional[str] = None
) -> dict[str, Any]:
    """Returns logging configuration."""

    # Call the function to ensure root logger has a StreamHandler with the correct formatter
    ensure_stream_handler_for_root()

    logging_config: LoggingConfig = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "colored": {
                "()": colorlog.ColoredFormatter,
                "format": "%(log_color)s%(message)s",
                "log_colors": cast(Dict[str, str], ColorConfig.color_scheme),
            },
            "standard": {
                "format": "%(message)s",
            },
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "level": log_level,  # Set handler level to the passed log_level
                "formatter": "colored",
                "stream": "ext://sys.stdout",
            },
            "cli_output": {
                "class": "logging.StreamHandler",
                "formatter": "colored",
                "level": CLI_OUTPUT_LEVEL,
            },
        },
        "loggers": {
            "automata": {
                "handlers": ["console"],
                "level": log_level,  # Set automata logger level to the passed log_level
                "propagate": False,
            }
        },
        "root": {"handlers": ["console"], "level": log_level},
    }

    if log_file:
        logging_config["handlers"]["file"] = {
            "class": "logging.FileHandler",
            "filename": log_file,
            "formatter": "standard",
            "level": log_level,
        }
        logging_config["root"]["handlers"].append("file")

    return cast(dict[str, Any], logging_config)


def is_sorted(lst):
    """Check if a list is sorted."""

    return all(a <= b for a, b in zip(lst, lst[1:]))


def calculate_similarity(
    content_a: str, content_b: str, provider: "EmbeddingVectorProvider"
) -> float:
    """Calculate the similarity between two strings."""

    embedding_a = provider.build_embedding_vector(content_a)
    embedding_b = provider.build_embedding_vector(content_b)
    dot_product = np.dot(embedding_a, embedding_b)
    magnitude_a = np.sqrt(np.dot(embedding_a, embedding_a))
    magnitude_b = np.sqrt(np.dot(embedding_b, embedding_b))
    return dot_product / (magnitude_a * magnitude_b)


def retry(max_retries: int = 3, initial_delay: float = 1.0, max_delay: Optional[float] = None, allowed_exceptions: Tuple[Type[BaseException], ...] = ()) -> Any:
    """
    Retry calling the decorated function using an exponential backoff.
    """

    def decorator(func: Any) -> Any:
        """A decorator for retrying a function or method in case of exceptions with exponential backoff."""
        @wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            """A wrapper for retrying a function or method in case of exceptions with exponential backoff."""
            delay = initial_delay
            for _ in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except allowed_exceptions or Exception as e:
                    if _ == max_retries - 1:
                        raise e
                    time.sleep(delay)
                    delay *= 2.0
                    if max_delay:
                        delay = min(delay, max_delay)

        return wrapper

    return decorator