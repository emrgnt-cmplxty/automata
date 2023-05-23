import numpy as np
from conftest import get_sem, patch_get_embedding

from automata.tools.search.symbol_rank.symbol_similarity import SymbolSimilarity


def test_generate_similarity_matrix(
    monkeypatch,
    mock_embedding,
    mock_simple_method_symbols,
    mock_symbol_converter,
):
    # Define the behavior of the mock get_embedding function
    patch_get_embedding(monkeypatch, mock_embedding)

    # Create an instance of the class
    sem = get_sem(mock_symbol_converter, mock_simple_method_symbols, build_new_embedding_map=True)
    sim = SymbolSimilarity(sem.embedding_map)

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
    print("matrix = ", matrix)
    distances = SymbolSimilarity.calculate_similarity_matrix(matrix)
    assert distances[0][0] == 1.0
    assert distances[0][1] == distances[1][0]
    assert distances[0][1] == 0.8642101667343084
