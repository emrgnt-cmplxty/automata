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
    ]
    for option in reversed(options):
        command = option(command)
    return command
