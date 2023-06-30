import abc
from typing import Any, List, Optional

import numpy as np

from automata.core.base.database.vector import JSONVectorDatabase
from automata.core.base.embedding import EmbeddingProvider
from automata.core.base.symbol import Symbol


class SymbolEmbedding(abc.ABC):
    """Abstract base class for different types of embeddings"""

    def __init__(self, symbol: Symbol, embedding_source: str, vector: np.ndarray):
        self.symbol = symbol
        self.embedding_source = embedding_source
        self.vector = vector

    @abc.abstractmethod
    def __str__(self) -> str:
        pass


class JSONSymbolEmbeddingVectorDatabase(JSONVectorDatabase):
    """Concrete class to provide a vector database that saves into a JSON file."""

    def __init__(self, file_path: str):
        super().__init__(file_path)

    def entry_to_key(self, entry: SymbolEmbedding) -> str:
        """Method to generate a hashable key from an entry of type T."""
        return entry.symbol.dotpath

    def get_all_entries(self) -> List[SymbolEmbedding]:
        return sorted(self.data, key=lambda x: self.entry_to_key(x))


class SymbolCodeEmbedding(SymbolEmbedding):
    """A concrete class for symbol code embeddings"""

    def __init__(self, symbol: Symbol, source_code: str, vector: np.ndarray):
        super().__init__(symbol, source_code, vector)

    def __str__(self) -> str:
        return f"SymbolCodeEmbedding(\nsymbol={self.symbol},\n\nembedding_source={self.embedding_source}\n\nvector_length={len(self.vector)}\n)"


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
        return f"SymbolDocEmbedding(\nsymbol={self.symbol},\n\nembedding_source={self.embedding_source}\n\nvector_length={len(self.vector)}\n\nsource_code={self.source_code}\n\nsummary={self.summary}\n\ncontext={self.context}\n)"


class SymbolEmbeddingBuilder(abc.ABC):
    """An abstract class to build embeddings for symbols"""

    def __init__(
        self,
        embedding_provider: EmbeddingProvider,
    ) -> None:
        self.embedding_provider = embedding_provider

    @abc.abstractmethod
    def build(self, source_text: str, symbol: Symbol) -> Any:
        """An abstract method to build the embedding for a symbol"""
        pass

    def fetch_embedding_context(self, symbol: Symbol) -> str:
        """For a code embedding the context is the source code itself."""
        from automata.core.symbol.symbol_utils import (  # imported late for mocking
            convert_to_fst_object,
        )

        return str(convert_to_fst_object(symbol))


class SymbolEmbeddingHandler(abc.ABC):
    """An abstract class to handle the embedding of symbols"""

    @abc.abstractmethod
    def __init__(
        self,
        embedding_db: JSONSymbolEmbeddingVectorDatabase,
        embedding_builder: SymbolEmbeddingBuilder,
    ) -> None:
        """An abstract constructor for SymbolEmbeddingHandler"""
        self.embedding_db = embedding_db
        self.embedding_builder = embedding_builder

    @abc.abstractmethod
    def get_embedding(self, symbol: Symbol) -> Any:
        """An abstract method to get the embedding for a symbol"""
        pass

    @abc.abstractmethod
    def process_embedding(self, symbol: Symbol) -> None:
        """An abstract method to process the embedding for a symbol"""
        pass

    def get_all_supported_symbols(self) -> List[Symbol]:
        return [embedding.symbol for embedding in self.embedding_db.get_all_entries()]
