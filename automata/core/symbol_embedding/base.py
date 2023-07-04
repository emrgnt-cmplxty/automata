import abc
from typing import Any, List, Optional, Set

import numpy as np

from automata.core.base.database.vector import JSONVectorDatabase
from automata.core.embedding.base import (
    Embedding,
    EmbeddingBuilder,
    EmbeddingHandler,
    EmbeddingVectorProvider,
)
from automata.core.symbol.base import ISymbolProvider, Symbol
from automata.core.utils import is_sorted


class SymbolEmbedding(Embedding):
    """An abstract class for symbol code embeddings"""

    @abc.abstractmethod
    def __init__(self, key: Symbol, input_object: str, vector: np.ndarray):
        super().__init__(key, input_object, vector)

    @property
    def symbol(self) -> Symbol:
        return self.key

    @symbol.setter
    def symbol(self, value: Symbol):
        self.key = value

    @abc.abstractmethod
    def __str__(self) -> str:
        pass


class SymbolCodeEmbedding(SymbolEmbedding):
    """A concrete class for symbol code embeddings"""

    def __init__(self, symbol: Symbol, source_code: str, vector: np.ndarray):
        super().__init__(symbol, source_code, vector)

    def __str__(self) -> str:
        return f"SymbolCodeEmbedding(\nsymbol={self.symbol},\n\nembedding_source={self.input_object}\n\nvector_length={len(self.vector)}\n)"


class SymbolDocEmbedding(SymbolEmbedding):
    """A concrete class for symbol document embeddings"""

    def __init__(
        self,
        symbol: Symbol,
        document: str,
        vector: np.ndarray,
        source_code: Optional[str] = None,
        summary: Optional[str] = None,
        context: Optional[str] = None,
    ) -> None:
        super().__init__(symbol, document, vector)
        # begin additional meta data
        self.source_code = source_code
        self.summary = summary
        self.context = context

    def __str__(self) -> str:
        return f"SymbolDocEmbedding(\nsymbol={self.symbol},\n\nembedding_source={self.input_object}\n\nvector_length={len(self.vector)}\n\nsource_code={self.source_code}\n\nsummary={self.summary}\n\ncontext={self.context}\n)"


class JSONSymbolEmbeddingVectorDatabase(JSONVectorDatabase):
    """Concrete class to provide a vector database that saves into a JSON file."""

    def __init__(self, file_path: str):
        super().__init__(file_path)

    def entry_to_key(self, entry: SymbolEmbedding) -> str:
        """Concrete implementation to generate a simple hashable key from a Symbol."""
        return entry.symbol.dotpath

    def get_ordered_embeddings(self) -> List[SymbolEmbedding]:
        return sorted(self.data, key=lambda x: self.entry_to_key(x))


class SymbolEmbeddingHandler(EmbeddingHandler, ISymbolProvider):
    """An abstract class to handle the embedding of symbols"""

    @abc.abstractmethod
    def __init__(
        self,
        embedding_db: JSONSymbolEmbeddingVectorDatabase,
        embedding_builder: EmbeddingBuilder,
    ) -> None:
        """An abstract constructor for SymbolEmbeddingHandler"""
        self.embedding_db = embedding_db
        self.embedding_builder = embedding_builder
        self.sorted_supported_symbols = [
            ele.symbol for ele in self.embedding_db.get_ordered_embeddings()
        ]

    @abc.abstractmethod
    def get_embedding(self, symbol: Symbol) -> Any:
        """An abstract method to get the embedding for a symbol"""
        pass

    @abc.abstractmethod
    def process_embedding(self, symbol: Symbol) -> None:
        """An abstract method to process the embedding for a symbol"""
        pass

    def get_ordered_embeddings(self) -> List[SymbolEmbedding]:
        return [self.get_embedding(ele) for ele in self.sorted_supported_symbols]

    # ISymbolProvider methods

    def _get_sorted_supported_symbols(self) -> List[Symbol]:
        return self.sorted_supported_symbols

    def filter_symbols(self, new_sorted_supported_symbols: List[Symbol]) -> None:
        """Filter the symbols to only those in the new sorted_supported_symbols set"""
        self.sorted_supported_symbols = new_sorted_supported_symbols
