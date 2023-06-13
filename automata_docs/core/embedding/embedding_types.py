import abc
import logging
from enum import Enum
from typing import Any, Dict, List, Optional

import numpy as np
import openai

from automata_docs.core.database.vector import VectorDatabaseProvider
from automata_docs.core.symbol.symbol_types import Symbol, SymbolCodeEmbedding, SymbolEmbedding

logger = logging.getLogger(__name__)


class NormType(Enum):
    L1 = "l1"
    L2 = "l2"
    SOFTMAX = "softmax"


class EmbeddingsProvider:
    def __init__(self):
        if not openai.api_key:
            from config import OPENAI_API_KEY

            openai.api_key = OPENAI_API_KEY

    def build_embedding(self, symbol_source: str) -> np.ndarray:
        """
        Get the embedding for a symbol.
        Args:
            symbol_source (str): The source code of the symbol
        Returns:
            A numpy array representing the embedding
        """
        # wait to import build_embedding to allow easy mocking of the function in tests.
        from openai.embeddings_utils import get_embedding

        return np.array(get_embedding(symbol_source, engine="text-embedding-ada-002"))


class EmbeddingHandler(abc.ABC):
    @abc.abstractmethod
    def __init__(
        self,
        embedding_db: VectorDatabaseProvider,
        embedding_provider: Optional[EmbeddingsProvider],
    ):
        pass

    @abc.abstractmethod
    def get_embedding(self, symbol: Symbol) -> SymbolEmbedding:
        pass

    @abc.abstractmethod
    def update_embedding(self, symbol: Symbol) -> None:
        pass

    @abc.abstractmethod
    def get_all_supported_symbols(self) -> List[Symbol]:
        pass


class EmbeddingSimilarity(abc.ABC):
    @abc.abstractmethod
    def __init__(
        self,
        symbol_embedding_manager: EmbeddingHandler,
        norm_type: Optional[NormType],
    ):
        pass

    @abc.abstractmethod
    def get_query_similarity_dict(self, query_text: str) -> Dict[Any, float]:
        pass

    @abc.abstractmethod
    def get_nearest_entries_for_query(self, query_text: str, k_nearest: int) -> Dict[Any, float]:
        pass
