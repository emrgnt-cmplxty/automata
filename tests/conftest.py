import os
import random
import shutil
from typing import Any, Set
from unittest.mock import MagicMock

import numpy as np
import pytest

from automata.agent import AgentToolkitNames, OpenAIAutomataAgent
from automata.config import AgentConfigName, OpenAIAutomataAgentConfigBuilder
from automata.embedding import EmbeddingSimilarityCalculator
from automata.experimental.search import SymbolRankConfig, SymbolSearch
from automata.memory_store import SymbolCodeEmbeddingHandler
from automata.singletons.dependency_factory import dependency_factory
from automata.singletons.github_client import GitHubClient, RepositoryClient
from automata.symbol.graph.symbol_graph import SymbolGraph
from automata.symbol.parser import parse_symbol
from automata.tasks.agent_database import AutomataTaskRegistry
from automata.tasks.environment import AutomataTaskEnvironment
from automata.tasks.tasks import AutomataTask
from automata.tools.factory import AgentToolFactory


@pytest.fixture
def temp_output_vector_dir():
    """Creates a temporary output filename which is deleted after the test is run"""
    this_dir = os.path.dirname(os.path.abspath(__file__))
    filename = os.path.join(this_dir, "test_output_vec")
    yield filename
    try:
        if os.path.exists(filename):
            os.remove(filename)
    except OSError:
        pass

    # The TemporaryDirectory context manager should already clean up the directory,
    # but just in case it doesn't (e.g. due to an error), we'll try removing it manually as well.
    try:
        shutil.rmtree(filename + "/")
    except OSError:
        pass


@pytest.fixture
def temp_output_filename():
    """Creates a temporary output filename which is deleted after the test is run"""
    this_dir = os.path.dirname(os.path.abspath(__file__))
    filename = os.path.join(this_dir, "test_output.json")
    yield filename
    try:
        if os.path.exists(filename):
            os.remove(filename)
    except OSError:
        pass

    # The TemporaryDirectory context manager should already clean up the directory,
    # but just in case it doesn't (e.g. due to an error), we'll try removing it manually as well.
    try:
        shutil.rmtree(filename + "/")
    except OSError:
        pass


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
            "scip-python python automata v0.0.0 `config.automata_agent_config`/AutomataAgentConfig#description."
        ),
        # Symbol with a method with foreign argument
        parse_symbol(
            "scip-python python automata v0.0.0 `config.automata_agent_config`/AutomataAgentConfig#load().(config_name)"
        ),
        # Symbol with a locally defined object
        parse_symbol(
            "scip-python python automata v0.0.0 `core.tasks.automata_task_executor`/logger."
        ),
        # Symbol with a class object and class variable
        parse_symbol(
            "scip-python python automata v0.0.0 `config.automata_agent_config`/AutomataAgentConfig#verbose."
        ),
        # Symbol with a class method
        parse_symbol(
            "scip-python python automata v0.0.0 `evals.eval_helpers`/EvalAction#__init__().(action)"
        ),
        # Symbol with an object
        parse_symbol(
            "scip-python python automata v0.0.0 `core.agent.automata_agent_enums`/ActionIndicator#CODE."
        ),
        # Class Name
        parse_symbol(
            "scip-python python automata v0.0.0 `core.agent.automata_agent_enums`/ActionIndicator#"
        ),
        # Init
        parse_symbol(
            "scip-python python automata v0.0.0 `core.tools.base`/ToolNotFoundError#__init__()."
        ),
    ]

    return symbols


EXAMPLE_SYMBOL_PREFIX = (
    "scip-python python automata v0.0.0 `config.automata_agent_config`/"
)


@pytest.fixture
def mock_simple_method_symbols():
    """Returns a list of 100 mock symbols with a simple method"""
    return [
        parse_symbol(
            EXAMPLE_SYMBOL_PREFIX + str(random.random()) + "_uri_ex_method()."
        )
        for _ in range(100)
    ]


@pytest.fixture
def mock_simple_class_symbols():
    """Returns a list of 100 mock symbols with a simple class"""
    return [
        parse_symbol(
            EXAMPLE_SYMBOL_PREFIX + str(random.random()) + "_uri_ex_method#"
        )
        for _ in range(100)
    ]


@pytest.fixture
def mock_embedding():
    """Returns a random mock embedding vector"""
    return np.array([random.random() for _ in range(1024)])


@pytest.fixture
def symbol_graph_mock(mocker):
    """Mock a SymbolGraph object for cases where we don't need to test the graph itself"""
    return mocker.MagicMock(spec=SymbolGraph)


@pytest.fixture
def symbol_search(mocker, symbol_graph_mock):
    """Creates a SymbolSearch object with Mock dependencies for testing"""
    symbol_similarity_mock = mocker.MagicMock(
        spec=EmbeddingSimilarityCalculator
    )
    symbol_similarity_mock.embedding_handler = mocker.MagicMock(
        spec=SymbolCodeEmbeddingHandler
    )

    symbol_code_embedding_handler = mocker.MagicMock(
        spec=SymbolCodeEmbeddingHandler
    )

    symbol_rank_config_mock = mocker.MagicMock(spec=SymbolRankConfig)
    symbol_rank_config_mock.validate_config = mocker.MagicMock()

    return SymbolSearch(
        symbol_graph_mock,
        symbol_rank_config_mock,
        symbol_code_embedding_handler,
        symbol_similarity_mock,
    )


@pytest.fixture
def automata_agent_config_builder():
    config_name = AgentConfigName.TEST
    # We must mock the get method on the dependency factory at this location
    # Otherwise, the dependency factory will attempt to actually instantiate the dependencies
    import unittest.mock

    dependency_factory.get = unittest.mock.MagicMock(return_value=None)

    return OpenAIAutomataAgentConfigBuilder.from_name(config_name)


@pytest.fixture
def automata_agent(mocker, automata_agent_config_builder):
    """Creates a mock AutomataAgent object for testing"""

    llm_toolkits_list = ["context-oracle"]
    kwargs = {}

    dependencies: Set[Any] = set()
    for tool in llm_toolkits_list:
        for dependency_name, _ in AgentToolFactory.TOOLKIT_TYPE_TO_ARGS[
            AgentToolkitNames(tool)
        ]:
            dependencies.add(dependency_name)

    for dependency in dependencies:
        kwargs[dependency] = dependency_factory.get(dependency)
    tools = AgentToolFactory.build_tools(["context-oracle"], **kwargs)

    instructions = "Test instruction."

    return OpenAIAutomataAgent(
        instructions,
        config=automata_agent_config_builder.with_tools(tools)
        .with_stream(False)
        .with_system_template_formatter({})
        .build(),
    )


class MockRepositoryClient(RepositoryClient):
    def clone_repository(self, local_path: str):
        pass

    def create_branch(self, branch_name: str):
        pass

    def checkout_branch(self, repo_local_path: str, branch_name: str):
        pass

    def stage_all_changes(self, repo_local_path: str):
        pass

    def commit_and_push_changes(
        self, repo_local_path: str, branch_name: str, commit_message: str
    ):
        pass

    def create_pull_request(self, branch_name: str, title: str, body: str):
        pass

    def branch_exists(self, branch_name: str) -> bool:
        return False

    def fetch_issue(self, issue_number: int) -> Any:
        pass

    def merge_pull_request(
        self, pull_request_number: int, commit_message: str
    ) -> Any:
        pass


@pytest.fixture
def task():
    repo_manager = MockRepositoryClient()
    return AutomataTask(
        repo_manager,
        config_to_load=AgentConfigName.TEST.to_path(),
        generate_deterministic_id=False,
        instructions="This is a test.",
    )


@pytest.fixture
def environment():
    github_mock = MagicMock(spec=GitHubClient)
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
