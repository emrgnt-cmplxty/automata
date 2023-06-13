from unittest.mock import MagicMock, Mock

from automata_docs.core.database.vector import JSONVectorDatabase
from automata_docs.core.embedding.symbol_embedding import (
    EmbeddingsProvider,
    SymbolCodeEmbeddingHandler,
)
from automata_docs.core.symbol.symbol_types import SymbolCodeEmbedding


def test_update_embeddings(
    monkeypatch,
    mock_embedding,
    mock_simple_method_symbols,
    mock_simple_class_symbols,
):
    monkeypatch.setattr(
        "automata_docs.core.symbol.symbol_utils.convert_to_fst_object",
        lambda args: "symbol_source",
    )

    # Mock EmbeddingsProvider methods
    mock_provider = Mock(EmbeddingsProvider)
    mock_provider.build_embedding.return_value = mock_embedding

    # Mock JSONVectorDatabase methods
    mock_db = MagicMock(JSONVectorDatabase)
    mock_db.get.return_value = SymbolCodeEmbedding(
        mock_simple_method_symbols[0], mock_embedding, "symbol_source"
    )
    mock_db.contains.return_value = False

    # Create the Mock objects for the method parameters
    mock_symbols = mock_simple_method_symbols + mock_simple_class_symbols

    # Create an instance of the class
    cem = SymbolCodeEmbeddingHandler(embedding_provider=mock_provider, embedding_db=mock_db)

    # Update embeddings for half of the symbols
    symbols_to_update = mock_symbols[: len(mock_symbols) // 2]
    for symbol in symbols_to_update:
        cem.update_embedding(symbol)

    # Verify the results
    for symbol in symbols_to_update:
        assert mock_db.add.call_count == len(symbols_to_update)


def test_get_embedding(
    monkeypatch,
    mock_embedding,
    mock_simple_method_symbols,
):
    # Mock EmbeddingsProvider methods
    mock_provider = Mock(EmbeddingsProvider)
    mock_provider.build_embedding.return_value = mock_embedding

    # Mock JSONVectorDatabase methods
    mock_db = MagicMock(JSONVectorDatabase)
    mock_db.get.return_value = SymbolCodeEmbedding(
        mock_simple_method_symbols[0], mock_embedding, "symbol_source"
    )

    # Create an instance of the class
    cem = SymbolCodeEmbeddingHandler(embedding_provider=mock_provider, embedding_db=mock_db)

    # Call the method
    embedding = cem.get_embedding(mock_simple_method_symbols[0])

    # Verify the results
    assert embedding.vector.all() == mock_embedding.all()


def test_add_new_embedding(monkeypatch, mock_simple_method_symbols):
    # Test exception in build_embedding function
    monkeypatch.setattr(
        "automata_docs.core.symbol.symbol_utils.convert_to_fst_object",
        lambda args: "symbol_source",
    )

    # Mock EmbeddingsProvider methods
    mock_provider = Mock(EmbeddingsProvider)
    mock_provider.build_embedding.return_value = [1, 2, 3]

    # Mock JSONVectorDatabase methods
    mock_db = MagicMock(JSONVectorDatabase)
    mock_db.data = []
    mock_db.contains = lambda x: False
    mock_db.add = lambda x: mock_db.data.append(x)

    cem = SymbolCodeEmbeddingHandler(embedding_provider=mock_provider, embedding_db=mock_db)

    # If exception occurs during the get_embedding operation, the database should not contain any new entries
    cem.update_embedding(mock_simple_method_symbols[0])

    assert len(cem.embedding_db.data) == 1  # Expect empty embedding map because of exception


def test_update_embedding(monkeypatch, mock_simple_method_symbols):
    # Test exception in build_embedding function
    monkeypatch.setattr(
        "automata_docs.core.symbol.symbol_utils.convert_to_fst_object",
        lambda args: "symbol_source",
    )

    # Mock EmbeddingsProvider methods
    mock_provider = Mock(EmbeddingsProvider)
    mock_provider.build_embedding.return_value = [1, 2, 3]

    # Mock JSONVectorDatabase methods
    mock_db = MagicMock(JSONVectorDatabase)
    mock_db.data = []
    mock_db.contains = lambda x: False
    mock_db.add = lambda x: mock_db.data.append(x)
    mock_db.get = lambda x: mock_db.data[0]

    cem = SymbolCodeEmbeddingHandler(embedding_provider=mock_provider, embedding_db=mock_db)

    # If exception occurs during the get_embedding operation, the database should not contain any new entries
    cem.update_embedding(mock_simple_method_symbols[0])
    monkeypatch.setattr(
        "automata_docs.core.symbol.symbol_utils.convert_to_fst_object",
        lambda args: "xx",
    )
    cem.embedding_provider.build_embedding.return_value = [1, 2, 3, 4]
    cem.embedding_db.contains = lambda x: True

    cem.update_embedding(mock_simple_method_symbols[0])
    embedding = cem.embedding_db.data[0].vector
    print("cem.embedding_db = ", cem.embedding_db.data)
    assert len(cem.embedding_db.data) == 1  # Expect empty embedding map because of exception
    assert embedding == [1, 2, 3, 4]


def test_get_embedding_exception(monkeypatch, mock_simple_method_symbols):
    # Test exception in build_embedding function
    monkeypatch.setattr(
        "automata_docs.core.symbol.symbol_utils.convert_to_fst_object",
        lambda args: "symbol_source",
    )

    # Mock EmbeddingsProvider methods
    mock_provider = Mock(EmbeddingsProvider)
    mock_provider.build_embedding.side_effect = Exception("Test exception")

    # Mock JSONVectorDatabase methods
    mock_db = MagicMock(JSONVectorDatabase)
    mock_db.data = []
    mock_db.contains = lambda x: False
    mock_db.add = lambda x: mock_db.data.append(x)

    cem = SymbolCodeEmbeddingHandler(embedding_provider=mock_provider, embedding_db=mock_db)

    # If exception occurs during the get_embedding operation, the database should not contain any new entries
    cem.update_embedding(mock_simple_method_symbols[0])

    assert len(cem.embedding_db.data) == 0  # Expect empty embedding map because of exception
