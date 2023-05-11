import logging
from typing import Any, Dict

from automata.configs.automata_agent_configs import AutomataAgentConfig
from automata.configs.config_enums import AgentConfigVersion
from automata.core.utils import get_logging_config, root_py_path
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


def check_kwargs(kwargs):
    assert not (
        kwargs.get("instructions") is None and kwargs.get("session_id") is None
    ), "You must provide instructions for the agent if you are not providing a session_id."
    assert not (
        kwargs.get("instructions") and kwargs.get("session_id")
    ), "You must provide either instructions for the agent or a session_id."
    assert (
        "helper_agent_names" in kwargs
    ), "You must provide a list of helper agents, with field helper_agent_names."
    assert (
        "main_config_name" in kwargs
    ), "You must provide a main agent config name, with field main_config_name."


def process_kwargs(**kwargs) -> Dict[str, Any]:
    logger.debug(f"Loading helper configs...")
    helper_agent_names = kwargs.get("helper_agent_names")
    if not isinstance(helper_agent_names, str):
        raise ValueError("helper_agent_names must be a comma-separated string.")

    helper_agent_configs = {
        AgentConfigVersion(config_name): AutomataAgentConfig.load(AgentConfigVersion(config_name))
        for config_name in helper_agent_names.split(",")
    }
    kwargs["helper_agent_configs"] = helper_agent_configs
    del kwargs["helper_agent_names"]

    logger.debug(f"Loading main agent config..   .")
    kwargs["agent_config"] = AutomataAgentConfig.load(
        AgentConfigVersion(kwargs.get("main_config_name"))
    )
    del kwargs["main_config_name"]

    if kwargs.get("include_overview"):
        instruction_payload = kwargs.get("instruction_payload", {})
        instruction_payload["overview"] = PythonIndexer.build_overview(root_py_path())
        kwargs["instruction_payload"] = instruction_payload

    return kwargs
