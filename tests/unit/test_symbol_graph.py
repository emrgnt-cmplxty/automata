from automata.context_providers.symbol_synchronization import (
    SymbolProviderSynchronizationContext,
)
from automata.singletons.py_module_loader import py_module_loader
from automata.symbol import Symbol
from automata.symbol.graph.symbol_graph import SymbolGraph

from ..utils.factories import symbol_graph_static_test  # noqa: F401


def test_get_all_symbols(symbol_graph_static_test):  # noqa: F811
    with SymbolProviderSynchronizationContext() as synchronization_context:
        synchronization_context.register_provider(symbol_graph_static_test)
        synchronization_context.synchronize()

    graph_symbols = symbol_graph_static_test.get_sorted_supported_symbols()
    assert isinstance(graph_symbols, list)
    assert all(isinstance(s, Symbol) for s in graph_symbols)


def test_build_real_graph(symbol_graph_static_test):  # noqa: F811
    with SymbolProviderSynchronizationContext() as synchronization_context:
        synchronization_context.register_provider(symbol_graph_static_test)
        synchronization_context.synchronize()

    all_symbols = sorted(
        symbol_graph_static_test.get_sorted_supported_symbols(), key=lambda x: x.dotpath
    )

    assert isinstance(symbol_graph_static_test, SymbolGraph)
    assert len(all_symbols) == 1_874


def test_build_real_graph_and_subgraph(symbol_graph_static_test):  # noqa: F811
    with SymbolProviderSynchronizationContext() as synchronization_context:
        synchronization_context.register_provider(symbol_graph_static_test)
        synchronization_context.synchronize()

    py_module_loader.initialize()

    # build the subgraph
    subgraph = symbol_graph_static_test.default_rankable_subgraph
    assert len(subgraph) == 29

    py_module_loader.initialized = False
    py_module_loader.rel_py_path = None
    py_module_loader.root_fpath = None
