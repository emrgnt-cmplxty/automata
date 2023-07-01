import abc
import logging
from enum import Enum
from typing import Dict

import numpy as np

from automata.core.base.symbol import Symbol

logger = logging.getLogger(__name__)


class EmbeddingNormType(Enum):
    L1 = "l1"
    L2 = "l2"
    SOFTMAX = "softmax"


class EmbeddingProvider(abc.ABC):
    """A class to provide embeddings for symbols"""

    @abc.abstractmethod
    def build_embedding_array(self, symbol_source: str) -> np.ndarray:
        pass


class EmbeddingSimilarityCalculator(abc.ABC):
    @abc.abstractmethod
    def calculate_query_similarity_dict(self, query_text: str) -> Dict[Symbol, float]:
        """An abstract method to get the similarity between a query and all symbols"""
        pass

    @abc.abstractmethod
    def _calculate_embedding_similarity(self, embedding_array: np.ndarray) -> np.ndarray:
        """An abstract method to calculate the similarity between the embedding array target embeddings."""
        pass

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
