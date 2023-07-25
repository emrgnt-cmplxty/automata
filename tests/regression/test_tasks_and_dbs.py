# TODO - Agent tests should depend on actions for verification, not specific output
import logging

import pytest

from automata.core.run_handlers import run_setup, run_with_task
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
CORE_PARAMS = "instructions, agent_config, toolkit_list, model, max_iterations"


@pytest.mark.regression
@pytest.mark.parametrize(
    f"{CORE_PARAMS}",
    [
        # A simple 'hello-world' style instruction with task framework
        (
            "This is a dummy instruction, return True.",
            "automata-main",
            [],
            "gpt-3.5-turbo-16k",
            1,
        ),
    ],
)
def test_basic_task_execution(
    instructions,
    agent_config,
    toolkit_list,
    model,
    max_iterations,
):
    """Test that the agent can execute a simple instruction."""

    tools, agent_config_name = run_setup(agent_config, toolkit_list)

    task_db = AutomataAgentTaskDatabase()
    task_registry = AutomataTaskRegistry(task_db)
    task_environment = AutomataTaskEnvironment(
        environment_mode=EnvironmentMode.LOCAL_COPY
    )

    task = run_with_task(
        instructions,
        agent_config_name,
        tools,
        model,
        max_iterations,
        task_registry,
        task_environment,
    )

    session_id = str(task.session_id)

    # Check that task is saved correctly to the registry / db
    lookup_task = task_registry.fetch_task_by_id(session_id)
    assert task.session_id == lookup_task.session_id
    assert task.instructions == lookup_task.instructions
    assert task.status == lookup_task.status
    assert task.status == TaskStatus.SUCCESS

    conversation_db = OpenAIAutomataConversationDatabase()
    messages = conversation_db.get_messages(session_id)
    assert len(messages) == 7
    # TODO - Are there any other checks we want to hard-code on the messages?
