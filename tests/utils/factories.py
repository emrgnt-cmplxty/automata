import io
import os
import pickle

import pytest

from automata.experimental.search.symbol_search import SymbolSearch
from automata.singletons.dependency_factory import dependency_factory
from automata.symbol import SymbolGraph


@pytest.fixture
def static_indices_graph_dynamic() -> SymbolGraph:
    """
    Creates a non-mock SymbolGraph object for testing the graph

    Note:
        Subgraphs produced from this graph can change as the underlying code evolves in automata/
        This is because the graph is loading up indices that point to the actual code.
    """
    # assuming the path to a valid index protobuf file, you should replace it with your own file path
    file_dir = os.path.dirname(os.path.abspath(__file__))
    index_path = os.path.join(file_dir, "..", "test.scip")
    return SymbolGraph(index_path, save_graph_pickle=False)


@pytest.fixture
def static_indices_graph_static() -> SymbolGraph:
    """
    Creates a serialized and then deserialized (via pickle) non-mock SymbolGraph object for testing the graph.

    This fixture provides a way to test the pickling and unpickling processes of SymbolGraph objects. The object
    is first pickled into an in-memory binary stream, then immediately unpickled from that same stream. This is
    helpful when you want to create a copy of the object that doesn't share references with the original, or
    when testing the object's serialization and deserialization processes.

    Note:
        As the unpickling process involves loading up indices that point to the actual code, subgraphs
        produced from this graph can change as the underlying code evolves in automata/.
    """
    file_dir = os.path.dirname(os.path.abspath(__file__))
    index_path = os.path.join(file_dir, "..", "test.scip")
    symbol_graph = SymbolGraph(index_path, save_graph_pickle=False)

    stream = io.BytesIO()
    pickle.dump(symbol_graph, stream)
    stream.seek(0)

    return pickle.load(stream)


@pytest.fixture
def symbol_search_live() -> SymbolSearch:
    """
    Creates a non-mock SymbolRank object to be used for testing the search

    """
    dependency_factory.reset()
    return dependency_factory.get("symbol_search")
