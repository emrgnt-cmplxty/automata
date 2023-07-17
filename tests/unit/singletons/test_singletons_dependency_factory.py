from unittest.mock import MagicMock, patch

import networkx as nx
import pytest

from automata.agent.error import AgentGeneralError
from automata.experimental.search import SymbolSearch
from automata.singletons.dependency_factory import DependencyFactory


@pytest.fixture
def dependency_factory():
    return DependencyFactory()


@patch("automata.symbol.graph.SymbolGraph.__init__", return_value=None)
def test_create_symbol_graph(mock_init, dependency_factory):
    symbol_graph = dependency_factory.create_symbol_graph()
    assert symbol_graph is not None
    mock_init.assert_called_once()


@patch.object(DependencyFactory, "get")
def test_create_symbol_search(mock_get, dependency_factory):
    mock_get.return_value = MagicMock()
    symbol_search = dependency_factory.create_symbol_search()
    assert symbol_search is not None
    assert isinstance(symbol_search, SymbolSearch)


@pytest.mark.skip("This test works only when in isolation from the other test")
def test_get_with_override(dependency_factory):
    override = MagicMock()
    dependency_factory.set_overrides(symbol_graph=override)
    symbol_graph = dependency_factory.get("symbol_graph")
    assert symbol_graph == override


def test_create_subgraph_is_instance(dependency_factory):
    mock_symbol_graph = MagicMock()
    mock_symbol_graph.default_rankable_subgraph = nx.DiGraph()
    dependency_factory.get = MagicMock(return_value=mock_symbol_graph)
    subgraph = dependency_factory.create_subgraph()
    dependency_factory.get.assert_called_once_with("symbol_graph")
    assert mock_symbol_graph.default_rankable_subgraph == subgraph
    assert isinstance(subgraph, nx.DiGraph)


@patch("automata.experimental.search.SymbolRank.__init__", return_value=None)
def test_create_symbol_rank(mock_init, dependency_factory):
    symbol_rank = dependency_factory.create_symbol_rank()
    assert symbol_rank is not None
    mock_init.assert_called_once()


@patch(
    "automata.memory_store.SymbolCodeEmbeddingHandler.__init__",
    return_value=None,
)
def test_create_symbol_code_embedding_handler(mock_init, dependency_factory):
    symbol_code_embedding_handler = (
        dependency_factory.create_symbol_code_embedding_handler()
    )
    assert symbol_code_embedding_handler is not None
    mock_init.assert_called_once()


@patch(
    "automata.memory_store.SymbolDocEmbeddingHandler.__init__",
    return_value=None,
)
def test_create_symbol_doc_embedding_handler(mock_init, dependency_factory):
    symbol_doc_embedding_handler = (
        dependency_factory.create_symbol_doc_embedding_handler()
    )
    assert symbol_doc_embedding_handler is not None
    mock_init.assert_called_once()


def test_set_overrides_raises_exception(dependency_factory):
    dependency_factory._class_cache = {"some_key": "some_value"}
    with pytest.raises(AgentGeneralError):
        dependency_factory.set_overrides(some_dependency=MagicMock())


# Test for reset method
def test_reset(dependency_factory):
    dependency_factory._class_cache = {"some_key": "some_value"}
    dependency_factory._instances = {"another_key": "another_value"}
    dependency_factory.overrides = {"yet_another_key": "yet_another_value"}

    dependency_factory.reset()

    assert not dependency_factory._class_cache
    assert not dependency_factory._instances
    assert not dependency_factory.overrides
