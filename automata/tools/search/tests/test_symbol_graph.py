# test_symbol_graph.py

from automata.tools.search.local_types import Symbol


def test_get_all_files(symbol_graph):
    files = symbol_graph.get_all_files()
    assert isinstance(files, list)
    for f in files:
        assert isinstance(f, str)


def test_get_all_symbols(symbol_graph, symbols):
    graph_symbols = symbol_graph.get_all_symbols()
    assert isinstance(graph_symbols, list)
    assert all(isinstance(s, Symbol) for s in graph_symbols)


def test_get_symbol_references(symbol_graph, symbols):
    for symbol in symbols:
        print("symbol = ", symbol)
        references = symbol_graph.get_symbol_references(symbol)
        assert isinstance(references, dict)
        assert all(isinstance(k, str) and isinstance(v, list) for k, v in references.items())


def test_get_symbols_along_path(symbol_graph):
    partial_path = "automata"
    symbols = symbol_graph.get_symbols_along_path(partial_path)
    assert isinstance(symbols, set)
    assert all("automata" in s.uri for s in symbols)


def test_get_symbol_context(symbol_graph, symbols):
    for symbol in symbols:
        context = symbol_graph.get_symbol_context(symbol)
        assert isinstance(context, str)


def test_find_return_symbol(symbol_graph, symbols):
    for symbol in symbols:
        return_symbol = symbol_graph.find_return_symbol(symbol)
        assert return_symbol is None or isinstance(return_symbol, Symbol)
