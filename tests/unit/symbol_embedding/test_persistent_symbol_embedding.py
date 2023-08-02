import numpy as np
import pytest

from automata.symbol_embedding import SymbolCodeEmbedding, SymbolDocEmbedding


@pytest.mark.parametrize(
    "embedding_type, vector",
    [(SymbolDocEmbedding, [0, 1, 2]), (SymbolCodeEmbedding, [1, 2, 3])],
)
def test_symbol_embedding(
    embedding_type,
    vector,
    symbols,
    chroma_vector_db_persistent,
):
    chroma_vector_db_persistent.clear()

    for i in range(2):
        embedding = create_embedding(embedding_type, symbols[i], vector, i)
        fetched_embedding = _extracted_from_test_symbol_doc_embedding(
            chroma_vector_db_persistent, embedding, symbols[i].dotpath
        )

        assert fetched_embedding.source_code == embedding.source_code
        assert fetched_embedding.summary == embedding.summary
        assert fetched_embedding.context == embedding.context
        assert False


def create_embedding(embedding_type, symbol, vector, i):
    if embedding_type == SymbolDocEmbedding:
        return SymbolDocEmbedding(
            key=symbol,
            document=f"x{i}",
            vector=vector,
            source_code=f"y{i}",
            summary=f"z{i}",
            context=f"a{i}",
        )
    elif embedding_type == SymbolCodeEmbedding:
        return SymbolCodeEmbedding(
            key=symbol,
            document=f"x{i}",
            vector=vector,
        )


def _extracted_from_test_symbol_doc_embedding(
    chroma_vector_db_persistent, embedding, dotpath
):
    chroma_vector_db_persistent.add(embedding)
    chroma_vector_db_persistent.save()
    result = chroma_vector_db_persistent.get(dotpath)
    assert embedding.symbol == result.symbol
    assert embedding.document == result.document
    assert np.allclose(embedding.vector, result.vector)
    return result
