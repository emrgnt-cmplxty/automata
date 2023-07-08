import click


def common_options(command: click.Command, *args, **kwargs) -> click.Command:
    """
    Common options shared across cli

    Args:
        command (click.Command): Command to add options to

    Returns:
        click.Command: Command with options added
    """
    options = [
        click.option(
            "--log-level",
            type=str,
            default="DEBUG",
            help="Execute script in verbose mode?",
        ),
        click.option(
            "--index-file",
            default="automata.scip",
            help="Which index file to use for the embedding modifications.",
        ),
        click.option(
            "--code-embedding-file",
            default="symbol_code_embedding.json",
            help="Which embedding file to save to.",
        ),
        click.option(
            "--doc-embedding-file",
            default="symbol_doc_embedding_l2.json",
            help="Which embedding file to save to.",
        ),
    ]
    for option in reversed(options):
        command = option(command)
    return command


def agent_options(command: click.Command, *args, **kwargs) -> click.Command:
    """
    Common options used in agent configuration

    Args:
        command (click.Command): Command to add options to

    Returns:
        click.Command: Command with options added
    """
    options = [
        click.option(
            "--instructions",
            help="Which instructions to use for the agent.",
        ),
        click.option(
            "--toolkit-list",
            default="context-oracle",
            help="Which LLM tools to use?",
        ),
        click.option(
            "--model",
            default="gpt-4-0613",
            help="Which model to use?",
        ),
        click.option(
            "--max_iterations",
            default=None,
            help="How many iterations can we use?",
            type=int,
        ),
        click.option(
            "--config-to-load",
            default="automata-main",
            help="Which agent to use for this task?",
        ),
    ]
    for option in reversed(options):
        command = option(command)
    return command
