import os
import pickle

import networkx as nx
import pytest

from automata.cli.cli_utils import initialize_py_module_loader
from automata.singletons.dependency_factory import DependencyFactory
from automata.symbol import SymbolGraph


@pytest.fixture
def symbol_graph():
    initialize_py_module_loader()
    graph = SymbolGraph(
        os.path.join(DependencyFactory.DEFAULT_SCIP_FPATH, "automata.scip"),
        save_graph_pickle=True,
    )
    graph.is_synchronized = True
    return graph


def test_subgraph_pickle_creation(symbol_graph):
    symbol_graph.default_rankable_subgraph

    assert os.path.exists(
        symbol_graph.subgraph_pickle_path
    ), f"No pickle file found at {symbol_graph.subgraph_pickle_path}"

    with open(symbol_graph.subgraph_pickle_path, "rb") as f:
        pickled_subgraph = pickle.load(f)

    assert isinstance(pickled_subgraph, nx.DiGraph)
