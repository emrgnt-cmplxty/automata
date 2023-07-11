from unittest.mock import MagicMock

import numpy as np

from automata.embedding import (
    EmbeddingBuilder,
    EmbeddingSimilarityCalculator,
    EmbeddingVectorProvider,
)
from automata.memory_store.symbol_code_embedding import SymbolCodeEmbeddingHandler
from automata.symbol_embedding.base import SymbolCodeEmbedding
from automata.symbol_embedding.vector_databases import JSONSymbolEmbeddingVectorDatabase


def test_get_nearest_symbols_for_query(
    monkeypatch, mock_embedding, mock_simple_method_symbols, temp_output_filename
):
    # Mocking symbols and their embeddings
    symbol1 = mock_simple_method_symbols[0]
    symbol2 = mock_simple_method_symbols[1]
    symbol3 = mock_simple_method_symbols[2]

    embedding1 = SymbolCodeEmbedding(
        key=symbol1, vector=np.array([1, 0, 0, 0]), document="symbol1"
    )
    embedding2 = SymbolCodeEmbedding(
        key=symbol2, vector=np.array([0, 1, 0, 0]), document="symbol2"
    )
    embedding3 = SymbolCodeEmbedding(
        key=symbol3, vector=np.array([0, 0, 1, 0]), document="symbol3"
    )

    # Mock JSONSymbolEmbeddingVectorDatabase methods
    embedding_db = JSONSymbolEmbeddingVectorDatabase(temp_output_filename)
    embedding_db.add(embedding1)
    embedding_db.add(embedding2)
    embedding_db.add(embedding3)

    # Create an instance of the class
    mock_builder = MagicMock(EmbeddingBuilder)
    cem = SymbolCodeEmbeddingHandler(embedding_db=embedding_db, embedding_builder=mock_builder)
    mock_provider = MagicMock(EmbeddingVectorProvider)
    embeddings = {symbol1: embedding1, symbol2: embedding2, symbol3: embedding3}
    cem.get_embeddings = lambda x: embeddings[x]  # MagicMock(return_value=embeddings[x])
    symbol_similarity = EmbeddingSimilarityCalculator(mock_provider)

    # Test with query_text that is most similar to symbol1
    symbol_similarity.embedding_provider.build_embedding_vector.return_value = np.array(
        [1, 0, 0, 0]
    )
    ordered_embeddings = embedding_db.get_ordered_entries()
    result = symbol_similarity.calculate_query_similarity_dict(ordered_embeddings, "symbol1")
    assert list(result.keys())[np.argmax(list(result.values()))] == symbol1

    # # Test with query_text that is most similar to symbol2
    symbol_similarity.embedding_provider.build_embedding_vector.return_value = np.array(
        [0, 1, 0, 0]
    )
    result = symbol_similarity.calculate_query_similarity_dict(ordered_embeddings, "symbol2")
    assert list(result.keys())[np.argmax(list(result.values()))] == symbol2

    # # Test with query_text that is most similar to symbol3
    symbol_similarity.embedding_provider.build_embedding_vector.return_value = np.array(
        [0, 0, 1, 0]
    )
    result = symbol_similarity.calculate_query_similarity_dict(ordered_embeddings, "symbol3")
    assert list(result.keys())[np.argmax(list(result.values()))] == symbol3
