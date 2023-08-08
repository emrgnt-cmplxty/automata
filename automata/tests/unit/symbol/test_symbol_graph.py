import pytest

from automata.context_providers.symbol_synchronization_context import (
    SymbolProviderSynchronizationContext,
)
from automata.singletons.py_module_loader import py_module_loader
from automata.symbol import Symbol, SymbolGraph
from automata.tests.utils.factories import static_indices_graph_dynamic  # noqa


@pytest.fixture
def sync_context(static_indices_graph_dynamic):  # noqa
    with SymbolProviderSynchronizationContext() as synchronization_context:
        synchronization_context.register_provider(static_indices_graph_dynamic)
        synchronization_context.synchronize()
    return synchronization_context


def test_get_all_symbols(static_indices_graph_dynamic, sync_context):  # noqa
    graph_symbols = static_indices_graph_dynamic.get_sorted_supported_symbols()
    assert isinstance(graph_symbols, list)
    assert all(isinstance(s, Symbol) for s in graph_symbols)


def test_build_real_graph(static_indices_graph_dynamic, sync_context):  # noqa
    all_symbols = sorted(
        static_indices_graph_dynamic.get_sorted_supported_symbols(),
        key=lambda x: x.dotpath,
    )

    assert isinstance(static_indices_graph_dynamic, SymbolGraph)
    assert len(all_symbols) == 1_874


def test_build_real_graph_and_subgraph(
    static_indices_graph_dynamic, sync_context  # noqa
):  # noqa
    py_module_loader.reset()
    py_module_loader.initialize()

    # build the subgraph
    subgraph = static_indices_graph_dynamic.default_rankable_subgraph
    assert len(subgraph) == 43
    py_module_loader.reset()
