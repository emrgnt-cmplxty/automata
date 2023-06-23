import logging
import logging.config

import click

from automata.core.utils import get_logging_config

from .options import agent_options, common_options

logger = logging.getLogger(__name__)


def reconfigure_logging(log_level_str: str) -> None:
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
    matplotlib_logger = logging.getLogger("openai")
    matplotlib_logger.setLevel(logging.INFO)


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

    reconfigure_logging(kwargs.get("log_level", "DEBUG"))
    logger.info("Calling run_code_embedding")
    main(**kwargs)


@common_options
@cli.command()
@click.pass_context
def run_doc_embedding_l2(ctx, *args, **kwargs) -> None:
    """Run the document embedding Level-2 pipeline."""
    from automata.cli.scripts.run_doc_embedding_l2 import main

    reconfigure_logging(kwargs.get("log_level", "DEBUG"))
    logger.info("Calling run_doc_embedding_l2")
    main(**kwargs)


@common_options
@cli.command()
@click.pass_context
def run_doc_embedding_l3(ctx, *args, **kwargs) -> None:
    """Run the document embedding Level-3 pipeline."""
    from automata.cli.scripts.run_doc_embedding_l3 import main

    reconfigure_logging(kwargs.get("log_level", "DEBUG"))
    logger.info("Calling run_doc_embedding_l3")
    main(**kwargs)


@common_options
@cli.command()
@click.pass_context
def run_doc_post_process(ctx, *args, **kwargs) -> None:
    """Run the document post-processor."""
    from automata.cli.scripts.run_doc_post_process import main

    reconfigure_logging(kwargs.get("log_level", "DEBUG"))
    logger.info("Running doc post-process")
    main(**kwargs)


@common_options
@agent_options
@cli.command()
@click.pass_context
def run_agent(ctx, *args, **kwargs) -> None:
    """Run the agent."""
    from automata.cli.scripts.run_agent import main

    reconfigure_logging(kwargs.get("log_level", "DEBUG"))
    logger.info("Running agent")
    main(**kwargs)


@common_options
@agent_options
@cli.command()
@click.option("--fetch-issues", default="", help="Comma-separated list of issue numbers to fetch")
@click.pass_context
def run_agent_task(ctx, *args, **kwargs) -> None:
    """
    Run an agent task.

    Note - This is similar to run_agent, but executes the agent
    within the task framework. This allows for more flexibility
    across multiple tasks.

    """
    from automata.cli.scripts.run_agent_task import main

    reconfigure_logging(kwargs.get("log_level", "DEBUG"))
    logger.info("Running the task")
    main(**kwargs)
