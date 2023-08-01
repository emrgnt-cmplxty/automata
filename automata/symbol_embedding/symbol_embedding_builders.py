"""Contains the `SymbolCodeEmbeddingBuilder` class for building `SymbolCodeEmbedding`s."""
from typing import List

from automata.embedding import EmbeddingBuilder
from automata.symbol import Symbol
from automata.symbol_embedding import SymbolCodeEmbedding


class SymbolCodeEmbeddingBuilder(EmbeddingBuilder):
    """Builds `Symbol` source code embeddings."""

    def build(self, source_code: str, symbol: Symbol) -> SymbolCodeEmbedding:
        """Build the embedding for a symbol's source code."""
        embedding_vector = self.embedding_provider.build_embedding_vector(
            source_code
        )
        return SymbolCodeEmbedding(symbol, source_code, embedding_vector)

    def batch_build(
        self, source_codes: List[str], symbols: List[Symbol]
    ) -> List[SymbolCodeEmbedding]:
        """Build the embeddings for a list of symbols' source code."""
        embedding_vectors = (
            self.embedding_provider.batch_build_embedding_vector(source_codes)
        )
        return [
            SymbolCodeEmbedding(symbol, source_code, embedding_vector)
            for symbol, source_code, embedding_vector in zip(
                symbols, source_codes, embedding_vectors
            )
        ]
