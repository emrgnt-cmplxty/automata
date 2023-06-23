import logging
import logging.config

from automata.config import GITHUB_API_KEY, REPOSITORY_NAME, TASK_DB_PATH
from automata.core.agent.task.executor import (
    AutomataExecuteBehavior,
    TaskExecutor,
    TestExecuteBehavior,
)
from automata.core.agent.task.registry import AutomataTaskDatabase, AutomataTaskRegistry
from automata.core.agent.task.task import AutomataTask
from automata.core.base.github_manager import GitHubManager

logger = logging.getLogger(__name__)


def initialize_task(*args, **kwargs) -> AutomataTask:
    """
    Initialize a new AutomataTask with the provided kwargs.
    """

    github_manager = GitHubManager(access_token=GITHUB_API_KEY, remote_name=REPOSITORY_NAME)
    task_registry = AutomataTaskRegistry(AutomataTaskDatabase(TASK_DB_PATH), github_manager)

    task = AutomataTask(**kwargs)
    task_registry.initialize_task(task)

    return task


def run(*args, **kwargs) -> None:
    """
    Run the provided task.

    :param task_id: ID of the initialized AutomataTask.
    """
    github_manager = GitHubManager(access_token=GITHUB_API_KEY, remote_name=REPOSITORY_NAME)
    task_registry = AutomataTaskRegistry(AutomataTaskDatabase(TASK_DB_PATH), github_manager)
    executor = TaskExecutor(
        TestExecuteBehavior() if kwargs.get("is_test", None) else AutomataExecuteBehavior(),
        task_registry,
    )
    if not kwargs.get("task_id"):
        raise ValueError("You must provide a task_id.")
    task_id = kwargs.pop("task_id")
    task = task_registry.get_task_by_id(task_id)
    if task is None:
        raise ValueError(f"Task with id {task_id} does not exist.")
    executor.execute(task)


def main(*args, **kwargs):
    initialize_task(**kwargs)
    # task = initialize_task(**kwargs)
    # result = run(task_id=task.task_id)
    # logger.info(f"Final Result = {result}")
    # return result
