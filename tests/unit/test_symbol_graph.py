from automata_docs.core.symbol.symbol_types import Symbol, SymbolFile


def test_get_all_files(symbol_graph):
    files = symbol_graph.get_all_files()
    assert isinstance(files, list)
    for f in files:
        assert isinstance(f, SymbolFile)


def test_get_all_symbols(symbol_graph):
    graph_symbols = symbol_graph.get_all_available_symbols()
    assert isinstance(graph_symbols, list)
    assert all(isinstance(s, Symbol) for s in graph_symbols)
