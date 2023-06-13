import abc
import logging
from typing import List, Optional

from automata_docs.core.database.vector import VectorDatabaseProvider
from automata_docs.core.symbol.symbol_types import (
    Symbol,
    SymbolCodeEmbedding,
    SymbolDocumentEmbedding,
    SymbolEmbedding,
)

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
                    else:
                        logger.debug("Source code is unchanged, embedding is unchanged")
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


class SymbolDocumentEmbeddingHandler(SymbolEmbeddingHandler):
    def __init__(
        self,
        embedding_db: VectorDatabaseProvider,
        embedding_provider: EmbeddingsProvider = EmbeddingsProvider(),
    ):
        """
        A constructor for SymbolCodeEmbeddingHandler

        Args:
            embedding_db (VectorDatabaseProvider): The database to store the embeddings in
            embedding_provider (Optional[EmbeddingsProvider]): The provider to get the embeddings from
        """

        super().__init__(embedding_db, embedding_provider)

    def get_embedding(self, symbol: Symbol) -> SymbolDocumentEmbedding:
        """
        Get the embedding of a symbol.
        Args:
            symbol (Symbol): Symbol to get the embedding for
        Returns:
            SymbolDocumentEmbedding: The embedding of the symbol documentation
        """
        return self.embedding_db.get(symbol)

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

        symbol_module = convert_to_fst_object(symbol)
        import pdb

        pdb.set_trace()

        # from automata_docs.core.symbol.symbol_utils import (  # imported late for mocking
        #     convert_to_fst_object,
        # )

        # desc_path_to_symbol = {
        #     ".".join([desc.name for desc in symbol.descriptors]): symbol
        #     for symbol in self.embedding_db.get_all_symbols()
        # }
        # try:
        #     symbol_desc_identifier = ".".join([desc.name for desc in symbol.descriptors])
        #     symbol_source = str(convert_to_fst_object(symbol))
        #     if symbol_desc_identifier in desc_path_to_symbol:
        #         existing_embedding = self.embedding_db.get(
        #             desc_path_to_symbol[symbol_desc_identifier]
        #         )

        #         if isinstance(existing_embedding, SymbolCodeEmbedding):
        #             # If the symbol is already in the embedding map, check if the source code is the same
        #             # If not, we can update the embedding
        #             if existing_embedding.source_code != symbol_source:
        #                 logger.debug("Modifying existing embedding for symbol: %s" % symbol)
        #                 new_embedding = self.embedding_provider.build_embedding(symbol_source)
        #                 existing_embedding.vector = new_embedding
        #                 existing_embedding.source_code = symbol_source
        #                 # Update the embedding in the database
        #                 self.embedding_db.update(existing_embedding)
        #     else:
        #         # If the symbol does not exist in the embedding map, we add a new embedding
        #         logger.debug("Adding a new symbol: %s" % symbol)
        #         symbol_embedding = self.embedding_provider.build_embedding(symbol_source)

        #         new_embedding = SymbolCodeEmbedding(
        #             symbol=symbol,
        #             vector=symbol_embedding,
        #             source_code=symbol_source,
        #         )

        #         # Add the new embedding to the database
        #         self.embedding_db.add(new_embedding)
        # except Exception as e:
        #     if "local" not in symbol.uri:
        #         logger.error("Updating embedding for symbol: %s failed with %s" % (symbol, e))
