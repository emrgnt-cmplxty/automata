import logging
import logging.config
import os
import time
from abc import ABC, abstractmethod
from typing import Optional

from automata.core.tasks.task import AutomataTask, TaskStatus
from automata.core.tasks.task_registry import TaskRegistry

logger = logging.getLogger(__name__)


class IExecuteBehavior(ABC):
    """
    Interface for executing different types of tasks.
    """

    @abstractmethod
    def execute(self, task: "AutomataTask") -> Optional[str]:
        pass


class AutomataExecuteBehavior(IExecuteBehavior):
    """
    Class for executing general tasks.
    """

    def execute(self, task: AutomataTask) -> Optional[str]:
        task.status = TaskStatus.RUNNING
        try:
            result = task.builder.build().run()
            task.result = result
            task.status = TaskStatus.SUCCESS
        except Exception as e:
            logger.exception(f"AutomataTask failed: {e}")
            task.error = str(e)
            task.status = TaskStatus.FAILED
            task.retry_count += 1
            raise

        return task.result


class TestExecuteBehavior(IExecuteBehavior):
    """
    Class for executing test tasks.
    """

    def execute(self, task: AutomataTask) -> Optional[str]:
        from automata.tools.python_tools.python_indexer import PythonIndexer
        from automata.tools.python_tools.python_writer import PythonWriter

        logger.info("Running a test execution...")
        if not isinstance(task.rel_py_path, str):
            raise TypeError("A relative python path must be set for the test executor.")

        indexer = PythonIndexer(os.path.join(task.task_dir, task.rel_py_path))  # type: ignore
        writer = PythonWriter(indexer)
        writer.update_module(
            module_path="core.agent.automata_agent",
            source_code="def test123(x): return True",
            write_to_disk=True,
        )
        return None


class TaskExecutor:
    """
    Class for executing tasks using different behaviors.
    """

    def __init__(self, execute_behavior: IExecuteBehavior, task_registry: TaskRegistry):
        self.execute_behavior = execute_behavior
        self.task_registry = task_registry

    def initialize_task(self, task: AutomataTask):
        self.task_registry.initialize_task(task)

    def execute(self, task: AutomataTask) -> Optional[str]:
        """
        Executes the task using the specified behavior.
        """
        if task.status != TaskStatus.PENDING:
            raise ValueError("Task must be in pending state to be executed.")

        if task.task_dir is None:
            raise ValueError("Task must have a task_dir set to be executed.")

        for attempt in range(task.max_retries):
            try:
                logger.info("Executing task %s", task.task_id)
                task.status = TaskStatus.RUNNING
                execution_result = self.execute_behavior.execute(task)

                logger.info("Task executed successfully")
                task.status = TaskStatus.SUCCESS

                return execution_result
            except Exception as e:
                logging.exception(f"AutomataTask failed: {e}")
                task.status = TaskStatus.RETRYING
                task.error = str(e)

                # If we've used up all retries, re-raise the exception
                if attempt == task.max_retries - 1:
                    raise e

                # Otherwise, wait before retrying
                time.sleep(self._exponential_backoff(attempt))
        return None

    @staticmethod
    def _exponential_backoff(attempt_number: int) -> int:
        """
        Waits for a specified amount of time before retrying the task
        """
        return 2**attempt_number  # Exponential backoff in seconds


if __name__ == "__main__":
    import random

    from automata.config import DEFAULT_REMOTE_URL, GITHUB_API_KEY, TASK_DB_NAME
    from automata.configs.automata_agent_configs import AutomataAgentConfig
    from automata.configs.config_enums import AgentConfigVersion
    from automata.core.agent.automata_agent_helpers import create_instruction_payload
    from automata.core.base.github_manager import GitHubManager
    from automata.core.tasks.task_registry import AutomataTaskDatabase
    from automata.core.utils import get_logging_config

    logging.config.dictConfig(get_logging_config())

    github_manager = GitHubManager(access_token=GITHUB_API_KEY, remote_url=DEFAULT_REMOTE_URL)
    task_registry = TaskRegistry(AutomataTaskDatabase(TASK_DB_NAME), github_manager)
    executor = TaskExecutor(TestExecuteBehavior(), task_registry)

    agent_config = AutomataAgentConfig.load(AgentConfigVersion.AUTOMATA_INDEXER_DEV)
    instruction_payload = create_instruction_payload(overview="Overview", agents_message="Message")
    task = AutomataTask(
        agent_config=agent_config,
        llm_toolkits="",
        instruction_payload=instruction_payload,
        stream=True,
        rel_py_path="automata",
    )

    executor.initialize_task(task)
    executor.execute(task)

    rand_branch = random.randint(0, 100000)
    task_registry.commit_task(
        task,
        github_manager=github_manager,
        commit_message="This is a commit message",
        pull_title="This is a test",
        pull_body="I am testing this...",
        pull_branch_name="test_branch_%s" % (rand_branch),
    )
    tasks = task_registry.get_all_tasks()
    for task in tasks:
        print("Task = ", task)
