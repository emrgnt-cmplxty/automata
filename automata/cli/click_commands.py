# Add this import at the beginning of your file
import click

from automata.configs.config_enums import InstructionConfigVersion

from .click_options import common_options


class Namespace:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)


@click.group()
@click.pass_context
def cli(ctx):
    pass


@common_options
@cli.command()
@click.option(
    "--instruction_version",
    type=str,
    default=f"{InstructionConfigVersion.AGENT_INTRODUCTION_DEV.value}",
    help="The config version of the agent.",
)
@click.option(
    "--include_overview",
    type=bool,
    help="Should the instruction prompt include an overview?",
)
@click.pass_context
def master(ctx, *args, **kwargs):
    from .scripts.run_coordinator import main

    namespace = Namespace(**kwargs)
    main(namespace)
