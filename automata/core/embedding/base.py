import abc
import logging
from enum import Enum
from typing import Any, Dict, Sequence

import numpy as np

from automata.core.base.database.vector import VectorDatabaseProvider
from automata.core.symbol.base import Symbol

logger = logging.getLogger(__name__)


class EmbeddingNormType(Enum):
    L1 = "l1"
    L2 = "l2"
    SOFTMAX = "softmax"


class EmbeddingVectorProvider(abc.ABC):
    """A class to provide embeddings for symbols"""

    @abc.abstractmethod
    def build_embedding_vector(self, symbol_source: str) -> np.ndarray:
        pass


class Embedding(abc.ABC):
    """Abstract base class for different types of embeddings"""

    def __init__(self, key: Any, input_object: str, vector: np.ndarray):
        self.key = key
        self.input_object = input_object
        self.vector = vector

    @abc.abstractmethod
    def __str__(self) -> str:
        pass


class EmbeddingBuilder(abc.ABC):
    """An abstract class to build embeddings"""

    def __init__(
        self,
        embedding_provider: EmbeddingVectorProvider,
    ) -> None:
        self.embedding_provider = embedding_provider

    @abc.abstractmethod
    def build(self, source_text: str, symbol: Symbol) -> Any:
        """An abstract method to build the embedding for a symbol"""
        pass

    def fetch_embedding_source_code(self, symbol: Symbol) -> str:
        """An abstract method for embedding the context is the source code itself."""
        from automata.core.symbol.symbol_utils import (  # imported late for mocking
            convert_to_fst_object,
        )

        return str(convert_to_fst_object(symbol))


class EmbeddingHandler(abc.ABC):
    """An abstract class to handle embeddings"""

    @abc.abstractmethod
    def __init__(
        self,
        embedding_db: VectorDatabaseProvider,
        embedding_builder: EmbeddingBuilder,
    ) -> None:
        """An abstract constructor for EmbeddingHandler"""
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


class EmbeddingSimilarityCalculator:
    def __init__(
        self,
        embedding_provider: EmbeddingVectorProvider,
        norm_type: EmbeddingNormType = EmbeddingNormType.L2,
    ) -> None:
        """Initializes SymbolSimilarity by building the associated symbol mappings."""
        self.embedding_provider: EmbeddingVectorProvider = embedding_provider
        self.norm_type = norm_type

    def calculate_query_similarity_dict(
        self, ordered_embeddings: Sequence[Embedding], query_text: str, return_sorted: bool = True
    ) -> Dict[Symbol, float]:
        """
        Similarity is calculated between the dot product
        of the query embedding and the symbol embeddings.
        Return result is sorted in descending order by default.
        """
        query_embedding_vector = self.embedding_provider.build_embedding_vector(query_text)
        # Compute the similarity of the query to all symbols
        similarity_scores = self._calculate_embedding_similarity(
            np.array([ele.vector for ele in ordered_embeddings]), query_embedding_vector
        )

        similarity_dict = {
            ele.key: similarity_scores[i] for i, ele in enumerate(ordered_embeddings)
        }

        if return_sorted:
            # Sort the dictionary by values in descending order
            similarity_dict = dict(
                sorted(similarity_dict.items(), key=lambda item: item[1], reverse=True)
            )

        return similarity_dict

    def _calculate_embedding_similarity(
        self, ordered_embeddings: np.ndarray, embedding_array: np.ndarray
    ) -> np.ndarray:
        """Calculate the similarity score between the embedding with all symbol embeddings"""
        # Normalize the embeddings and the query embedding
        embeddings_norm = self._normalize_embeddings(ordered_embeddings, self.norm_type)
        normed_embedding = self._normalize_embeddings(
            embedding_array[np.newaxis, :], self.norm_type
        )[0]

        return np.dot(embeddings_norm, normed_embedding)

    @staticmethod
    def _normalize_embeddings(
        embeddings_array: np.ndarray, norm_type: EmbeddingNormType
    ) -> np.ndarray:
        if norm_type == EmbeddingNormType.L1:
            norm = np.sum(np.abs(embeddings_array), axis=1, keepdims=True)
            return embeddings_array / norm
        elif norm_type == EmbeddingNormType.L2:
            return embeddings_array / np.linalg.norm(embeddings_array, axis=1, keepdims=True)
        elif norm_type == EmbeddingNormType.SOFTMAX:
            e_x = np.exp(embeddings_array - np.max(embeddings_array, axis=1, keepdims=True))
            return e_x / np.sum(e_x, axis=1, keepdims=True)
        else:
            raise ValueError(f"Invalid normalization type {norm_type}")
