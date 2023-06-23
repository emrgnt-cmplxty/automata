import logging
import logging.config
import time
from abc import ABC, abstractmethod

from automata.core.agent.task.registry import AutomataTaskRegistry
from automata.core.agent.task.task import AutomataTask, TaskStatus
from automata.core.coding.py_coding.module_tree import LazyModuleTreeMap

logger = logging.getLogger(__name__)


class IExecuteBehavior(ABC):
    """
    Interface for executing different types of tasks.
    """

    @abstractmethod
    def execute(self, task: "AutomataTask"):
        pass


class AutomataExecuteBehavior(IExecuteBehavior):
    """
    Class for executing general tasks.
    """

    def execute(self, task: AutomataTask):
        task.status = TaskStatus.RUNNING
        try:
            result = task.build_agent().run()
            task.result = result
            task.status = TaskStatus.SUCCESS
        except Exception as e:
            logger.exception(f"AutomataTask failed: {e}")
            task.error = str(e)
            task.status = TaskStatus.FAILED
            task.retry_count += 1
            raise


class TestExecuteBehavior(IExecuteBehavior):
    """
    Class for executing test tasks.
    """

    def execute(self, task: AutomataTask):
        import os
        import shutil

        from automata.core.coding.py_coding.retriever import PyCodeRetriever
        from automata.core.coding.py_coding.writer import PyCodeWriter
        from automata.core.utils import root_fpath

        logger.debug("Running a test execution...")
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
        shutil.rmtree(os.path.join(root_fpath(), task.path_to_root_py))


class TaskExecutor:
    """
    Class for executing tasks using different behaviors.
    """

    def __init__(self, execute_behavior: IExecuteBehavior, task_registry: AutomataTaskRegistry):
        self.execute_behavior = execute_behavior
        self.task_registry = task_registry

    def initialize_task(self, task: AutomataTask):
        self.task_registry.initialize_task(task)

    def execute(self, task: AutomataTask):
        """
        Executes the task using the specified behavior.
        """
        task.validate_pending()
        for attempt in range(task.max_retries):
            try:
                logger.debug(f"Executing task {task.task_id}")
                task.status = TaskStatus.RUNNING
                self.execute_behavior.execute(task)

                logger.debug("Task executed successfully")
                task.status = TaskStatus.SUCCESS

            except Exception as e:
                logging.exception(f"AutomataTask failed: {e}")
                task.status = TaskStatus.RETRYING
                task.error = str(e)

                # If we've used up all retries, re-raise the exception
                if attempt == task.max_retries - 1:
                    raise e

                # Otherwise, wait before retrying
                time.sleep(self._exponential_backoff(attempt))

    @staticmethod
    def _exponential_backoff(attempt_number: int) -> int:
        """
        Waits for a specified amount of time before retrying the task
        """
        return 2**attempt_number  # Exponential backoff in seconds
