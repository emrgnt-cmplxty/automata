import logging
from typing import Any, Set

from automata.config.agent_config_builder import AutomataAgentConfigBuilder
from automata.config.config_types import AgentConfigName
from automata.core.agent.agent import AutomataAgent
from automata.core.agent.tools.tool_utils import (
    AgentToolFactory,
    DependencyFactory,
    build_llm_toolkits,
)
from automata.core.base.tool import ToolkitType
from automata.core.coding.py.module_loader import py_module_loader

logger = logging.getLogger(__name__)


def main(*args, **kwargs) -> str:
    """
    Runs the main automata agent

    Keyword Args:
        instructions (str): The instructions to run the agent with
            Defaults to "This is a dummy instruction, return True."
        tools (str): A comma-separated list of tools to use
            Defaults to "context_oracle"
            Valid tools can be quickly observed in automata/core/agent/tools/tool_utils
        model (str): The model to use for the agent
            Defaults to "GPT-4"
        agent_name (str): The name of the agent
            Defaults to "automata_retriever"
    """

    py_module_loader.initialize()

    instructions = kwargs.get("instructions") or "This is a dummy instruction, return True."
    llm_toolkits_list = kwargs.get("llm_toolkits", "context_oracle").split(",")

    # A list of all dependencies that will be used to build the toolkits
    dependencies: Set[Any] = set()
    for tool in llm_toolkits_list:
        for dependency_name, _ in AgentToolFactory.TOOLKIT_TYPE_TO_ARGS[ToolkitType(tool)]:
            dependencies.add(dependency_name)
    kwargs = {}

    logger.info("  - Building dependencies...")
    for dependency in dependencies:
        logger.info(f"Building {dependency}...")
        kwargs[dependency] = DependencyFactory().get(dependency)

    llm_toolkits = build_llm_toolkits(llm_toolkits_list, **kwargs)
    logger.info("Done building toolkits...")

    config_name = AgentConfigName(kwargs.get("agent_name", "automata_retriever"))
    agent_config = (
        AutomataAgentConfigBuilder.from_name(config_name)
        .with_llm_toolkits(llm_toolkits)
        .with_model(kwargs.get("model", "gpt-4"))
        .build()
    )

    agent = AutomataAgent(instructions, config=agent_config)
    agent.setup()
    return agent.run()
