import logging
from typing import List

import openai
from jinja2 import Template

from automata.config.prompt.docs import DEFAULT_DOC_GENERATION_PROMPT
from automata.core.context.py_context.retriever import PyContextRetriever
from automata.core.database.vector import VectorDatabaseProvider
from automata.core.symbol.search.symbol_search import SymbolSearch
from automata.core.symbol.symbol_types import Symbol, SymbolDocEmbedding

from .embedding_types import EmbeddingProvider, SymbolEmbeddingHandler

logger = logging.getLogger(__name__)


class SymbolDocEmbeddingHandler(SymbolEmbeddingHandler):
    def __init__(
        self,
        embedding_db: VectorDatabaseProvider,
        embedding_provider: EmbeddingProvider,
        symbol_search: SymbolSearch,
        retriever: PyContextRetriever,
    ) -> None:
        """
        A constructor for SymbolDocEmbeddingHandler

        Args:
            embedding_db (VectorDatabaseProvider): The database to store the embeddings in
            embedding_provider (EmbeddingProvider): The provider to get the embeddings from
            code_embedding_handler (SymbolCodeEmbeddingHandler): The code embedding handler

        TODO: Add more logic around documentation updating
        """
        super().__init__(embedding_db, embedding_provider)
        self.symbol_search = symbol_search
        self.retriever = retriever

    def get_embedding(self, symbol: Symbol) -> SymbolDocEmbedding:
        """
        Get the embedding of a symbol.
        Args:
            symbol (Symbol): Symbol to get the embedding for
        Returns:
            SymbolDocEmbedding: The embedding of the symbol documentation
        """
        return self.embedding_db.get(symbol)

    def update_embedding(self, symbol: Symbol) -> None:
        """
        Concrete method to update the embedding for a symbol.

        Args:
            symbols_to_update (List[Symbol]): List of symbols to update

        Raises:
            ValueError: If the symbol has no source code

        NOTE: This method always updates the embedding and associated documentation
            We should add some logic to check if the documentation needs updating
            This is non-trivial because of how dependencies interact
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
        Build the embedding for a symbol's documentation

        Args:
            source_code (str): The source code of the symbol
            symbol (Symbol): The symbol to build the embedding for

        Returns:
            SymbolDocEmbedding: The embedding for the symbol's documentation
        """
        abbreviated_selected_symbol = symbol.uri.split("/")[1].split("#")[0]

        def get_doc(prompt: str) -> str:
            """
            Get the documentation for a symbol

            Args:
                prompt (str): The prompt to use to generate the documentation

            Returns:
                str: The completed documentation for the symbol
            """
            completion = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {
                        "role": "user",
                        "content": prompt,
                    }
                ],
            )
            if not completion.choices:
                return "Error: No completion found"

            return completion.choices[0]["message"]["content"]

        def get_summary(input_doc: str) -> str:
            """
            Get a summary for a symbol's documentation

            Args:
                prompt (str): The prompt to use to generate the documentation

            Returns:
                str: The completed documentation for the symbol
            """

            completion = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {
                        "role": "user",
                        "content": f"Condense the documentation below down to one to two concise paragraphs:\n {input_doc}\nIf there is an example, include that in full in the output.",
                    }
                ],
            )
            if not completion.choices:
                return "Error: No completion found"

            return completion.choices[0]["message"]["content"]

        # Splice the search results on the symbol
        # with the search results biased on tests
        # this is to get bias towards specific examples for the documentation
        search_results = self.symbol_search.symbol_rank_search(f"{abbreviated_selected_symbol}")
        search_results_with_tests = [ele for ele in search_results if "test" in ele[0].uri]
        search_results_without_tests = [ele for ele in search_results if "test" not in ele[0].uri]
        search_list: List[Symbol] = []
        for i in range(max(len(search_results_with_tests), len(search_results_without_tests))):
            set_list = set(search_list)
            if (
                i < len(search_results_with_tests) - 1
                and search_results_with_tests[i] not in set_list
            ):
                search_list.append(search_results_with_tests[i][0])
            if (
                i < len(search_results_without_tests) - 1
                and search_results_without_tests[i] not in set_list
            ):
                search_list.append(search_results_without_tests[i][0])

        self.retriever.reset()
        self.retriever.process_symbol(symbol, search_list)

        prompt = Template(DEFAULT_DOC_GENERATION_PROMPT).render(
            symbol_dotpath=abbreviated_selected_symbol,
            symbol_context=self.retriever.get_context_buffer(),
        )

        document = get_doc(prompt)
        summary = get_summary(document)
        embedding = self.embedding_provider.build_embedding(document)

        return SymbolDocEmbedding(
            symbol,
            vector=embedding,
            source_code=source_code,
            document=document,
            summary=summary,
            context=prompt,
        )

    def update_existing_embedding(self, source_code: str, symbol: Symbol) -> None:
        """
        Check if the embedding for a symbol needs to be updated.
        This is done by comparing the source code of the symbol to the source code

        Args:
            source_code (str): The source code of the symbol
            symbol (Symbol): The symbol to update
        """
        existing_embedding = self.embedding_db.get(symbol)
        # FIXME - We need to add logic similar to what we have
        # in the code embedding handler to update documentation
        # when a sufficient threshold has been breached
        # the following is a representative snippet -
        # if existing_embedding.embedding_source != source_code:
        # logger.debug("Building a new embedding for %s", symbol)
        # self.embedding_db.discard(symbol)
        # symbol_embedding = self.build_embedding(source_code, symbol)
        # self.embedding_db.add(symbol_embedding)

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
