import abc
from typing import List

from automata.core.base.database.vector import VectorDatabaseProvider
from automata.embedding.base import EmbeddingBuilder, EmbeddingHandler
from automata.symbol.base import ISymbolProvider, Symbol
from automata.symbol_embedding.base import SymbolEmbedding


class SymbolEmbeddingHandler(EmbeddingHandler, ISymbolProvider):
    """An abstract class to handle the embedding of symbols"""

    def __init__(
        self,
        embedding_db: VectorDatabaseProvider,
        embedding_builder: EmbeddingBuilder,
    ) -> None:
        """An abstract constructor for SymbolEmbeddingHandler"""
        self.embedding_db = embedding_db
        self.embedding_builder = embedding_builder
        self.sorted_supported_symbols = [
            ele.symbol for ele in self.embedding_db.get_ordered_entries()
        ]

    @abc.abstractmethod
    def process_embedding(self, symbol: Symbol) -> None:
        """An abstract method to process the embedding for a symbol"""
        pass

    def get_embedding(self, symbol: Symbol) -> SymbolEmbedding:
        return self.embedding_db.get(symbol.dotpath)

    def get_ordered_entries(self) -> List[SymbolEmbedding]:
        return [self.get_embedding(ele) for ele in self.sorted_supported_symbols]

    # ISymbolProvider methods

    def _get_sorted_supported_symbols(self) -> List[Symbol]:
        return self.sorted_supported_symbols

    def filter_symbols(self, new_sorted_supported_symbols: List[Symbol]) -> None:
        """Filter the symbols to only those in the new sorted_supported_symbols set"""
        self.sorted_supported_symbols = new_sorted_supported_symbols
