import logging
import logging.config

from automata.config import GITHUB_API_KEY, REPOSITORY_NAME, TASK_DB_PATH
from automata.core.agent.task.environment import AutomataTaskEnvironment
from automata.core.agent.task.executor import (
    AutomataTaskExecutor,
    IAutomataTaskExecution,
)
from automata.core.agent.task.registry import AutomataTaskDatabase, AutomataTaskRegistry
from automata.core.agent.task.task import AutomataTask
from automata.core.base.github_manager import GitHubManager
from automata.core.base.task import TaskStatus

logger = logging.getLogger(__name__)


def main(*args, **kwargs):
    task = AutomataTask(**kwargs)  # TaskStatus = CREATED

    # Register the task with the task registry
    task_registry = AutomataTaskRegistry(AutomataTaskDatabase(TASK_DB_PATH))
    task_registry.register(task)  # TaskStatus = REGISTERED

    # Setup task environment
    github_manager = GitHubManager(access_token=GITHUB_API_KEY, remote_name=REPOSITORY_NAME)
    task_env = AutomataTaskEnvironment(github_manager)
    task_env.setup(task)  # TaskStatus = PENDING

    # Create an executor and run the task
    executor = AutomataTaskExecutor(IAutomataTaskExecution())
    try:
        executor.execute(task)  # TaskStatus = SUCCESS
    except Exception as e:
        logger.exception(f"Task failed: {e}")
        task.error = str(e)
        task.status = TaskStatus.FAILED

    # TODO - Consider best practice for committing the task to Github
    # TODO - Consider best practice for logging the task
    # TODO - Consider best practice for cleaning up the task
