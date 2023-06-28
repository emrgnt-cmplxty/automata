from unittest.mock import MagicMock

import numpy as np

from automata.core.base.database.vector import JSONVectorDatabase
from automata.core.embedding.code_embedding import (
    EmbeddingProvider,
    SymbolCodeEmbeddingHandler,
)
from automata.core.embedding.symbol_similarity import SymbolSimilarityCalculator
from automata.core.symbol.symbol_types import SymbolCodeEmbedding


def test_get_nearest_symbols_for_query(
    monkeypatch, mock_embedding, mock_simple_method_symbols, temp_output_filename
):
    # Mocking symbols and their embeddings
    symbol1 = mock_simple_method_symbols[0]
    symbol2 = mock_simple_method_symbols[1]
    symbol3 = mock_simple_method_symbols[2]

    embedding1 = SymbolCodeEmbedding(
        symbol=symbol1, vector=np.array([1, 0, 0, 0]), source_code="symbol1"
    )
    embedding2 = SymbolCodeEmbedding(
        symbol=symbol2, vector=np.array([0, 1, 0, 0]), source_code="symbol2"
    )
    embedding3 = SymbolCodeEmbedding(
        symbol=symbol3, vector=np.array([0, 0, 1, 0]), source_code="symbol3"
    )

    # Mock JSONVectorDatabase methods
    embedding_db = JSONVectorDatabase(temp_output_filename)
    embedding_db.add(embedding1)
    embedding_db.add(embedding2)
    embedding_db.add(embedding3)

    # Create an instance of the class
    mock_provider = MagicMock(EmbeddingProvider)
    cem = SymbolCodeEmbeddingHandler(embedding_db=embedding_db, embedding_provider=mock_provider)

    symbol_similarity = SymbolSimilarityCalculator(cem)

    # Test with query_text that is most similar to symbol1
    cem.embedding_provider.build_embedding_array.return_value = np.array([1, 0, 0, 0])
    result = symbol_similarity.calculate_query_similarity_dict("symbol1")
    assert list(result.keys())[np.argmax(list(result.values()))] == symbol1

    # # Test with query_text that is most similar to symbol2
    cem.embedding_provider.build_embedding_array.return_value = np.array([0, 1, 0, 0])
    result = symbol_similarity.calculate_query_similarity_dict("symbol1")
    assert list(result.keys())[np.argmax(list(result.values()))] == symbol2

    # # Test with query_text that is most similar to symbol3
    cem.embedding_provider.build_embedding_array.return_value = np.array([0, 0, 1, 0])
    result = symbol_similarity.calculate_query_similarity_dict("symbol3")
    assert list(result.keys())[np.argmax(list(result.values()))] == symbol3
