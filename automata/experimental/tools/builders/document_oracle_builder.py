"""This module provides a toolkit builder for the document oracle."""
import logging
import textwrap
from typing import List

from automata.agent import (
    AgentToolkitBuilder,
    AgentToolkitNames,
    OpenAIAgentToolkitBuilder,
)
from automata.config.config_base import LLMProvider
from automata.experimental.memory_store import SymbolDocEmbeddingHandler
from automata.experimental.search import SymbolSearch
from automata.llm import OpenAITool
from automata.singletons.toolkit_registry import (
    OpenAIAutomataAgentToolkitRegistry,
)
from automata.tools.tool_base import Tool

logger = logging.getLogger(__name__)


class DocumentOracleToolkitBuilder(AgentToolkitBuilder):
    """
    The DocumentOracleToolkitBuilder provides tools which translate a NLP
    query to relevant context.
    """

    def __init__(
        self,
        symbol_search: SymbolSearch,
        symbol_doc_embedding_handler: SymbolDocEmbeddingHandler,
        **kwargs,
    ) -> None:
        self.symbol_search = symbol_search
        self.symbol_doc_embedding_handler = symbol_doc_embedding_handler

    def build(self) -> List[Tool]:
        """Builds the tools associated with the context oracle."""
        return [
            Tool(
                name="document-oracle",
                function=self._get_best_match,
                description=textwrap.dedent(
                    """The DocumentOracleToolkitBuilder is a tool that translates a given natural language query into relevant context by finding the most semantically similar symbol's documentation in a Python codebase. It uses SymbolSearch and EmbeddingSimilarityCalculator to identify this symbol. The tool then returns the corresponding class documentation, providing valuable context for the query."""
                ),
            )
        ]

    def _get_best_match(self, query: str) -> str:
        """
        Retrieves the best matching class documentation corresponding to a
        given query.

        This method constructs the gets the best matching class documentation
        according to the best-ranked symbol match to the user provided query.
        """

        symbol_rank_search_results = (
            self.symbol_search.get_symbol_rank_results(query)
        )

        most_similar_symbol = symbol_rank_search_results[0][0]

        result = ""
        try:
            most_similar_doc_embedding = (
                self.symbol_doc_embedding_handler.get_embeddings(
                    [most_similar_symbol]
                )[0]
            )
            result += (
                f"Documentation:\n\n{most_similar_doc_embedding.document}"
            )
        except Exception as e:
            error = f"Failed to get embedding for symbol {most_similar_symbol} with error: {e}"
            logger.error(error)
            return error
        return result


@OpenAIAutomataAgentToolkitRegistry.register_tool_manager
class DocumentOracleOpenAIToolkitBuilder(
    DocumentOracleToolkitBuilder, OpenAIAgentToolkitBuilder
):
    TOOL_NAME = AgentToolkitNames.DOCUMENT_ORACLE
    LLM_PROVIDER = LLMProvider.OPENAI

    def build_for_open_ai(self) -> List[OpenAITool]:
        """Builds the tools associated with the context oracle for the OpenAI API."""
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
