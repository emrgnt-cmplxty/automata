import pytest

from automata_docs.core.search.symbol_types import Symbol, SymbolFile, SymbolReference


def test_get_all_files(symbol_graph):
    files = symbol_graph.get_all_files()
    assert isinstance(files, list)
    for f in files:
        assert isinstance(f, SymbolFile)


def test_get_all_symbols(symbol_graph, symbols):
    graph_symbols = symbol_graph.get_all_defined_symbols()
    assert isinstance(graph_symbols, list)
    assert all(isinstance(s, Symbol) for s in graph_symbols)


def test_get_symbol_references(symbol_graph, symbols):
    for symbol in symbols:
        print("Getting references...")
        references = symbol_graph.get_references_to_symbol(symbol)
        print("references = ", references)
        assert isinstance(references, dict)
        assert all(
            [isinstance(ele, SymbolReference) for ele in v] and isinstance(v, list)
            for k, v in references.items()
        )


@pytest.mark.skip(reason="Not implemented yet")
def test_find_return_symbol(symbol_graph, symbols):
    for symbol in symbols:
        return_symbol = symbol_graph.find_return_symbol(symbol)
        assert return_symbol is None or isinstance(return_symbol, Symbol)
