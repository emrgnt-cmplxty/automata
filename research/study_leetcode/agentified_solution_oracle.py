import logging
from typing import List

from leetcode_solutions_finder import LeetCodeSolutionsFinder

from automata.agent import (
    AgentToolkitBuilder,
    AgentToolkitNames,
    OpenAIAgentToolkitBuilder,
)
from automata.config import LLMProvider
from automata.llm import OpenAITool
from automata.singletons.toolkit_registry import (
    OpenAIAutomataAgentToolkitRegistry,
)
from automata.tools.tool_base import Tool

logger = logging.getLogger(__name__)


class AgentifiedSolutionOracleToolkitBuilder(AgentToolkitBuilder):
    """Builds tools for agent facilitated solution oracle"""

    FAILURE_STRING = "Agentified solution oracle failed to find a solution"

    def __init__(
        self,
        leetcode_solution_finder: LeetCodeSolutionsFinder,
        *args,
        **kwargs,
    ) -> None:  # sourcery skip: docstrings-for-functions
        self.leetcode_solution_finder = leetcode_solution_finder
        self.leetcode_solution_finder = leetcode_solution_finder

    def build(self) -> List[Tool]:
        """Builds tools associated with agentified solution oracle."""

        return [
            Tool(
                name="solution-oracle",
                function=self._get_solution,
                description="Find the best matching solution for the given input query.",
            ),
        ]

    def _get_solution(self, query: str) -> str:
        """Find the best matching solution for the input query."""
        try:
            return (
                self.leetcode_solution_finder.find_best_match_and_explanation(
                    query
                )
            )
        except Exception as e:
            logger.error(
                f"Exception {e} occurred for query {query}. Returning failure string."
            )
            return f"{AgentifiedSolutionOracleToolkitBuilder.FAILURE_STRING} with error {e}"


@OpenAIAutomataAgentToolkitRegistry.register_tool_manager
class AgentifiedSolutionOracleOpenAIToolkitBuilder(
    AgentifiedSolutionOracleToolkitBuilder, OpenAIAgentToolkitBuilder
):
    TOOL_NAME = (
        AgentToolkitNames.AGENTIFIED_SOLUTION_ORACLE
    )  # Define the toolkit name as needed
    LLM_PROVIDER = LLMProvider.OPENAI

    def build_for_open_ai(self) -> List[OpenAITool]:
        """Builds the tools associated with the agentified solution oracle for the OpenAI API."""
        tools = super().build()

        # Predefined properties and required parameters
        properties = {
            "query": {
                "type": "string",
                "description": "The query string to search for.",
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
