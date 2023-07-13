from unittest.mock import MagicMock

import numpy as np
import pytest

from automata.embedding import (
    EmbeddingBuilder,
    EmbeddingSimilarityCalculator,
    EmbeddingVectorProvider,
)
from automata.memory_store import SymbolCodeEmbeddingHandler
from automata.symbol_embedding import (
    JSONSymbolEmbeddingVectorDatabase,
    SymbolCodeEmbedding,
)


@pytest.fixture
def embedding_db(temp_output_filename, mock_simple_method_symbols):
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

    return embedding_db


@pytest.fixture
def embedding_handler(embedding_db):
    mock_builder = MagicMock(EmbeddingBuilder)
    cem = SymbolCodeEmbeddingHandler(embedding_db=embedding_db, embedding_builder=mock_builder)
    return cem


@pytest.fixture
def symbol_similarity(embedding_handler):
    mock_provider = MagicMock(EmbeddingVectorProvider)
    symbol_similarity = EmbeddingSimilarityCalculator(mock_provider)
    return symbol_similarity


@pytest.mark.parametrize(
    "symbol_key, query_text",
    [
        ("symbol1", np.array([1, 0, 0, 0])),
        ("symbol2", np.array([0, 1, 0, 0])),
        ("symbol3", np.array([0, 0, 1, 0])),
    ],
)
def test_get_nearest_symbols_for_query(
    embedding_handler, symbol_similarity, symbol_key, query_text
):
    embedding_handler.get_embeddings = lambda x: embedding_handler.embedding_db[
        x
    ]  # MagicMock(return_value=embeddings[x])
    symbol_similarity.embedding_provider.build_embedding_vector.return_value = query_text
    ordered_embeddings = embedding_handler.embedding_db.get_ordered_embeddings()

    result = symbol_similarity.calculate_query_similarity_dict(ordered_embeddings, symbol_key)

    assert list(result.keys())[np.argmax(list(result.values()))] == symbol_key
