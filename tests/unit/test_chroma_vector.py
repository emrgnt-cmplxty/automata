import numpy as np
import pytest

from automata.symbol_embedding.base import SymbolCodeEmbedding, SymbolDocEmbedding
from automata.symbol_embedding.vector_databases import (
    ChromaSymbolEmbeddingVectorDatabase,
)

db_name = "a_test_db"


# Parameterized fixture for embedding type
@pytest.fixture(params=[SymbolCodeEmbedding, SymbolDocEmbedding])
def embedding_type(request):
    return request.param


# Factory fixture for creating embeddings
@pytest.fixture
def make_embedding(embedding_type):
    def _make_embedding(symbol, document, vector):
        if embedding_type == SymbolDocEmbedding:
            # Add extra fields for SymbolDocEmbedding
            return embedding_type(
                symbol,
                document,
                vector,
                source_code="some code",
                summary="summary",
                context="context",
            )
        else:
            return embedding_type(symbol, document, vector)

    return _make_embedding


# Factory fixture for creating database instances
@pytest.fixture
def vector_db(embedding_type):
    return ChromaSymbolEmbeddingVectorDatabase(db_name, factory=embedding_type.from_args)


# Factory fixture for creating database instances
@pytest.fixture
def vector_db_persistent(embedding_type, temp_output_filename):
    return ChromaSymbolEmbeddingVectorDatabase(
        db_name, factory=embedding_type.from_args, persist_directory=temp_output_filename
    )


@pytest.fixture
def symbol_set(symbols):
    symbols = [symbols[0], symbols[1]]
    return symbols


def test_vector_initialization(vector_db):
    assert vector_db is not None


def test_add_single_symbol(vector_db, symbol_set, make_embedding):
    symbol = symbol_set[0]
    embedded_symbol = make_embedding(symbol, "x", np.array([1, 2, 3]).astype(int))
    vector_db.add(embedded_symbol)
    result = vector_db.get(symbol.dotpath)
    assert result.symbol == embedded_symbol.symbol


def test_add_single_symbol_persistent(vector_db_persistent, symbol_set, make_embedding):
    vector_db_persistent.clear()
    symbol = symbol_set[0]
    embedded_symbol = make_embedding(symbol, "x", np.array([1, 2, 3]).astype(int))
    vector_db_persistent.add(embedded_symbol)
    result = vector_db_persistent.get(symbol.dotpath)
    assert result.symbol == embedded_symbol.symbol
    vector_db_persistent.clear()


def test_delete_single_symbol(vector_db, symbol_set, make_embedding):
    symbol = symbol_set[0]
    embedded_symbol = make_embedding(symbol, "x", np.array([1, 2, 3]).astype(int))
    vector_db.add(embedded_symbol)
    vector_db.discard(symbol.dotpath)
    with pytest.raises(KeyError):
        vector_db.get(symbol.dotpath)


@pytest.mark.parametrize("index", [0, 1])
def test_add_and_get_single_symbol(vector_db, symbols, index, make_embedding):
    symbol = symbols[index]
    embedded_symbol = make_embedding(symbol, "x", np.array([1, 2, 3]).astype(int))
    vector_db.add(embedded_symbol)
    result = vector_db.get(symbol.dotpath)
    assert result.symbol == embedded_symbol.symbol


@pytest.mark.parametrize("index", [0, 1])
def test_add_and_discard_single_symbol(vector_db, symbols, index, make_embedding):
    symbol = symbols[index]
    embedded_symbol = make_embedding(symbol, "x", np.array([1, 2, 3]).astype(int))
    vector_db.add(embedded_symbol)
    vector_db.discard(symbol.dotpath)
    with pytest.raises(KeyError):
        vector_db.get(symbol.dotpath)


def test_clear(vector_db, symbols, make_embedding):
    symbol = symbols[0]
    embedded_symbol = make_embedding(symbol, "x", np.array([1, 2, 3]).astype(int))
    vector_db.add(embedded_symbol)
    vector_db.clear()
    with pytest.raises(KeyError):
        vector_db.get(symbol.dotpath)


def test_contains(vector_db, symbols, make_embedding):
    symbol = symbols[0]
    embedded_symbol = make_embedding(symbol, "x", np.array([1, 2, 3]).astype(int))
    vector_db.add(embedded_symbol)
    assert vector_db.contains(symbol.dotpath)


def test_get_ordered_embeddings(vector_db, symbols, make_embedding):
    symbol1 = symbols[0]
    symbol2 = symbols[1]
    embedded_symbol1 = make_embedding(symbol1, "x", np.array([1, 2, 3]).astype(int))
    embedded_symbol2 = make_embedding(symbol2, "y", np.array([4, 5, 6]).astype(int))
    vector_db.add(embedded_symbol2)
    vector_db.add(embedded_symbol1)
    embeddings = vector_db.get_ordered_embeddings()
    assert np.array_equal(embeddings[0].vector, embedded_symbol1.vector)
    assert np.array_equal(embeddings[1].vector, embedded_symbol2.vector)


def test_update_database(vector_db, symbols, make_embedding):
    symbol = symbols[0]
    embedded_symbol = make_embedding(symbol, "x", np.array([1, 2, 3]).astype(int))
    vector_db.add(embedded_symbol)
    updated_embedded_symbol = make_embedding(symbol, "y", np.array([4, 5, 6]).astype(int))
    vector_db.update_database(updated_embedded_symbol)
    result = vector_db.get(symbol.dotpath)
    assert np.array_equal(result.vector, updated_embedded_symbol.vector)
    assert result.document == updated_embedded_symbol.document


@pytest.fixture
def vector_db_old():
    return ChromaSymbolEmbeddingVectorDatabase(db_name, factory=SymbolCodeEmbedding.from_args)


@pytest.fixture
def symbol_set_old(symbols):
    symbols = [symbols[0], symbols[1]]
    return symbols


def test_vector_initialization_old(vector_db_old):
    assert vector_db_old is not None


def test_add_single_symbol_old(vector_db_old, symbol_set_old):
    symbol = symbol_set_old[0]
    embedded_symbol = SymbolCodeEmbedding(symbol, "x", np.array([1, 2, 3]).astype(int))
    vector_db_old.add(embedded_symbol)
    result = vector_db_old.get(symbol.dotpath)
    assert result.symbol == embedded_symbol.symbol


def test_delete_single_symbol_old(vector_db_old, symbol_set_old):
    symbol = symbol_set_old[0]
    embedded_symbol = SymbolCodeEmbedding(symbol, "x", np.array([1, 2, 3]).astype(int))
    vector_db_old.add(embedded_symbol)
    vector_db_old.discard(symbol.dotpath)
    with pytest.raises(KeyError):
        vector_db_old.get(symbol.dotpath)


@pytest.mark.parametrize("index", [0, 1])
def test_add_and_get_single_symbol_old(vector_db_old, symbols, index):
    symbol = symbols[index]
    embedded_symbol = SymbolCodeEmbedding(symbol, "x", np.array([1, 2, 3]).astype(int))
    vector_db_old.add(embedded_symbol)
    result = vector_db_old.get(symbol.dotpath)
    assert result.symbol == embedded_symbol.symbol


@pytest.mark.parametrize("index", [0, 1])
def test_add_and_discard_single_symbol_old(vector_db_old, symbols, index):
    symbol = symbols[index]
    embedded_symbol = SymbolCodeEmbedding(symbol, "x", np.array([1, 2, 3]).astype(int))
    vector_db_old.add(embedded_symbol)
    vector_db_old.discard(symbol.dotpath)
    with pytest.raises(KeyError):
        vector_db_old.get(symbol.dotpath)


def test_clear_old(vector_db_old, symbols):
    symbol = symbols[0]
    embedded_symbol = SymbolCodeEmbedding(symbol, "x", np.array([1, 2, 3]).astype(int))
    vector_db_old.add(embedded_symbol)
    vector_db_old.clear()
    with pytest.raises(KeyError):
        vector_db_old.get(symbol.dotpath)


def test_contains_old(vector_db_old, symbols):
    symbol = symbols[0]
    embedded_symbol = SymbolCodeEmbedding(symbol, "x", np.array([1, 2, 3]).astype(int))
    vector_db_old.add(embedded_symbol)
    assert vector_db_old.contains(symbol.dotpath)


def test_get_ordered_embeddings_old(vector_db_old, symbols):
    symbol1 = symbols[0]
    symbol2 = symbols[1]
    embedded_symbol1 = SymbolCodeEmbedding(symbol1, "x", np.array([1, 2, 3]).astype(int))
    embedded_symbol2 = SymbolCodeEmbedding(symbol2, "y", np.array([4, 5, 6]).astype(int))
    vector_db_old.add(embedded_symbol2)
    vector_db_old.add(embedded_symbol1)
    embeddings = vector_db_old.get_ordered_embeddings()  # [symbol1.dotpath, symbol2.dotpath])
    assert np.array_equal(embeddings[0].vector, embedded_symbol1.vector)
    assert np.array_equal(embeddings[1].vector, embedded_symbol2.vector)


def test_update_database_old(vector_db_old, symbols):
    symbol = symbols[0]
    embedded_symbol = SymbolCodeEmbedding(symbol, "x", np.array([1, 2, 3]).astype(int))
    vector_db_old.add(embedded_symbol)
    updated_embedded_symbol = SymbolCodeEmbedding(symbol, "y", np.array([4, 5, 6]).astype(int))
    vector_db_old.update_database(updated_embedded_symbol)
    result = vector_db_old.get(symbol.dotpath)
    assert np.array_equal(result.vector, updated_embedded_symbol.vector)
    assert result.document == updated_embedded_symbol.document
