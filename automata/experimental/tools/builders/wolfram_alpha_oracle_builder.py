"""Implementation of a toolkit builder for the Wolfram Alpha API."""

import logging
import logging.config
from typing import List

from automata.agent import AgentToolkitNames, OpenAIAgentToolkitBuilder
from automata.config.config_base import LLMProvider
from automata.core.utils import get_logging_config
from automata.experimental.tools.wolfram_alpha_oracle import WolframAlphaOracle
from automata.llm import OpenAITool
from automata.singletons.toolkit_registry import (
    OpenAIAutomataAgentToolkitRegistry,
)
from automata.tools.tool_base import Tool

logger = logging.getLogger(__name__)
logging.config.dictConfig(get_logging_config())


class WolframAlphaToolkitBuilder:
    """Builder for setting up the Wolfram Alpha Tool."""

    def build(self) -> List[Tool]:
        """Build and return a list containing an instance of the Wolfram Alpha Tool wrapped in a Tool object."""
        return [
            Tool(
                name="wolfram-alpha-oracle",
                function=self.query_wolfram_alpha,
                description="A tool to query the Wolfram Alpha API and retrieve results.",
            )
        ]

    def query_wolfram_alpha(self, input_str: str, **kwargs) -> str:
        """A wrapper function to query the Wolfram Alpha API."""
        oracle = WolframAlphaOracle()
        if result := oracle.query(input_str, **kwargs):
            return result
        return "Failed to get data from Wolfram Alpha."


@OpenAIAutomataAgentToolkitRegistry.register_tool_manager
class WolframAlphaOpenAIToolkitBuilder(
    WolframAlphaToolkitBuilder, OpenAIAgentToolkitBuilder
):
    TOOL_NAME = AgentToolkitNames.WOLFRAM_ALPHA_ORACLE
    LLM_PROVIDER = LLMProvider.OPENAI

    def __init__(self, **kwargs):
        super().__init__()

    def build_for_open_ai(self) -> List[OpenAITool]:
        """Builds the tools associated with the Wolfram Alpha oracle for the OpenAI API."""
        tools = super().build()

        properties = {
            "query": {
                "type": "string",
                "description": "The query string to send to Wolfram Alpha.",
            },
        }
        required = ["query"]

        openai_tools = []
        for tool in tools:
            openai_tool = OpenAITool(
                function=tool.function,
                name=tool.name,
                description=tool.description,
                properties=properties,
                required=required,
            )
            openai_tools.append(openai_tool)

        return openai_tools
