import pytest

from automata_docs.core.database.vector import JSONVectorDatabase
from automata_docs.core.symbol.symbol_types import SymbolEmbedding


def test_init_vector(temp_output_filename):
    JSONVectorDatabase(temp_output_filename)


def test_add_symbol(temp_output_filename, symbols):
    vector_db = JSONVectorDatabase(temp_output_filename)
    symbol = symbols[0]
    embedded_symbol = SymbolEmbedding(symbol, "x", [1, 2, 3])
    vector_db.add(embedded_symbol)


def test_delete_symbol(temp_output_filename, symbols):
    vector_db = JSONVectorDatabase(temp_output_filename)
    symbol = symbols[0]
    embedded_symbol = SymbolEmbedding(symbol, "x", [1, 2, 3])
    vector_db.add(embedded_symbol)
    vector_db.discard(symbol)


def test_add_symbols(temp_output_filename, symbols):
    vector_db = JSONVectorDatabase(temp_output_filename)
    embedded_symbol_0 = SymbolEmbedding(symbols[0], "x", [1, 2, 3])
    vector_db.add(embedded_symbol_0)
    embedded_symbol_1 = SymbolEmbedding(symbols[1], "y", [1, 2, 3, 4])
    vector_db.add(embedded_symbol_1)


def test_lookup_symbol(temp_output_filename, symbols):
    vector_db = JSONVectorDatabase(temp_output_filename)
    embedded_symbol_0 = SymbolEmbedding(symbols[0], "x", [1, 2, 3])
    vector_db.add(embedded_symbol_0)
    embedded_symbol_1 = SymbolEmbedding(symbols[1], "y", [1, 2, 3, 4])
    vector_db.add(embedded_symbol_1)

    vector_db.get(symbols[0])


def test_lookup_symbol_fail(temp_output_filename, symbols):
    vector_db = JSONVectorDatabase(temp_output_filename)
    embedded_symbol_0 = SymbolEmbedding(symbols[0], "x", [1, 2, 3])
    vector_db.add(embedded_symbol_0)
    embedded_symbol_1 = SymbolEmbedding(symbols[1], "y", [1, 2, 3, 4])
    vector_db.add(embedded_symbol_1)

    vector_db.discard(symbols[0])

    with pytest.raises(KeyError):
        vector_db.get(symbols[0])


def test_save(temp_output_filename, symbols):
    vector_db = JSONVectorDatabase(temp_output_filename)
    embedded_symbol_0 = SymbolEmbedding(symbols[0], "x", [1, 2, 3])
    vector_db.add(embedded_symbol_0)
    embedded_symbol_1 = SymbolEmbedding(symbols[1], "y", [1, 2, 3, 4])
    vector_db.add(embedded_symbol_1)
    vector_db.save()


def test_load(temp_output_filename, symbols):
    vector_db = JSONVectorDatabase(temp_output_filename)
    embedded_symbol_0 = SymbolEmbedding(symbols[0], "x", [1, 2, 3])
    vector_db.add(embedded_symbol_0)
    embedded_symbol_1 = SymbolEmbedding(symbols[1], "y", [1, 2, 3, 4])
    vector_db.add(embedded_symbol_1)
    vector_db.save()

    vector_db_2 = JSONVectorDatabase(temp_output_filename)

    embedded_symbol_0 = vector_db_2.get(symbols[0])
    embedded_symbol_1 = vector_db_2.get(symbols[1])
