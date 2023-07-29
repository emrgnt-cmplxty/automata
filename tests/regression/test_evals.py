# TODO - Agent tests should depend on actions for verification, not specific output
import logging

import pytest

from automata.core.run_handlers import run_setup, run_with_eval
from automata.eval import OpenAIFunctionCallAction
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
def test_basic_eval_task(
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
