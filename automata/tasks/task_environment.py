import logging
import logging.config
import os
import shutil
from enum import Enum
from typing import Optional

from automata.core.utils import get_root_py_fpath
from automata.singletons.github_client import GitHubClient
from automata.singletons.py_module_loader import py_module_loader
from automata.tasks.automata_task import AutomataTask
from automata.tasks.task_base import Task, TaskEnvironment, TaskStatus
from automata.tasks.task_error import TaskGeneralError, TaskStateError

logger = logging.getLogger(__name__)


class EnvironmentMode(Enum):
    GITHUB = "github"
    LOCAL_COPY = "local_copy"


class AutomataTaskEnvironment(TaskEnvironment):
    """A concrete implementation of the Abstract TaskEnvironment for Automata providers."""

    # TODO - We should make it clearer what happens when a github client is not passed
    # e.g. there should be an associated enum at initialization or some such which
    # specifies how the task environment is created.
    def __init__(
        self,
        github_manager: Optional[GitHubClient] = None,
        environment_mode: EnvironmentMode = EnvironmentMode.GITHUB,
    ) -> None:
        if environment_mode == EnvironmentMode.GITHUB and not github_manager:
            raise ValueError(
                f"Invalid arguments, github_manager must not be None if environment_mode={EnvironmentMode.GITHUB}"
            )
        self.environment_mode = environment_mode
        self.github_manager = github_manager

    def setup(self, task: Task) -> None:
        """
        Set up the environment by cloning the repository into the task directory.
        Further, set the task status to PENDING.

        Raises:
            Exception: If the task is not status CREATED.
        """

        if task.status != TaskStatus.REGISTERED:
            raise TaskStateError(
                f"Cannot setup task environment because task is not in REGISTERED state. Task status = {task.status}"
            )
        if not isinstance(task, AutomataTask):
            raise TaskGeneralError(
                "AutomataTaskEnvironment requires an AutomataTask instance"
            )

        logger.debug(
            f"Setting up the task environment in directory {task.task_dir}."
        )
        # TODO - Consider more methods for environment initlization than git clone
        if self.environment_mode == EnvironmentMode.GITHUB:
            # TODO - How can I avoid this and type ignores elsewhere?
            self.github_manager.clone_repository(task.task_dir)  # type: ignore
        else:
            # copy automata directory into task directory
            # TODO - Add tests for local env standup
            shutil.copytree(
                get_root_py_fpath(),
                os.path.join(task.task_dir, py_module_loader.project_name),
            )

        task.status = TaskStatus.PENDING
        logger.info(f"Task {task.session_id} environment setup successfully.")

    def teardown(self) -> None:
        """Tears down the task_environment, not implemented."""

        # TODO - Implement teardown environment
        raise NotImplementedError

    def validate(self) -> None:
        """Validates the task_environment, not implemented."""

        # TODO - Implement validate environment
        raise NotImplementedError

    def reset(self) -> None:
        """Resets the task_environment, not implemented."""

        # TODO - Implement reset environment which clears the state
        raise NotImplementedError

    def commit_task(
        self,
        task: AutomataTask,
        commit_message: str,
        pull_title: str,
        pull_body: str,
        pull_branch_name: str = "feature/test",
    ) -> str:
        """
        Commits the task to the remote repository.

        Raises AgentTaskException:
            If the task is not status SUCCESS.
            If the task output directory is missing.
            If the branch already exists.
            If the checkout fails.
            If the commit fails.
        """

        logger.debug("Comitting task...")

        if not self.github_manager:
            raise ValueError("Cannot commit task without a github manager.")

        if task.status != TaskStatus.SUCCESS:
            raise TaskStateError(
                "Cannot commit task to repository because the task has not been successfully executed."
            )

        if not os.path.exists(task.task_dir):
            raise TaskGeneralError(
                "Cannot commit task to repository because the task output directory is missing."
            )

        # Check if the branch already exists, if not create it
        if not self.github_manager.branch_exists(pull_branch_name):
            self.github_manager.create_branch(pull_branch_name)

        # Checkout the new branch
        try:
            self.github_manager.checkout_branch(
                task.task_dir, pull_branch_name
            )
        except Exception as e:
            logger.debug(
                f"Checkout failed with exception: {e}, Trying with b=False"
            )
            self.github_manager.checkout_branch(
                task.task_dir, pull_branch_name, b=False
            )

        # Stage all changes
        self.github_manager.stage_all_changes(task.task_dir)

        try:
            # Commit and push changes
            self.github_manager.commit_and_push_changes(
                task.task_dir, pull_branch_name, commit_message
            )
        except Exception as e:
            logger.debug(f"Commit failed with exception: {e}")

        # Create a pull request
        pull_request = self.github_manager.create_pull_request(
            pull_branch_name, pull_title, pull_body
        )
        pull_url = pull_request.html_url
        task.status = TaskStatus.COMMITTED

        logger.info(
            "Task %s committed successfully with Title:\n%s\n\nBody:\n%s\n\nBranch:\n%s\nAt URL:\n%s\n"
            % (
                task.session_id,
                pull_title,
                pull_body,
                pull_branch_name,
                pull_url,
            ),
        )

        return pull_request.html_url
