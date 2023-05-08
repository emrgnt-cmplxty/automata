import os
import uuid
from enum import Enum
from typing import Optional

from retrying import retry

from automata.config import DEFAULT_REMOTE_URL, GITHUB_API_KEY
from automata.core.agent.automata_agent_helpers import (
    create_builder_from_args,
    create_instruction_payload,
)
from automata.core.base.github_manager import GitHubManager
from automata.core.utils import root_path

JOB_DIR_NAME = "jobs"


class TaskStatus(Enum):
    PENDING = "pending"
    RUNNING = "running"
    SUCCESS = "success"
    FAILED = "failed"


class AutomataTask:
    """
    The AutomataTask class represents a task that is to be executed by the Automata agent.
    """

    def __init__(self, github_manager: GitHubManager, *args, **kwargs):
        self.github_manager = github_manager
        self.task_id = uuid.uuid4()

        self.priority = kwargs.get("priority", 0)
        self.max_retries = kwargs.get("max_retries", 3)
        self.status = TaskStatus(kwargs.get("status", "pending"))
        self.rel_py_path = kwargs.get("rel_py_path", "automata")

        builder = create_builder_from_args(*args, **kwargs)

        self.agent = builder.build()
        self.result = None
        self.error: Optional[str] = None
        self.retry_count = 0

    def create_task_env(self):
        """
        Creates the environment for the task
        """
        # Generate a unique directory name for the task
        task_dir_name = f"task_{self.task_id}"
        job_dir = os.path.join(root_path(), JOB_DIR_NAME)

        # Create the jobs directory if it does not exist
        if not os.path.exists(job_dir):
            os.makedirs(job_dir)

        self.task_dir = os.path.join(job_dir, task_dir_name)
        self.github_manager.clone_repository(self.task_dir)

    def wait_exponential(self, retry_state):
        """
        Waits for a specified amount of time before retrying the task
        """
        return (2**retry_state.attempt_number) * 1000  # Exponential backoff in milliseconds

    @retry(
        retry_on_exception=lambda e: isinstance(e, Exception),
        wait_func=wait_exponential,
        stop_max_attempt_number=lambda self: self.max_retries,
    )
    def execute(self) -> Optional[str]:
        """
        Executes the task
        """
        from automata.tools.python_tools.python_indexer import PythonIndexer
        from automata.tools.python_tools.python_writer import PythonWriter

        indexer = PythonIndexer(os.path.join(self.task_dir, self.rel_py_path))
        writer = PythonWriter(indexer)

        writer.update_module(
            module_path="core.agent.automata_agent",
            source_code="def test123(x): return True",
            write_to_disk=True,
        )
        return None

        # overview = indexer.build_overview()
        # print("Overview = ", overview)
        # self.status = TaskStatus.RUNNING
        # try:
        #     # self.result = self.agent.run()
        #     self.status = TaskStatus.SUCCESS
        # except Exception as e:
        #     logging.exception(f"AutomataTask failed: {e}")
        #     self.error = str(e)
        #     self.status = TaskStatus.FAILED
        #     self.retry_count += 1
        #     raise

        # return self.result

    def commit_task(
        self,
        pull_branch_name: str = "feature/test",
        commit_message: str = "This is a commit message",
        pull_title="This is a test",
        pull_body="I am testing this...",
    ):
        """
        Commits the task to the repository
        """
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


if __name__ == "__main__":
    from automata.configs.automata_agent_configs import AutomataAgentConfig
    from automata.configs.config_enums import AgentConfigVersion

    instruction_payload = create_instruction_payload(overview="Overview", agents_message="Message")
    github_manager = GitHubManager(access_token=GITHUB_API_KEY, remote_url=DEFAULT_REMOTE_URL)

    task = AutomataTask(
        agent_config=AutomataAgentConfig.load(AgentConfigVersion.AUTOMATA_INDEXER_DEV),
        llm_toolkits="",
        model="gpt-4",
        instruction_payload=instruction_payload,
        stream=True,
        github_manager=github_manager,
    )
    task.create_task_env()
    task.execute()
    task.commit_task("test_branch_9")
