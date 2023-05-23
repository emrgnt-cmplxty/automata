import logging
from typing import Dict, List

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
        symbols = list(self.embedding_map.keys())
        self.index_to_symbol = {i: symbol for i, symbol in enumerate(symbols)}
        self.symbol_to_index = {symbol: i for i, symbol in enumerate(symbols)}

    def generate_similarity_matrix(self) -> List[List[float]]:
        """
        Generate a similarity matrix for all symbols in the embedding map.

        Returns:
            A 2D numpy array representing the similarity matrix
        """
        embeddings = [symbol_embedding.vector for symbol_embedding in self.embedding_map.values()]

        return SymbolSimilarity.calculate_similarity_matrix(embeddings)

    def get_nearest_symbols_for_query(self, query_text: str, k: int = 10) -> List[Symbol]:
        """
        Get the k most similar symbols to the query_text.
        Args:
            query_text (str): The query text
            k (int): The number of similar symbols to return
        Returns:
            A list of the k most similar symbols
        """
        query_embedding = self.embedding_provider.get_embedding(query_text)
        print("query_embedding = ", query_embedding)
        # Compute the similarity of the query to all symbols
        similarity_scores = []
        for symbol, symbol_embedding in self.embedding_map.items():
            similarity = SymbolSimilarity._calculate_similarity(
                query_embedding, symbol_embedding.vector
            )
            similarity_scores.append(similarity)

        print("similarity_scores = ", similarity_scores)
        # Get the indices of the symbols with the highest similarity scores
        nearest_indices = np.argpartition(similarity_scores, -k)[-k:]

        # Return the corresponding symbols
        return [self.index_to_symbol[index] for index in nearest_indices]

    @staticmethod
    def calculate_similarity_matrix(embeddings: List[List[float]]) -> List[List[float]]:
        results: List[List[float]] = [
            [0.0 for _ in range(len(embeddings))] for _ in range(len(embeddings))
        ]

        for i in range(len(embeddings)):
            for j in range(len(embeddings)):
                if j > i:
                    continue
                results[i][j] = SymbolSimilarity._calculate_similarity(
                    embeddings[i], embeddings[j]
                )
                results[j][i] = results[i][j]

        return results

    @staticmethod
    def _calculate_similarity(embedding_a: List[float], embedding_b: List[float]) -> float:
        """
        Calculate the similarity between two symbols
        Args:
            embedding_a (List[float]): The first embedding
            embedding_b (List[float]): The second embedding
        Returns:
            The similarity between the two symbolss
        """

        dot_product = np.dot(embedding_a, embedding_b)
        magnitude_a = np.sqrt(np.dot(embedding_a, embedding_a))
        magnitude_b = np.sqrt(np.dot(embedding_b, embedding_b))
        similarity = dot_product / (magnitude_a * magnitude_b)

        return similarity
