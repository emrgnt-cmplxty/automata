from automata.core.embedding.base import EmbeddingHandler
from automata.core.symbol.graph import SymbolGraph
from automata.core.utils import filter_graph_by_symbols


def synchronize_graph_and_handler(symbol_graph: SymbolGraph, embedding_handler: EmbeddingHandler):
    graph_symbols = symbol_graph.get_all_supported_symbols()
    embedding_symbols = embedding_handler.get_all_supported_symbols()
    supported_symbols = set(graph_symbols).intersection(set(embedding_symbols))

    filter_graph_by_symbols(symbol_graph.rankable_subgraph, supported_symbols)
