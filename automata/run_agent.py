# sourcery skip: avoid-global-variables
"""
This script is used to run an agent with a given set of instructions and tools.
"""
import argparse
import os
import openai
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

DEFAULT_SYSTEM_INSTRUCTION = (
    "You are a helpful assistant, return your results with `call-termination`."
)


def create_default_config(
    model: str = "gpt-4",
    stream: bool = True,
    verbose: bool = True,
    max_iterations: int = 10,
    system_instruction: str = DEFAULT_SYSTEM_INSTRUCTION,
    abs_max_tokens: Optional[int] = None,
    tools: Optional[list] = None,
    **kwargs,
) -> dict:
    """Creates a default configuration dictionary for the agent."""
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
    user_instructions = kwargs["user_instructions"]
    toolkits = kwargs.get("toolkits", "py-interpreter").split(",")
    tools = []
    if "wolfram-alpha-oracle" in toolkits:
        tools.extend(WolframAlphaOpenAIToolkitBuilder().build_for_open_ai())
    elif "py-interpreter" in toolkits:
        tools.extend(PyInterpreterOpenAIToolkitBuilder().build_for_open_ai())

    agent_config_vars = create_default_config(
        **kwargs,
        tools=tools,
    )

    agent_config = OpenAIAutomataAgentConfig(**agent_config_vars)

    agent = OpenAIAutomataAgent(user_instructions, config=agent_config)
    return agent.run()


if __name__ == "__main__":
    """Run the agent with the given instructions and tools."""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--user-instructions",
        type=str,
        default="This is a dummy instruction, return 'True' with call-termination..",
        help="",
    )
    parser.add_argument(
        "--toolkits",
        type=str,
        default="py-interpreter",
        help="",
    )
    parser.add_argument(
        "--log-level",
        type=str,
        default="INFO",
        help="",
    )

    from automata.core.utils import configure_logging

    openai.api_key = os.environ["OPENAI_API_KEY"]
    args = parser.parse_args()
    configure_logging(args.log_level)
    main(**vars(args))
