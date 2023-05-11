import logging
import logging.config

from automata.cli.cli_utils import process_kwargs
from automata.config import DEFAULT_REMOTE_URL, GITHUB_API_KEY, TASK_DB_NAME
from automata.core.base.github_manager import GitHubManager
from automata.core.tasks.task import AutomataTask
from automata.core.tasks.task_executor import (
    AutomataExecuteBehavior,
    TaskExecutor,
    TestExecuteBehavior,
)
from automata.core.tasks.task_registry import AutomataTaskDatabase, TaskRegistry
from automata.core.utils import get_logging_config

logger = logging.getLogger(__name__)


def configure_logging(verbose: bool):
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


def run(kwargs):
    """
    Create coordinator and agents based on the provided arguments.

    :param args: Parsed command line arguments.
    :return: Tuple containing the AutomataCoordinator and instruction_payload.
    """

    check_input(kwargs)
    kwargs = process_kwargs(**kwargs)

    logging.config.dictConfig(get_logging_config())

    github_manager = GitHubManager(access_token=GITHUB_API_KEY, remote_url=DEFAULT_REMOTE_URL)
    task_registry = TaskRegistry(AutomataTaskDatabase(TASK_DB_NAME), github_manager)
    executor = TaskExecutor(
        TestExecuteBehavior() if kwargs.get("is_test", None) else AutomataExecuteBehavior(),
        task_registry,
    )

    task = AutomataTask(**kwargs)

    executor.initialize_task(task)
    executor.execute(task)

    tasks = task_registry.get_all_tasks()
    for task in tasks:
        print("Task = ", task)


def main(kwargs):
    verbose = kwargs.pop("verbose")
    configure_logging(verbose)

    result = run(kwargs)
    logger.info(f"Final Result = {result}")
    return result
