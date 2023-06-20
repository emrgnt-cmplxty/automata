import logging

from automata.core.database.vector import VectorDatabaseProvider
from automata.core.symbol.symbol_types import Symbol, SymbolCodeEmbedding

from .embedding_types import EmbeddingProvider, SymbolEmbeddingHandler

logger = logging.getLogger(__name__)


class SymbolCodeEmbeddingHandler(SymbolEmbeddingHandler):
    def __init__(
        self,
        embedding_db: VectorDatabaseProvider,
        embedding_provider: EmbeddingProvider,
    ) -> None:
        """
        A constructor for SymbolCodeEmbeddingHandler

        Args:
            embedding_db (VectorDatabaseProvider): The database to store the embeddings in
            embedding_provider (Optional[EmbeddingProvider]): The provider to
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

    def update_embedding(self, symbol: Symbol) -> None:
        """
        Concrete method to update the embedding for a symbol.

        Args:
            symbols_to_update (List[Symbol]): List of symbols to update

        Raises:
            ValueError: If the symbol has no source code
        """
        from automata.core.symbol.symbol_utils import (  # imported late for mocking
            convert_to_fst_object,
        )

        source_code = str(convert_to_fst_object(symbol))

        if not source_code:
            raise ValueError(f"Symbol {symbol} has no source code")

        if self.embedding_db.contains(symbol):
            self.update_existing_embedding(source_code, symbol)
        else:
            symbol_embedding = self.build_embedding(source_code, symbol)
            self.embedding_db.add(symbol_embedding)

    def build_embedding(self, source_code: str, symbol: Symbol) -> SymbolCodeEmbedding:
        """
        Build the embedding for a symbol.

        Args:
            symbol (Symbol): Symbol to build the embedding for

        Returns:
            SymbolEmbedding: The embedding for the symbol
        """
        embedding_vector = self.embedding_provider.build_embedding(source_code)
        return SymbolCodeEmbedding(symbol, source_code, embedding_vector)

    def update_existing_embedding(self, source_code: str, symbol: Symbol) -> None:
        """
        Check if the embedding for a symbol needs to be updated.
        This is done by comparing the source code of the symbol to the source code

        Args:
            source_code (str): The source code of the symbol
            symbol (Symbol): The symbol to update
        """
        existing_embedding = self.embedding_db.get(symbol)
        if existing_embedding.embedding_source != source_code:
            logger.debug("Building a new embedding for %s", symbol)
            self.embedding_db.discard(symbol)
            symbol_embedding = self.build_embedding(source_code, symbol)
            self.embedding_db.add(symbol_embedding)
        elif existing_embedding.symbol != symbol:
            logger.debug("Updating the embedding for %s", symbol)
            self.embedding_db.discard(symbol)
            existing_embedding.symbol = symbol
            self.embedding_db.add(existing_embedding)
        else:
            logger.debug("Passing for %s", symbol)
            pass
