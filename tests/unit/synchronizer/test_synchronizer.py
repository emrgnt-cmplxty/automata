from copy import deepcopy
from unittest.mock import MagicMock

import networkx as nx
import numpy as np
import pytest

from automata.context_providers import SymbolProviderSynchronizationContext
from automata.embedding import EmbeddingBuilder
from automata.memory_store import SymbolCodeEmbeddingHandler
from automata.symbol_embedding import (
    JSONSymbolEmbeddingVectorDatabase,
    SymbolCodeEmbedding,
)
from tests.utils.factories import symbol_graph_static_test  # noqa: F401, F811


# Use fixtures for common setup
@pytest.fixture
def symbols_and_embeddings(mock_simple_method_symbols):
    symbol1 = mock_simple_method_symbols[0]
    symbol2 = mock_simple_method_symbols[1]
    symbol3 = mock_simple_method_symbols[2]

    embedding1 = SymbolCodeEmbedding(
        key=symbol1, vector=np.array([1, 0, 0, 0]), document="symbol1"
    )
    embedding2 = SymbolCodeEmbedding(
        key=symbol2, vector=np.array([0, 1, 0, 0]), document="symbol2"
    )
    embedding3 = SymbolCodeEmbedding(
        key=symbol3, vector=np.array([0, 0, 1, 0]), document="symbol3"
    )
    return symbol1, symbol2, symbol3, embedding1, embedding2, embedding3


@pytest.fixture
def embedding_db(temp_output_filename, symbols_and_embeddings):
    _, _, _, embedding1, embedding2, embedding3 = symbols_and_embeddings
    # Mock JSONSymbolEmbeddingVectorDatabase methods
    embedding_db = JSONSymbolEmbeddingVectorDatabase(temp_output_filename)
    embedding_db.add(embedding1)
    embedding_db.add(embedding2)
    embedding_db.add(embedding3)
    return embedding_db


def test_build_graph_and_handler(
    embedding_db, mock_simple_method_symbols, symbol_graph_static_test  # noqa: F811
):
    symbol1, symbol2, _, _, _, _ = mock_simple_method_symbols

    # Create an instance of the class
    mock_builder = MagicMock(EmbeddingBuilder)
    cem = SymbolCodeEmbeddingHandler(embedding_db=embedding_db, embedding_builder=mock_builder)

    G = nx.DiGraph()
    G.add_node(symbol1, label="symbol")
    G.add_edge(symbol1, symbol2, label="symbol")
    symbol_graph_tester = deepcopy(symbol_graph_static_test)
    symbol_graph_tester._graph = G
    symbol_graph_tester.navigator._graph = G

    return cem, symbol_graph_tester


def test_synchronize(cem, symbol_graph_tester):
    with SymbolProviderSynchronizationContext() as synchronization_context:
        from automata.context_providers import SymbolProviderRegistry

        SymbolProviderRegistry._providers = set([])
        SymbolProviderRegistry.sorted_supported_symbols = []

        synchronization_context.register_provider(symbol_graph_tester)
        synchronization_context.register_provider(cem)
        synchronization_context.synchronize()

    assert len(symbol_graph_tester.get_sorted_supported_symbols()) == 1
    assert len(cem.get_sorted_supported_symbols()) == 1  # post synchronization
