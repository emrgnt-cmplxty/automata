import pytest

from automata.symbol_embedding import JSONSymbolEmbeddingVectorDatabase


def test_add_symbol(json_vector_db, embedded_symbol):
    json_vector_db.add(embedded_symbol)


def test_delete_symbol(json_vector_db, embedded_symbol):
    json_vector_db.add(embedded_symbol)
    json_vector_db.discard(embedded_symbol.symbol.dotpath)


def test_add_symbols(json_vector_db, symbols, embedded_symbol):
    json_vector_db.add(embedded_symbol)


def test_lookup_symbol(json_vector_db, embedded_symbol):
    json_vector_db.add(embedded_symbol)
    json_vector_db.get(embedded_symbol.symbol.dotpath)


def test_lookup_symbol_fail(json_vector_db, embedded_symbol):
    json_vector_db.add(embedded_symbol)
    json_vector_db.discard(embedded_symbol.symbol.dotpath)

    with pytest.raises(KeyError):
        json_vector_db.get(embedded_symbol.symbol.dotpath)


def test_save(json_vector_db, embedded_symbol):
    json_vector_db.add(embedded_symbol)
    json_vector_db.save()


def test_load(json_vector_db, temp_output_filename, symbols, embedded_symbol):
    json_vector_db.add(embedded_symbol)
    json_vector_db.save()

    vector_db_2 = JSONSymbolEmbeddingVectorDatabase(temp_output_filename)
    vector_db_2.add(embedded_symbol)
    vector_db_2.save()
