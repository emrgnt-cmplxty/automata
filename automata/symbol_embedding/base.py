import abc
from typing import Any, Dict, Optional

import numpy as np

from automata.embedding import Embedding
from automata.symbol import Symbol


class SymbolEmbedding(Embedding):
    """An abstract class for symbol code embeddings"""

    def __init__(
        self,
        key: Symbol,
        document: str,
        vector: np.ndarray,
        *args: Any,
        **kwargs: Any,
    ):
        super().__init__(key, document, vector)

    @property
    def symbol(self) -> Symbol:
        return self.key

    @symbol.setter
    def symbol(self, value: Symbol):
        self.key = value

    def __str__(self) -> str:
        return f"SymbolEmbedding(\nsymbol={self.symbol},\n\nembedding_source={self.document}\n\nvector_length={len(self.vector)}\n)"

    @property
    @abc.abstractmethod
    def metadata(self) -> Dict[str, str]:
        pass

    @classmethod
    def from_args(cls, **kwargs: Any) -> "SymbolEmbedding":
        """Create a SymbolEmbedding from the given arguments"""
        return cls(**kwargs)


class SymbolCodeEmbedding(SymbolEmbedding):
    """A concrete class for symbol code embeddings"""

    def __init__(self, key: Symbol, document: str, vector: np.ndarray):
        super().__init__(key, document, vector)

    def __str__(self) -> str:
        return f"SymbolCodeEmbedding(\nsymbol={self.symbol},\n\nembedding_source={self.document}\n\nvector_length={len(self.vector)}\n)"

    @property
    def metadata(self) -> Dict[str, str]:
        return {}


class SymbolDocEmbedding(SymbolEmbedding):
    """A concrete class for symbol document embeddings"""

    def __init__(
        self,
        key: Symbol,
        document: str,
        vector: np.ndarray,
        source_code: Optional[str] = None,
        summary: Optional[str] = None,
        context: Optional[str] = None,
    ) -> None:
        super().__init__(key, document, vector)
        # begin additional meta data
        self.source_code = source_code
        self.summary = summary
        self.context = context

    def __str__(self) -> str:
        return f"SymbolDocEmbedding(\nsymbol={self.symbol},\n\nembedding_source={self.document}\n\nvector_length={len(self.vector)}\n\nsource_code={self.source_code}\n\nsummary={self.summary}\n\ncontext={self.context}\n)"

    @property
    def metadata(self) -> Dict[str, str]:
        return {
            "source_code": self.source_code or "",
            "summary": self.summary or "",
            "context": self.context or "",
        }
