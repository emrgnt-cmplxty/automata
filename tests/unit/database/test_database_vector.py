import pytest

from automata.symbol_embedding import (
    JSONSymbolEmbeddingVectorDatabase,
    SymbolCodeEmbedding,
)


@pytest.fixture
def vector_db(temp_output_filename):
    return JSONSymbolEmbeddingVectorDatabase(temp_output_filename)


@pytest.fixture(params=[0, 1])
def embedded_symbol(symbols, request):
    data = [("x", [1, 2, 3]), ("y", [1, 2, 3, 4])][request.param]
    return SymbolCodeEmbedding(symbols[request.param], data[0], data[1])


def test_init_vector(vector_db):
    pass


def test_add_symbol(vector_db, embedded_symbol):
    vector_db.add(embedded_symbol)


def test_delete_symbol(vector_db, embedded_symbol):
    vector_db.add(embedded_symbol)
    vector_db.discard(embedded_symbol.symbol.full_dotpath)


def test_add_symbols(vector_db, symbols, embedded_symbol):
    vector_db.add(embedded_symbol)


def test_lookup_symbol(vector_db, embedded_symbol):
    vector_db.add(embedded_symbol)
    vector_db.get(embedded_symbol.symbol.full_dotpath)


def test_lookup_symbol_fail(vector_db, embedded_symbol):
    vector_db.add(embedded_symbol)
    vector_db.discard(embedded_symbol.symbol.full_dotpath)

    with pytest.raises(KeyError):
        vector_db.get(embedded_symbol.symbol.full_dotpath)


def test_save(vector_db, embedded_symbol):
    vector_db.add(embedded_symbol)
    vector_db.save()


def test_load(vector_db, temp_output_filename, symbols, embedded_symbol):
    vector_db.add(embedded_symbol)
    vector_db.save()

    vector_db_2 = JSONSymbolEmbeddingVectorDatabase(temp_output_filename)
    vector_db_2.add(embedded_symbol)
    vector_db_2.save()
