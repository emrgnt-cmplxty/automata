import os
import random
import shutil
import uuid
from typing import Any, Dict, Generator, List, Set
from unittest.mock import MagicMock

import numpy as np
import pytest

from automata.agent import AgentToolkitNames, OpenAIAutomataAgent
from automata.config import AgentConfigName, OpenAIAutomataAgentConfigBuilder
from automata.embedding import EmbeddingSimilarityCalculator
from automata.eval import (
    AgentEvaluationHarness,
    CodeWritingEval,
    OpenAIFunctionEval,
    SymbolSearchEval,
    ToolEvaluationHarness,
)
from automata.eval.agent.agent_eval_composite import AgentEvalComposite
from automata.eval.agent.agent_eval_database import AgentEvalResultDatabase
from automata.experimental.search import SymbolRankConfig, SymbolSearch
from automata.experimental.tools import AgentifiedSearchToolkitBuilder
from automata.llm import FunctionCall
from automata.memory_store import (
    OpenAIAutomataConversationDatabase,
    SymbolCodeEmbeddingHandler,
)
from automata.singletons.dependency_factory import dependency_factory
from automata.singletons.github_client import GitHubClient
from automata.symbol import Symbol, SymbolGraph, parse_symbol
from automata.symbol_embedding import (
    ChromaSymbolEmbeddingVectorDatabase,
    JSONSymbolEmbeddingVectorDatabase,
    SymbolCodeEmbedding,
    SymbolDocEmbedding,
)
from automata.tasks import (
    AutomataAgentTaskDatabase,
    AutomataTask,
    AutomataTaskEnvironment,
    AutomataTaskExecutor,
    AutomataTaskRegistry,
    IAutomataTaskExecution,
)
from automata.tools import Tool, ToolExecution, ToolExecutor
from automata.tools.agent_tool_factory import AgentToolFactory

# General Fixtures


@pytest.fixture
def temp_output_dir() -> Generator:
    """Creates a temporary output filename which is deleted after the test is run"""
    this_dir = os.path.dirname(os.path.abspath(__file__))
    filename = os.path.join(this_dir, "test_output_vec")
    if not os.path.exists(filename):
        os.mkdir(filename)
    yield filename
    try:
        if os.path.exists(filename):
            os.remove(filename)
    except OSError:
        pass

    # The TemporaryDirectory context manager should already clean up the directory,
    # but just in case it doesn't (e.g. due to an error), we'll try removing it manually as well.
    try:
        shutil.rmtree(f"{filename}/")
    except OSError:
        pass


@pytest.fixture
def temp_output_filename(temp_output_dir: str) -> str:
    """Creates a temporary output filename which is deleted after the test is run"""
    return os.path.join(temp_output_dir, "test_output.json")


# `Symbol` Fixtures


EXAMPLE_SYMBOL_PREFIX = (
    "scip-python python automata v0.0.0 `config.automata_agent_config`/"
)


@pytest.fixture
def symbols() -> List[Symbol]:
    """
    Mock several realistic symbols for testing

    Note:
        These symbols at one point reflected existing code
        but they are not guaranteed to be up to date.
    """
    return [
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


@pytest.fixture
def mock_simple_method_symbols() -> List[Symbol]:
    """Returns a list of 100 mock symbols with a simple method"""
    return [
        parse_symbol(
            EXAMPLE_SYMBOL_PREFIX + str(random.random()) + "_uri_ex_method()."
        )
        for _ in range(100)
    ]


# `Embedding` Fixtures


# Parameterized fixture for embedding type
@pytest.fixture(params=[SymbolCodeEmbedding, SymbolDocEmbedding])
def embedding_type(request):
    return request.param


@pytest.fixture(params=[0, 1])
def embedded_symbol(symbols, request):
    data = [("x", [1, 2, 3]), ("y", [1, 2, 3, 4])][request.param]
    return SymbolCodeEmbedding(symbols[request.param], data[0], data[1])


@pytest.fixture
def mock_embedding():
    """Returns a random mock embedding vector"""
    return np.array([random.random() for _ in range(1024)])


# Factory fixture for creating embeddings
@pytest.fixture
def embedding_maker(embedding_type):
    def _make_embedding(symbol, document, vector):
        if embedding_type == SymbolDocEmbedding:
            # Add extra fields for SymbolDocEmbedding
            return embedding_type(
                symbol,
                document,
                vector,
                source_code="some code",
                summary="summary",
                context="context",
            )
        else:
            return embedding_type(symbol, document, vector)

    return _make_embedding


# Advanced `Symbol` structures


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


# Database Fixtures


@pytest.fixture
def json_vector_db(
    tmpdir_factory,
) -> Generator[JSONSymbolEmbeddingVectorDatabase, Any, Any]:
    """Creates a JSONSymbolEmbeddingVectorDatabase object for testing"""
    db_file = tmpdir_factory.mktemp("data").join("test_json.db")
    yield JSONSymbolEmbeddingVectorDatabase(str(db_file))
    if os.path.exists(str(db_file)):
        os.remove(str(db_file))


CHROMA_COLLECTION_NAME = "a_test_chroma_collection"


@pytest.fixture
def chroma_vector_db(embedding_type) -> ChromaSymbolEmbeddingVectorDatabase:
    """Creates a in-memory Chroma Symbol database for testing"""
    return ChromaSymbolEmbeddingVectorDatabase(
        CHROMA_COLLECTION_NAME, factory=embedding_type.from_args
    )


@pytest.fixture
def chroma_vector_db_persistent(
    embedding_type,
    tmpdir_factory,
) -> Generator[ChromaSymbolEmbeddingVectorDatabase, Any, Any]:
    db_file = tmpdir_factory.mktemp("data").join("test_json.db")
    db_dir = os.path.dirname(str(db_file))
    """Creates a persistent Chroma Symbol database for testing"""
    yield ChromaSymbolEmbeddingVectorDatabase(
        CHROMA_COLLECTION_NAME,
        factory=embedding_type.from_args,
        persist_directory=db_dir,
    )
    if os.path.exists(str(db_file)):
        os.remove(str(db_file))


@pytest.fixture
def conversation_db(
    tmpdir_factory,
) -> Generator[OpenAIAutomataConversationDatabase, Any, Any]:
    db_file = tmpdir_factory.mktemp("data").join("test_conversation.db")
    db = OpenAIAutomataConversationDatabase(str(db_file))
    yield db
    db.close()
    if os.path.exists(str(db_file)):
        os.remove(str(db_file))


@pytest.fixture
def task_db(tmpdir_factory) -> Generator[AutomataAgentTaskDatabase, Any, Any]:
    db_file = tmpdir_factory.mktemp("data").join("test_task.db")
    db = AutomataAgentTaskDatabase(str(db_file))
    yield db
    db.close()
    if os.path.exists(str(db_file)):
        os.remove(str(db_file))


@pytest.fixture
def eval_db(tmpdir_factory) -> Generator[AgentEvalResultDatabase, Any, Any]:
    db_file = tmpdir_factory.mktemp("data").join("test_eval.db")
    db = AgentEvalResultDatabase(str(db_file))
    yield db
    db.close()
    if os.path.exists(str(db_file)):
        os.remove(str(db_file))


# `Agent` Fixtures


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

    llm_toolkits_list = ["advanced-context-oracle"]
    dependencies: Set[Any] = set()
    for tool in llm_toolkits_list:
        for dependency_name, _ in AgentToolFactory.TOOLKIT_TYPE_TO_ARGS[
            AgentToolkitNames(tool)
        ]:
            dependencies.add(dependency_name)

    kwargs = {
        dependency: dependency_factory.get(dependency)
        for dependency in dependencies
    }
    tools = AgentToolFactory.build_tools(["advanced-context-oracle"], **kwargs)

    instructions = "Test instruction."

    return OpenAIAutomataAgent(
        instructions,
        config=automata_agent_config_builder.with_tools(tools)
        .with_stream(False)
        .with_system_template_formatter({})
        .build(),
    )


# `Task` Fixtures


@pytest.fixture
def tasks():
    repo_manager = MagicMock()
    task_0 = AutomataTask(
        repo_manager,
        # session_id = automata_agent.session_id,
        config_to_load=AgentConfigName.TEST.to_path(),
        instructions="This is a test.",
        session_id=str(uuid.uuid4()),
    )

    task_1 = AutomataTask(
        repo_manager,
        # session_id = automata_agent.session_id,
        config_to_load=AgentConfigName.TEST.to_path(),
        instructions="This is a test2.",
    )
    return [task_0, task_1]


@pytest.fixture
def task_w_agent_matched_session(automata_agent):
    repo_manager = MagicMock()
    return AutomataTask(
        repo_manager,
        session_id=automata_agent.session_id,
        config_to_load=AgentConfigName.TEST.to_path(),
        instructions="This is a test.",
    )


@pytest.fixture
def task_environment():
    github_mock = MagicMock(spec=GitHubClient)
    return AutomataTaskEnvironment(github_mock)


@pytest.fixture
def task_registry(task_db):
    return AutomataTaskRegistry(task_db)


# `Eval` Fixtures


@pytest.fixture
def function_evaluator():
    return OpenAIFunctionEval()


@pytest.fixture
def code_evaluator():
    return CodeWritingEval(target_variables=["x", "y", "z"])


@pytest.fixture
def search_evaluator():
    return SymbolSearchEval()


@pytest.fixture
def composite_evaluator(function_evaluator, code_evaluator):
    evaluators = [function_evaluator, code_evaluator]
    return AgentEvalComposite(evaluators)


@pytest.fixture
def agent_eval_harness(function_evaluator, code_evaluator):
    database = MagicMock()
    return AgentEvaluationHarness(
        [function_evaluator, code_evaluator], database
    )


@pytest.fixture
def tool_eval_harness(search_evaluator):
    return ToolEvaluationHarness([search_evaluator])


@pytest.fixture
def setup(
    mocker,
    automata_agent,
    tasks,
    task_environment,
    task_registry,
    conversation_db,
):
    # Mock the API response
    mock_openai_chatcompletion_create = mocker.patch(
        "openai.ChatCompletion.create"
    )

    task_0, task_1 = tasks
    # Register and setup task
    task_registry.register(task_0)
    task_environment.setup(task_0)

    task_registry.register(task_1)
    task_environment.setup(task_1)

    # Use the agent's set_database_provider method
    automata_agent.set_database_provider(conversation_db)

    execution = IAutomataTaskExecution()
    IAutomataTaskExecution._build_agent = MagicMock(
        return_value=automata_agent
    )
    task_executor = AutomataTaskExecutor(execution)

    return mock_openai_chatcompletion_create, automata_agent, task_executor


@pytest.fixture
def matched_setup(
    mocker,
    automata_agent,
    task_w_agent_matched_session,
    task_environment,
    task_registry,
    conversation_db,
):
    # Mock the API response
    mock_openai_chatcompletion_create = mocker.patch(
        "openai.ChatCompletion.create"
    )

    # Register and setup task
    task_registry.register(task_w_agent_matched_session)
    task_environment.setup(task_w_agent_matched_session)

    # Use the agent's set_database_provider method
    automata_agent.set_database_provider(conversation_db)

    execution = IAutomataTaskExecution()
    IAutomataTaskExecution._build_agent = MagicMock(
        return_value=automata_agent
    )
    task_executor = AutomataTaskExecutor(execution)

    return (
        mock_openai_chatcompletion_create,
        automata_agent,
        task_executor,
        task_registry,
    )


# `Tool` Fixtures


class TestTool(Tool):
    def run(self, tool_input: Dict[str, str]) -> str:
        return "TestTool response"


@pytest.fixture
def test_tool(request) -> TestTool:
    name = request.node.get_closest_marker("tool_name")
    description = request.node.get_closest_marker("tool_description")
    function = request.node.get_closest_marker("tool_function")

    return TestTool(
        name=name.args[0] if name else "TestTool",
        description=description.args[0]
        if description
        else "A test tool for testing purposes",
        function=function.args[0]
        if function
        else (lambda x: "TestTool response"),
    )


@pytest.mark.tool_name("TestTool")
@pytest.mark.tool_description("A test tool for testing purposes")
def test_tool_instantiation(test_tool: TestTool) -> None:
    """Test that the TestTool class can be instantiated."""
    assert test_tool.name == "TestTool"
    assert test_tool.description == "A test tool for testing purposes"
    assert test_tool.function is not None


@pytest.fixture
def function_call() -> FunctionCall:
    return FunctionCall(name="TestTool", arguments={"test": "test"})


@pytest.fixture
def tool_execution(test_tool) -> ToolExecution:
    return ToolExecution([test_tool])


@pytest.fixture
def tool_executor(tool_execution) -> ToolExecutor:
    return ToolExecutor(tool_execution)


@pytest.fixture
def setup_tool(mocker, symbols):
    # Mock the API response

    # Create a mock for the SymbolSearch instance
    symbol_search_mock = MagicMock()

    symbol_0 = symbols[0]
    symbol_1 = symbols[1]
    symbol_2 = symbols[2]

    # Mock the get_symbol_rank_results method
    symbol_search_mock.get_symbol_rank_results = MagicMock(
        return_value=[
            (symbol_0, 0.3),
            (symbol_1, 0.2),
            (symbol_2, 0.1),
            (symbols[3], 0.01),  # pad to top k (5)
            (symbols[4], 0.01),
        ]
    )

    # Create tools using the factory
    symbol_search_tools = AgentToolFactory.create_tools_from_builder(
        AgentToolkitNames.SYMBOL_SEARCH, symbol_search=symbol_search_mock
    )

    # Create the tool execution instance with the tools
    tool_execution = ToolExecution(symbol_search_tools)

    return ToolExecutor(execution=tool_execution)


@pytest.fixture
def agentified_search_tool_builder(symbols):
    """Returns an agentified search tool builder mock"""
    symbol_search_mock = MagicMock(spec=SymbolSearch)
    symbol_doc_embedding_handler_mock = MagicMock()
    completion_provider_mock = MagicMock()

    # set the return value on the symbol_search_mock
    symbol_search_mock.get_symbol_code_similarity_results = MagicMock(
        return_value=[(symbols[0], 1), (symbols[1], 0.8), (symbols[2], 0.6)]
    )

    agentified_search_tool_builder = AgentifiedSearchToolkitBuilder(
        symbol_search=symbol_search_mock,
        symbol_doc_embedding_handler=symbol_doc_embedding_handler_mock,
        completion_provider=completion_provider_mock,
    )
    agentified_search_tool_builder.completion_provider.standalone_call = (
        MagicMock(return_value=symbols[1].dotpath)
    )

    return agentified_search_tool_builder
