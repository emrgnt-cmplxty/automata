import logging
import logging.config

from automata.config import GITHUB_API_KEY, REPOSITORY_NAME, TASK_DB_PATH
from automata.core.base.github_manager import GitHubManager
from automata.core.tasks.automata_task_executor import (
    AutomataExecuteBehavior,
    TaskExecutor,
    TestExecuteBehavior,
)
from automata.core.tasks.automata_task_registry import AutomataTaskDatabase, AutomataTaskRegistry
from automata.core.tasks.task import AutomataTask
from automata.core.utils import get_logging_config

logger = logging.getLogger(__name__)


def reconfigure_logging(verbose: bool):
    """
    Configure the logging settings.

    :param verbose: Boolean, if True, set log level to DEBUG, else set to INFO.
    """
    logging_config = get_logging_config(log_level=logging.DEBUG if verbose else logging.INFO)
    logging.config.dictConfig(logging_config)

    # Set the logging level for the requests logger to WARNING
    requests_logger = logging.getLogger("urllib3")
    requests_logger.setLevel(logging.INFO)
    openai_logger = logging.getLogger("openai")
    openai_logger.setLevel(logging.INFO)


def check_input(kwargs):
    assert not (
        kwargs.get("instructions") is None and kwargs.get("session_id") is None
    ), "You must provide instructions for the agent if you are not providing a session_id."
    assert not (
        kwargs.get("instructions") and kwargs.get("session_id")
    ), "You must provide either instructions for the agent or a session_id."
    assert (
        "helper_agent_names" in kwargs
    ), "You must provide a list of helper agents, with field helper_agent_names."
    assert (
        "main_config_name" in kwargs
    ), "You must provide a main agent config name, with field main_config_name."


def initialize_task(kwargs) -> AutomataTask:
    """
    Create coordinator and agents based on the provided arguments.

    :param args: Parsed command line arguments.
    :return: AutomataTask instance.
    """
    check_input(kwargs)
    log_level = logging.DEBUG if kwargs.get("verbose") else logging.INFO
    logging.config.dictConfig(get_logging_config(log_level=log_level))

    github_manager = GitHubManager(access_token=GITHUB_API_KEY, remote_name=REPOSITORY_NAME)
    task_registry = AutomataTaskRegistry(AutomataTaskDatabase(TASK_DB_PATH), github_manager)
    executor = TaskExecutor(
        TestExecuteBehavior(),  # Execution does not occur here so a test instance is sufficient
        task_registry,
    )

    task = AutomataTask(**kwargs)

    executor.initialize_task(task)
    return task


def run(kwargs) -> None:
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


def main(kwargs):
    verbose = kwargs.pop("verbose")
    reconfigure_logging(verbose)
    task = initialize_task(kwargs)
    result = run(task_id=task.task_id)
    logger.info(f"Final Result = {result}")
    return result
