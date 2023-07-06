import numpy as np
import pytest

from automata.symbol_embedding.base import SymbolCodeEmbedding
from automata.symbol_embedding.vector_databases import (
    ChromaSymbolEmbeddingVectorDatabase,
)

db_name = "a_test_db"


@pytest.fixture
def vector_db():
    return ChromaSymbolEmbeddingVectorDatabase(db_name, factory=SymbolCodeEmbedding.from_args)


@pytest.fixture
def symbol_set(symbols):
    symbols = [symbols[0], symbols[1]]
    return symbols


def test_vector_initialization(vector_db):
    assert vector_db is not None


def test_add_single_symbol(vector_db, symbol_set):
    symbol = symbol_set[0]
    embedded_symbol = SymbolCodeEmbedding(symbol, "x", np.array([1, 2, 3]).astype(int))
    vector_db.add(embedded_symbol)
    result = vector_db.get(symbol.dotpath)
    assert result.symbol == embedded_symbol.symbol


def test_delete_single_symbol(vector_db, symbol_set):
    symbol = symbol_set[0]
    embedded_symbol = SymbolCodeEmbedding(symbol, "x", np.array([1, 2, 3]).astype(int))
    vector_db.add(embedded_symbol)
    vector_db.discard(symbol.dotpath)
    with pytest.raises(KeyError):
        vector_db.get(symbol.dotpath)


@pytest.mark.parametrize("index", [0, 1])
def test_add_and_get_single_symbol(vector_db, symbols, index):
    symbol = symbols[index]
    embedded_symbol = SymbolCodeEmbedding(symbol, "x", np.array([1, 2, 3]).astype(int))
    vector_db.add(embedded_symbol)
    result = vector_db.get(symbol.dotpath)
    assert result.symbol == embedded_symbol.symbol


@pytest.mark.parametrize("index", [0, 1])
def test_add_and_discard_single_symbol(vector_db, symbols, index):
    symbol = symbols[index]
    embedded_symbol = SymbolCodeEmbedding(symbol, "x", np.array([1, 2, 3]).astype(int))
    vector_db.add(embedded_symbol)
    vector_db.discard(symbol.dotpath)
    with pytest.raises(KeyError):
        vector_db.get(symbol.dotpath)
