import abc
import logging
from enum import Enum
from typing import Any, Dict, List

import numpy as np

from automata.core.base.database.vector import VectorDatabaseProvider
from automata.core.symbol.symbol_types import Symbol

logger = logging.getLogger(__name__)


class EmbeddingNormType(Enum):
    L1 = "l1"
    L2 = "l2"
    SOFTMAX = "softmax"


class EmbeddingProvider(abc.ABC):
    """A class to provide embeddings for symbols"""

    @abc.abstractmethod
    def build_embedding(self, symbol_source: str) -> np.ndarray:
        pass


class SymbolEmbeddingHandler(abc.ABC):
    """An abstract class to handle the embedding of symbols"""

    @abc.abstractmethod
    def __init__(
        self,
        embedding_db: VectorDatabaseProvider,
        embedding_provider: EmbeddingProvider,
    ) -> None:
        """An abstract constructor for SymbolEmbeddingHandler"""
        self.embedding_db = embedding_db
        self.embedding_provider = embedding_provider

    @abc.abstractmethod
    def get_embedding(self, symbol: Symbol) -> Any:
        """An abstract method to get the embedding for a symbol"""
        pass

    @abc.abstractmethod
    def update_embedding(self, symbol: Symbol) -> None:
        """An abstract method to update the embedding for a symbol"""
        pass

    def get_all_supported_symbols(self) -> List[Symbol]:
        """
        Get all the symbols in the database.

        Returns:
            List[Symbol]: List of all the symbols in the database
        """
        return self.embedding_db.get_all_symbols()


class EmbeddingSimilarity(abc.ABC):
    @abc.abstractmethod
    def get_query_similarity_dict(self, query_text: str) -> Dict[Symbol, float]:
        """An abstract method to get the similarity between a query and all symbols"""
        pass

    @abc.abstractmethod
    def get_nearest_entries_for_query(
        self, query_text: str, k_nearest: int
    ) -> Dict[Symbol, float]:
        """An abstract method to get the k nearest symbols to a query"""
        pass
