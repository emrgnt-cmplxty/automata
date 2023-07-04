from automata.core.symbol.base import Symbol, SymbolFile
from automata.tests.utils.factories import symbol_graph_static_test  # noqa: F401


def test_get_all_files(symbol_graph_static_test):  # noqa: F811
    files = symbol_graph_static_test.get_all_files()
    assert isinstance(files, list)
    for f in files:
        assert isinstance(f, SymbolFile)


def test_get_all_symbols(symbol_graph_static_test):  # noqa: F811
    graph_symbols = symbol_graph_static_test.get_all_supported_symbols()
    assert isinstance(graph_symbols, list)
    assert all(isinstance(s, Symbol) for s in graph_symbols)
