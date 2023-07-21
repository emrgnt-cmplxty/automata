import os
from unittest.mock import MagicMock, patch

import pytest

from automata.agent import OpenAIAutomataAgent
from automata.core.utils import get_root_fpath
from automata.llm import LLMChatMessage
from automata.memory_store import OpenAIAutomataConversationDatabase
from automata.singletons.py_module_loader import py_module_loader
from automata.tasks.base import Task, TaskStatus
from automata.tasks.executor import (
    AutomataTaskExecutor,
    IAutomataTaskExecution,
    ITaskExecution,
)


@pytest.fixture(scope="module", autouse=True)
def db(tmpdir_factory):
    db_file = tmpdir_factory.mktemp("data").join("test.db")
    db = OpenAIAutomataConversationDatabase(str(db_file))
    yield db
    db.close()
    if os.path.exists(str(db_file)):
        os.remove(str(db_file))


mock_message = MagicMock(spec=LLMChatMessage)
mock_message.role = "assistant"
mock_message.content = "Hello, world!"

mock_agent = MagicMock(spec=OpenAIAutomataAgent)
mock_agent.run.return_value = "Test result"


class TestExecuteBehavior(ITaskExecution):
    """
    Class for executing test tasks.
    """

    def execute(self, task: Task):
        print("in the test execute method")
        task.result = mock_agent.run()


@pytest.fixture(autouse=True)
def module_loader():
    # FIXME - This can't be a good pattern, let's cleanup later.
    py_module_loader.reset()
    py_module_loader.initialize(get_root_fpath())
    yield py_module_loader


@pytest.fixture
def patch_logging(mocker):
    return mocker.patch("logging.config.dictConfig", return_value=None)


def test_agent_session_id_matches_task(automata_agent, task_w_agent_session):
    assert automata_agent.session_id == task_w_agent_session.session_id


def test_execute_automata_task_success(
    patch_logging, module_loader, task, environment, registry
):
    registry.register(task)
    environment.setup(task)

    execution = TestExecuteBehavior()
    task_executor = AutomataTaskExecutor(execution)

    result = task_executor.execute(task)

    assert task.status == TaskStatus.SUCCESS
    assert task.result == "Test result"
    assert result is None


def test_execute_automata_task_fail(
    patch_logging, module_loader, task, environment, registry
):
    registry.register(task)
    environment.setup(task)

    execution = MagicMock(spec=TestExecuteBehavior())
    task_executor = AutomataTaskExecutor(execution)
    task_executor.execution.execute.side_effect = Exception("Execution failed")

    with pytest.raises(Exception, match="Execution failed"):
        task_executor.execute(task)

    assert task.status == TaskStatus.FAILED
    assert task.error == "Execution failed"


def mock_openai_response_with_completion_message():
    return {
        "choices": [
            {
                "message": {
                    "role": "assistant",
                    "function_call": {
                        "name": "call_termination",
                        "arguments": '{"result": "Success"}',
                    },
                    "content": None,
                }
            }
        ]
    }


@pytest.mark.parametrize(
    "api_response", [mock_openai_response_with_completion_message()]
)
@patch("openai.ChatCompletion.create")
def test_execute_automata_task_with_database_saving(
    mock_openai_chatcompletion_create,
    api_response,
    db,
    automata_agent,
    task,
    environment,
    registry,
):
    # Mock the API response
    mock_openai_chatcompletion_create.return_value = api_response

    # Create a task and set record_conversation to True
    registry.register(task)
    environment.setup(task)

    automata_agent.set_database_provider(db)

    # Execute the task
    execution = IAutomataTaskExecution()
    IAutomataTaskExecution._build_agent = MagicMock(
        return_value=automata_agent
    )
    task_executor = AutomataTaskExecutor(execution)
    task_executor.execute(task)

    assert task.status == TaskStatus.SUCCESS
    assert task.result == "Execution Result:\n\nSuccess"

    saved_messages = db.get_messages(automata_agent.session_id)
    assert len(saved_messages) == 2
