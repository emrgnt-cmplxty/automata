import abc
import logging
from typing import Dict, List, Optional

import numpy as np
import openai

from automata_docs.core.database.vector import VectorDatabaseProvider
from automata_docs.core.symbol.symbol_types import Symbol, SymbolCodeEmbedding, SymbolEmbedding

from .embedding_types import EmbeddingHandler, EmbeddingsProvider

logger = logging.getLogger(__name__)


class SymbolEmbeddingHandler(EmbeddingHandler):
    def __init__(
        self,
        embedding_db: VectorDatabaseProvider,
        embedding_provider: Optional[EmbeddingsProvider],
    ):
        self.embedding_db = embedding_db
        self.embedding_provider = embedding_provider or EmbeddingsProvider()

    @abc.abstractmethod
    def get_embedding(self, symbol: Symbol) -> SymbolEmbedding:
        pass

    @abc.abstractmethod
    def update_embedding(self, symbol: Symbol) -> None:
        pass

    @abc.abstractmethod
    def get_all_supported_symbols(self) -> List[Symbol]:
        pass


class SymbolCodeEmbeddingHandler(SymbolEmbeddingHandler):
    def __init__(
        self,
        embedding_db: VectorDatabaseProvider,
        embedding_provider: EmbeddingsProvider = EmbeddingsProvider(),
    ):
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

    def update_embedding(self, symbol: Symbol) -> None:
        """
        Update the embedding map with new symbols.

        Args:
            symbols_to_update (List[Symbol]): List of symbols to update
        Result:
            None
        """
        from automata_docs.core.symbol.symbol_utils import (  # imported late for mocking
            convert_to_fst_object,
        )

        try:
            symbol_source = str(convert_to_fst_object(symbol))
            symbol_desc_identifier = ".".join([desc.name for desc in symbol.descriptors])

            if self.embedding_db.contains(symbol):
                existing_embedding = self.embedding_db.get(symbol)

                if isinstance(existing_embedding, SymbolCodeEmbedding):
                    # If the symbol is already in the embedding map, check if the source code is the same
                    # If not, we can update the embedding
                    if existing_embedding.source_code != symbol_source:
                        logger.debug("Modifying existing embedding for symbol: %s" % symbol)
                        new_embedding = self.embedding_provider.build_embedding(symbol_source)
                        existing_embedding.vector = new_embedding
                        existing_embedding.source_code = symbol_source

                        # Update the embedding in the database
                        self.embedding_db.update(existing_embedding)
            else:
                # If the symbol does not exist in the embedding map, we add a new embedding
                logger.debug("Adding a new symbol: %s" % symbol)
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

    def get_all_supported_symbols(self) -> List[Symbol]:
        """
        Get all supported symbols.
        Args:
            None
        Returns:
            List[Symbol]: List of all supported symbols
        """
        return self.embedding_db.get_all_symbols()
