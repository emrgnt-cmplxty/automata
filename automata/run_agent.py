"""
This script is used to run an agent with a given set of instructions and tools.
"""

import logging
import logging.config
from typing import Optional

from automata.agent import OpenAIAutomataAgent
from automata.config.openai_config import (
    SUPPORTED_MODEL_INFORMATION,
    OpenAIAutomataAgentConfig,
)
from automata.core.utils import get_logging_config
from automata.tools.builders import (
    PyInterpreterOpenAIToolkitBuilder,
    WolframAlphaOpenAIToolkitBuilder,
)

logger = logging.getLogger(__name__)
logging.config.dictConfig(get_logging_config())

DEFAULT_ISSUES_PROMPT_PREFIX = """Provide a comprehensive explanation and full code implementation (in Markdown) which address the Github issue(s) that follow:"""

DEFAULT_ISSUES_PROMPT_SUFFIX = """You may use the context oracle (multiple times if necessary) to ensure that you have proper context to answer this question. If you are tasked with writing code, then keep to the SOLID Principles Further, pay special attention to Dependency Inversion Principle and Dependency Injection."""


def create_default_config(
    model: str = "gpt-4",
    stream: bool = False,
    verbose: bool = True,
    max_iterations: int = 10,
    system_instruction: str = "You are a helpful assistant.",
    abs_max_tokens: Optional[int] = None,
    tools: Optional[list] = None,
    **kwargs,
) -> dict:
    """Creates a default configuration dictionary for the agent."""
    # Default configurations
    return {
        "model": model,
        "stream": stream,
        "verbose": verbose,
        "max_iterations": max_iterations,
        "system_instruction": system_instruction,
        "abs_max_tokens": abs_max_tokens
        or SUPPORTED_MODEL_INFORMATION[model].abs_max_tokens,
        "tools": tools or [],
    }


# Modify the main function
def main(*args, **kwargs) -> str:
    """Run the agent with the given instructions and tools."""

    instructions = (
        kwargs.get("instructions")
        or "This is a dummy instruction, return True."
    )
    tools = []
    toolkits = kwargs.get("toolkits", "wolfram-alpha-oracle").split(",")
    if "wolfram-alpha-oracle" in toolkits:
        tools.extend(WolframAlphaOpenAIToolkitBuilder().build_for_open_ai())
    elif "py-executor" in toolkits:
        tools.extend(PyInterpreterOpenAIToolkitBuilder().build_for_open_ai())

    agent_config_dict = create_default_config(
        **kwargs,
        tools=tools,
    )

    agent_config_obj = OpenAIAutomataAgentConfig(**agent_config_dict)

    agent = OpenAIAutomataAgent(instructions, config=agent_config_obj)
    print("Running agent...")
    return agent.run()


if __name__ == "__main__":
    main()
