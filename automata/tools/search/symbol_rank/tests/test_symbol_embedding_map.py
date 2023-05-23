from unittest.mock import Mock

from automata.tools.search.symbol_rank.symbol_embedding_map import SymbolEmbeddingMap


def get_sem(mock_symbol_converter, mock_symbols, build_new_embedding_map=False):
    return SymbolEmbeddingMap(
        symbol_converter=mock_symbol_converter,
        # Symbols with kind 'Method' are processed, 'Local' are skipped
        all_defined_symbols=mock_symbols,
        build_new_embedding_map=build_new_embedding_map,
    )


def patch_get_embedding(monkeypatch, mock_embedding):
    # Define the behavior of the mock get_embedding function
    mock_get_embedding = Mock(return_value=mock_embedding)
    monkeypatch.setattr("openai.embeddings_utils.get_embedding", mock_get_embedding)


def test_build_embedding_map(
    monkeypatch,
    mock_embedding,
    mock_simple_method_symbols,
    mock_simple_class_symbols,
    mock_symbol_converter,
):
    # Define the behavior of the mock get_embedding function
    patch_get_embedding(monkeypatch, mock_embedding)
    # Create the Mock objects for the method parameters
    mock_symbols = mock_simple_method_symbols + mock_simple_class_symbols
    # Create an instance of the class
    sem = get_sem(mock_symbol_converter, mock_symbols)
    # Call the method
    embedding_map = sem._build_embedding_map(mock_symbol_converter, mock_symbols)

    # Verify the results
    assert len(embedding_map) == 200
    for _, symbol_embedding in embedding_map.items():
        assert symbol_embedding.vector == mock_embedding


def test_save_load_embedding_map(
    monkeypatch,
    mock_embedding,
    temp_output_filename,
    mock_simple_method_symbols,
    mock_symbol_converter,
):
    # Define the behavior of the mock get_embedding function
    patch_get_embedding(monkeypatch, mock_embedding)
    # Create an instance of the class
    sem = get_sem(
        mock_symbol_converter, mock_simple_method_symbols[0:10], build_new_embedding_map=True
    )
    # Call the method
    sem.save(temp_output_filename)

    sem_load = SymbolEmbeddingMap.load(temp_output_filename)
    for key, val in sem_load.embedding_map.items():
        assert key.uri in [symbol.uri for symbol in sem.embedding_map.keys()]


def test_get_embedding_sets_correct_result(
    monkeypatch,
    mock_embedding,
    mock_simple_method_symbols,
    mock_simple_class_symbols,
    mock_symbol_converter,
):
    # Define the behavior of the mock get_embedding function
    patch_get_embedding(monkeypatch, mock_embedding)
    # Create the Mock objects for the method parameters
    mock_symbols = mock_simple_method_symbols + mock_simple_class_symbols
    # Create an instance of the class
    sem = get_sem(mock_symbol_converter, mock_simple_method_symbols, build_new_embedding_map=False)

    # Call the method
    embedding_map = sem._build_embedding_map(mock_symbol_converter, mock_symbols)

    for key, val in embedding_map.items():
        val.source_code == "symbol_source"


def test_update_embeddings(
    monkeypatch,
    mock_embedding,
    mock_simple_method_symbols,
    mock_simple_class_symbols,
    mock_symbol_converter,
):
    # Define the behavior of the mock get_embedding function
    patch_get_embedding(monkeypatch, mock_embedding)
    # Create the Mock objects for the method parameters
    mock_symbols = mock_simple_method_symbols + mock_simple_class_symbols
    # Create an instance of the class
    sem = get_sem(mock_symbol_converter, mock_symbols, build_new_embedding_map=True)

    # Update embeddings for half of the symbols
    symbols_to_update = mock_symbols[: len(mock_symbols) // 2]
    sem.update_embeddings(mock_symbol_converter, symbols_to_update)

    # Verify the results
    for symbol in symbols_to_update:
        assert symbol in sem.embedding_map
        assert sem.embedding_map[symbol].vector == mock_embedding


def test_empty_input(monkeypatch, mock_symbol_converter):
    # Test empty input scenario
    sem = get_sem(mock_symbol_converter, [], build_new_embedding_map=True)
    assert len(sem.embedding_map) == 0  # Expect empty embedding map


def test_get_embedding_exception(monkeypatch, mock_symbol_converter, mock_simple_method_symbols):
    # Test exception in get_embedding function
    mock_get_embedding = Mock(side_effect=Exception("Test exception"))
    monkeypatch.setattr("openai.embeddings_utils.get_embedding", mock_get_embedding)
    sem = get_sem(mock_symbol_converter, mock_simple_method_symbols, build_new_embedding_map=True)
    assert len(sem.embedding_map) == 0  # Expect empty embedding map because of exception

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
    similarity_matrix = sem.generate_similarity_matrix()
    # # Mock the EmbeddingsProvider's calculate_similarity_matrix method to return a constant matrix
    # mock_matrix = [[1.0, 0.5], [0.5, 1.0]]
    # sem.embedding_provider.calculate_similarity_matrix = Mock(return_value=mock_matrix)

    # # Call the method
    # sem.generate_similarity_matrix()

    # print("sem.similarity_matrix = ", sem.similarity_matrix)
    # # Verify the results
    # assert sem.index_to_symbol == {0: mock_simple_method_symbols[0], 1: mock_simple_method_symbols[1]}
    # assert sem.symbol_to_index == {mock_simple_method_symbols[0]: 0, mock_simple_method_symbols[1]: 1}
    # assert sem.similarity_matrix == mock_matrix
