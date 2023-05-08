import logging
import logging.config
import os
from abc import ABC, abstractmethod
from typing import Optional

from retrying import retry

from automata.core.task.task import AutomataTask, TaskStatus
from automata.core.utils import get_logging_config

logger = logging.getLogger(__name__)
logging.config.dictConfig(get_logging_config())


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
            result = task.agent.run()
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

        if not isinstance(task.rel_py_path, str):
            raise TypeError("A relative python path must be set for the test executor.")

        if not isinstance(task.task_dir, str):
            raise TypeError("A task directory must be set for the test executor.")

        indexer = PythonIndexer(os.path.join(task.task_dir, task.rel_py_path))
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

    def __init__(self, execute_behavior: IExecuteBehavior):
        self.execute_behavior = execute_behavior

    def exponential_backoff(self, retry_state):
        """
        Waits for a specified amount of time before retrying the task
        """
        return (2**retry_state.attempt_number) * 1000  # Exponential backoff in milliseconds

    @retry(
        retry_on_exception=lambda e: isinstance(e, Exception),
        wait_func=exponential_backoff,
        stop_max_attempt_number=lambda self: self.max_retries,
    )
    def execute(self, task: AutomataTask) -> Optional[str]:
        """
        Executes the task using the specified behavior.
        """
        if task.status != TaskStatus.PENDING:
            raise ValueError("Task must be in pending state to be executed.")

        try:
            task.status = TaskStatus.RUNNING
            execution_result = self.execute_behavior.execute(task)
            task.status = TaskStatus.SUCCESS
            logger.info("Task executed successfully")
            return execution_result
        except Exception as e:
            logging.exception(f"AutomataTask failed: {e}")
            task.error = str(e)
            task.retry_count += 1
            if task.retry_count == task.max_retries:
                task.status = TaskStatus.FAILED
                logger.error("Task failed with max retries, with a final exception: %s", e)

            raise e


if __name__ == "__main__":
    import random

    from automata.config import DEFAULT_REMOTE_URL, GITHUB_API_KEY
    from automata.configs.automata_agent_configs import AutomataAgentConfig
    from automata.configs.config_enums import AgentConfigVersion
    from automata.core.agent.automata_agent_helpers import create_instruction_payload
    from automata.core.base.github_manager import GitHubManager

    github_manager = GitHubManager(access_token=GITHUB_API_KEY, remote_url=DEFAULT_REMOTE_URL)
    executor = TaskExecutor(TestExecuteBehavior())

    instruction_payload = create_instruction_payload(overview="Overview", agents_message="Message")
    task = AutomataTask(
        agent_config=AutomataAgentConfig.load(AgentConfigVersion.AUTOMATA_INDEXER_DEV),
        llm_toolkits="",
        model="gpt-4",
        instruction_payload=instruction_payload,
        stream=True,
        github_manager=github_manager,
        rel_py_path="automata",
    )
    task.create_task_env()
    executor.execute(task)

    rand_branch = random.randint(0, 100000)

    task.commit_task(
        commit_message="This is a commit message",
        pull_title="This is a test",
        pull_body="I am testing this...",
        pull_branch_name="test_branch_%s" % (rand_branch),
    )
