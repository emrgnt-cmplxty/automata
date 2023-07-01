import logging
from typing import Dict, List, Optional, Set

import numpy as np

from automata.core.base.embedding import (
    EmbeddingNormType,
    EmbeddingProvider,
    EmbeddingSimilarityCalculator,
)
from automata.core.base.symbol import Symbol
from automata.core.base.symbol_embedding import SymbolEmbeddingHandler

logger = logging.getLogger(__name__)


class SymbolSimilarityCalculator(EmbeddingSimilarityCalculator):
    """A class responsible for calculating the similarity between symbols."""

    def __init__(
        self,
        symbol_embedding_handler: SymbolEmbeddingHandler,
        embedding_provider: EmbeddingProvider,
        norm_type: EmbeddingNormType = EmbeddingNormType.L2,
    ) -> None:
        """Initializes SymbolSimilarity by building the associated symbol mappings."""
        self.embedding_handler: SymbolEmbeddingHandler = symbol_embedding_handler
        self.embedding_provider: EmbeddingProvider = embedding_provider
        self.norm_type = norm_type
        supported_symbols = self.embedding_handler.get_all_supported_symbols()
        self.index_to_symbol = dict(enumerate(supported_symbols))
        self.symbol_to_index = {symbol: i for i, symbol in enumerate(supported_symbols)}
        self.available_symbols: Optional[Set[Symbol]] = None
        self.ordered_embeddings = self._calculate_ordered_embeddings()

    def set_available_symbols(self, available_symbols: Set[Symbol]) -> None:
        """Set the available symbols to use for similarity calculation."""
        self.available_symbols = available_symbols

    def get_available_symbols(self) -> List[Symbol]:
        """Gets a list of available symbols to use for similarity calculation."""
        return [
            symbol
            for symbol in self.symbol_to_index
            if not self.available_symbols or symbol in self.available_symbols
        ]

    def calculate_query_similarity_dict(
        self, query_text: str, return_sorted: bool = True
    ) -> Dict[Symbol, float]:
        """
        Similarity is calculated between the dot product
        of the query embedding and the symbol embeddings.
        Return result is sorted in descending order by default.
        """
        query_embedding_array = self.embedding_provider.build_embedding_array(query_text)
        # Compute the similarity of the query to all symbols
        similarity_scores = self._calculate_embedding_similarity(query_embedding_array)
        similarity_dict = {
            self.index_to_symbol[i]: similarity_scores[i]
            for i in range(len(self.index_to_symbol))
            if (not self.available_symbols) or self.index_to_symbol[i] in self.available_symbols
        }

        if return_sorted:
            # Sort the dictionary by values in descending order
            similarity_dict = dict(
                sorted(similarity_dict.items(), key=lambda item: item[1], reverse=True)
            )

        return similarity_dict

    def _calculate_embedding_similarity(self, embedding_array: np.ndarray) -> np.ndarray:
        """Calculate the similarity score between the embedding with all symbol embeddings"""
        # Normalize the embeddings and the query embedding
        embeddings_norm = self._normalize_embeddings(self.ordered_embeddings, self.norm_type)
        normed_embedding = self._normalize_embeddings(
            embedding_array[np.newaxis, :], self.norm_type
        )[0]

        return np.dot(embeddings_norm, normed_embedding)

    def _calculate_ordered_embeddings(self) -> np.ndarray:
        """Returns the embeddings in the correct order."""
        return np.array(
            [
                self.embedding_handler.get_embedding(symbol).vector
                for symbol in self.index_to_symbol.values()
            ]
        )
