from unittest.mock import MagicMock, patch

import pytest

from automata.core.utils import get_root_py_fpath
from automata.singletons.pyast_module_loader import pyast_module_loader
from automata.tasks.base import Task, TaskStatus
from automata.tasks.executor import AutomataTaskExecutor, ITaskExecution


# TODO - Unify module loader fixture
@pytest.fixture(autouse=True)
def module_loader():
    pyast_module_loader.initialize(get_root_py_fpath())
    yield pyast_module_loader
    pyast_module_loader._dotpath_map = None
    pyast_module_loader.initialized = False
    pyast_module_loader.py_fpath = None
    pyast_module_loader.root_fpath = None


class TestExecuteBehavior(ITaskExecution):
    """
    Class for executing test tasks.
    """

    def execute(self, task: Task):
        task.result = "Test result"


@patch("logging.config.dictConfig", return_value=None)
def test_execute_automata_task_success(_, module_loader, task, environment, registry):
    registry.register(task)
    environment.setup(task)

    execution = TestExecuteBehavior()
    task_executor = AutomataTaskExecutor(execution)

    result = task_executor.execute(task)

    assert task.status == TaskStatus.SUCCESS
    assert task.result == "Test result"
    assert result is None


@patch("logging.config.dictConfig", return_value=None)
def test_execute_automata_task_fail(_, module_loader, task, environment, registry):
    registry.register(task)
    environment.setup(task)

    execution = MagicMock(spec=TestExecuteBehavior())
    task_executor = AutomataTaskExecutor(execution)
    task_executor.execution.execute.side_effect = Exception("Execution failed")

    with pytest.raises(Exception, match="Execution failed"):
        task_executor.execute(task)

    assert task.status == TaskStatus.FAILED
    assert task.error == "Execution failed"
