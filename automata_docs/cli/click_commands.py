import logging
import logging.config
from typing import Any, List, Optional, TypedDict, Union, cast

import click

from .click_options import common_options


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


def reconfigure_logging(log_level_str: str):
    """
    Configure the logging settings.

    :param verbose: Boolean, if True, set log level to DEBUG, else set to INFO.
    """
    log_level = logging.DEBUG

    if log_level_str == "INFO":
        log_level = logging.INFO
    elif log_level_str != "DEBUG":
        raise ValueError(f"Unknown log level: {log_level_str}")

    logging_config = get_logging_config(log_level=log_level)
    logging.config.dictConfig(logging_config)

    # Avoid spam from the aux libraries
    requests_logger = logging.getLogger("urllib3")
    requests_logger.setLevel(logging.INFO)
    matplotlib_logger = logging.getLogger("matplotlib")
    matplotlib_logger.setLevel(logging.INFO)
    # openai_logger = logging.getLogger("openai")
    # openai_logger.setLevel(logging.INFO)


@click.group()
@click.pass_context
def cli(ctx):
    pass


@common_options
@cli.command()
@click.option(
    "--index_file",
    default="index.scip",
    help="Which index file to use for the embedding modifications.",
)
@click.option(
    "--embedding_file",
    default="symbol_code_embedding.json",
    help="Which embedding file to save to.",
)
@click.pass_context
def run_code_embedding(ctx, *args, **kwargs):
    """Run the code embedding pipeline."""
    from automata_docs.cli.scripts.run_code_embedding import main

    reconfigure_logging(kwargs.get("log_level", "DEBUG"))
    main(kwargs)


@common_options
@cli.command()
@click.option(
    "--index_file",
    default="index.scip",
    help="Which index file to use for the embedding modifications.",
)
@click.option(
    "--embedding_file",
    default="symbol_doc_embedding.json",
    help="Which embedding file to save to.",
)
@click.pass_context
def run_doc_embedding_l2(ctx, *args, **kwargs):
    """Run the document embedding Level-2 pipeline."""
    from automata_docs.cli.scripts.run_doc_embedding_l2 import main

    print("Calling run_doc_embedding_l2")
    reconfigure_logging(kwargs.get("log_level", "DEBUG"))
    main(kwargs)
