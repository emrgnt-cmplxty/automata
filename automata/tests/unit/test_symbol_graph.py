from automata.core.symbol.graph import SymbolGraph
from automata.core.symbol.symbol_types import Symbol, SymbolFile


def test_get_all_files(symbol_graph):
    files = symbol_graph.get_all_files()
    assert isinstance(files, list)
    for f in files:
        assert isinstance(f, SymbolFile)


def test_get_all_symbols(symbol_graph):
    graph_symbols = symbol_graph.get_all_available_symbols()
    assert isinstance(graph_symbols, list)
    assert all(isinstance(s, Symbol) for s in graph_symbols)


def test_build_real_graph_and_subgraph():
    # get local pwd
    import os

    path = os.path.dirname(os.path.realpath(__file__))

    graph = SymbolGraph(os.path.join(path, "index.scip"))
    subgraph = graph.get_rankable_symbol_subgraph()
    all_symbols = sorted(graph.get_all_available_symbols(), key=lambda x: x.dotpath)
    all_files = graph.get_all_files()

    assert isinstance(graph, SymbolGraph)
    assert len(all_symbols) == 1_874
    assert len(all_files) == 91
    assert len(subgraph.graph) == 69
    assert subgraph.graph.number_of_edges() == 203
