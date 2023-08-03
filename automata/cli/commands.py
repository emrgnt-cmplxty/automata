"""
This module contains the CLI commands for the Automata CLI.
"""

import logging
import logging.config
from typing import Optional

import click

from automata.cli.cli_output_logger import CLI_OUTPUT_LEVEL, CustomLogger
from automata.cli.cli_utils import ask_choice, setup_files
from automata.cli.env_operations import (
    delete_key_value,
    load_env_vars,
    replace_key,
    show_key_value,
    update_graph_type,
    update_key_value,
)
from automata.cli.options import agent_options, common_options, eval_options
from automata.core.utils import get_logging_config

logging.setLoggerClass(CustomLogger)
logger = logging.getLogger(__name__)


def reconfigure_logging(log_level_str: str) -> None:
    """Reconfigures the logging for the local project."""

    log_level = logging.DEBUG
    if log_level_str == "INFO":
        log_level = logging.INFO
    elif log_level_str == "CLI_OUTPUT":
        log_level = CLI_OUTPUT_LEVEL
    elif log_level_str != "DEBUG":
        raise ValueError(f"Unknown log level: {log_level_str}")

    logging_config = get_logging_config(log_level=log_level)
    logging.config.dictConfig(logging_config)

    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)

    # External libraries we want to quiet down
    for library in ["urllib3", "matplotlib", "openai", "github"]:
        logging.getLogger(library).setLevel(logging.INFO)


@click.group()
@click.pass_context
def cli(ctx: click.Context) -> None:
    """Automata CLI"""

    pass


@common_options
@cli.command()
@click.option("--GITHUB_API_KEY", default="", help="GitHub API key")
@click.option("--OPENAI_API_KEY", default="", help="OpenAI API key")
@click.pass_context
def configure(
    ctx: click.Context,
    github_api_key: Optional[str],
    openai_api_key: Optional[str],
    *args,
    **kwargs,
) -> None:
    """
    Configures environment variables for Automata

    This command uses click to create an interactive CLI command for configuring
    envirnoment variables. Upon running the automata configure command, the .env
    is created if it doesn't already exist and the user is prompted to enter the
    values for their environment variables. This ensures that the user does not
    have to manually edit the .env file.
    """

    logger.info("Configuring Automata:")

    reconfigure_logging(kwargs.get("log-level", "INFO"))

    DOTENV_PATH = ".env"
    SCRIPTS_PATH = "scripts/"
    DEFAULT_KEYS = {
        "GITHUB_API_KEY": "your_github_api_key",
        "OPENAI_API_KEY": "your_openai_api_key",
        "GRAPH_TYPE": "dynamic",
        "DATA_ROOT_PATH": "automata-embedding-data",
    }

    setup_files(scripts_path=SCRIPTS_PATH, dotenv_path=DOTENV_PATH)
    load_env_vars(dotenv_path=DOTENV_PATH, default_keys=DEFAULT_KEYS)

    if github_api_key:
        replace_key(DOTENV_PATH, "GITHUB_API_KEY", github_api_key)

    if openai_api_key:
        replace_key(DOTENV_PATH, "OPENAI_API_KEY", openai_api_key)

    if github_api_key and openai_api_key:
        return

    logger.info("Configuring Automata:")

    while True:
        config_choice = ask_choice(
            "Select item to configure", list(DEFAULT_KEYS.keys()) + ["Exit"]
        )
        if config_choice == "Exit":
            break

        operation_choice = ask_choice(
            "Select operation", ["Show", "Update", "Delete"]
        )

        if operation_choice == "Show":
            show_key_value(DOTENV_PATH, config_choice)
        elif operation_choice == "Update":
            if config_choice != "GRAPH_TYPE":
                update_key_value(DOTENV_PATH, config_choice)
            else:
                graph_choice = ask_choice(
                    "Select graph type", ["dynamic", "static"]
                )
                update_graph_type(DOTENV_PATH, graph_choice)
        elif operation_choice == "Delete":
            delete_key_value(DOTENV_PATH, config_choice)


@common_options
@cli.command()
@click.pass_context
def install_indexing(ctx: click.Context, *args, **kwargs) -> None:
    """Run the install_index script."""

    from automata.cli.install_indexing import (
        generate_local_indices,
        install_indexing,
    )

    reconfigure_logging(kwargs.get("log-level", "DEBUG"))

    logger.info("Installing indices")
    install_indexing()

    logger.info("Generating local indices")
    generate_local_indices()


@common_options
@cli.command()
@click.pass_context
def run_code_embedding(ctx: click.Context, *args, **kwargs) -> None:
    """Run the code embedding pipeline."""

    from automata.cli.scripts.run_code_embedding import main

    reconfigure_logging(kwargs.get("log-level", "INFO"))
    logger.debug("Calling run_code_embedding")
    main(**kwargs)


@common_options
@cli.command()
@click.pass_context
@click.argument("symbols", nargs=-1)
@click.option(
    "--embedding-level", type=int, default=2, help="Level of the embedding."
)
@click.option(
    "--overwrite",
    is_flag=True,
    default=False,
    help="Overwrite the existing doc embeddings in the database.",
)
def run_doc_embedding(
    ctx: click.Context, symbols: str, overwrite: bool, *args, **kwargs
) -> None:
    """Run the document embedding pipeline."""

    from automata.cli.scripts.run_doc_embedding import main

    reconfigure_logging(kwargs.get("log-level", "INFO"))
    logger.info("Calling run_doc_embedding")

    result = main(overwrite=overwrite, *args, **kwargs)
    logger.info(f"Result = {result}")


@common_options
@cli.command()
@click.pass_context
def run_doc_post_process(ctx: click.Context, *args, **kwargs) -> None:
    """Run the document post-processor."""

    from automata.cli.scripts.run_doc_post_process import main

    reconfigure_logging(kwargs.get("log-level", "DEBUG"))
    logger.info("Running doc post-process")
    main(**kwargs)


@common_options
@agent_options
@cli.command()
@click.option(
    "--fetch-issues",
    default="",
    help="Comma-separated list of issue numbers to fetch",
)
@click.pass_context
def run_agent(ctx: click.Context, *args, **kwargs) -> None:
    """
    Run the automata agent.

    Ex:
    poetry run automata run-agent --model="gpt-4" --toolkits="agent-search" --log-level=DEBUG --max-iterations=3 --instructions="Return a markdown snippet containing python code which creates an instance of symbol search  and stores it into a variable `x` when executed."

    """
    from automata.cli.scripts.run_agent import main

    reconfigure_logging(kwargs.get("log-level", "DEBUG"))
    logger.info("Running agent")
    main(**kwargs)


@common_options
@agent_options
@eval_options
@cli.command()
@click.pass_context
def run_agent_eval(ctx: click.Context, *args, **kwargs) -> None:
    """
    Run the evaluation.

    Ex:
    poetry run automata run-agent-eval --evals-filepath=automata/config/eval/primary_agent_payload.json --model="gpt-4" --toolkits="document-oracle,py-reader" --log-level=DEBUG --max-iterations=3
    """

    from automata.cli.scripts.run_agent_eval import main

    if kwargs.get("instructions"):
        raise ValueError("Instructions should not be passed to run_agent_eval")

    reconfigure_logging(kwargs.get("log-level", "DEBUG"))
    logger.info("Running Evaluation")
    main(**kwargs)


@common_options
@agent_options
@eval_options
@cli.command()
@click.pass_context
def run_tool_eval(ctx: click.Context, *args, **kwargs) -> None:
    """
    Run the evaluation.

    Here is an exmaple command -
    poetry run automata run-tool-eval --evals-filepath=automata/config/eval/single_target_search_payload.json --toolkits="symbol-search" --log-level=DEBUG

    """

    from automata.cli.scripts.run_tool_eval import main

    if kwargs.get("instructions"):
        raise ValueError("Instructions should not be passed to run_agent_eval")

    reconfigure_logging(kwargs.get("log-level", "DEBUG"))
    logger.info("Running Evaluation")
    main(**kwargs)
