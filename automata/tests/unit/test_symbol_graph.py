from automata.core.symbol.graph import SymbolGraph
from automata.core.symbol.base import Symbol
from automata.tests.utils.factories import symbol_graph_static_test  # noqa: F401
from automata.core.context_providers.symbol_synchronization import (
    SymbolProviderSynchronizationContext,
)
from automata.core.singletons.py_module_loader import py_module_loader


def test_get_all_symbols(symbol_graph_static_test):  # noqa: F811
    with SymbolProviderSynchronizationContext() as synchronization_context:
        synchronization_context.register_provider(symbol_graph_static_test)
        synchronization_context.synchronize()

    graph_symbols = symbol_graph_static_test.get_all_supported_symbols()
    assert isinstance(graph_symbols, list)
    assert all(isinstance(s, Symbol) for s in graph_symbols)


def test_build_real_graph(symbol_graph_static_test):  # noqa: F811
    with SymbolProviderSynchronizationContext() as synchronization_context:
        synchronization_context.register_provider(symbol_graph_static_test)
        synchronization_context.synchronize()

    all_symbols = sorted(
        symbol_graph_static_test.get_all_supported_symbols(), key=lambda x: x.dotpath
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
    assert len(subgraph) == 12

    py_module_loader.initialized = False
