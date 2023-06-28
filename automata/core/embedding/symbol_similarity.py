import logging
from typing import Dict, List, Optional, Set

import numpy as np

from automata.core.llm.embedding import (
    EmbeddingNormType,
    EmbeddingProvider,
    EmbeddingSimilarityCalculator,
    SymbolEmbeddingHandler,
)
from automata.core.symbol.symbol_types import Symbol

logger = logging.getLogger(__name__)


class SymbolSimilarityCalculator(EmbeddingSimilarityCalculator):
    """A class responsible for calculating the similarity between symbols."""

    def __init__(
        self,
        symbol_embedding_manager: SymbolEmbeddingHandler,
        norm_type: EmbeddingNormType = EmbeddingNormType.L2,
    ) -> None:
        """Initializes SymbolSimilarity by building the associated symbol mappings."""
        self.embedding_handler: SymbolEmbeddingHandler = symbol_embedding_manager
        self.embedding_provider: EmbeddingProvider = symbol_embedding_manager.embedding_provider
        self.norm_type = norm_type
        supported_symbols = self.embedding_handler.get_all_supported_symbols()
        self.index_to_symbol = dict(enumerate(supported_symbols))
        self.symbol_to_index = {symbol: i for i, symbol in enumerate(supported_symbols)}
        self.available_symbols: Optional[Set[Symbol]] = None

    @property
    def ordered_embeddings(self) -> np.ndarray:
        """Returns the embeddings in the correct order."""
        return np.array(
            [
                self.embedding_handler.get_embedding(symbol).vector
                for symbol in self.index_to_symbol.values()
            ]
        )

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

    def calculate_query_similarity_dict(self, query_text: str) -> Dict[Symbol, float]:
        """
        Similarity is calculated between the dot product
        of the query embedding and the symbol embeddings.
        """
        query_embedding_array = self.embedding_provider.build_embedding(query_text)

        # Compute the similarity of the query to all symbols
        similarity_scores = self._calculate_embedding_similarity(query_embedding_array)

        return {
            self.index_to_symbol[i]: similarity_scores[i]
            for i in range(len(self.index_to_symbol))
            if (not self.available_symbols) or self.index_to_symbol[i] in self.available_symbols
        }

    def _calculate_embedding_similarity(self, embedding_array: np.ndarray) -> np.ndarray:
        """Calculate the similarity score between the embedding with all symbol embeddings"""
        # Normalize the embeddings and the query embedding
        embeddings_norm = self._normalize_embeddings(self.ordered_embeddings, self.norm_type)
        normed_embedding = self._normalize_embeddings(
            embedding_array[np.newaxis, :], self.norm_type
        )[0]

        return np.dot(embeddings_norm, normed_embedding)
