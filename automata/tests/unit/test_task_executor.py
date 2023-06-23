import os
import uuid
from unittest.mock import MagicMock, PropertyMock, patch

import pytest

from automata.config.config_types import AgentConfigName
from automata.core.agent.task.executor import (
    AutomataTaskExecutor,
    IAutomataTaskExecution,
    ITaskExecution,
)
from automata.core.agent.task.task import AutomataTask
from automata.core.base.task import TaskStatus
from automata.core.coding.py_coding.module_tree import LazyModuleTreeMap
from automata.core.coding.py_coding.retriever import PyCodeRetriever
from automata.core.coding.py_coding.writer import PyCodeWriter
from automata.core.utils import root_fpath

from ..conftest import MockRepositoryManager


class TestExecuteBehavior(ITaskExecution):
    """
    Class for executing test tasks.
    """

    def execute(self, task: AutomataTask):
        import os
        import shutil

        if not isinstance(task.path_to_root_py, str):
            raise TypeError("A relative python path must be set for the test executor.")

        module_map = LazyModuleTreeMap(task.path_to_root_py)
        retriever = PyCodeRetriever(module_map)
        writer = PyCodeWriter(retriever)

        # Create a new module
        writer.create_new_module(
            module_dotpath="automata.core.agent.agent",
            source_code="def test123(x): return True",
            do_write=True,
        )
        task.result = "Test result"

        # Cleanup the new output file
        # if os.path.exists(task.path_to_root_py):
        # shutil.rmtree(os.path.join(root_fpath(), task.path_to_root_py))


# @patch("logging.config.dictConfig", return_value=None)
# def test_execute_automata_task_success(_, task, environment, registry):
#     registry.register(task)
#     environment.setup(task)

#     execution = TestExecuteBehavior()
#     task_executor = AutomataTaskExecutor(execution)

#     result = task_executor.execute(task)

#     assert task.status == TaskStatus.SUCCESS
#     assert task.result == "Success"
#     assert result is None


# @patch("logging.config.dictConfig", return_value=None)
# def test_execute_test_task_success(task):
#     execution = TestExecuteBehavior()
#     task_registry = MagicMock()
#     task_executor = AutomataTaskExecutor(execution)

#     task_executor.initialize_task(task)
#     task.status = TaskStatus.PENDING
#     task.path_to_root_py = "test_path"
#     result = task_executor.execute(task)

#     assert task.status == TaskStatus.SUCCESS
#     assert result is None


# @patch("logging.config.dictConfig", return_value=None)
# def test_execute_automata_task_fail(task):
#     execution = IAutomataTaskExecution()
#     task_registry = MagicMock()
#     task_executor = AutomataTaskExecutor(execution)

#     task_executor.initialize_task(task)
#     task.status = TaskStatus.PENDING
#     task.build_agent.return_value.run.side_effect = Exception("Execution failed")
#     task.max_retries = 2

#     with pytest.raises(Exception, match="Execution failed"):
#         task_executor.execute(task)

#     assert task.status == TaskStatus.RETRYING
#     assert task.error == "Execution failed"
