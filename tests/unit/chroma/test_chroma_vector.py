import numpy as np
import pytest

# TODO - We need more tests around persistence
# FIXME - We need to make sure db folder clears after running tests


def test_vector_initialization(chroma_vector_db):
    assert chroma_vector_db is not None


def test_add_single_symbol(chroma_vector_db, symbols, embedding_maker):
    symbol = symbols[0]
    embedded_symbol = embedding_maker(
        symbol, "x", np.array([1, 2, 3]).astype(int)
    )
    chroma_vector_db.add(embedded_symbol)
    result = chroma_vector_db.get(symbol.full_dotpath)
    assert result.symbol == embedded_symbol.symbol


def test_add_single_symbol_persistent(
    chroma_vector_db_persistent, symbols, embedding_maker
):
    chroma_vector_db_persistent.clear()
    symbol = symbols[0]
    embedded_symbol = embedding_maker(
        symbol, "x", np.array([1, 2, 3]).astype(int)
    )
    chroma_vector_db_persistent.add(embedded_symbol)
    result = chroma_vector_db_persistent.get(symbol.full_dotpath)
    assert result.symbol == embedded_symbol.symbol
    chroma_vector_db_persistent.clear()


def test_delete_single_symbol(chroma_vector_db, symbols, embedding_maker):
    symbol = symbols[0]
    embedded_symbol = embedding_maker(
        symbol, "x", np.array([1, 2, 3]).astype(int)
    )
    chroma_vector_db.add(embedded_symbol)
    chroma_vector_db.discard(symbol.full_dotpath)
    with pytest.raises(KeyError):
        chroma_vector_db.get(symbol.full_dotpath)


@pytest.mark.parametrize("index", [0, 1])
def test_add_and_get_single_symbol(
    chroma_vector_db, symbols, index, embedding_maker
):
    symbol = symbols[index]
    embedded_symbol = embedding_maker(
        symbol, "x", np.array([1, 2, 3]).astype(int)
    )
    chroma_vector_db.add(embedded_symbol)
    result = chroma_vector_db.get(symbol.full_dotpath)
    assert result.symbol == embedded_symbol.symbol


@pytest.mark.parametrize("index", [0, 1])
def test_add_and_discard_single_symbol(
    chroma_vector_db, symbols, index, embedding_maker
):
    symbol = symbols[index]
    embedded_symbol = embedding_maker(
        symbol, "x", np.array([1, 2, 3]).astype(int)
    )
    chroma_vector_db.add(embedded_symbol)
    chroma_vector_db.discard(symbol.full_dotpath)
    with pytest.raises(KeyError):
        chroma_vector_db.get(symbol.full_dotpath)


def test_clear(chroma_vector_db, symbols, embedding_maker):
    symbol = symbols[0]
    embedded_symbol = embedding_maker(
        symbol, "x", np.array([1, 2, 3]).astype(int)
    )
    chroma_vector_db.add(embedded_symbol)
    chroma_vector_db.clear()
    with pytest.raises(KeyError):
        chroma_vector_db.get(symbol.full_dotpath)


def test_contains(chroma_vector_db, symbols, embedding_maker):
    symbol = symbols[0]
    embedded_symbol = embedding_maker(
        symbol, "x", np.array([1, 2, 3]).astype(int)
    )
    chroma_vector_db.add(embedded_symbol)
    assert chroma_vector_db.contains(symbol.full_dotpath)


def test_get_ordered_embeddings(chroma_vector_db, symbols, embedding_maker):
    symbol1 = symbols[0]
    symbol2 = symbols[1]
    embedded_symbol1 = embedding_maker(
        symbol1, "x", np.array([1, 2, 3]).astype(int)
    )
    embedded_symbol2 = embedding_maker(
        symbol2, "y", np.array([4, 5, 6]).astype(int)
    )
    chroma_vector_db.add(embedded_symbol2)
    chroma_vector_db.add(embedded_symbol1)
    embeddings = chroma_vector_db.get_all_ordered_embeddings()
    assert np.array_equal(embeddings[0].vector, embedded_symbol1.vector)
    assert np.array_equal(embeddings[1].vector, embedded_symbol2.vector)


def test_update_database(chroma_vector_db, symbols, embedding_maker):
    symbol = symbols[0]
    embedded_symbol = embedding_maker(
        symbol, "x", np.array([1, 2, 3]).astype(int)
    )
    chroma_vector_db.add(embedded_symbol)
    updated_embedded_symbol = embedding_maker(
        symbol, "y", np.array([4, 5, 6]).astype(int)
    )
    chroma_vector_db.update_entry(updated_embedded_symbol)
    result = chroma_vector_db.get(symbol.full_dotpath)
    assert np.array_equal(result.vector, updated_embedded_symbol.vector)
    assert result.document == updated_embedded_symbol.document


def test_size(chroma_vector_db, symbols, embedding_maker):
    symbol1 = symbols[0]
    symbol2 = symbols[1]
    embedded_symbol1 = embedding_maker(
        symbol1, "x", np.array([1, 2, 3]).astype(int)
    )
    embedded_symbol2 = embedding_maker(
        symbol2, "y", np.array([4, 5, 6]).astype(int)
    )
    chroma_vector_db.add(embedded_symbol1)
    chroma_vector_db.add(embedded_symbol2)
    assert len(chroma_vector_db) == 2


def test_batch_add_and_remove(chroma_vector_db, symbols, embedding_maker):
    embedded_symbols = [
        embedding_maker(symbol, "x", np.array([i, i + 1, i + 2]).astype(int))
        for i, symbol in enumerate(symbols)
    ]
    chroma_vector_db.batch_add(embedded_symbols)
    assert all(
        chroma_vector_db.contains(symbol.full_dotpath) for symbol in symbols
    )
    chroma_vector_db.batch_discard([symbol.full_dotpath for symbol in symbols])
    assert not any(
        chroma_vector_db.contains(symbol.full_dotpath) for symbol in symbols
    )


def test_add_duplicate_symbol(chroma_vector_db, symbols, embedding_maker):
    symbol = symbols[0]
    embedded_symbol1 = embedding_maker(
        symbol, "x", np.array([1, 2, 3]).astype(int)
    )
    chroma_vector_db.add(embedded_symbol1)
    with pytest.raises(KeyError):
        chroma_vector_db.add(embedded_symbol1)


def test_get_all_symbols(chroma_vector_db, symbols, embedding_maker):
    embedded_symbols = [
        embedding_maker(symbol, "x", np.array([i, i + 1, i + 2]).astype(int))
        for i, symbol in enumerate(symbols)
    ]
    chroma_vector_db.batch_add(embedded_symbols)
    all_symbols = chroma_vector_db.get_ordered_keys()
    assert len(all_symbols) == len(symbols)
    assert all(symbol.full_dotpath in all_symbols for symbol in list(symbols))
