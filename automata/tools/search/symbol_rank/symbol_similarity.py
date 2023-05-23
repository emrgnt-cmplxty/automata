import logging
from typing import Dict

import numpy as np

from automata.tools.search.local_types import Symbol, SymbolEmbedding
from automata.tools.search.symbol_rank.symbol_embedding_map import (
    EmbeddingsProvider,
    SymbolEmbeddingMap,
)

logger = logging.getLogger(__name__)


class SymbolSimilarity:
    def __init__(
        self,
        symbol_embedding_map: SymbolEmbeddingMap,
    ):
        """
        Initialize SymbolSimilarity
        Args:
            symbol_embedding_map (SymbolSimilarity): SymbolSimilarity object
        Result:
            An instance of SymbolSimilarity
        """
        self.embedding_map: Dict[Symbol, SymbolEmbedding] = symbol_embedding_map.embedding_map
        self.embedding_provider: EmbeddingsProvider = symbol_embedding_map.embedding_provider
        symbols = sorted(list(self.embedding_map.keys()), key=lambda x: x.uri)
        self.index_to_symbol = {i: symbol for i, symbol in enumerate(symbols)}
        self.symbol_to_index = {symbol: i for i, symbol in enumerate(symbols)}

    def generate_unit_normed_query_vector(self, query_text: str) -> np.ndarray:
        """
        Generate a unit-normed vector where the ith component is
        the similarity between symbol i and the query.

        Args:
            query_text (str): The query text

        Returns:
            A unit-normed vector as a numpy array.
        """
        similarity_scores = np.zeros(len(self.embedding_map))
        query_embedding = self.embedding_provider.get_embedding(query_text)

        for idx, symbol_embedding in enumerate(self.embedding_map.values()):
            similarity = SymbolSimilarity._calculate_similarity(
                query_embedding, symbol_embedding.vector
            )
            similarity_scores[idx] = similarity

        # Normalizing the vector
        norm = np.linalg.norm(similarity_scores)
        unit_normed_vector = (
            np.array(similarity_scores) / norm if norm != 0 else np.array(similarity_scores)
        )

        return unit_normed_vector

    def normalize_matrix(self, M: np.ndarray) -> np.ndarray:
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

    def transform_similarity_matrix(self, S: np.ndarray, query_text: str) -> np.ndarray:
        """
        Perform a unitary transformation on the similarity matrix.

        Args:
            S (np.ndarray): The similarity matrix
            query_text (str): The query text

        Returns:
            The transformed similarity matrix as a numpy array.
        """
        # Step 1: Construct a unit-normed vector (e)
        e = self.generate_unit_normed_query_vector(query_text)

        # Step 2: Reshape e to have shape (n, 1) so it can be used in broadcasting operation
        e = np.reshape(e, (-1, 1))

        # Step 3: Perform a transformation on the similarity matrix, e.g. compute e * S
        transformed_similarity_matrix = e * S

        # Step 4: Re-normalize the transformed similarity matrix
        transformed_similarity_matrix = self.normalize_matrix(transformed_similarity_matrix)

        return transformed_similarity_matrix

    def generate_similarity_matrix(self) -> np.ndarray:
        """
        Generate a similarity matrix for all symbols in the embedding map.

        Returns:
            A 2D numpy array representing the similarity matrix
        """
        embeddings = np.array(
            [self.embedding_map[symbol].vector for symbol in self.index_to_symbol.values()]
        )

        return SymbolSimilarity.calculate_similarity_matrix(embeddings)

    def get_nearest_symbols_for_query(self, query_text: str, k: int = 10) -> Dict[Symbol, float]:
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
        similarity_scores = np.zeros(len(self.embedding_map))

        for idx, symbol_embedding in enumerate(self.embedding_map.values()):
            similarity = SymbolSimilarity._calculate_similarity(
                query_embedding, symbol_embedding.vector
            )
            similarity_scores[idx] = similarity

        # Get the indices of the symbols with the highest similarity scores
        nearest_indices = np.argsort(similarity_scores)[-k:]

        # Return the corresponding symbols
        return {
            self.index_to_symbol[index]: similarity_scores[index]
            for index in reversed(nearest_indices)
        }

    @staticmethod
    def calculate_similarity_matrix(embeddings: np.ndarray) -> np.ndarray:
        """
        Calculate the similarity matrix for a list of embeddings
        Args:
            embeddings (np.ndarray): A list of embeddings
        Returns:
            A 2D numpy array representing the similarity matrix
        """
        calculate_similarity_vectorized = np.vectorize(
            SymbolSimilarity._calculate_similarity, signature="(n),(n)->()"
        )
        similarity_matrix = calculate_similarity_vectorized(embeddings[:, np.newaxis], embeddings)

        return similarity_matrix

    @staticmethod
    def _calculate_similarity(embedding_a: np.ndarray, embedding_b: np.ndarray) -> float:
        """
        Calculate the similarity between two symbols
        Args:
            embedding_a (np.ndarray): The first embedding
            embedding_b (np.ndarray): The second embedding
        Returns:
            The similarity between the two symbolss
        """

        dot_product = np.dot(embedding_a, embedding_b)
        magnitude_a = np.sqrt(np.dot(embedding_a, embedding_a))
        magnitude_b = np.sqrt(np.dot(embedding_b, embedding_b))
        similarity = dot_product / (magnitude_a * magnitude_b)

        return similarity
