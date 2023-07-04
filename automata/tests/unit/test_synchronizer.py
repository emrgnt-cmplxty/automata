from copy import deepcopy
import networkx as nx
from automata.core.memory_store.symbol_code_embedding import SymbolCodeEmbeddingHandler
import numpy as np
from automata.core.symbol_embedding.base import (
    SymbolCodeEmbedding,
    JSONSymbolEmbeddingVectorDatabase,
)
from unittest.mock import MagicMock
from automata.core.embedding.base import EmbeddingBuilder

from automata.core.context_providers.symbol_synchronization import (
    SymbolProviderSynchronizationContext,
)
from automata.tests.utils.factories import symbol_graph_static_test  # noqa: F401


def test_build_graph_and_handler_and_synchronize(
    temp_output_filename, mock_simple_method_symbols, symbol_graph_static_test
):  # noqa: F811
    symbol1 = mock_simple_method_symbols[0]
    symbol2 = mock_simple_method_symbols[1]
    symbol3 = mock_simple_method_symbols[2]

    embedding1 = SymbolCodeEmbedding(
        symbol=symbol1, vector=np.array([1, 0, 0, 0]), source_code="symbol1"
    )
    embedding2 = SymbolCodeEmbedding(
        symbol=symbol2, vector=np.array([0, 1, 0, 0]), source_code="symbol2"
    )
    embedding3 = SymbolCodeEmbedding(
        symbol=symbol3, vector=np.array([0, 0, 1, 0]), source_code="symbol3"
    )

    # Mock JSONSymbolEmbeddingVectorDatabase methods
    embedding_db = JSONSymbolEmbeddingVectorDatabase(temp_output_filename)
    embedding_db.add(embedding1)
    embedding_db.add(embedding2)
    embedding_db.add(embedding3)

    # Create an instance of the class
    mock_builder = MagicMock(EmbeddingBuilder)
    cem = SymbolCodeEmbeddingHandler(embedding_db=embedding_db, embedding_builder=mock_builder)

    G = nx.DiGraph()
    G.add_node(symbol1, label="symbol")
    G.add_edge(symbol1, symbol2, label="symbol")
    symbol_graph_tester = deepcopy(symbol_graph_static_test)
    symbol_graph_tester._graph = G
    symbol_graph_tester.navigator._graph = G

    with SymbolProviderSynchronizationContext() as synchronization_context:
        from automata.core.context_providers.symbol_synchronization import SymbolProviderRegistry

        SymbolProviderRegistry._providers = set([])
        SymbolProviderRegistry.sorted_supported_symbols = []

        synchronization_context.register_provider(symbol_graph_tester)
        synchronization_context.register_provider(cem)
        synchronization_context.synchronize()

    assert len(symbol_graph_tester.get_sorted_supported_symbols()) == 1
    assert len(cem.get_sorted_supported_symbols()) == 1  # post synchronization
