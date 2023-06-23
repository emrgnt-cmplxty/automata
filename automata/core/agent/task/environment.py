import logging
import logging.config
import os

from automata.core.agent.task.task import AutomataTask
from automata.core.base.github_manager import GitHubManager
from automata.core.base.task import TaskEnvironment, TaskStatus

logger = logging.getLogger(__name__)


class AutomataTaskEnvironment(TaskEnvironment):
    """
    This is a concrete implementation of the AbstractEnvironment.
    """

    def __init__(self, github_manager: GitHubManager) -> None:
        """
        Args:
            github_manager (GitHubManager): The GitHubManager to use for interacting with the remote repository.
        """
        self.github_manager = github_manager

    def setup(self, task: AutomataTask) -> None:
        """
        Set up the environment by cloning the repository into the task directory.
        Sets the task status to REGISTERED.

        Raises:
            Exception: If the task is not status CREATED.
        """
        if task.status != TaskStatus.REGISTERED:
            raise Exception(
                f"Cannot setup task environment because task is not in REGISTERED state. Task status = {task.status}"
            )
        logger.debug(f"Setting up the task environment in directory {task.task_dir}.")
        # TODO - Consider more methods for environment initlization than git clone
        self.github_manager.clone_repository(task.task_dir)

        task.status = TaskStatus.PENDING
        logger.info(f"Task {task.task_id} environment setup successfully.")

    def teardown(self) -> None:
        """
        Tear down the environment.
        """
        # TODO - Implement teardown environment
        raise NotImplementedError

    def validate(self) -> None:
        """
        Validate the environment.
        """
        # TODO - Implement validate environment
        raise NotImplementedError

    def reset(self) -> None:
        """
        Reset the environment to its initial state.
        """
        # TODO - Implement reset environment which clears the state
        # and erases the task directory, and re-runs setup
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

        Args:
            task (AutomataTask): The task to commit.
            commit_message (str): The commit message to use.
            pull_title (str): The title of the pull request.
            pull_body (str): The body of the pull request.
            pull_branch_name (str, optional): The name of the branch to create. Defaults to "feature/test".

        Raises:
            Exception: If the task is not status SUCCESS.
            Exception: If the task output directory is missing.
            Exception: If the branch already exists.
            Exception: If the checkout fails.
            Exception: If the commit fails.
        """
        print("calling commit task..")
        logger.debug("Comitting task...")

        if task.status != TaskStatus.SUCCESS:
            raise Exception(
                "Cannot commit task to repository because the task has not been successfully executed."
            )
        if not os.path.exists(task.task_dir):
            raise Exception(
                "Cannot commit task to repository because the task output directory is missing."
            )
        # Check if the branch already exists, if not create it
        if not self.github_manager.branch_exists(pull_branch_name):
            self.github_manager.create_branch(pull_branch_name)
        # Checkout the new branch
        try:
            self.github_manager.checkout_branch(task.task_dir, pull_branch_name)
        except Exception as e:
            logger.debug(f"Checkout failed with exception: {e}, Trying with b=False")
            self.github_manager.checkout_branch(task.task_dir, pull_branch_name, b=False)

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
            % (task.task_id, pull_title, pull_body, pull_branch_name, pull_url),
        )

        return pull_request.html_url
