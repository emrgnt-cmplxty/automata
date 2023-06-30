import abc
from typing import Optional

import numpy as np

from automata.core.symbol.base import Symbol


class SymbolEmbedding(abc.ABC):
    """Abstract base class for different types of embeddings"""

    def __init__(self, symbol: Symbol, embedding_source: str, vector: np.ndarray):
        self.symbol = symbol
        self.embedding_source = embedding_source
        self.vector = vector

    @abc.abstractmethod
    def __str__(self) -> str:
        pass


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
