"""
This script is used to run an agent with a given set of instructions and tools.
"""

import logging
import logging.config
from typing import List

from automata.agent import OpenAIAutomataAgent
from automata.config import (
    AgentConfigName,
    OpenAIAutomataAgentConfigBuilder,
)
from automata.core.utils import get_logging_config
from automata.tools.agent_tool_factory import AgentToolFactory

logger = logging.getLogger(__name__)
logging.config.dictConfig(get_logging_config())

DEFAULT_ISSUES_PROMPT_PREFIX = """Provide a comprehensive explanation and full code implementation (in Markdown) which address the Github issue(s) that follow:"""

DEFAULT_ISSUES_PROMPT_SUFFIX = """You may use the context oracle (multiple times if necessary) to ensure that you have proper context to answer this question. If you are tasked with writing code, then keep to the SOLID Principles Further, pay special attention to Dependency Inversion Principle and Dependency Injection."""


def main(*args, **kwargs) -> str:
    """Run the agent with the given instructions and tools."""

    instructions = (
        kwargs.get("instructions")
        or "This is a dummy instruction, return True."
    )
    toolkits = kwargs.get("toolkits", "advanced-context-oracle").split(",")

    tool_dependencies = dependency_factory.build_dependencies_for_tools(
        toolkits
    )
    tools = AgentToolFactory.build_tools(toolkits, **tool_dependencies)
    logger.info("Done building tools...")
    config_name = AgentConfigName(kwargs.get("agent_name", "automata-main"))
    agent_config_builder = (
        OpenAIAutomataAgentConfigBuilder.from_name(config_name)
        .with_tools(tools)
        .with_model(kwargs.get("model", "gpt-4"))
    )

    max_iterations = kwargs.get("max_iterations", None)
    if max_iterations is not None:
        agent_config_builder = agent_config_builder.with_max_iterations(
            max_iterations
        )

    agent = OpenAIAutomataAgent(
        instructions, config=agent_config_builder.build()
    )
    return agent.run()
