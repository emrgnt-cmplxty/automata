import logging
import textwrap
from typing import List

from automata.config.base import LLMProvider
from automata.core.agent.agent import AgentToolkitBuilder, AgentToolkitNames
from automata.core.agent.providers import OpenAIAgentToolkitBuilder
from automata.core.llm.providers.openai import OpenAITool
from automata.core.embedding.base import EmbeddingSimilarityCalculator
from automata.core.tools.base import Tool
from automata.core.singletons.toolkit_registries import OpenAIAutomataAgentToolkitRegistry
from automata.core.memory_store.symbol_code_embedding import SymbolCodeEmbeddingHandler
from automata.core.memory_store.symbol_doc_embedding import SymbolDocEmbeddingHandler

logger = logging.getLogger(__name__)


class ContextOracleToolkitBuilder(AgentToolkitBuilder):
    """The ContextOracleToolkitBuilder provides tools which translate NLP queries to relevant context."""

    def __init__(
        self,
        symbol_doc_embedding_handler: SymbolDocEmbeddingHandler,
        symbol_code_embedding_handler: SymbolCodeEmbeddingHandler,
        embedding_similarity_calculator: EmbeddingSimilarityCalculator,
        **kwargs,
    ) -> None:
        self.symbol_doc_embedding_handler = symbol_doc_embedding_handler
        self.symbol_code_embedding_handler = symbol_code_embedding_handler
        self.embedding_similarity_calculator = embedding_similarity_calculator

    def build(self) -> List[Tool]:
        """Builds the tools associated with the context oracle."""
        return [
            Tool(
                name="context-oracle",
                function=self._get_context,
                description=textwrap.dedent(
                    """This tool utilizes the EmbeddingSimilarityCalculator and SymbolSearch to provide context for a given query by computing semantic similarity between the query and all available symbols' documentation and code. The symbol with the highest combined similarity score is identified, with its source code and documentation summary forming the primary context. Additionally, if enabled, the documentation summaries of related symbols (those next most similar to the query) are included."""
                ),
            )
        ]

    def _get_context(self, query: str, max_related_symbols=1) -> str:
        """
        Retrieves the context corresponding to a given query.

        The function constructs the context by concatenating the source code and documentation of the most semantically
        similar symbol to the query with the documentation summary of the most highly
        ranked symbols. The ranking of symbols is based on their semantic similarity to the query.
        Precisely, this ranking is the max similarity between the query string and the source code string.
        This metric was chosen because the document embedding is incomplete, but often gives strong positive
        results when populated for the relevant query. Thus, selecting the maximum will factor in documentation
        when populated.
        """
        doc_embeddings = self.symbol_doc_embedding_handler.get_ordered_embeddings()
        doc_search_results = self.embedding_similarity_calculator.calculate_query_similarity_dict(
            doc_embeddings, query
        )
        code_embeddings = self.symbol_code_embedding_handler.get_ordered_embeddings()
        code_search_results = self.embedding_similarity_calculator.calculate_query_similarity_dict(
            code_embeddings, query
        )
        combined_results = {
            key: max(doc_search_results.get(key, 0), code_search_results.get(key, 0))
            for key in set(doc_search_results).union(code_search_results)
        }

        most_similar_symbols = [
            ele[0] for ele in sorted(combined_results.items(), key=lambda x: -x[1])
        ]

        most_similar_symbol = most_similar_symbols[0]

        most_similar_code_embedding = self.symbol_code_embedding_handler.get_embedding(
            most_similar_symbol
        )

        result = most_similar_code_embedding.input_object

        try:
            most_similar_doc_embedding = self.symbol_doc_embedding_handler.get_embedding(
                most_similar_symbol
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
                    result += (
                        f"{self.symbol_doc_embedding_handler.get_embedding(symbol).summary}\n\n"
                    )
                    counter += 1
                except Exception as e:
                    logger.error(
                        "Failed to get embedding for symbol %s with error: %s",
                        symbol,
                        e,
                    )
                    continue

        return result


@OpenAIAutomataAgentToolkitRegistry.register_tool_manager
class ContextOracleOpenAIToolkitBuilder(ContextOracleToolkitBuilder, OpenAIAgentToolkitBuilder):
    TOOL_TYPE = AgentToolkitNames.CONTEXT_ORACLE
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
