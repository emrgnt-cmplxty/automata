import pickle

import pytest

from automata.context_providers.symbol_synchronization_context import (
    SymbolProviderSynchronizationContext,
)
from automata.singletons.py_module_loader import py_module_loader
from automata.symbol import Symbol, SymbolGraph
from automata.symbol.graph.data_root_settings import data_root_path
from tests.utils.factories import static_symbol_graph_static_test  # noqa

# @pytest.fixture
# def symbol_graph_test():
#     with open("/Users/nolantremelling/automata/automata-embedding-data/test_symbol_graph.pkl", "rb") as f:
#             graph = pickle.load(f)
#     return SymbolGraph.from_graph(graph)


@pytest.fixture
def sync_context(static_symbol_graph_static_test):  # noqa
    with SymbolProviderSynchronizationContext() as synchronization_context:
        synchronization_context.register_provider(
            static_symbol_graph_static_test
        )
        synchronization_context.synchronize()
    return synchronization_context


def test_get_all_symbols(
    static_symbol_graph_static_test, sync_context
):  # noqa
    graph_symbols = (
        static_symbol_graph_static_test.get_sorted_supported_symbols()
    )
    assert isinstance(graph_symbols, list)
    assert all(isinstance(s, Symbol) for s in graph_symbols)


def test_build_real_graph(
    static_symbol_graph_static_test, sync_context
):  # noqa
    all_symbols = sorted(
        static_symbol_graph_static_test.get_sorted_supported_symbols(),
        key=lambda x: x.full_dotpath,
    )

    assert isinstance(static_symbol_graph_static_test, SymbolGraph)
    assert len(all_symbols) == 1_874


def test_build_real_graph_and_subgraph(
    static_symbol_graph_static_test, sync_context  # noqa
):  # noqa
    py_module_loader.reset()
    py_module_loader.initialize()

    # build the subgraph
    subgraph = static_symbol_graph_static_test.default_rankable_subgraph
    assert len(subgraph) == 46
    py_module_loader.reset()
