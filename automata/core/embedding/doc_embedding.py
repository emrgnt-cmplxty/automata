import logging
from typing import List

from jinja2 import Template

from automata.config.prompt.doc_generation import DEFAULT_DOC_GENERATION_PROMPT
from automata.core.base.database.vector import VectorDatabaseProvider
from automata.core.context.py.retriever import PyContextRetriever
from automata.core.llm.completion import LLMChatCompletionProvider
from automata.core.llm.embedding import EmbeddingProvider, SymbolEmbeddingHandler
from automata.core.symbol.search.symbol_search import SymbolSearch
from automata.core.symbol.symbol_types import Symbol, SymbolDocEmbedding

logger = logging.getLogger(__name__)


class SymbolDocEmbeddingHandler(SymbolEmbeddingHandler):
    """
    Handles a database and provider for `Symbol` documentation embeddings.
    TODO: Add more robust logic for documentation updates.
    """

    def __init__(
        self,
        embedding_db: VectorDatabaseProvider,
        embedding_provider: EmbeddingProvider,
        completion_provider: LLMChatCompletionProvider,
        symbol_search: SymbolSearch,
        retriever: PyContextRetriever,
    ) -> None:
        super().__init__(embedding_db, embedding_provider)
        self.symbol_search = symbol_search
        self.retriever = retriever
        self.completion_provider = completion_provider

    def get_embedding(self, symbol: Symbol) -> SymbolDocEmbedding:
        return self.embedding_db.get(symbol)

    def process_embedding(self, symbol: Symbol) -> None:
        """
        Processes the embedding for a `Symbol` by calling either `update_existing_embedding`
        or `build_symbol_doc_embedding`, depending on whether the symbol is already in the database.

        Raises:
            ValueError: If the symbol has no source code for the symbol.
        """
        from automata.core.symbol.symbol_utils import (  # imported late for mocking
            convert_to_fst_object,
        )

        source_code = str(convert_to_fst_object(symbol))

        if not source_code:
            raise ValueError(f"Symbol {symbol} has no source code")

        if self.embedding_db.contains(symbol):
            self.update_existing_embedding(source_code, symbol)
            return

        symbol_embedding = self.build_symbol_doc_embedding(source_code, symbol)
        self.embedding_db.add(symbol_embedding)

    def build_symbol_doc_embedding(self, source_code: str, symbol: Symbol) -> SymbolDocEmbedding:
        """

        Build the embedding for a symbol's documentation.

        Example Document Output:
        ===========

        AgentConfig
        ===========

        ``AgentConfig`` is an abstract base class that provides a template for
        configurations related to agents. It contains abstract methods like
        ``setup()`` and ``load()`` that need to be implemented by subclasses.
        This class also handles the configuration of arbitrary types during the
        initialization.

        Overview
        --------

        ``AgentConfig`` is designed for ensuring configurability of agents.
        Subclasses need to provide implementations for the ``setup()`` and
        ``load()`` methods in order to properly define the behavior during the
        agent setup and configuration loading processes. This class follows the
        BaseModel design, making it easy to extend and customize according to
        specific agent requirements.

        Related Symbols
        ---------------

        -  ``automata.core.agent.instances.AutomataOpenAIAgentInstance.Config``
        -  ``automata.tests.unit.test_automata_agent_builder.test_builder_default_config``
        -  ``automata.tests.unit.test_task_environment.TestURL``
        -  ``automata.core.base.agent.AgentInstance.Config``

        Example
        -------

        The following example demonstrates how to create a custom agent
        configuration by extending the ``AgentConfig`` class:

        .. code:: python

        from config.config_types import AgentConfig

        class CustomAgentConfig(AgentConfig):

            def setup(self):
                # Define your custom agent setup process
                pass

            @classmethod
            def load(cls, config_name: AgentConfigName) -> "CustomAgentConfig":
                # Load the config for your custom agent
                pass

        Limitations
        -----------

        ``AgentConfig`` itself is an abstract class and cannot directly be
        instantiated. It must be subclassed, and its methods need to be
        implemented by the extending class according to the specific agent
        requirements. Additionally, the current implementation allows for
        arbitrary types, which may lead to code that is not type-safe.

        Follow-up Questions:
        --------------------

        -  How can we ensure type safety while maintaining the flexibility and
        customizability provided by ``AgentConfig``?



        """
        abbreviated_selected_symbol = symbol.uri.split("/")[1].split("#")[0]

        search_list = self.generate_search_list(abbreviated_selected_symbol)

        self.retriever.reset()
        self.retriever.process_symbol(symbol, search_list)

        prompt = Template(DEFAULT_DOC_GENERATION_PROMPT).render(
            symbol_dotpath=abbreviated_selected_symbol,
            symbol_context=self.retriever.get_context_buffer(),
        )

        document = self.completion_provider.standalone_call(prompt)
        summary = self.completion_provider.standalone_call(
            f"Condense the documentation below down to one to two concise paragraphs:\n {document}\nIf there is an example, include that in full in the output."
        )
        embedding = self.embedding_provider.build_embedding_array(document)

        return SymbolDocEmbedding(
            symbol,
            vector=embedding,
            source_code=source_code,
            document=document,
            summary=summary,
            context=prompt,
        )

    def generate_search_list(self, abbreviated_selected_symbol: str) -> List[Symbol]:
        """Generate a search list by splicing the search results on the symbol with the search results biased on tests."""
        search_results = self.symbol_search.symbol_rank_search(f"{abbreviated_selected_symbol}")
        search_results_with_tests = [ele for ele in search_results if "test" in ele[0].uri]
        search_results_without_tests = [ele for ele in search_results if "test" not in ele[0].uri]
        search_list: List[Symbol] = []
        for i in range(max(len(search_results_with_tests), len(search_results_without_tests))):
            set_list = set(search_list)
            if i < len(search_results_with_tests) and search_results_with_tests[i] not in set_list:
                search_list.append(search_results_with_tests[i][0])
            if (
                i < len(search_results_without_tests)
                and search_results_without_tests[i] not in set_list
            ):
                search_list.append(search_results_without_tests[i][0])
        return search_list

    def update_existing_embedding(self, source_code: str, symbol: Symbol) -> None:
        """
        Check if the embedding for a symbol needs to be updated.
        This is done by comparing the source code of the symbol to the source code


        FIXME - We need to add logic similar to what we have
            in the code embedding handler to update documentation
            when a sufficient threshold has been breached
            the following is a representative snippet -
            if existing_embedding.embedding_source != source_code:
            logger.debug("Building a new embedding for %s", symbol)
            self.embedding_db.discard(symbol)
            symbol_embedding = self.build_embedding_array(source_code, symbol)
            self.embedding_db.add(symbol_embedding)
        """
        existing_embedding = self.embedding_db.get(symbol)
        # For now, we will just automatically roll the existing documentation forward
        if existing_embedding.symbol != symbol or existing_embedding.source_code != source_code:
            logger.debug(
                f"Rolling forward the embedding for {existing_embedding.symbol} to {symbol}"
            )
            self.embedding_db.discard(symbol)
            existing_embedding.symbol = symbol
            existing_embedding.source_code = source_code
            self.embedding_db.add(existing_embedding)
        else:
            logger.debug("Passing for %s", symbol)
