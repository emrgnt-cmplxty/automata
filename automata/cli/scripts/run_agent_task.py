import logging
import logging.config
from typing import Any, List, Set

from automata.config import GITHUB_API_KEY, REPOSITORY_NAME, TASK_DB_PATH
from automata.core.agent.task.environment import AutomataTaskEnvironment
from automata.core.agent.task.executor import (
    AutomataTaskExecutor,
    IAutomataTaskExecution,
)
from automata.core.agent.task.registry import AutomataTaskDatabase, AutomataTaskRegistry
from automata.core.agent.task.task import AutomataTask
from automata.core.agent.tools.tool_utils import AgentToolFactory, DependencyFactory
from automata.core.base.github_manager import GitHubManager
from automata.core.base.task import TaskStatus
from automata.core.base.tool import ToolkitType

logger = logging.getLogger(__name__)

DEFAULT_ISSUES_PROMPT = """Provide an explanation and code snippets (in Markdown) which address the Github issue(s) that follow. You may use the context oracle (multiple times if necessary) to ensure that you have proper context to answer this question. Solve the GitHub issues by writing the relevant code via the PyWriter tool. The issues begin now:"""


def process_issues(issue_numbers: List[int], github_manager: GitHubManager) -> List[str]:
    """
    Process the issues and create tasks for each of them.

    Args:
        issue_numbers: The issue numbers to process.
    """
    issue_infos = []
    for issue_number in issue_numbers:
        issue = github_manager.fetch_issue(issue_number)
        if not issue:
            raise ValueError(f"Could not fetch issue #{issue_number}.")

        issue_info = f"Issue #{issue.number}: {issue.title}\n{issue.body}"
        issue_infos.append(issue_info)

    if not issue_infos:
        raise ValueError("No valid issues provided.")

    return issue_infos


def main(*args, **kwargs):
    github_manager = GitHubManager(access_token=GITHUB_API_KEY, remote_name=REPOSITORY_NAME)

    # Pre-process issues if they are passsed
    issue_numbers = kwargs.get("fetch_issues", "")
    issue_numbers = list(map(int, issue_numbers.split(","))) if issue_numbers else []
    if len(issue_numbers):
        issue_infos = process_issues(issue_numbers, github_manager)
        # Concatenate instructions and issue information
        kwargs["instructions"] = kwargs.get("instructions") or DEFAULT_ISSUES_PROMPT + "\n".join(
            issue_infos
        )

    llm_toolkits_list = kwargs.get("llm_toolkits", "context_oracle").split(",")
    # TODO - The following is a copy pasta from automata/cli/scripts/run_agent.py
    # Where should this reside to avoid redundancy?

    # A list of all dependencies that will be used to build the toolkits
    dependencies: Set[Any] = set()
    for tool in llm_toolkits_list:
        for dependency_name, _ in AgentToolFactory.TOOLKIT_TYPE_TO_ARGS[ToolkitType(tool)]:
            dependencies.add(dependency_name)

    logger.info("  - Building dependencies...")
    for dependency in dependencies:
        logger.info(f"Building {dependency}...")
        kwargs[dependency] = DependencyFactory().get(dependency)

    task = AutomataTask(**kwargs)  # TaskStatus = CREATED
    # Register the task with the task registry
    task_registry = AutomataTaskRegistry(AutomataTaskDatabase(TASK_DB_PATH))
    task_registry.register(task)  # TaskStatus = REGISTERED

    # Setup task environment
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

    # # TODO - Consider best practice for committing the task to Github
    # # TODO - Consider best practice for logging the task
    # # TODO - Consider best practice for cleaning up the task
