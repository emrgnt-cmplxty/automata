import logging
import textwrap
from typing import List

from automata.config.base import LLMProvider
from automata.core.agent.tool.registry import AutomataOpenAIAgentToolBuilderRegistry
from automata.core.base.agent import AgentToolBuilder, AgentToolProviders
from automata.core.base.tool import Tool
from automata.core.embedding.symbol_similarity import SymbolSimilarityCalculator
from automata.core.llm.providers.openai import OpenAIAgentToolBuilder, OpenAITool

logger = logging.getLogger(__name__)


class ContextOracleToolBuilder(AgentToolBuilder):
    """The ContextOracleTools provides a tool that combines SymbolSearch and SymbolSimilarity to create contexts."""

    def __init__(
        self,
        symbol_doc_similarity: SymbolSimilarityCalculator,
        symbol_code_similarity: SymbolSimilarityCalculator,
        **kwargs,
    ) -> None:
        self.symbol_doc_similarity = symbol_doc_similarity
        self.symbol_code_similarity = symbol_code_similarity

    def build(self) -> List[Tool]:
        """Builds the tools associated with the context oracle."""
        return [
            Tool(
                name="context-oracle",
                function=self._get_context,
                description=textwrap.dedent(
                    """This tool utilizes the SymbolSimilarityCalculator and SymbolSearch to provide context for a given query by computing semantic similarity between the query and all available symbols' documentation and code. The symbol with the highest combined similarity score is identified, with its source code and documentation summary forming the primary context. Additionally, if enabled, the documentation summaries of related symbols (those next most similar to the query) are included."""
                ),
            )
        ]

    def _get_context(self, query: str, max_related_symbols=1) -> str:
        """
        Retrieves the context corresponding to a given query.

        The function constructs the context by concatenating the source code and documentation of the most semantically
        similar symbol to the query with the documentation summary of the most highly
        ranked symbols. The ranking of symbols is based on their semantic similarity to the query.
        """
        doc_search_results = self.symbol_doc_similarity.calculate_query_similarity_dict(query)
        code_search_results = self.symbol_code_similarity.calculate_query_similarity_dict(query)

        combined_results = {}

        for key in list(set(list(doc_search_results) + list(code_search_results))):
            combined_results[key] = doc_search_results.get(key, 0) + code_search_results.get(
                key, 0
            )

        most_similar_symbols = [
            ele[0] for ele in sorted(combined_results.items(), key=lambda x: -x[1])
        ]
        most_similar_symbol = most_similar_symbols[0]

        most_similar_embedding = self.symbol_code_similarity.embedding_handler.get_embedding(
            most_similar_symbol
        )

        result = most_similar_embedding.embedding_source

        try:
            most_similar_doc_embedding = (
                self.symbol_doc_similarity.embedding_handler.get_embedding(most_similar_symbol)
            )
            result += f"Documentation Summary:\n\n{most_similar_doc_embedding.summary}"
        except Exception as e:
            logger.error(
                "Failed to get embedding for symbol %s with error: %s",
                most_similar_symbol,
                e,
            )
        if max_related_symbols > 0:
            result += f"Fetching related context now for {max_related_symbols} symbols...\n\n"

            counter = 0

            for symbol in most_similar_symbols:
                if symbol == most_similar_symbol:
                    continue
                if counter >= max_related_symbols:
                    break
                try:
                    result += f"{symbol.dotpath}\n\n"
                    result += f"{self.symbol_doc_similarity.embedding_handler.get_embedding(symbol).summary}\n\n"
                    counter += 1
                except Exception as e:
                    logger.error(
                        "Failed to get embedding for symbol %s with error: %s",
                        symbol,
                        e,
                    )
                    continue

        return result


@AutomataOpenAIAgentToolBuilderRegistry.register_tool_manager
class ContextOracleOpenAIToolBuilder(ContextOracleToolBuilder, OpenAIAgentToolBuilder):
    TOOL_TYPE = AgentToolProviders.CONTEXT_ORACLE
    PLATFORM = LLMProvider.OPENAI

    def build_for_open_ai(self) -> List[OpenAITool]:
        tools = super().build()

        # Predefined properties and required parameters
        properties = {
            "query": {"type": "string", "description": "The query string to search for."},
            "max_additional_related_symbols": {
                "type": "integer",
                "description": "The maximum number of additional related symbols to return documentation for.",
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
