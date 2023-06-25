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
            "--log_level",
            type=str,
            default="DEBUG",
            help="Execute script in verbose mode?",
        ),
        click.option(
            "--index_file",
            default="index.scip",
            help="Which index file to use for the embedding modifications.",
        ),
        click.option(
            "--embedding_file",
            default="symbol_code_embedding.json",
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
            "--tool_builders",
            default="context_oracle",
            help="Which LLM toolkits to use?",
        ),
        click.option(
            "--model",
            default="gpt-4",
            help="Which model to use?",
        ),
        click.option(
            "--main_config_name",
            default="automata_reader",
            help="Which agent to use for this task?",
        ),
    ]
    for option in reversed(options):
        command = option(command)
    return command
