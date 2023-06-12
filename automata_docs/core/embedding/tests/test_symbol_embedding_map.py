from unittest.mock import Mock

from automata_docs.core.embedding.symbol_embedding_map import SymbolEmbeddingMap

from .conftest import get_sem, patch_get_embedding


def test_build_embedding_map(
    monkeypatch,
    mock_embedding,
    mock_simple_method_symbols,
    mock_simple_class_symbols,
):
    # Define the behavior of the mock build_embedding function
    patch_get_embedding(monkeypatch, mock_embedding)
    # Create the Mock objects for the method parameters
    mock_symbols = mock_simple_method_symbols + mock_simple_class_symbols
    # Create an instance of the class
    sem = get_sem(monkeypatch, mock_symbols)
    # Call the method
    embedding_dict = sem._build_embedding_map(mock_symbols)

    # Verify the results
    assert len(embedding_dict) == 200
    for _, symbol_embedding in embedding_dict.items():
        assert symbol_embedding.vector.all() == mock_embedding.all()


def test_save_load_embedding_map(
    monkeypatch,
    mock_embedding,
    temp_output_filename,
    mock_simple_method_symbols,
):
    # Define the behavior of the mock build_embedding function
    patch_get_embedding(monkeypatch, mock_embedding)
    # Create an instance of the class
    sem = get_sem(monkeypatch, mock_simple_method_symbols[0:10], build_new_embedding_map=True)
    # Call the method
    sem.save(temp_output_filename)
    sem_load = SymbolEmbeddingMap.load(temp_output_filename)
    for key, val in sem_load.items():
        assert key.uri in [symbol.uri for symbol in sem.embedding_dict.keys()]


def test_get_embedding_sets_correct_result(
    monkeypatch,
    mock_embedding,
    mock_simple_method_symbols,
    mock_simple_class_symbols,
):
    # Define the behavior of the mock build_embedding function
    patch_get_embedding(monkeypatch, mock_embedding)
    # Create the Mock objects for the method parameters
    mock_symbols = mock_simple_method_symbols + mock_simple_class_symbols
    # Create an instance of the class
    sem = get_sem(monkeypatch, mock_simple_method_symbols, build_new_embedding_map=False)

    # Call the method
    embedding_dict = sem._build_embedding_map(mock_symbols)

    for key, val in embedding_dict.items():
        assert val.source_code == "symbol_source"


def test_update_embeddings(
    monkeypatch,
    mock_embedding,
    mock_simple_method_symbols,
    mock_simple_class_symbols,
):
    # Define the behavior of the mock build_embedding function
    patch_get_embedding(monkeypatch, mock_embedding)
    # Create the Mock objects for the method parameters
    mock_symbols = mock_simple_method_symbols + mock_simple_class_symbols
    # Create an instance of the class
    sem = get_sem(monkeypatch, mock_symbols, build_new_embedding_map=True)

    # Update embeddings for half of the symbols
    symbols_to_update = mock_symbols[: len(mock_symbols) // 2]
    sem.update_embeddings(symbols_to_update)

    # Verify the results
    for symbol in symbols_to_update:
        assert symbol in sem.embedding_dict
        assert sem.embedding_dict[symbol].vector.all() == mock_embedding.all()


def test_empty_input(monkeypatch):
    # Test empty input scenario
    sem = get_sem(monkeypatch, [], build_new_embedding_map=True)
    assert len(sem.embedding_dict) == 0  # Expect empty embedding map


def test_get_embedding_exception(monkeypatch, mock_simple_method_symbols):
    # Test exception in build_embedding function
    mock_get_embedding = Mock(side_effect=Exception("Test exception"))
    monkeypatch.setattr("openai.embeddings_utils.get_embedding", mock_get_embedding)
    sem = get_sem(monkeypatch, mock_simple_method_symbols, build_new_embedding_map=True)
    assert len(sem.embedding_dict) == 0  # Expect empty embedding map because of exception
