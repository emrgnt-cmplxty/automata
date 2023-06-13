import logging
from typing import Dict, Optional, Set

import numpy as np

from automata_docs.core.embedding.symbol_embedding import SymbolCodeEmbeddingHandler
from automata_docs.core.symbol.symbol_types import Symbol

from .embedding_types import EmbeddingSimilarity, EmbeddingsProvider, NormType

logger = logging.getLogger(__name__)


class SymbolSimilarity(EmbeddingSimilarity):
    def __init__(
        self,
        symbol_embedding_manager: SymbolCodeEmbeddingHandler,
        norm_type: NormType = NormType.L2,
    ):
        """
        Initialize SymbolSimilarity

        Args:
            symbol_embedding_manager: A CodeEmbeddingManager
            norm_type (NormType): The norm type to use for calculating similarity

        Returns:
            An instance of SymbolSimilarity
        """
        self.embedding_handler: SymbolCodeEmbeddingHandler = symbol_embedding_manager
        self.embedding_provider: EmbeddingsProvider = symbol_embedding_manager.embedding_provider
        self.norm_type = norm_type
        supported_symbols = self.embedding_handler.get_all_supported_symbols()
        self.index_to_symbol = {i: symbol for i, symbol in enumerate(supported_symbols)}
        self.symbol_to_index = {symbol: i for i, symbol in enumerate(supported_symbols)}
        self.available_symbols: Optional[Set[Symbol]] = None

    def set_available_symbols(self, available_symbols: Set[Symbol]):
        """
        Set the available symbols to use for similarity calculation

        Args:
            available_symbols (Set[Symbol]): The available symbols to
                use for similarity calculation
        """
        self.available_symbols = available_symbols

    def get_query_similarity_dict(self, query_text: str) -> Dict[Symbol, float]:
        """
        Get the similarity scores of all symbols for the query_text

        Args:
            query_text (str): The query text

        Returns:
            A dictionary mapping each symbol's uri to its similarity score with the query
        """
        query_embedding = self.embedding_provider.build_embedding(query_text)

        # Compute the similarity of the query to all symbols
        similarity_scores = self._calculate_query_similarity_vec(query_embedding)

        similarity_dict = {
            self.index_to_symbol[i]: similarity_scores[i]
            for i in range(len(self.index_to_symbol))
            if (not self.available_symbols) or self.index_to_symbol[i] in self.available_symbols
        }
        return similarity_dict

    def get_nearest_entries_for_query(self, query_text: str, k: int = 10) -> Dict[Symbol, float]:
        """
        Get the k most similar symbols to the query_text
        Args:
            query_text (str): The query text
            k (int): The number of similar symbols to return
        Returns:
            A dictionary mapping the k most similar symbols to their similarity score
        """
        query_embedding = self.embedding_provider.build_embedding(query_text)
        # Compute the similarity of the query to all symbols
        similarity_scores = self._calculate_query_similarity_vec(query_embedding)

        if self.available_symbols is not None:
            # Filter the indices by available symbols
            available_indices = [
                i
                for i in range(len(self.index_to_symbol))
                if self.index_to_symbol[i] in self.available_symbols
            ]
            # Get the similarity scores for the available symbols
            available_similarity_scores = similarity_scores[available_indices]
            # Get the indices of the k symbols with the highest similarity scores among the available symbols
            top_k_indices_in_available = np.argsort(available_similarity_scores)[-k:]
            # Convert these indices back to the indices in the original list of symbols
            top_k_indices = [available_indices[i] for i in top_k_indices_in_available]
        else:
            # Get the indices of the k symbols with the highest similarity scores
            top_k_indices = np.argsort(similarity_scores)[-k:]

        # Return the corresponding symbols
        return {
            self.index_to_symbol[index]: similarity_scores[index]
            for index in reversed(top_k_indices)
        }

    def _get_ordered_embeddings(self) -> np.ndarray:
        """
        Get the embeddings in the correct order

        Returns:
            A numpy array containing the ordered embeddings
        """
        return np.array(
            [
                self.embedding_handler.get_embedding(symbol).vector
                for symbol in self.index_to_symbol.values()
            ]
        )

    def _calculate_query_similarity_vec(self, query_embedding: np.ndarray) -> np.ndarray:
        """
        Calculate the similarity scores of the query embedding with all symbol embeddings
        Args:
            query_embedding (np.ndarray): The query embedding
            norm_type (str): The type of normalization ('l2' for L2 norm, 'softmax' for softmax)
        Returns:
            A numpy array containing the similarity scores
        """
        embeddings = self._get_ordered_embeddings()

        # Normalize the embeddings and the query embedding
        embeddings_norm = self._normalize_embeddings(embeddings, self.norm_type)
        query_embedding_norm = self._normalize_embeddings(
            query_embedding[np.newaxis, :], self.norm_type
        )[0]

        # Compute the dot product between normalized embeddings and query
        similarity_scores = np.dot(embeddings_norm, query_embedding_norm)

        return similarity_scores

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
