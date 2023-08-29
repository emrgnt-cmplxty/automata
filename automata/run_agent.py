"""
This script is used to run an agent with a given set of instructions and tools.
"""

import logging
import logging.config
from typing import List
import uuid

from automata.agent import OpenAIAutomataAgent
from automata.tools.agent_tool_dependency_factory import build_dependencies_for_tools
from automata.core.utils import get_logging_config
from automata.tools.agent_tool_factory import AgentToolFactory
from automata.config.openai_config import OpenAIAutomataAgentConfig, SUPPORTED_MODEL_INFORMATION

logger = logging.getLogger(__name__)
logging.config.dictConfig(get_logging_config())

DEFAULT_ISSUES_PROMPT_PREFIX = """Provide a comprehensive explanation and full code implementation (in Markdown) which address the Github issue(s) that follow:"""

DEFAULT_ISSUES_PROMPT_SUFFIX = """You may use the context oracle (multiple times if necessary) to ensure that you have proper context to answer this question. If you are tasked with writing code, then keep to the SOLID Principles Further, pay special attention to Dependency Inversion Principle and Dependency Injection."""


def create_config(agent_name=None, model="gpt-4", session_id=None, stream=None,
                  verbose=None, max_iterations=None, abs_max_tokens=None, tools=None):
    
    # Default configurations
    return {
        'model': model,
        'session_id': session_id or str(uuid.uuid4()),
        'stream': stream,
        'verbose': verbose,
        'max_iterations': max_iterations,
        'abs_max_tokens': abs_max_tokens or SUPPORTED_MODEL_INFORMATION[model].abs_max_tokens,
        'tools': tools
    }


# Modify the main function
def main(*args, **kwargs) -> str:
    """Run the agent with the given instructions and tools."""

    instructions = (
        kwargs.get("instructions")
        or "This is a dummy instruction, return True."
    )
    toolkits = kwargs.get("toolkits", "advanced-context-oracle").split(",")

    tool_dependencies = build_dependencies_for_tools(toolkits)
    tools = AgentToolFactory.build_tools(toolkits, **tool_dependencies)
    logger.info("Done building tools...")
    
    config_name = kwargs.get("agent_name", "automata-main")

    agent_config_dict = create_config(
        agent_name=config_name,
        model=kwargs.get("model", "gpt-4"),
        max_iterations=kwargs.get("max_iterations", None),
        tools=tools
    )
    
    agent_config_obj = OpenAIAutomataAgentConfig.from_dict(agent_config_dict)

    agent = OpenAIAutomataAgent(instructions, config=agent_config_obj)
    return agent.run()
