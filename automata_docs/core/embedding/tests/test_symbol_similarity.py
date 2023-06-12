import numpy as np

from automata_docs.core.embedding.symbol_embedding_map import (
    EmbeddingsProvider,
    SymbolEmbeddingMap,
)
from automata_docs.core.embedding.symbol_similarity import NormType, SymbolSimilarity
from automata_docs.core.symbol.symbol_types import SymbolEmbedding

from .conftest import get_sem, patch_get_embedding


def test_generate_similarity_matrix(
    monkeypatch,
    mock_embedding,
    mock_simple_method_symbols,
):
    # Define the behavior of the mock get_embedding function
    patch_get_embedding(monkeypatch, mock_embedding)

    # Create an instance of the class
    sem = get_sem(monkeypatch, mock_simple_method_symbols, build_new_embedding_map=True)
    sim = SymbolSimilarity(sem)

    similarity_matrix = sim.generate_similarity_matrix()
    assert (
        np.sum(similarity_matrix)
        - len(similarity_matrix) * len(similarity_matrix[0])
        - len(similarity_matrix)
        < 0.0001
    )


def test_calculate_similarity():
    np.random.seed(0)
    matrix = np.random.rand(10, 10)
    distances = SymbolSimilarity._calculate_similarity_matrix(matrix, NormType.L2)
    assert distances[0][0] == 1.0
    assert distances[0][1] == distances[1][0]
    assert distances[0][1] == 0.8642101667343082


def test_get_nearest_symbols_for_query(monkeypatch, mock_simple_method_symbols):
    # Mocking symbols and their embeddings
    symbol1 = mock_simple_method_symbols[0]
    symbol2 = mock_simple_method_symbols[1]
    symbol3 = mock_simple_method_symbols[2]

    embedding1 = SymbolEmbedding(
        symbol=symbol1, vector=np.array([1, 0, 0, 0]), source_code="symbol1"
    )
    embedding2 = SymbolEmbedding(
        symbol=symbol2, vector=np.array([0, 1, 0, 0]), source_code="symbol2"
    )
    embedding3 = SymbolEmbedding(
        symbol=symbol3, vector=np.array([0, 0, 1, 0]), source_code="symbol3"
    )

    embedding_dict = {symbol1: embedding1, symbol2: embedding2, symbol3: embedding3}

    # Mocking get_embedding function of EmbeddingsProvider class
    def mock_get_embedding(_, symbol_source):
        if symbol_source == "symbol1":
            return embedding1.vector
        elif symbol_source == "symbol2":
            return embedding2.vector
        else:
            return embedding3.vector

    monkeypatch.setattr(EmbeddingsProvider, "get_embedding", mock_get_embedding)

    symbol_embedding_map = SymbolEmbeddingMap(
        load_embedding_map=True, embedding_dict=embedding_dict
    )

    symbol_similarity = SymbolSimilarity(symbol_embedding_map)

    # Test with query_text that is most similar to symbol1
    result = symbol_similarity.get_nearest_symbols_for_query("symbol1", k=1)
    assert list(result.keys()) == [symbol1]

    # Test with query_text that is most similar to symbol2
    result = symbol_similarity.get_nearest_symbols_for_query("symbol2", k=1)
    assert list(result.keys()) == [symbol2]

    # Test with query_text that is most similar to symbol3
    result = symbol_similarity.get_nearest_symbols_for_query("symbol3", k=1)
    assert list(result.keys()) == [symbol3]


def test_transform_similarity_matrix(monkeypatch, mock_simple_method_symbols):
    # Similar to previous tests, mock symbols and their embeddings
    symbol1 = mock_simple_method_symbols[0]
    symbol2 = mock_simple_method_symbols[1]
    symbol3 = mock_simple_method_symbols[2]

    embedding1 = SymbolEmbedding(
        symbol=symbol1, vector=np.array([1, 0, 0, 0]), source_code="symbol1"
    )
    embedding2 = SymbolEmbedding(
        symbol=symbol2, vector=np.array([0, 1, 0, 0]), source_code="symbol2"
    )
    embedding3 = SymbolEmbedding(
        symbol=symbol3, vector=np.array([0, 0, 1, 0]), source_code="symbol3"
    )

    embedding_dict = {symbol1: embedding1, symbol2: embedding2, symbol3: embedding3}

    def mock_get_embedding(_, symbol_source):
        if symbol_source == "symbol1":
            return embedding1.vector
        elif symbol_source == "symbol2":
            return embedding2.vector
        else:
            return embedding3.vector

    monkeypatch.setattr(EmbeddingsProvider, "get_embedding", mock_get_embedding)

    symbol_embedding_map = SymbolEmbeddingMap(
        load_embedding_map=True, embedding_dict=embedding_dict
    )

    symbol_similarity = SymbolSimilarity(symbol_embedding_map)

    # Generate similarity matrix first
    similarity_matrix = symbol_similarity.generate_similarity_matrix()

    # Now test the transform_similarity_matrix method
    transformed_similarity_matrix = symbol_similarity.transform_similarity_matrix(
        similarity_matrix, "symbol1"
    )

    # The transformed matrix should have different values than the original one
    assert np.any(transformed_similarity_matrix != similarity_matrix)


def test_generate_unit_normed_query_vector(monkeypatch, mock_simple_method_symbols):
    # Similar to previous tests, mock symbols and their embeddings, and use the same mock_get_embedding function
    symbol1 = mock_simple_method_symbols[0]
    symbol2 = mock_simple_method_symbols[1]
    symbol3 = mock_simple_method_symbols[2]

    embedding1 = SymbolEmbedding(
        symbol=symbol1, vector=np.array([1, 0, 0, 0]), source_code="symbol1"
    )
    embedding2 = SymbolEmbedding(
        symbol=symbol2, vector=np.array([0, 1, 0, 0]), source_code="symbol2"
    )
    embedding3 = SymbolEmbedding(
        symbol=symbol3, vector=np.array([0, 0, 1, 0]), source_code="symbol3"
    )

    embedding_dict = {symbol1: embedding1, symbol2: embedding2, symbol3: embedding3}

    def mock_get_embedding(_, symbol_source):
        if symbol_source == "symbol1":
            return embedding1.vector
        elif symbol_source == "symbol2":
            return embedding2.vector
        else:
            return embedding3.vector

    monkeypatch.setattr(EmbeddingsProvider, "get_embedding", mock_get_embedding)

    symbol_embedding_map = SymbolEmbeddingMap(
        load_embedding_map=True, embedding_dict=embedding_dict
    )

    symbol_similarity = SymbolSimilarity(symbol_embedding_map)

    # Test the _generate_unit_normed_query_vector method
    unit_normed_vector = symbol_similarity._generate_unit_normed_query_vector(
        "symbol1", NormType.L2
    )

    # The vector should be unit normed, so its norm should be close to 1
    assert np.isclose(np.linalg.norm(unit_normed_vector), 1.0)
