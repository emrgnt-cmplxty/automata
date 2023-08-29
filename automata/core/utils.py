"""
Utility functions for Automata.
"""
import json
import logging
import logging.config
import os
from typing import (
    Any,
    Dict,
    List,
    Optional,
    TypedDict,
    Union,
    cast,
)

import colorlog
import openai


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


class ColorConfig:
    """A class representing the color scheme for the CLI"""

    color_scheme: ColorScheme = {
        "DEBUG": "cyan",
        "INFO": "green",
        "WARNING": "yellow",
        "ERROR": "red",
        "CRITICAL": "bold_red",
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


def configure_logging(log_level_str: str) -> None:
    """Reconfigures the logging for the local project."""

    log_level = logging.INFO
    if log_level_str == "INFO":
        log_level = logging.INFO
    elif log_level_str == "DEBUG":
        log_level = logging.DEBUG
    else:
        raise ValueError(f"Unknown log level: {log_level_str}")

    logging_config = get_logging_config(log_level=log_level)
    logging.config.dictConfig(logging_config)

    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)
    logging.getLogger(__name__).setLevel(
        log_level
    )  # Explicitly set the level for the current module's logger

    # External libraries we want to quiet down
    for library in ["urllib3", "matplotlib", "openai", "github", "asyncio"]:
        logging.getLogger(library).setLevel(logging.INFO)


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


def is_sorted(lst: list) -> bool:
    """Check if a list is sorted."""

    return all(a <= b for a, b in zip(lst, lst[1:]))
