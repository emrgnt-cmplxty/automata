from unittest.mock import MagicMock, Mock

import numpy as np
import pytest

from automata.embedding.base import EmbeddingBuilder
from automata.memory_store.symbol_code_embedding import SymbolCodeEmbeddingHandler
from automata.symbol_embedding.base import SymbolCodeEmbedding
from automata.symbol_embedding.vector_databases import (
    ChromaSymbolEmbeddingVectorDatabase,
)


def test_update_embeddings(
    monkeypatch,
    mock_embedding,
    mock_simple_method_symbols,
    mock_simple_class_symbols,
):
    monkeypatch.setattr(
        "automata.symbol.symbol_utils.convert_to_ast_object",
        lambda args: "symbol_source",
    )

    # Mock EmbeddingVectorProvider methods
    mock_provider = Mock(EmbeddingBuilder)
    # mock_provider.build_embedding_vector.return_value = mock_embedding

    # Mock ChromaSymbolEmbeddingVectorDatabase methods
    mock_db = MagicMock(ChromaSymbolEmbeddingVectorDatabase)
    mock_db.get.return_value = SymbolCodeEmbedding(
        mock_simple_method_symbols[0], mock_embedding, "symbol_source"
    )
    mock_db.contains.return_value = False

    # Create the Mock objects for the method parameters
    mock_symbols = mock_simple_method_symbols + mock_simple_class_symbols

    mock_provider.fetch_embedding_source_code.return_value = "X"
    mock_db.contains.return_value = False
    # Create an instance of the class
    cem = SymbolCodeEmbeddingHandler(embedding_builder=mock_provider, embedding_db=mock_db)

    # Update embeddings for half of the symbols
    symbols_to_update = mock_symbols[: len(mock_symbols) // 2]
    for symbol in symbols_to_update:
        cem.process_embedding(symbol)
    # mock expected result of process_embedding
    assert len(cem.to_build) == len(symbols_to_update)

    with pytest.raises(TypeError):
        cem.flush()  # type error when iterating on mock object


def test_get_embedding(
    monkeypatch,
    mock_embedding,
    mock_simple_method_symbols,
):
    # Mock EmbeddingVectorProvider methods
    mock_provider = Mock(EmbeddingBuilder)
    # mock_provider.build_embedding_vector.return_value = mock_embedding

    # Mock ChromaSymbolEmbeddingVectorDatabase methods
    mock_db = MagicMock(ChromaSymbolEmbeddingVectorDatabase)
    mock_db.batch_get.return_value = [
        SymbolCodeEmbedding(mock_simple_method_symbols[0], "symbol_source", mock_embedding)
    ]

    # Create an instance of the class
    cem = SymbolCodeEmbeddingHandler(embedding_builder=mock_provider, embedding_db=mock_db)

    # Call the method
    embedding = cem.get_embeddings([mock_simple_method_symbols[0]])

    # Verify the results
    assert embedding[0].vector.all() == mock_embedding.all()


def test_add_new_embedding(monkeypatch, mock_simple_method_symbols):
    # Test exception in build_embedding_vector function
    monkeypatch.setattr(
        "automata.symbol.symbol_utils.convert_to_ast_object",
        lambda args: "symbol_source",
    )

    # Mock EmbeddingVectorProvider methods
    mock_provider = Mock(EmbeddingBuilder)
    # mock_provider.build_embedding_vector.return_value = [1, 2, 3]

    # Mock ChromaSymbolEmbeddingVectorDatabase methods
    mock_db = MagicMock(ChromaSymbolEmbeddingVectorDatabase)
    mock_db.data = []
    mock_db.contains = lambda x: False
    mock_db.add = lambda x: mock_db.data.append(x)

    cem = SymbolCodeEmbeddingHandler(embedding_builder=mock_provider, embedding_db=mock_db)

    # If exception occurs during the get_embedding operation, the database should not contain any new entries
    cem.process_embedding(mock_simple_method_symbols[0])

    # Flushing should trigger an exception, because the mock object is not iterable
    with pytest.raises(TypeError):
        cem.flush()


def test_update_embedding(monkeypatch, mock_simple_method_symbols):
    # Test exception in build_embedding_vector function
    monkeypatch.setattr(
        "automata.symbol.symbol_utils.convert_to_ast_object",
        lambda args: "symbol_source",
    )

    # Mock EmbeddingVectorProvider methods
    mock_provider = Mock(EmbeddingBuilder)

    # Mock ChromaSymbolEmbeddingVectorDatabase methods
    mock_db = MagicMock(ChromaSymbolEmbeddingVectorDatabase)
    mock_db.data = []
    mock_db.contains = lambda x: False
    mock_db.add = lambda x: mock_db.data.append(x)
    mock_db.discard = lambda x: mock_db.data.pop(0)
    mock_db.batch_get = lambda x: mock_db.data[0]

    cem = SymbolCodeEmbeddingHandler(embedding_builder=mock_provider, embedding_db=mock_db)

    # If exception occurs during the get_embedding operation, the database should not contain any new entries
    cem.process_embedding(mock_simple_method_symbols[0])
    monkeypatch.setattr(
        "automata.symbol.symbol_utils.convert_to_ast_object",
        lambda args: "xx",
    )

    cem.embedding_builder.build.return_value = SymbolCodeEmbedding(
        key=mock_simple_method_symbols[0], document="xx", vector=np.array([1, 2, 3, 4])
    )
    cem.embedding_db.contains = lambda x: True
    cem.embedding_db.get_all_symbols = lambda: [mock_simple_method_symbols[0]]
    cem.embedding_db.batch_get = lambda x: cem.embedding_db.data[0]

    cem.process_embedding(mock_simple_method_symbols[0])
    # TODO - Revisit this test in light of recent changes to handler
    # embedding = cem.embedding_db.data[0].vector
    # assert len(cem.embedding_db.data) == 1  # Expect empty embedding map because of exception
    # assert list(embedding) == [1, 2, 3, 4]


def test_get_embedding_exception(monkeypatch, mock_simple_method_symbols):
    # Test exception in build_embedding_vector function
    monkeypatch.setattr(
        "automata.symbol.symbol_utils.convert_to_ast_object",
        lambda args: "symbol_source",
    )

    # Mock EmbeddingVectorProvider methods
    mock_provider = Mock(EmbeddingBuilder)
    mock_provider.build.side_effect = Exception("Test exception")

    # Mock ChromaSymbolEmbeddingVectorDatabase methods
    mock_db = MagicMock(ChromaSymbolEmbeddingVectorDatabase)
    mock_db.data = []
    mock_db.contains = lambda x: False
    mock_db.add = lambda x: mock_db.data.append(x)

    cem = SymbolCodeEmbeddingHandler(embedding_builder=mock_provider, embedding_db=mock_db)

    # If exception occurs during the get_embedding operation, the database should not contain any new entries
    try:
        cem.process_embedding(mock_simple_method_symbols[0])
    except Exception:
        pass

    assert len(cem.embedding_db.data) == 0  # Expect empty embedding map because of exception
