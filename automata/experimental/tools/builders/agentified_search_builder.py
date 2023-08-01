"""This module contains the AgentifiedSearchToolkitBuilder class."""
import ast
import logging
from typing import List, Optional

# Import the entire symbol module so that we can properly patch convert_to_ast_object
import automata.symbol
from automata.agent import (
    AgentToolkitBuilder,
    AgentToolkitNames,
    OpenAIAgentToolkitBuilder,
)
from automata.config import LLMProvider
from automata.config.prompt import AGENTIFIED_SEARCH_TEMPLATE
from automata.experimental.memory_store import SymbolDocEmbeddingHandler
from automata.experimental.search import SymbolSearch, SymbolSimilarityResult
from automata.llm import (
    LLMChatCompletionProvider,
    OpenAIChatCompletionProvider,
    OpenAIConversation,
    OpenAITool,
)
from automata.singletons.toolkit_registry import (
    OpenAIAutomataAgentToolkitRegistry,
)
from automata.symbol import Symbol
from automata.tools.tool_base import Tool

logger = logging.getLogger(__name__)


class AgentifiedSearchToolkitBuilder(AgentToolkitBuilder):
    """Builds tools for agent facilitated search"""

    TOP_N = 20
    MODEL = "gpt-4"
    TEMPERATURE = 0.7
    STREAM = True
    FAILURE_STRING = "No code found for best match, please try again."

    def __init__(
        self,
        # TODO - Move minimum necessary pieces out of experimental search implementation
        # So that this class can be entirely non-experimental.
        symbol_search: SymbolSearch,
        symbol_doc_embedding_handler: SymbolDocEmbeddingHandler,
        top_n: int = TOP_N,
        completion_provider: Optional[LLMChatCompletionProvider] = None,
        model: Optional[str] = None,
        temperature: Optional[float] = None,
        stream: Optional[bool] = None,
        **kwargs,
    ) -> None:  # sourcery skip: docstrings-for-functions
        self.symbol_search = symbol_search
        self.symbol_doc_embedding_handler = symbol_doc_embedding_handler
        self.top_n = top_n

        if completion_provider:
            if model or temperature or stream:
                raise ValueError(
                    "Do not provide a model, temperature, or stream setting when supplying a completion provider."
                )
            self.completion_provider = completion_provider
        else:
            conversation = OpenAIConversation()

            self.completion_provider = OpenAIChatCompletionProvider(
                model=model or AgentifiedSearchToolkitBuilder.MODEL,
                temperature=temperature
                or AgentifiedSearchToolkitBuilder.TEMPERATURE,
                stream=stream or AgentifiedSearchToolkitBuilder.STREAM,
                conversation=conversation,
                functions=[],
            )

    def build(self) -> List[Tool]:
        """Builds tools associated with directly retrieving python code."""

        return [
            Tool(
                name="search-top-matches",
                function=self._get_top_matches,
                description=f"Performs an agent-facilitated similarity-based search of symbols based on a given query string. The result is formatted as a string, with each line representing a match from the top {self.top_n} best matches.  An example of the output would be:\n'Top {self.top_n} Search Results:\nautomata.agent.openai_agent.OpenAIAutomataAgent._get_next_user_response\n...\n'",
            ),
            Tool(
                name="search-best-match-code",
                function=self._get_code_for_best_match,
                description='Returns the code of the best match from the results of `search-top-matches`. The output is formatted as a Python code block. The following is an abbreviated example output:\n\'```python\ndef _get_next_user_response(self, query: str) -> str:\n    """Gets the next response from the user.\n\n    Args:\n        ...\n```\'',
            ),
            Tool(
                name="search-best-match-docs",
                function=self._get_docs_for_best_match,
                description="Similar to `search-best-match-code`, but returns developer documentation if it exists for the match, and the source code otherwise.",
            ),
        ]

    def _get_top_matches(self, query: str) -> str:
        """
        Performs an agentified similarity based search of symbols based on
        the query string.

        Get the top N matches using the agent model and the symbol search API
        The matches could be in the form of fully qualified symbol names, for example
        """
        query_result = self.symbol_search.get_symbol_code_similarity_results(
            query
        )
        print("query_result = ", query_result)
        best_match = self._agent_selected_best_match(query, query_result)

        # Move the best match to the front of the list
        query_result = [item for item in query_result if item[0] != best_match]
        DUMMY_SCORE = (
            1.0  # Put a dummy score since it is removed immediately afterwards
        )
        query_result.insert(0, (best_match, DUMMY_SCORE))

        # Return the formatted result
        return self._get_formatted_search_results(query_result)

    def _get_formatted_search_results(
        self, query_result: SymbolSimilarityResult
    ) -> str:
        """
        Formats the search results into a string with each dotpath on a new line.
        """
        # print('query_result = ', query_result[0])
        # print('query_result.full_dotpath = ', query_result[0][0].full_dotpath)
        return "\n".join(
            [symbol.full_dotpath for symbol, _ in query_result][: self.top_n]
        )

    def _agent_selected_best_match(
        self, query: str, query_result: SymbolSimilarityResult
    ) -> Symbol:
        """
        Uses the agent model to select the best match from the query result.
        For now the agent is just a single completion call to the OpenAI API.
        """
        formatted_search_results = self._get_formatted_search_results(
            query_result
        )
        formatted_input_prompt = AGENTIFIED_SEARCH_TEMPLATE.format(
            SEARCH_RESULTS=formatted_search_results, QUERY=query
        )

        # Use the completion provider to locate the best match.
        best_match_dotpath = self.completion_provider.standalone_call(
            formatted_input_prompt
        ).strip()

        # Find the selected symbol where the dotpath matches the best_match_dotpath
        selected_symbol = next(
            (
                symbol
                for symbol, _ in query_result
                if symbol.full_dotpath == best_match_dotpath
            ),
            None,
        )

        # In case no match is found (which should not happen), default to the topmost match
        return (
            query_result[0][0] if selected_symbol is None else selected_symbol
        )

    def _get_code_for_best_match(
        self, query: str, best_matched_symbol: Optional[Symbol] = None
    ) -> str:
        """This method gets the the code of the best match to the input query."""
        if not best_matched_symbol:
            query_result = (
                self.symbol_search.get_symbol_code_similarity_results(query)
            )
            best_matched_symbol = self._agent_selected_best_match(
                query, query_result
            )
        try:
            return ast.unparse(
                automata.symbol.convert_to_ast_object(best_matched_symbol)
            )
        except Exception as e:
            logger.error(
                f"Exception {e} occurred for query {query}. Returning failure string."
            )
            return AgentifiedSearchToolkitBuilder.FAILURE_STRING

    def _get_docs_for_best_match(self, query: str) -> str:
        """This method gets the documentation of the best match to the input query, or the code if no documentation exists."""

        query_result = self.symbol_search.get_symbol_code_similarity_results(
            query
        )
        best_matched_symbol = self._agent_selected_best_match(
            query, query_result
        )

        try:
            most_similar_doc_embedding = (
                self.symbol_doc_embedding_handler.get_embeddings(
                    [best_matched_symbol]
                )[0]
            )
            return f"Documentation:\n\n{most_similar_doc_embedding.document}"
        except Exception as e:
            logger.warning(f"Error {e}, no match found for query {query}")
            return self._get_code_for_best_match(query, best_matched_symbol)


@OpenAIAutomataAgentToolkitRegistry.register_tool_manager
class AgentifiedSearchOpenAIToolkitBuilder(
    AgentifiedSearchToolkitBuilder, OpenAIAgentToolkitBuilder
):
    TOOL_NAME = (
        AgentToolkitNames.AGENTIFIED_SEARCH
    )  # Define the toolkit name as needed
    LLM_PROVIDER = LLMProvider.OPENAI

    def build_for_open_ai(self) -> List[OpenAITool]:
        """Builds the tools associated with the agentified search for the OpenAI API."""
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
