import logging
import logging.config

import click

from automata.cli.cli_output_logger import CustomLogger
from automata.cli.cli_utils import ask_choice, setup_files
from automata.cli.env_operations import (
    delete_key_value,
    load_env_vars,
    show_key_value,
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
def cli(ctx) -> None:
    pass


@common_options
@cli.command()
@click.pass_context
def configure(ctx, *args, **kwargs) -> None:
    """Configures the Automata"""
    # TODO - Can we add a few more lines of comments here?

    logger.info("Configuring Automata:")

    reconfigure_logging(kwargs.get("log-level", "INFO"))

    DOTENV_PATH = ".env"
    SCRIPTS_PATH = "scripts/"
    DEFAULT_KEYS = {
        "GITHUB_API_KEY": "your_github_api_key",
        "OPENAI_API_KEY": "your_openai_api_key",
    }

    setup_files(scripts_path=SCRIPTS_PATH, dotenv_path=DOTENV_PATH)
    load_env_vars(dotenv_path=DOTENV_PATH, default_keys=DEFAULT_KEYS)

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
@cli.command()
@click.pass_context
def build(ctx, *args, **kwargs) -> None:
    """Run the install_index script."""

    from automata.cli.build import generate_local_indices, install_indexing

    reconfigure_logging(kwargs.get("log-level", "DEBUG"))

    logger.info("Running install_index")
    install_indexing()

    logger.info("Running generate_local_indices")
    generate_local_indices()


@common_options
@cli.command()
@click.pass_context
def run_code_embedding(ctx, *args, **kwargs) -> None:
    """Run the code embedding pipeline."""

    from automata.cli.scripts.run_code_embedding import main

    reconfigure_logging(kwargs.get("log-level", "DEBUG"))
    logger.info("Calling run_code_embedding")
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
def run_doc_embedding(ctx, symbols, overwrite, *args, **kwargs) -> None:
    from automata.cli.scripts.run_doc_embedding import main

    reconfigure_logging(kwargs.get("log-level", "DEBUG"))
    logger.info("Calling run_doc_embedding")

    result = main(overwrite=overwrite, *args, **kwargs)
    logger.info(f"Result = {result}")


@common_options
@cli.command()
@click.pass_context
def run_doc_post_process(ctx, *args, **kwargs) -> None:
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
def run_agent(ctx, *args, **kwargs) -> None:
    """Run the agent."""
    from automata.cli.scripts.run_agent import main

    reconfigure_logging("DEBUG")  # kwargs.get("log-level", "DEBUG"))
    # reconfigure_logging(kwargs.get("log-level", "DEBUG"))
    logger.info("Running agent")
    main(**kwargs)


@common_options
@agent_options
@eval_options
@cli.command()
@click.pass_context
def run_eval(ctx, *args, **kwargs) -> None:
    """
    Run the evaluation.

    Here is an exmaple command -
    poetry run automata run-eval --evals-filepath=automata/config/eval/primary_agent_payload.json --model="gpt-4" --toolkits="document-oracle,py-reader" --log-level=DEBUG --max-iterations=3


    """
    from automata.cli.scripts.run_eval import main

    if kwargs.get("instructions"):
        raise ValueError("Instructions should not be passed to run_eval")

    reconfigure_logging(kwargs.get("log-level", "DEBUG"))
    logger.info("Running Evaluation")
    main(**kwargs)
