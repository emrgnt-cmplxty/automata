import logging
import logging.config

import click

from automata.core.utils import get_logging_config

from .options import common_options

logger = logging.getLogger(__name__)


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
    from automata.cli.scripts.run_code_embedding import main

    reconfigure_logging(kwargs.get("log_level", "DEBUG"))
    logger.info("Calling run_code_embedding")
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
    from automata.cli.scripts.run_doc_embedding_l2 import main

    reconfigure_logging(kwargs.get("log_level", "DEBUG"))
    logger.info("Calling run_doc_embedding_l2")
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
def run_doc_embedding_l3(ctx, *args, **kwargs):
    """Run the document embedding Level-3 pipeline."""
    from automata.cli.scripts.run_doc_embedding_l3 import main

    reconfigure_logging(kwargs.get("log_level", "DEBUG"))
    logger.info("Calling run_doc_embedding_l3")
    main(kwargs)
