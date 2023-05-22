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
