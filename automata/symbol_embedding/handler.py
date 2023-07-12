import abc
from typing import List

from automata.core.base import VectorDatabaseProvider
from automata.embedding import EmbeddingBuilder, EmbeddingHandler
from automata.symbol import ISymbolProvider, Symbol
from automata.symbol_embedding import SymbolEmbedding


class SymbolEmbeddingHandler(EmbeddingHandler, ISymbolProvider):
    """An abstract class to handle the embedding of symbols"""

    def __init__(
        self,
        embedding_db: VectorDatabaseProvider,
        embedding_builder: EmbeddingBuilder,
        batch_size: int,
    ) -> None:
        """An abstract constructor for SymbolEmbeddingHandler"""

        if batch_size > 2048:
            raise ValueError("Batch size must be less than 2048")
        self.embedding_db = embedding_db
        self.embedding_builder = embedding_builder
        self.batch_size = batch_size

        self.sorted_supported_symbols = [
            ele.symbol for ele in self.embedding_db.get_ordered_embeddings()
        ]
        self.to_add: List[SymbolEmbedding] = []
        self.to_discard: List[str] = []

    @abc.abstractmethod
    def process_embedding(self, symbol: Symbol) -> None:
        """An abstract method to process the embedding for a symbol"""
        pass

    def get_embeddings(self, symbols: List[Symbol]) -> List[SymbolEmbedding]:
        return self.embedding_db.batch_get([symbol.dotpath for symbol in symbols])

    def get_ordered_embeddings(self) -> List[SymbolEmbedding]:
        return self.embedding_db.batch_get(
            [symbol.dotpath for symbol in self.sorted_supported_symbols]
        )

    def flush(self):
        """Perform any remaining updates that do not form a complete batch."""
        if self.to_discard:
            self.embedding_db.batch_discard(self.to_discard)
        if self.to_add:
            self.embedding_db.batch_add(self.to_add)
        # Reset the lists for next operations
        self.to_discard = []
        self.to_add = []

    # ISymbolProvider methods

    def _get_sorted_supported_symbols(self) -> List[Symbol]:
        return self.sorted_supported_symbols

    def filter_symbols(self, new_sorted_supported_symbols: List[Symbol]) -> None:
        """Filter the symbols to only those in the new sorted_supported_symbols set"""
        self.sorted_supported_symbols = new_sorted_supported_symbols
