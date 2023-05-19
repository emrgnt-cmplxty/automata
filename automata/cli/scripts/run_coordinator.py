import logging
import logging.config

from termcolor import colored

from automata.cli.cli_utils import (
    check_kwargs,
    create_instructions_and_config_from_kwargs,
    reconfigure_logging,
)
from automata.configs.automata_agent_config_utils import AutomataAgentConfigFactory
from automata.core.agent.automata_agent_utils import AutomataAgentFactory
from automata.core.manager.automata_manager_factory import AutomataManagerFactory

logger = logging.getLogger(__name__)


def run(kwargs):
    """
    Create coordinator and agents based on the provided arguments.

    :param args: Parsed command line arguments.
    :return: Tuple containing the AutomataCoordinator and instruction_payload.
    """
    check_kwargs(kwargs)
    instructions, kwargs = create_instructions_and_config_from_kwargs(**kwargs)
    logger.info(
        f"Passing in instructions:\n{colored(instructions, color='green', attrs=['reverse'])}"
    )
    logger.info("-" * 60)

    logger.info("Creating main agent...")

    main_config = AutomataAgentConfigFactory.create_config(**kwargs)
    main_agent = AutomataAgentFactory.create_agent(instructions, config=main_config)

    logger.info("Creating agent manager...")
    agent_manager = AutomataManagerFactory.create_manager(
        main_agent, kwargs.get("helper_agent_configs")
    )

    if not kwargs.get("session_id"):
        return agent_manager.run()
    else:
        agent_manager.replay_messages()


def main(kwargs):
    verbose = kwargs.pop("verbose")
    reconfigure_logging(verbose)

    result = run(kwargs)
    logger.info(f"Final Result = {result}")
    return result
