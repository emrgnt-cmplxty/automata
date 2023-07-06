from unittest.mock import MagicMock, patch

import pytest

from automata.core.code_handling.py.reader import PyReader
from automata.core.code_handling.py.writer import PyWriter
from automata.core.singletons.py_module_loader import py_module_loader
from automata.core.tasks.base import Task, TaskStatus
from automata.core.tasks.executor import AutomataTaskExecutor, ITaskExecution
from automata.core.utils import get_root_py_fpath


# TODO - Unify module loader fixture
@pytest.fixture(autouse=True)
def module_loader():
    py_module_loader.initialize(get_root_py_fpath())
    yield py_module_loader
    py_module_loader._dotpath_map = None
    py_module_loader.initialized = False
    py_module_loader.py_fpath = None
    py_module_loader.root_fpath = None


class TestExecuteBehavior(ITaskExecution):
    """
    Class for executing test tasks.
    """

    def execute(self, task: Task):
        import os

        retriever = PyReader()
        writer = PyWriter(retriever)

        # Create a new module
        writer.create_new_module(
            module_dotpath="core.agent.test_agent",
            source_code="def test123(x): return True",
            do_write=True,
        )
        task.result = "Test result"

        # Cleanup the new output file
        os.remove(os.path.join(get_root_py_fpath(), "core", "agent", "test_agent.py"))


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
