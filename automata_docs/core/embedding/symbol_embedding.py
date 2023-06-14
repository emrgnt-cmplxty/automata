import abc
import logging
import os
from typing import List, Optional

import openai
from jinja2 import Template

from automata_docs.config.config_enums import ConfigCategory
from automata_docs.config.prompt.docs import DEFAULT_DOC_GENERATION_PROMPT
from automata_docs.core.context.py_context.retriever import PyContextRetriever
from automata_docs.core.database.vector import JSONVectorDatabase, VectorDatabaseProvider
from automata_docs.core.symbol.graph import SymbolGraph
from automata_docs.core.symbol.symbol_types import (
    Symbol,
    SymbolCodeEmbedding,
    SymbolDocEmbedding,
    SymbolEmbedding,
)
from automata_docs.core.utils import config_fpath

from .embedding_types import EmbeddingHandler, EmbeddingsProvider

logger = logging.getLogger(__name__)


class SymbolEmbeddingHandler(EmbeddingHandler):
    def __init__(
        self,
        embedding_db: VectorDatabaseProvider,
        embedding_provider: Optional[EmbeddingsProvider],
    ):
        """
        A constructor for SymbolEmbeddingHandler

        Args:
            embedding_db (VectorDatabaseProvider): The database to store the embeddings in
            embedding_provider (Optional[EmbeddingsProvider]): The provider to get the embeddings from
        """
        self.embedding_db = embedding_db
        self.embedding_provider = embedding_provider or EmbeddingsProvider()

    def get_all_supported_symbols(self) -> List[Symbol]:
        """
        Get all the symbols that are supported by the embedding provider.

        Returns:
            List[Symbol]: A list of all the symbols that are supported by the embedding provider
        """
        return self.embedding_db.get_all_symbols()

    @abc.abstractmethod
    def get_embedding(self, symbol: Symbol) -> SymbolEmbedding:
        """An abstract method to get the embedding for a symbol"""
        pass

    @abc.abstractmethod
    def update_embedding(self, symbol: Symbol):
        """An abstract method to update the embedding for a symbol"""
        pass


class SymbolCodeEmbeddingHandler(SymbolEmbeddingHandler):
    def __init__(
        self,
        embedding_db: VectorDatabaseProvider,
        embedding_provider: EmbeddingsProvider = EmbeddingsProvider(),
    ):
        """
        A constructor for SymbolCodeEmbeddingHandler

        Args:
            embedding_db (VectorDatabaseProvider): The database to store the embeddings in
            embedding_provider (Optional[EmbeddingsProvider]): The provider to
                get the embeddings from
        """
        super().__init__(embedding_db, embedding_provider)

    def get_embedding(self, symbol: Symbol) -> SymbolCodeEmbedding:
        """
        Get the embedding of a symbol.

        Args:
            symbol (Symbol): Symbol to get the embedding for

        Returns:
            Embedding: The embedding of the symbol
        """
        return self.embedding_db.get(symbol)

    def update_embedding(self, symbol: Symbol):
        """
        Update the embedding map with new symbols.

        Args:
            symbols_to_update (List[Symbol]): List of symbols to update
        """
        from automata_docs.core.symbol.symbol_utils import (  # imported late for mocking
            convert_to_fst_object,
        )

        desc_path_to_symbol = {
            ".".join([desc.name for desc in symbol.descriptors]): symbol
            for symbol in self.embedding_db.get_all_symbols()
        }
        try:
            symbol_desc_identifier = ".".join([desc.name for desc in symbol.descriptors])
            symbol_source = str(convert_to_fst_object(symbol))
            if symbol_desc_identifier in desc_path_to_symbol:
                logger.info(
                    f"Embedding already exists for symbol {symbol_desc_identifier}, updating ..."
                )
                existing_embedding = self.embedding_db.get(
                    desc_path_to_symbol[symbol_desc_identifier]
                )

                if isinstance(existing_embedding, SymbolCodeEmbedding):
                    # If the symbol is already in the embedding map, check if the source code is the same
                    # If not, we can update the embedding
                    if existing_embedding.source_code != symbol_source:
                        logger.debug("Regenerating the embedding")
                        new_embedding = self.embedding_provider.build_embedding(symbol_source)
                        existing_embedding.vector = new_embedding
                        existing_embedding.source_code = symbol_source
                        # Update the embedding in the database
                        self.embedding_db.update(existing_embedding)
                    elif existing_embedding.symbol != symbol:
                        existing_embedding.symbol = symbol
                        self.embedding_db.discard(existing_embedding.symbol)
                        self.embedding_db.add(existing_embedding)
                    # Otherwise, we don't need to do anything
                    else:
                        pass
            else:
                # If the symbol does not exist in the embedding map, we add a new embedding
                logger.info(
                    f"Embedding does not exist for symbol {symbol_desc_identifier}, updating ..."
                )
                symbol_embedding = self.embedding_provider.build_embedding(symbol_source)

                new_embedding = SymbolCodeEmbedding(
                    symbol=symbol,
                    vector=symbol_embedding,
                    source_code=symbol_source,
                )

                # Add the new embedding to the database
                self.embedding_db.add(new_embedding)
        except Exception as e:
            if "local" not in symbol.uri:
                logger.error("Updating embedding for symbol: %s failed with %s" % (symbol, e))


class SymbolDocEmbeddingHandler(SymbolEmbeddingHandler):
    def __init__(
        self,
        embedding_db: VectorDatabaseProvider,
        embedding_provider: EmbeddingsProvider = EmbeddingsProvider(),
        code_embedding_fpath: Optional[str] = None,
    ):
        """
        A constructor for SymbolCodeEmbeddingHandler

        Args:
            embedding_db (VectorDatabaseProvider): The database to store the embeddings in
            embedding_provider (Optional[EmbeddingsProvider]): The provider to get the embeddings from
            code_embedding_fpath (Optional[str]): The path to the code embedding file
        """
        from automata_docs.core.embedding.symbol_similarity import SymbolSimilarity
        from automata_docs.core.symbol.search.rank import SymbolRankConfig
        from automata_docs.core.symbol.search.symbol_search import SymbolSearch

        super().__init__(embedding_db, embedding_provider)
        if not code_embedding_fpath:
            code_embedding_fpath = os.path.join(
                config_fpath(), ConfigCategory.SYMBOL.value, "symbol_code_embedding.json"
            )

        graph = SymbolGraph()
        subgraph = graph.get_rankable_symbol_subgraph()

        code_embedding_db = JSONVectorDatabase(code_embedding_fpath)
        code_embedding_handler = SymbolCodeEmbeddingHandler(code_embedding_db)
        symbol_similarity = SymbolSimilarity(code_embedding_handler)
        self.graph = graph
        self.symbol_search = SymbolSearch(
            graph, symbol_similarity, symbol_rank_config=SymbolRankConfig(), code_subgraph=subgraph
        )

    def get_embedding(self, symbol: Symbol) -> SymbolDocEmbedding:
        """
        Get the embedding of a symbol.
        Args:
            symbol (Symbol): Symbol to get the embedding for
        Returns:
            SymbolDocEmbedding: The embedding of the symbol documentation
        """
        return self.embedding_db.get(symbol)

    def build_symbol_doc_embedding(self, symbol: Symbol, source_code: str) -> SymbolDocEmbedding:
        abbreviated_selected_symbol = symbol.uri.split("/")[1].split("#")[0]

        def get_doc(prompt: str) -> str:
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
        search_results_0 = self.symbol_search.symbol_rank_search(f"{abbreviated_selected_symbol}")
        search_results_1 = self.symbol_search.symbol_rank_search(
            f"{abbreviated_selected_symbol} tests or conftest"
        )

        search_list: List[Symbol] = []
        for i in range(len(search_results_0)):
            set_list = set(search_list)
            if search_results_0[i] not in set_list:
                search_list.append(search_results_0[i][0])
            elif search_results_1[i] not in set_list:
                search_list.append(search_results_1[i][0])

        retriever = PyContextRetriever(self.graph)
        retriever.process_symbol(symbol, search_list)
        print("retriever.get_context_buffer(): ", retriever.get_context_buffer())

        prompt = Template(DEFAULT_DOC_GENERATION_PROMPT).render(
            symbol_dotpath=abbreviated_selected_symbol,
            symbol_context=retriever.get_context_buffer(),
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

    def update_embedding(self, symbol: Symbol):
        """
        Update the embedding map with new symbols.

        Args:
            symbols_to_update (List[Symbol]): List of symbols to update
        Returns:
            None
        """
        from automata_docs.core.symbol.symbol_utils import (  # imported late for mocking
            convert_to_fst_object,
        )

        desc_path_to_symbol = {
            ".".join([desc.name for desc in symbol.descriptors]): symbol
            for symbol in self.embedding_db.get_all_symbols()
        }
        try:
            symbol_desc_identifier = ".".join([desc.name for desc in symbol.descriptors])
            symbol_source_obj = convert_to_fst_object(symbol)
            print("calling update embedding..")
            if symbol_desc_identifier in desc_path_to_symbol:
                print("passing ...")
                pass
            else:
                new_embedding = self.build_symbol_doc_embedding(symbol, str(symbol_source_obj))
                self.embedding_db.add(new_embedding)
        except Exception as e:
            logger.error("Failed to get source code for symbol %s" % symbol)