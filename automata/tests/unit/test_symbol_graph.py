from automata.core.symbol.graph import SymbolGraph
from automata.core.symbol.symbol_types import Symbol, SymbolFile
from automata.tests.utils.factories import symbol_graph_static_test  # noqa: F401


def test_get_all_files(symbol_graph_static_test):  # noqa: F811
    files = symbol_graph_static_test.get_all_files()
    assert isinstance(files, list)
    for f in files:
        assert isinstance(f, SymbolFile)


def test_get_all_symbols(symbol_graph_static_test):  # noqa: F811
    graph_symbols = symbol_graph_static_test.get_all_available_symbols()
    assert isinstance(graph_symbols, list)
    assert all(isinstance(s, Symbol) for s in graph_symbols)


def test_build_real_graph_and_subgraph(symbol_graph_static_test):  # noqa: F811
    subgraph = symbol_graph_static_test.get_rankable_symbol_subgraph()
    all_symbols = sorted(
        symbol_graph_static_test.get_all_available_symbols(), key=lambda x: x.dotpath
    )
    all_files = symbol_graph_static_test.get_all_files()

    assert isinstance(symbol_graph_static_test, SymbolGraph)
    assert len(all_symbols) == 1_874
    assert len(all_files) == 91
    assert len(subgraph.graph) == 70
    assert subgraph.graph.number_of_edges() == 204
