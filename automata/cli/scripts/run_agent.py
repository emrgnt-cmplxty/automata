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

logger = logging.getLogger(__name__)


def main(*args, **kwargs) -> str:
    """
    Runs the main automata agent
    """
    logger.info("Building toolkits...")

    instructions = kwargs.get("instructions", "This is a dummy instruction, return True.")
    tool_list = kwargs.get("tools", "context_oracle").split(",")

    # A list of all dependencies that will be used to build the toolkits
    dependencies: Set[Any] = set()
    for tool in tool_list:
        for dependency_name, _ in AgentToolFactory.TOOLKIT_TYPE_TO_ARGS[ToolkitType(tool)]:
            dependencies.add(dependency_name)
    kwargs = {}
    logger.info("  - Building dependencies...")
    for dependency in dependencies:
        logger.info(f"Building {dependency}...")
        kwargs[dependency] = DependencyFactory().get(dependency)
    print("kwargs = ", kwargs)

    llm_toolkits = build_llm_toolkits(tool_list, **kwargs)
    logger.info("Done building toolkits...")

    config_name = AgentConfigName.AUTOMATA_RETRIEVER
    agent_config = (
        AutomataAgentConfigBuilder.from_name(config_name)
        .with_llm_toolkits(llm_toolkits)
        .with_model("gpt-3.5-turbo-16k")
        .build()
    )

    agent = AutomataAgent(instructions, config=agent_config)
    agent.setup()
    return agent.run()
