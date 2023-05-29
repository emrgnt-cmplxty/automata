import os
from unittest.mock import Mock

import pytest

from automata.core.search.symbol_graph import SymbolGraph
from automata.core.search.symbol_parser import parse_symbol
from automata.core.search.symbol_rank.symbol_embedding_map import SymbolEmbeddingMap
from automata.core.search.symbol_rank.symbol_rank import SymbolRankConfig
from automata.core.search.symbol_rank.symbol_similarity import SymbolSimilarity
from automata.tools.search.symbol_searcher import SymbolSearcher


@pytest.fixture
def symbols():
    symbols = [
        # Symbol with a simple attribute
        parse_symbol(
            "scip-python python automata 75482692a6fe30c72db516201a6f47d9fb4af065 `automata.configs.automata_agent_configs`/AutomataAgentConfig#description."
        ),
        # Symbol with a method with foreign argument
        parse_symbol(
            "scip-python python automata 75482692a6fe30c72db516201a6f47d9fb4af065 `automata.configs.automata_agent_configs`/AutomataAgentConfig#load().(config_name)"
        ),
        # Symbol with a class method, self as argument
        parse_symbol(
            "scip-python python automata 75482692a6fe30c72db516201a6f47d9fb4af065 `automata.tools.python_tools.python_ast_indexer`/PythonASTIndexer#get_module_path().(self)"
        ),
        # Symbol with a locally defined object
        parse_symbol(
            "scip-python python automata 75482692a6fe30c72db516201a6f47d9fb4af065 `automata.core.tasks.automata_task_executor`/logger."
        ),
        # Symbol with a class object and class variable
        parse_symbol(
            "scip-python python automata 75482692a6fe30c72db516201a6f47d9fb4af065 `automata.configs.automata_agent_configs`/AutomataAgentConfig#verbose."
        ),
        # Symbol with a function in a module
        # parse_symbol("scip-python python automata 75482692a6fe30c72db516201a6f47d9fb4af065 `automata.core.coordinator.tests.test_automata_coordinator`/test().(coordinator)"),
        # Symbol with a class method
        parse_symbol(
            "scip-python python automata 75482692a6fe30c72db516201a6f47d9fb4af065 `automata.evals.eval_helpers`/EvalAction#__init__().(action)"
        ),
        # Symbol with an object
        parse_symbol(
            "scip-python python automata 75482692a6fe30c72db516201a6f47d9fb4af065 `automata.core.agent.automata_agent_enums`/ActionIndicator#CODE."
        ),
        # Class Name
        parse_symbol(
            "scip-python python automata 75482692a6fe30c72db516201a6f47d9fb4af065 `automata.core.agent.automata_agent_enums`/ActionIndicator#"
        ),
        # Init
        parse_symbol(
            "scip-python python automata 75482692a6fe30c72db516201a6f47d9fb4af065 `automata.core.base.tool`/ToolNotFoundError#__init__()."
        ),
    ]

    return symbols


@pytest.fixture
def symbol_graph():
    # assuming the path to a valid index protobuf file, you should replace it with your own file path
    file_dir = os.path.dirname(os.path.abspath(__file__))
    index_path = os.path.join(file_dir, "index.scip")
    graph = SymbolGraph(index_path)
    return graph


@pytest.fixture
def symbol_graph_mock(mocker):
    mock = mocker.MagicMock(spec=SymbolGraph)
    return mock


@pytest.fixture
def symbol_searcher(mocker, symbol_graph_mock):
    symbol_embedding_mock = mocker.MagicMock(spec=SymbolEmbeddingMap)
    symbol_similarity_mock = mocker.MagicMock(spec=SymbolSimilarity)
    symbol_rank_config_mock = mocker.MagicMock(spec=SymbolRankConfig)

    return SymbolSearcher(
        symbol_graph_mock,
        symbol_embedding_mock,
        symbol_similarity_mock,
        symbol_rank_config_mock,
    )


def get_sem(monkeypatch, mock_symbols, build_new_embedding_map=False):
    monkeypatch.setattr(
        "automata.core.search.symbol_utils.convert_to_fst_object", lambda args: "symbol_source"
    )
    return SymbolEmbeddingMap(
        # Symbols with kind 'Method' are processed, 'Local' are skipped
        all_defined_symbols=mock_symbols,
        build_new_embedding_map=build_new_embedding_map,
    )


def patch_get_embedding(monkeypatch, mock_embedding):
    # Define the behavior of the mock get_embedding function
    mock_get_embedding = Mock(return_value=mock_embedding)
    monkeypatch.setattr("openai.embeddings_utils.get_embedding", mock_get_embedding)
