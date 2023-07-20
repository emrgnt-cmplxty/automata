from unittest.mock import MagicMock, patch

import pytest
from pytest_mock import MockerFixture
from automata.core.utils import get_root_fpath
from automata.singletons.py_module_loader import py_module_loader
from automata.tasks.base import Task, TaskStatus
from automata.tasks.executor import (
    AutomataTaskExecutor,
    ITaskExecution,
    IAutomataTaskExecution,
)
from automata.llm import LLMChatMessage
from automata.agent import OpenAIAutomataAgent

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
