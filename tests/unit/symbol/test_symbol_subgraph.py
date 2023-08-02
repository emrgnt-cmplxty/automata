import os
import pickle
from unittest import mock

import networkx as nx
import pytest
from google.protobuf.message import Message

from automata.cli.cli_utils import initialize_py_module_loader
from automata.singletons.dependency_factory import DependencyFactory
from automata.symbol import SymbolGraph


class MockProtoBuf(Message):
    def __init__(self, *args, **kwargs):
        self.documents = []


class MockDocument:
    def __init__(self, *args, **kwargs):
        self.symbols = []
        self.occurrences = []


@pytest.fixture
def symbol_graph_mocked_index():
    initialize_py_module_loader()
    with mock.patch(
        "automata.symbol.graph.symbol_graph._load_index_protobuf",
        return_value=MockProtoBuf(),
    ) as mock_load:
        mock_load.return_value.documents = [MockDocument(), MockDocument()]
        graph = SymbolGraph(
            os.path.join(
                DependencyFactory.DEFAULT_SCIP_FPATH, "automata.scip"
            ),
            save_graph_pickle=True,
        )
    graph.is_synchronized = True
    return graph


def test_subgraph_pickle_creation(symbol_graph_mocked_index):
    symbol_graph_mocked_index.default_rankable_subgraph

    with mock.patch("os.path.exists") as mock_exists:
        mock_exists.return_value = True
        assert os.path.exists(
            symbol_graph_mocked_index.subgraph_pickle_path
        ), f"No pickle file found at {symbol_graph_mocked_index.subgraph_pickle_path}"

        with mock.patch(
            "builtins.open",
            new_callable=mock.mock_open,
            read_data=pickle.dumps(nx.DiGraph()),
        ) as mock_open:
            with open(
                symbol_graph_mocked_index.subgraph_pickle_path, "rb"
            ) as f:
                pickled_subgraph = pickle.load(f)

    assert isinstance(pickled_subgraph, nx.DiGraph)
