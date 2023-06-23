from unittest.mock import MagicMock, patch

import pytest

from automata.core.agent.task.executor import AutomataTaskExecutor, ITaskExecution
from automata.core.base.task import Task, TaskStatus
from automata.core.coding.py.module_loader import ModuleLoader
from automata.core.coding.py.reader import PyReader
from automata.core.coding.py.writer import PyWriter
from automata.core.utils import root_py_fpath


class TestExecuteBehavior(ITaskExecution):
    """
    Class for executing test tasks.
    """

    def execute(self, task: Task):
        import os

        module_loader = ModuleLoader(root_py_fpath())
        retriever = PyReader(module_loader)
        writer = PyWriter(retriever)

        # Create a new module
        writer.create_new_module(
            module_dotpath="core.agent.test_agent",
            source_code="def test123(x): return True",
            do_write=True,
        )
        task.result = "Test result"

        # Cleanup the new output file
        os.remove(os.path.join(root_py_fpath(), "core", "agent", "test_agent.py"))


@patch("logging.config.dictConfig", return_value=None)
def test_execute_automata_task_success(_, task, environment, registry):
    registry.register(task)
    environment.setup(task)

    execution = TestExecuteBehavior()
    task_executor = AutomataTaskExecutor(execution)

    result = task_executor.execute(task)

    assert task.status == TaskStatus.SUCCESS
    assert task.result == "Test result"
    assert result is None


@patch("logging.config.dictConfig", return_value=None)
def test_execute_automata_task_fail(_, task, environment, registry):
    registry.register(task)
    environment.setup(task)

    execution = MagicMock(spec=TestExecuteBehavior())
    task_executor = AutomataTaskExecutor(execution)
    task_executor.execution.execute.side_effect = Exception("Execution failed")

    with pytest.raises(Exception, match="Execution failed"):
        task_executor.execute(task)

    assert task.status == TaskStatus.FAILED
    assert task.error == "Execution failed"
