import logging
import logging.config
from typing import Dict

from termcolor import colored

from automata.configs.automata_agent_configs import AutomataAgentConfig
from automata.configs.config_enums import AgentConfigVersion
from automata.core.agent.automata_agent import MasterAutomataAgent
from automata.core.agent.automata_agent_builder import AutomataAgentBuilder
from automata.core.agent.automata_agent_helpers import create_instruction_payload
from automata.core.base.tool import Toolkit, ToolkitType
from automata.core.coordinator.automata_coordinator import AutomataCoordinator, AutomataInstance
from automata.core.utils import get_logging_config, root_py_path
from automata.tool_management.tool_management_utils import build_llm_toolkits
from automata.tools.python_tools.python_indexer import PythonIndexer

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


def create_coordinator(agent_config_versions: str):
    """
    Create AutomataCoordinator and add agent instances.

    :param agent_config_versions: String containing comma-separated agent config versions.
    :return: AutomataCoordinator instance.
    """
    coordinator = AutomataCoordinator()
    agent_configs = {
        AgentConfigVersion(config_version): AutomataAgentConfig.load(
            AgentConfigVersion(config_version)
        )
        for config_version in agent_config_versions.split(",")
    }
    for config_version in agent_configs.keys():
        config = agent_configs[config_version]
        logger.info(
            f"Adding Agent with name={config_version.value}, description={config.description}"
        )
        agent = AutomataInstance(
            config_version=config_version,
            description=config.description,
            verbose=True,
            stream=True,
        )
        coordinator.add_agent_instance(agent)

    return coordinator


def create_master_agent(args, instruction_payload):
    """
    Create the master AutomataAgent instance.

    :param args: Parsed command line arguments.
    :param coordinator: AutomataCoordinator instance.
    :param instruction_payload: Dictionary containing the initial payload.
    :return: MasterAutomataAgent instance.
    """
    agent_version = AgentConfigVersion(AgentConfigVersion(args.master_config_version))
    agent_config = AutomataAgentConfig.load(agent_version)
    inputs = {
        "model": args.model,
    }
    master_llm_toolkits: Dict[ToolkitType, Toolkit] = build_llm_toolkits(
        args.llm_toolkits.split(","), **inputs
    )

    master_agent = MasterAutomataAgent.from_agent(
        AutomataAgentBuilder.from_config(agent_config)
        .with_instruction_payload(instruction_payload)
        .with_instructions(args.instructions)
        .with_llm_toolkits(master_llm_toolkits)
        .with_model(args.model)
        .with_session_id(args.session_id)
        .with_stream(args.stream)
        .with_instruction_version(args.instruction_version)
        .build()
    )

    return master_agent


def check_input(args):
    assert not (
        args.instructions is None and args.session_id is None
    ), "You must provide instructions for the agent if you are not providing a session_id."
    assert not (
        args.instructions and args.session_id
    ), "You must provide either instructions for the agent or a session_id."


def run(args):
    """get_overview
    Create coordinator and agents based on the provided arguments.

    :param args: Parsed command line arguments.
    :return: Tuple containing the AutomataCoordinator and instruction_payload.
    """
    check_input(args)
    logger.info(
        f"Passing in instructions:\n{colored(args.instructions, color='white', on_color='on_green')}"
    )
    logger.info("-" * 60)

    coordinator = create_coordinator(args.agent_config_versions)
    agents_message = coordinator.build_agent_message()
    overview = PythonIndexer(root_py_path()).build_overview() if args.include_overview else ""
    instruction_payload = create_instruction_payload(overview, agents_message)
    master_agent = create_master_agent(args, instruction_payload)

    coordinator.set_master_agent(master_agent)
    master_agent.set_coordinator(coordinator)
    if not args.session_id:
        return master_agent.run()
    else:
        master_agent.replay_messages()


def main(args):
    configure_logging(args.verbose)

    result = run(args)
    logger.info(f"Final Result = {result}")
    return result
