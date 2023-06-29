import os
import random
from typing import Any, Set
from unittest.mock import MagicMock

import numpy as np
import pytest

from automata.config.base import AgentConfigName
from automata.config.openai_agent import AutomataOpenAIAgentConfigBuilder
from automata.core.agent.providers import OpenAIAutomataAgent
from automata.core.agent.task.environment import AutomataTaskEnvironment
from automata.core.agent.task.registry import AutomataTaskRegistry
from automata.core.agent.task.task import AutomataTask
from automata.core.agent.tool.tool_utils import AgentToolFactory, dependency_factory
from automata.core.base.agent import AgentToolProviders
from automata.core.base.github_manager import GitHubManager, RepositoryManager
from automata.core.embedding.code_embedding import SymbolCodeEmbeddingHandler
from automata.core.embedding.symbol_similarity import SymbolSimilarityCalculator
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
def symbol_search(mocker, symbol_graph_mock):
    """Creates a SymbolSearch object with Mock dependencies for testing"""
    symbol_similarity_mock = mocker.MagicMock(spec=SymbolSimilarityCalculator)
    symbol_similarity_mock.embedding_handler = mocker.MagicMock(spec=SymbolCodeEmbeddingHandler)
    symbol_rank_config_mock = mocker.MagicMock(spec=SymbolRankConfig)
    code_subgraph_mock = mocker.MagicMock(spec=SymbolGraph.SubGraph)
    code_subgraph_mock.parent = symbol_graph_mock
    code_subgraph_mock.graph = mocker.MagicMock()

    return SymbolSearch(
        symbol_graph_mock,
        symbol_similarity_mock,
        symbol_rank_config_mock,
        code_subgraph_mock,
    )


@pytest.fixture
def automata_agent_config_builder():
    config_name = AgentConfigName.TEST
    # We must mock the get method on the dependency factory at this location
    # Otherwise, the dependency factory will attempt to actually instantiate the dependencies
    import unittest.mock

    from automata.core.agent.tool.tool_utils import dependency_factory

    dependency_factory.get = unittest.mock.MagicMock(return_value=None)

    return AutomataOpenAIAgentConfigBuilder.from_name(config_name)


@pytest.fixture
def automata_agent(mocker, automata_agent_config_builder):
    """Creates a mock AutomataAgent object for testing"""

    llm_toolkits_list = ["py-reader"]
    kwargs = {}

    dependencies: Set[Any] = set()
    for tool in llm_toolkits_list:
        for dependency_name, _ in AgentToolFactory.TOOLKIT_TYPE_TO_ARGS[AgentToolProviders(tool)]:
            dependencies.add(dependency_name)

    for dependency in dependencies:
        kwargs[dependency] = dependency_factory.get(dependency)
    tools = AgentToolFactory.build_tools(["py-reader"], **kwargs)

    instructions = "Test instruction."

    return OpenAIAutomataAgent(
        instructions,
        config=automata_agent_config_builder.with_tools(tools)
        .with_stream(False)
        .with_system_template_formatter({})
        .build(),
    )


class MockRepositoryManager(RepositoryManager):
    def clone_repository(self, local_path: str):
        pass

    def create_branch(self, branch_name: str):
        pass

    def checkout_branch(self, repo_local_path: str, branch_name: str):
        pass

    def stage_all_changes(self, repo_local_path: str):
        pass

    def commit_and_push_changes(self, repo_local_path: str, branch_name: str, commit_message: str):
        pass

    def create_pull_request(self, branch_name: str, title: str, body: str):
        pass

    def branch_exists(self, branch_name: str) -> bool:
        return False

    def fetch_issue(self, issue_number: int) -> Any:
        pass


@pytest.fixture
def task():
    repo_manager = MockRepositoryManager()
    return AutomataTask(
        repo_manager,
        config_to_load=AgentConfigName.TEST.value,
        generate_deterministic_id=False,
        instructions="This is a test.",
    )


@pytest.fixture
def environment():
    github_mock = MagicMock(spec=GitHubManager)
    return AutomataTaskEnvironment(github_mock)


@pytest.fixture
def registry(task):
    def mock_get_tasks_by_query(query, params):
        if params[0] == task.task_id:
            return [task]
        else:
            return []

    db = MagicMock()
    db.get_tasks_by_query.side_effect = (
        mock_get_tasks_by_query  # Assigning the side_effect attribute
    )
    registry = AutomataTaskRegistry(db)
    return registry
