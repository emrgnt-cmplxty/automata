import logging
import logging.config

import click

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

    reconfigure_logging(kwargs.get("log-level", "DEBUG"))
    logger.info("Running agent")
    main(**kwargs)
