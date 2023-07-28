import os

import pytest

from automata.experimental.search.symbol_search import SymbolSearch
from automata.singletons.dependency_factory import dependency_factory
from automata.symbol import SymbolGraph


@pytest.fixture
def symbol_graph_static_test() -> SymbolGraph:
    """
    Creates a non-mock SymbolGraph object for testing the graph

    Note:
        Subgraphs produced from this graph can change as the underlying code evolves in automata/
        This is because the graph is loading up indices that point to the actual code.
    """
    # assuming the path to a valid index protobuf file, you should replace it with your own file path
    file_dir = os.path.dirname(os.path.abspath(__file__))
    index_path = os.path.join(file_dir, "..", "test.scip")
    return SymbolGraph(index_path, pickle_graph=False)


@pytest.fixture
def symbol_search_live() -> SymbolSearch:
    """
    Creates a non-mock SymbolRank object to be used for testing the search

    """
    dependency_factory.reset()
    return dependency_factory.get("symbol_search")
