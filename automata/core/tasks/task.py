import logging
import logging.config
import os
import uuid
from collections.abc import Hashable
from enum import Enum
from typing import Optional

from automata.core.agent.automata_agent_helpers import create_builder_from_args
from automata.core.base.github_manager import GitHubManager
from automata.core.utils import get_logging_config, root_path

logger = logging.getLogger(__name__)
logging.config.dictConfig(get_logging_config())

JOB_DIR_NAME = "jobs"


class TaskStatus(Enum):
    SETUP = "setup"
    PENDING = "pending"
    RUNNING = "running"
    SUCCESS = "success"
    FAILED = "failed"


class Task:
    """
    A generic task object.
    """

    def __init__(self, *args, **kwargs):
        self.task_id = (
            self._deterministic_task_id(**kwargs)
            if kwargs.get("generate_deterministic_id", True)
            else uuid.uuid4()
        )
        self.priority = kwargs.get("priority", 0)
        self.max_retries = kwargs.get("max_retries", 3)
        self.status = TaskStatus(kwargs.get("status", "setup"))
        self.retry_count = 0

    def _deterministic_task_id(self, **kwargs):
        """
        Returns a deterministic session id for the task.
        """
        # Generate the hash of the hashable kwargs
        hashable_items = sorted([item for item in kwargs.items() if isinstance(item[1], Hashable)])
        kwargs_hash = hash(tuple(hashable_items))

        # Combine the hashes and use it as a seed for generating a deterministic UUID
        seed = f"{kwargs_hash}"
        deterministic_uuid = uuid.uuid5(uuid.NAMESPACE_DNS, seed)

        return deterministic_uuid


class GitHubTask(Task):
    """
    A task that is to be committed to a GitHub repository.
    """

    def __init__(self, github_manager: GitHubManager, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.github_manager = github_manager
        self.task_dir = None

    def create_task_env(self):
        """
        Creates the environment for the task.
        """
        # Generate a unique directory name for the task
        task_dir_name = f"task_{self.task_id}"
        job_dir = os.path.join(root_path(), JOB_DIR_NAME)

        # Create the jobs directory if it does not exist
        if not os.path.exists(job_dir):
            os.makedirs(job_dir)

        self.task_dir = os.path.join(job_dir, task_dir_name)
        self.github_manager.clone_repository(self.task_dir)
        self.status = TaskStatus.PENDING
        logger.info("Task environment created successfully")

    def commit_task(
        self,
        commit_message: str,
        pull_title: str,
        pull_body: str,
        pull_branch_name: str = "feature/test",
    ):
        """
        Commits the task to the remote repository.
        """
        if self.status != TaskStatus.SUCCESS:
            raise Exception(
                "Cannot commit task to repository because the task has not been successfully executed."
            )
        if self.task_dir is None:
            raise Exception(
                "Cannot commit task to repository because the task directory has not been created."
            )
        # Check if the branch already exists, if not create it
        if not self.github_manager.branch_exists(pull_branch_name):
            self.github_manager.create_branch(pull_branch_name)

        # Checkout the new branch
        repo_local_path = self.task_dir
        self.github_manager.checkout_branch(repo_local_path, pull_branch_name)

        # Stage all changes
        self.github_manager.stage_all_changes(repo_local_path)

        # Commit and push changes
        self.github_manager.commit_and_push_changes(
            repo_local_path, pull_branch_name, commit_message
        )

        # Create a pull request
        self.github_manager.create_pull_request(pull_branch_name, pull_title, pull_body)
        logger.info(
            "Task committed successfully with Title: %s\n\nBody: %s\n\nBranch: %s"
            % (pull_title, pull_body, pull_branch_name),
        )


class AutomataTask(GitHubTask):
    """
    A task that is to be executed by the AutomataAgent via the TaskExecutor.
    """

    def __init__(self, github_manager: GitHubManager, *args, **kwargs):
        super().__init__(github_manager, *args, **kwargs)
        self.rel_py_path = kwargs.get("rel_py_path", "")
        builder = create_builder_from_args(*args, **kwargs)
        self.agent = builder.build()
        self.result = None
        self.error: Optional[str] = None
