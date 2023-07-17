import logging
import logging.config

import click

from automata.cli.cli_utils import ask_choice, get_custom_style, setup_files
from automata.cli.env_operations import (
    delete_key_value,
    load_env_vars,
    show_key_value,
    update_key_value,
)
from automata.cli.options import agent_options, common_options
from automata.core.utils import get_logging_config

logger = logging.getLogger(__name__)


def reconfigure_logging(log_level_str: str) -> None:
    log_level = logging.DEBUG
    if log_level_str == "INFO":
        log_level = logging.INFO
    elif log_level_str != "DEBUG":
        raise ValueError(f"Unknown log level: {log_level_str}")
    logging_config = get_logging_config(log_level=log_level)
    logging.config.dictConfig(logging_config)
    # External libraries we want to quiet down
    for library in ["urllib3", "matplotlib", "openai", "github"]:
        logging.getLogger(library).setLevel(logging.INFO)


@click.group()
@click.pass_context
def cli(ctx) -> None:
    pass


@common_options
@cli.command() # type: ignore
@click.pass_context
def configure(ctx, *args, **kwargs) -> None:
    """Configure Automata"""

    DOTENV_PATH = ".env"
    SCRIPTS_PATH = "scripts/"
    DEFAULT_KEYS = {
        "GITHUB_API_KEY": "your_github_api_key",
        "OPENAI_API_KEY": "your_openai_api_key",
    }

    setup_files(SCRIPTS_PATH=SCRIPTS_PATH, DOTENV_PATH=DOTENV_PATH)
    load_env_vars(DOTENV_PATH=DOTENV_PATH, DEFAULT_KEYS=DEFAULT_KEYS)

    logger.info("Configuring Automata:")

    config_choice = ask_choice(
        "Select key to configure", list(DEFAULT_KEYS.keys())
    )
    operation_choice = ask_choice(
        "Select operation", ["Show", "Update", "Delete"]
    )

    if operation_choice == "Show":
        show_key_value(DOTENV_PATH, config_choice)
    elif operation_choice == "Update":
        update_key_value(DOTENV_PATH, config_choice)
    elif operation_choice == "Delete":
        delete_key_value(DOTENV_PATH, config_choice)


@common_options
@cli.command() # type: ignore
@click.pass_context
def run_code_embedding(ctx, *args, **kwargs) -> None:
    """Run the code embedding pipeline."""
    from automata.cli.scripts.run_code_embedding import main

    reconfigure_logging(kwargs.get("log-level", "DEBUG"))
    logger.info("Calling run_code_embedding")
    main(**kwargs)


@common_options
@cli.command() # type: ignore
@click.pass_context
@click.option(
    "--embedding-level", type=int, default=2, help="Level of the embedding."
)
def run_doc_embedding(ctx, *args, **kwargs) -> None:
    from automata.cli.scripts.run_doc_embedding import main

    """Run the document embedding pipeline."""
    reconfigure_logging(kwargs.get("log-level", "DEBUG"))
    logger.info("Calling run_doc_embedding")
    result = main(*args, **kwargs)
    logger.info(f"Result = {result}")


@common_options
@cli.command() # type: ignore
@click.pass_context
def run_doc_post_process(ctx, *args, **kwargs) -> None:
    """Run the document post-processor."""
    from automata.cli.scripts.run_doc_post_process import main

    reconfigure_logging(kwargs.get("log-level", "DEBUG"))
    logger.info("Running doc post-process")
    main(**kwargs)


@common_options
@agent_options
@cli.command() # type: ignore
@click.option(
    "--fetch-issues",
    default="",
    help="Comma-separated list of issue numbers to fetch",
)
@click.pass_context
def run_agent(ctx, *args, **kwargs) -> None:
    """Run the agent."""
    from automata.cli.scripts.run_agent import main

    reconfigure_logging(kwargs.get("log-level", "DEBUG"))
    logger.info("Running agent")
    main(**kwargs)
