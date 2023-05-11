import logging
import logging.config
from typing import Dict

from termcolor import colored

from automata.configs.automata_agent_configs import AutomataAgentConfig
from automata.configs.config_enums import AgentConfigVersion
from automata.core.agent.automata_agent_builder import AutomataAgentBuilder
from automata.core.agent.automata_agent_utils import AutomataAgentFactory
from automata.core.base.tool import Toolkit, ToolkitType
from automata.core.manager.automata_manager_factory import AutomataManagerFactory
from automata.core.utils import get_logging_config
from automata.tool_management.tool_management_utils import build_llm_toolkits

logger = logging.getLogger(__name__)


def configure_logging(verbose: bool):
    """
    Configure the logging settings.

    :param verbose: Boolean, if True, set log level to DEBUG, else set to INFO.
    """
    logging_config = get_logging_config(log_level=logging.DEBUG if verbose else logging.INFO)
    logging.config.dictConfig(logging_config)

    # Set the logging level for the requests logger to WARNING
    requests_logger = logging.getLogger("urllib3")
    requests_logger.setLevel(logging.INFO)
    openai_logger = logging.getLogger("openai")
    openai_logger.setLevel(logging.INFO)


def create_main_agent(args, instruction_payload, coordinator):
    """
    Create the main AutomataAgent instance.

    :param args: Parsed command line arguments.
    :param coordinator: AutomataCoordinator instance.
    :param instruction_payload: Dictionary containing the initial payload.
    :return: AutomataAgent instance.
    """
    agent_version = AgentConfigVersion(AgentConfigVersion(args.main_config_name))
    agent_config = AutomataAgentConfig.load(agent_version)
    main_llm_toolkits: Dict[ToolkitType, Toolkit] = build_llm_toolkits(
        args.llm_toolkits.split(",")
    )

    main_agent = (
        AutomataAgentBuilder.from_config(agent_config)
        .with_instruction_payload(instruction_payload)
        .with_instructions(args.instructions)
        .with_llm_toolkits(main_llm_toolkits)
        .with_model(args.model)
        .with_session_id(args.session_id)
        .with_stream(args.stream)
        .with_instruction_version(args.instruction_version)
        .build()
    )
    main_agent.set_coordinator(coordinator)

    return main_agent


def check_input(kwargs):
    assert not (
        kwargs.get("instructions") is None and kwargs.get("session_id") is None
    ), "You must provide instructions for the agent if you are not providing a session_id."
    assert not (
        kwargs.get("instructions") and kwargs.get("session_id")
    ), "You must provide either instructions for the agent or a session_id."


def run(kwargs):
    """
    Create coordinator and agents based on the provided arguments.

    :param args: Parsed command line arguments.
    :return: Tuple containing the AutomataCoordinator and instruction_payload.
    """
    check_input(kwargs)
    instructions = kwargs.get("instructions")
    logger.info(
        f"Passing in instructions:\n{colored(instructions, color='green', attrs=['reverse'])}"
    )
    logger.info("-" * 60)

    logger.info(f"Loading helper configs...")
    helper_agent_configs = {
        AgentConfigVersion(config_name): AutomataAgentConfig.load(AgentConfigVersion(config_name))
        for config_name in kwargs.get("helper_agent_names").split(",")
    }
    kwargs["helper_agent_configs"] = helper_agent_configs
    del kwargs["helper_agent_names"]

    logger.info(f"Loading main agent config..   .")
    kwargs["agent_config"] = AutomataAgentConfig.load(
        AgentConfigVersion(kwargs.get("main_config_name"))
    )
    del kwargs["main_config_name"]

    logger.info("Creating main agent...")
    main_agent = AutomataAgentFactory.create_agent(**kwargs)

    logger.info("Creating agent manager...")
    agent_manager = AutomataManagerFactory.create_manager(main_agent, helper_agent_configs)

    if not kwargs.get("session_id"):
        return agent_manager.run()
    else:
        agent_manager.replay_messages()


def main(kwargs):
    verbose = kwargs.pop("verbose")
    configure_logging(verbose)

    result = run(kwargs)
    logger.info(f"Final Result = {result}")
    return result
