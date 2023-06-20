import os
import random

import numpy as np
import pytest

from automata.config.agent_config_builder import AutomataAgentConfigBuilder
from automata.config.config_types import AgentConfigName, AutomataInstructionPayload
from automata.core.agent.agent import AutomataAgent
from automata.core.agent.tools.tool_utils import build_llm_toolkits
from automata.core.coding.py_coding.retriever import PyCodeRetriever
from automata.core.embedding.code_embedding import SymbolCodeEmbeddingHandler
from automata.core.embedding.symbol_similarity import SymbolSimilarity
from automata.core.symbol.graph import SymbolGraph
from automata.core.symbol.parser import parse_symbol
from automata.core.symbol.search.rank import SymbolRankConfig
from automata.core.symbol.search.symbol_search import SymbolSearch


@pytest.fixture
def temp_output_filename():
    """Creates a temporary output filename which is deleted after the test is run"""
    this_dir = os.path.dirname(os.path.abspath(__file__))
    filename = os.path.join(this_dir, "test_output.json")
    yield filename
    if os.path.exists(filename):
        os.remove(filename)


@pytest.fixture
def symbols():
    """
    Mock several realistic symbols for testing

    Note:
        These symbols at one point reflected existing code
        but they are not guaranteed to be up to date.
    """
    symbols = [
        # Symbol with a simple attribute
        parse_symbol(
            "scip-python python automata 75482692a6fe30c72db516201a6f47d9fb4af065 `config.automata_agent_config`/AutomataAgentConfig#description."
        ),
        # Symbol with a method with foreign argument
        parse_symbol(
            "scip-python python automata 75482692a6fe30c72db516201a6f47d9fb4af065 `config.automata_agent_config`/AutomataAgentConfig#load().(config_name)"
        ),
        # Symbol with a locally defined object
        parse_symbol(
            "scip-python python automata 75482692a6fe30c72db516201a6f47d9fb4af065 `core.tasks.automata_task_executor`/logger."
        ),
        # Symbol with a class object and class variable
        parse_symbol(
            "scip-python python automata 75482692a6fe30c72db516201a6f47d9fb4af065 `config.automata_agent_config`/AutomataAgentConfig#verbose."
        ),
        # Symbol with a class method
        parse_symbol(
            "scip-python python automata 75482692a6fe30c72db516201a6f47d9fb4af065 `evals.eval_helpers`/EvalAction#__init__().(action)"
        ),
        # Symbol with an object
        parse_symbol(
            "scip-python python automata 75482692a6fe30c72db516201a6f47d9fb4af065 `core.agent.automata_agent_enums`/ActionIndicator#CODE."
        ),
        # Class Name
        parse_symbol(
            "scip-python python automata 75482692a6fe30c72db516201a6f47d9fb4af065 `core.agent.automata_agent_enums`/ActionIndicator#"
        ),
        # Init
        parse_symbol(
            "scip-python python automata 75482692a6fe30c72db516201a6f47d9fb4af065 `core.base.tool`/ToolNotFoundError#__init__()."
        ),
    ]

    return symbols


EXAMPLE_SYMBOL_PREFIX = "scip-python python automata 75482692a6fe30c72db516201a6f47d9fb4af065 `config.automata_agent_config`/"


@pytest.fixture
def mock_simple_method_symbols():
    """Returns a list of 100 mock symbols with a simple method"""
    return [
        parse_symbol(EXAMPLE_SYMBOL_PREFIX + str(random.random()) + "_uri_ex_method().")
        for _ in range(100)
    ]


@pytest.fixture
def mock_simple_class_symbols():
    """Returns a list of 100 mock symbols with a simple class"""
    return [
        parse_symbol(EXAMPLE_SYMBOL_PREFIX + str(random.random()) + "_uri_ex_method#")
        for _ in range(100)
    ]


@pytest.fixture
def mock_embedding():
    """Returns a random mock embedding vector"""
    return np.array([random.random() for _ in range(1024)])


@pytest.fixture
def symbol_graph_mock(mocker):
    """Mock a SymbolGraph object for cases where we don't need to test the graph itself"""
    mock = mocker.MagicMock(spec=SymbolGraph)
    return mock


@pytest.fixture
def symbol_searcher(mocker, symbol_graph_mock):
    """Creates a SymbolSearch object with Mock dependencies for testing"""
    symbol_similarity_mock = mocker.MagicMock(spec=SymbolSimilarity)
    symbol_similarity_mock.embedding_handler = mocker.MagicMock(spec=SymbolCodeEmbeddingHandler)
    symbol_rank_config_mock = mocker.MagicMock(spec=SymbolRankConfig)
    code_subgraph_mock = mocker.MagicMock(spec=SymbolGraph.SubGraph)
    code_subgraph_mock.parent = symbol_graph_mock
    code_subgraph_mock.graph = mocker.MagicMock()

    return SymbolSearch(
        symbol_graph_mock, symbol_similarity_mock, symbol_rank_config_mock, code_subgraph_mock
    )


@pytest.fixture
def automata_agent_config_builder():
    config_name = AgentConfigName.TEST
    agent_config_builder = AutomataAgentConfigBuilder.from_name(config_name)
    return agent_config_builder


@pytest.fixture
def automata_agent(mocker, automata_agent_config_builder):
    """Creates a mock AutomataAgent object for testing"""
    tool_list = ["py_retriever"]
    mock_llm_toolkits = build_llm_toolkits(
        tool_list, py_retriever=mocker.MagicMock(spec=PyCodeRetriever)
    )

    instruction_payload = AutomataInstructionPayload(agents_message="", overview="", tools="")

    instructions = "Test instruction."

    agent = AutomataAgent(
        instructions,
        config=automata_agent_config_builder.with_instruction_payload(instruction_payload)
        .with_llm_toolkits(mock_llm_toolkits)
        .with_stream(False)
        .build(),
    )
    agent.setup()
    return agent
