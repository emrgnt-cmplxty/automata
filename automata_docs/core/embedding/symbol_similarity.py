import logging
from copy import deepcopy
from enum import Enum
from typing import Dict, Optional

import numpy as np

from automata_docs.core.embedding.symbol_embedding_map import (
    EmbeddingsProvider,
    SymbolEmbeddingMap,
)
from automata_docs.core.symbol.symbol_types import Symbol, SymbolEmbedding

logger = logging.getLogger(__name__)


class NormType(Enum):
    L1 = "l1"
    L2 = "l2"
    SOFTMAX = "softmax"


class SymbolSimilarity:
    def __init__(
        self,
        symbol_embedding_map: SymbolEmbeddingMap,
        norm_type: NormType = NormType.L2,
    ):
        """
        Initialize SymbolSimilarity
        Args:
            symbol_embedding_map (SymbolSimilarity): SymbolSimilarity object
        Result:
            An instance of SymbolSimilarity
        """
        self.embedding_dict: Dict[Symbol, SymbolEmbedding] = deepcopy(
            symbol_embedding_map.get_embedding_dict()
        )
        self.embedding_provider: EmbeddingsProvider = symbol_embedding_map.embedding_provider
        self.default_norm_type = norm_type
        symbols = sorted(list(self.embedding_dict.keys()), key=lambda x: x.uri)
        self.index_to_symbol = {i: symbol for i, symbol in enumerate(symbols)}
        self.symbol_to_index = {symbol: i for i, symbol in enumerate(symbols)}

    def transform_similarity_matrix(
        self, S: np.ndarray, query_text: str, norm_type: Optional[str] = None
    ) -> np.ndarray:
        """
        Perform a unitary transformation on the similarity matrix.

        Args:
            S (np.ndarray): The similarity matrix
            query_text (str): The query text

        Returns:
            The transformed similarity matrix as a numpy array.
        """
        # Step 1: Construct a unit-normed vector (e)
        e = self._generate_unit_normed_query_vector(query_text, self._process_norm_type(norm_type))

        # Step 2: Reshape e to have shape (n, 1) and (1, n) so it can be used in broadcasting operation
        e_row = np.reshape(e, (1, -1))
        e_col = np.reshape(e, (-1, 1))

        # Step 3: Construct the transformation matrix P
        P = e_col * e_row

        # Step 4: Perform a transformation on the similarity matrix, e.g. compute P * S
        transformed_similarity_matrix = P * S

        # Step 5: Normalize the transformed similarity matrix by its Frobenius norm
        transformed_similarity_matrix = transformed_similarity_matrix / np.linalg.norm(
            transformed_similarity_matrix
        )

        return transformed_similarity_matrix

    def generate_similarity_matrix(self, norm_type: Optional[str] = None) -> np.ndarray:
        """
        Generate a similarity matrix for all symbols in the embedding map.

        Returns:
            A 2D numpy array representing the similarity matrix
        """
        embeddings = self._get_ordered_embeddings()

        return SymbolSimilarity._calculate_similarity_matrix(
            embeddings, self._process_norm_type(norm_type)
        )

    def get_query_similarity_dict(
        self, query_text: str, norm_type: Optional[str] = None
    ) -> Dict[Symbol, float]:
        """
        Get the similarity scores of all symbols for the query_text.
        Args:
            query_text (str): The query text
        Returns:
            A dictionary mapping each symbol's uri to its similarity score with the query
        """
        query_embedding = self.embedding_provider.get_embedding(query_text)

        # Compute the similarity of the query to all symbols
        similarity_scores = self._calculate_query_similarity_vec(
            query_embedding, self._process_norm_type(norm_type)
        )

        similarity_dict = {
            self.index_to_symbol[i]: similarity_scores[i] for i in range(len(self.index_to_symbol))
        }
        return similarity_dict

    def get_nearest_symbols_for_query(
        self, query_text: str, k: int = 10, norm_type: Optional[str] = None
    ) -> Dict[Symbol, float]:
        """
        Get the k most similar symbols to the query_text.
        Args:
            query_text (str): The query text
            k (int): The number of similar symbols to return
        Returns:
            A dictionary mapping the k most similar symbols to their similarity score
        """
        query_embedding = self.embedding_provider.get_embedding(query_text)
        # Compute the similarity of the query to all symbols
        similarity_scores = self._calculate_query_similarity_vec(
            query_embedding, self._process_norm_type(norm_type)
        )

        # Get the indices of the symbols with the highest similarity scores
        nearest_indices = np.argsort(similarity_scores)[-k:]

        # Return the corresponding symbols
        return {
            self.index_to_symbol[index]: similarity_scores[index]
            for index in reversed(nearest_indices)
        }

    def _get_ordered_embeddings(self) -> np.ndarray:
        """
        Get the embeddings in the correct order.

        Returns:
            A numpy array containing the ordered embeddings.
        """
        return np.array(
            [self.embedding_dict[symbol].vector for symbol in self.index_to_symbol.values()]
        )

    def _generate_unit_normed_query_vector(
        self, query_text: str, norm_type: NormType
    ) -> np.ndarray:
        """
        Generate a unit-normed vector where the ith component is
        the similarity between symbol i and the query.

        Args:
            query_text (str): The query text

        Returns:
            A unit-normed vector as a numpy array.
        """
        query_embedding = self.embedding_provider.get_embedding(query_text)
        similarity_scores = self._calculate_query_similarity_vec(query_embedding, norm_type)

        # Normalizing the vector
        norm = np.linalg.norm(similarity_scores)
        unit_normed_vector = (
            np.array(similarity_scores) / norm if norm != 0 else np.array(similarity_scores)
        )

        return unit_normed_vector

    def _calculate_query_similarity_vec(
        self, query_embedding: np.ndarray, norm_type: NormType
    ) -> np.ndarray:
        """
        Calculate the similarity scores of the query embedding with all symbol embeddings.
        Args:
            query_embedding (np.ndarray): The query embedding
            norm_type (str): The type of normalization ('l2' for L2 norm, 'softmax' for softmax)
        Returns:
            A numpy array containing the similarity scores
        """
        embeddings = self._get_ordered_embeddings()

        # Normalize the embeddings and the query embedding
        embeddings_norm = self._normalize_embeddings(embeddings, norm_type)
        query_embedding_norm = self._normalize_embeddings(
            query_embedding[np.newaxis, :], norm_type
        )[0]

        # Compute the dot product between normalized embeddings and query
        similarity_scores = np.dot(embeddings_norm, query_embedding_norm)

        return similarity_scores

    def _process_norm_type(self, norm_type) -> NormType:
        return NormType(norm_type) if norm_type else self.default_norm_type

    @staticmethod
    def _calculate_similarity_matrix(embeddings: np.ndarray, norm_type: NormType) -> np.ndarray:
        """
        Calculate the similarity matrix for a list of embeddings.
        Args:
            embeddings (np.ndarray): A list of embeddings
            norm_type (str): The type of normalization ('l2' for L2 norm, 'softmax' for softmax)
        Returns:
            A 2D numpy array representing the similarity matrix
        """
        # Normalize the embeddings
        embeddings_norm = SymbolSimilarity._normalize_embeddings(embeddings, norm_type)

        # Compute the dot product between every pair of normalized embeddings
        similarity_matrix = np.dot(embeddings_norm, embeddings_norm.T)

        return similarity_matrix

    @staticmethod
    def _normalize_embeddings(embeddings: np.ndarray, norm_type: NormType) -> np.ndarray:
        """
        Normalize the embeddings.
        Args:
            embeddings (np.ndarray): The embeddings
            norm_type (NormType): The type of normalization (L1, L2, or softmax)
        Returns:
            The normalized embeddings
        """
        if norm_type == NormType.L1:
            norm = np.sum(np.abs(embeddings), axis=1, keepdims=True)
            return embeddings / norm
        elif norm_type == NormType.L2:
            return embeddings / np.linalg.norm(embeddings, axis=1, keepdims=True)
        elif norm_type == NormType.SOFTMAX:
            e_x = np.exp(embeddings - np.max(embeddings, axis=1, keepdims=True))
            return e_x / np.sum(e_x, axis=1, keepdims=True)
        else:
            raise ValueError(f"Invalid normalization type {norm_type}")

    @staticmethod
    def _normalize_matrix(M: np.ndarray) -> np.ndarray:
        """
        Normalize the values in a matrix to fall within [0, 1].

        Args:
            M (np.ndarray): The matrix to be normalized.

        Returns:
            The normalized matrix as a numpy array.
        """
        M_min = np.min(M)
        M_max = np.max(M)

        # Prevent division by zero in case of a matrix with all elements being the same
        if M_max == M_min:
            return M - M_min

        return (M - M_min) / (M_max - M_min)
