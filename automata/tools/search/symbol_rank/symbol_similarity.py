import logging
from typing import Dict, List

import numpy as np

from automata.tools.search.local_types import Symbol, SymbolEmbedding

logger = logging.getLogger(__name__)


class SymbolSimilarity:
    def __init__(
        self,
        embedding_map: Dict[Symbol, SymbolEmbedding],
    ):
        """
        Initialize SymbolSimilarity
        Args:
            symbol_embedding_map (SymbolSimilarity): SymbolSimilarity object
        Result:
            An instance of SymbolSimilarity
        """
        self.embedding_map = embedding_map

    def generate_similarity_matrix(self) -> List[List[float]]:
        """
        Generate a similarity matrix for all symbols in the embedding map.

        Returns:
            A 2D numpy array representing the similarity matrix
        """
        symbols = list(self.embedding_map.keys())
        embeddings = [symbol_embedding.vector for symbol_embedding in self.embedding_map.values()]

        self.index_to_symbol = {i: symbol for i, symbol in enumerate(symbols)}
        self.symbol_to_index = {symbol: i for i, symbol in enumerate(symbols)}

        return SymbolSimilarity.calculate_similarity_matrix(embeddings)

    @staticmethod
    def calculate_similarity_matrix(embeddings: List[List[float]]) -> List[List[float]]:
        results: List[List[float]] = [
            [0.0 for _ in range(len(embeddings))] for _ in range(len(embeddings))
        ]
        for i in range(len(embeddings)):
            for j in range(len(embeddings)):
                if j > i:
                    continue
                print("..")
                dot_product = np.dot(embeddings[i], embeddings[j])
                magnitude_a = np.sqrt(np.dot(embeddings[i], embeddings[i]))
                magnitude_b = np.sqrt(np.dot(embeddings[j], embeddings[j]))
                print("dot_product = ", dot_product)
                print(" (magnitude_a * magnitude_b) = ", (magnitude_a * magnitude_b))
                similarity = dot_product / (magnitude_a * magnitude_b)

                results[i][j] = similarity
                results[j][i] = results[i][j]

        return results
