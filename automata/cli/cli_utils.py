import logging
from typing import Any, Dict
from automata.configs.automata_agent_configs import AutomataAgentConfig
from automata.configs.config_enums import AgentConfigVersion

logger = logging.getLogger(__name__)


def process_kwargs(**kwargs) -> Dict[str, Any]:
    logger.info(f"Loading helper configs...")
    helper_agent_names = kwargs.get("helper_agent_names")
    if not isinstance(helper_agent_names, str):
        raise ValueError("helper_agent_names must be a comma-separated string.")

    helper_agent_configs = {
        AgentConfigVersion(config_name): AutomataAgentConfig.load(AgentConfigVersion(config_name))
        for config_name in helper_agent_names.split(",")
    }
    kwargs["helper_agent_configs"] = helper_agent_configs
    del kwargs["helper_agent_names"]

    logger.info(f"Loading main agent config..   .")
    kwargs["agent_config"] = AutomataAgentConfig.load(
        AgentConfigVersion(kwargs.get("main_config_name"))
    )
    del kwargs["main_config_name"]
    return kwargs
