# TODO - Agent tests should depend on actions for verification, not specific output
import logging
import random

import pytest

from automata.cli.commands import reconfigure_logging
from automata.core.run_handlers import run_setup, run_with_eval
from automata.eval import OpenAIFunctionCallAction, SymbolSearchEvalResult
from automata.eval.agent.agent_eval_database import AgentEvalResultDatabase
from automata.llm import OpenAIEmbeddingProvider
from automata.memory_store import OpenAIAutomataConversationDatabase
from automata.tasks import (
    AutomataAgentTaskDatabase,
    AutomataTaskEnvironment,
    AutomataTaskRegistry,
    EnvironmentMode,
    TaskStatus,
)

logger = logging.getLogger(__name__)

EMBEDDING_PROVIDER = OpenAIEmbeddingProvider()
BASIC_PARAMS = (
    "instructions, agent_config, toolkit_list, model, max_iterations"
)

ADVANCED_PARAMS = f"{BASIC_PARAMS}, expected_actions"


@pytest.fixture
def automata_setup():
    task_db = AutomataAgentTaskDatabase()
    task_registry = AutomataTaskRegistry(task_db)
    task_environment = AutomataTaskEnvironment(
        environment_mode=EnvironmentMode.LOCAL_COPY
    )

    return task_db, task_registry, task_environment


@pytest.mark.regression
@pytest.mark.parametrize(
    f"{BASIC_PARAMS}",
    [
        (
            "This is a dummy instruction, return True.",
            "automata-main",
            [],  # no tool necessary, default agent has a stop execution fn.
            "gpt-3.5-turbo-16k",
            1,
        ),
    ],
)
def test_basic_eval_tasks(
    instructions,
    agent_config,
    toolkit_list,
    model,
    max_iterations,
    automata_setup,
):
    """Test that the agent can execute a simple instruction."""

    tools, agent_config_name = run_setup(agent_config, toolkit_list)

    task_db, task_registry, task_environment = automata_setup

    eval_result = run_with_eval(
        instructions,
        agent_config_name,
        tools,
        model,
        max_iterations,
        task_registry,
        task_environment,
    )

    assert eval_result.session_id is not None
    assert eval_result.is_full_match is True
    assert eval_result.match_results == {}
    assert eval_result.extra_actions == [
        OpenAIFunctionCallAction(
            name="call_termination", arguments={"result": "True"}
        )
    ]

    eval_db = AgentEvalResultDatabase()
    eval_db.write_result(eval_result)

    session_id = eval_result.session_id

    eval_write_results = eval_db.get_results(session_id)
    assert len(eval_write_results) == 1
    eval_write_result = eval_write_results[0]
    assert eval_write_result.session_id == session_id

    # Check that task is saved correctly to the task_registry / db
    lookup_task = task_registry.fetch_task_by_id(session_id)
    assert eval_result.session_id == lookup_task.session_id
    assert lookup_task.status == TaskStatus.SUCCESS

    conversation_db = OpenAIAutomataConversationDatabase()
    messages = conversation_db.get_messages(session_id)
    assert len(messages) == 7


random_suffix = random.randint(0, 1000000)


@pytest.mark.regression
@pytest.mark.parametrize(
    f"{ADVANCED_PARAMS}",
    [
        (
            "This is a dummy instruction, return True.",
            "automata-main",
            [],  # no tool necessary, default agent has a stop execution fn.
            "gpt-3.5-turbo-16k",
            2,
            [
                OpenAIFunctionCallAction(
                    name="call_termination", arguments={"result": "True"}
                )
            ],
        ),
        (
            "Fetch the source code for symbol search",
            "automata-main",
            ["agent-search"],
            "gpt-4",
            2,
            [
                OpenAIFunctionCallAction(
                    name="search-best-match-code",
                    arguments={"query": "symbol search"},
                )
            ],
        ),
        (
            "Fetch the source code for VectorDatabaseProvider.",
            "automata-main",
            ["py-reader"],
            "gpt-4",
            2,
            [
                OpenAIFunctionCallAction(
                    name="retrieve-code",
                    arguments={
                        "module_path": "automata.core.base.database.vector_database",
                        "node_path": "VectorDatabaseProvider",
                    },
                )
            ],
        ),
        (
            f"Create a new module with the method ```python\ndef f(x):\n    return x**2``` in automata.test_module_{random_suffix}",
            "automata-main",
            ["py-writer"],
            "gpt-4",
            2,
            [
                OpenAIFunctionCallAction(
                    name="create-new-module",
                    arguments={
                        "module_dotpath": f"automata.test_module_{random_suffix}",
                        "code": "def f(x):\n    return x**2",
                    },
                )
            ],
        ),
    ],
)
def test_action_based_eval_tasks(
    instructions,
    agent_config,
    toolkit_list,
    model,
    max_iterations,
    expected_actions,
    automata_setup,
):
    """Test that the agent can execute a simple instruction."""
    reconfigure_logging("DEBUG")
    tools, agent_config_name = run_setup(agent_config, toolkit_list)

    _, task_registry, task_environment = automata_setup

    eval_result = run_with_eval(
        instructions,
        agent_config_name,
        tools,
        model,
        max_iterations,
        task_registry,
        task_environment,
        expected_actions=expected_actions,
    )
    # sourcery skip: no-conditionals-in-tests
    if not eval_result.is_full_match:
        if isinstance(eval_result, SymbolSearchEvalResult):
            raise ValueError(
                f"Expected actions did not match actual actions for eval result. Found matches {eval_result.match_results} and extra actions {eval_result.extra_actions}."
            )
        else:
            raise ValueError("Found error ")
