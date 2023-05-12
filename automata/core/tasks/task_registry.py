import logging
import logging.config
import os
import sqlite3
from typing import List, Optional, Tuple

import jsonpickle

from automata.core.base.github_manager import GitHubManager
from automata.core.tasks.task import AutomataTask, TaskStatus
from automata.core.utils import get_logging_config, root_path

logger = logging.getLogger(__name__)


class AutomataTaskDatabase:
    def __init__(self, db_path: str):
        self.conn = sqlite3.connect(db_path)
        self.create_table()

    def create_table(self) -> None:
        cursor = self.conn.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS tasks (
                task_id TEXT PRIMARY KEY,
                task_json TEXT
            )
        """
        )
        self.conn.commit()

    def insert_task(self, task: AutomataTask) -> None:
        cursor = self.conn.cursor()
        task_id = task.task_id
        task_json = jsonpickle.encode(task)
        cursor.execute(
            """
            INSERT INTO tasks (task_id, task_json)
            VALUES (?, ?)
        """,
            (str(task_id), task_json),
        )
        self.conn.commit()

    def update_task(self, task: AutomataTask) -> None:
        cursor = self.conn.cursor()
        task_json = jsonpickle.encode(task)
        cursor.execute(
            """
            UPDATE tasks SET task_json = ?
            WHERE task_id = ?
        """,
            (task_json, str(task.task_id)),
        )
        self.conn.commit()

    def get_tasks_by(self, query: str, params: Tuple = ()) -> List[AutomataTask]:
        cursor = self.conn.cursor()
        cursor.execute(query, params)
        rows = cursor.fetchall()

        tasks = []
        for row in rows:
            task_json = row[0]
            task = jsonpickle.decode(task_json)
            tasks.append(task)

        return tasks


class TaskRegistry:
    JOB_DIR_NAME = "jobs"
    TASK_LOG_NAME = "task.log"

    def __init__(self, db: AutomataTaskDatabase, github_manager: GitHubManager):
        self.db = db
        self.github_manager = github_manager

    def initialize_task(self, task):
        self._add_task(task)
        self._setup_task_env(task)
        task.observer = self.update_task

    def update_task(self, task: AutomataTask) -> None:
        task.observer = None
        self.db.update_task(task)
        task.observer = self.update_task

    def commit_task(
        self,
        task: AutomataTask,
        github_manager: GitHubManager,
        commit_message: str,
        pull_title: str,
        pull_body: str,
        pull_branch_name: str = "feature/test",
    ) -> str:
        """
        Commits the task to the remote repository.
        """
        logger.debug("Comitting task...")

        task_dir = self._get_task_dir(task)
        if task.status != TaskStatus.SUCCESS:
            raise Exception(
                "Cannot commit task to repository because the task has not been successfully executed."
            )
        if task_dir is None:
            raise Exception(
                "Cannot commit task to repository because the task directory has not been created."
            )
        # Check if the branch already exists, if not create it
        if not github_manager.branch_exists(pull_branch_name):
            github_manager.create_branch(pull_branch_name)
        # Checkout the new branch
        try:
            github_manager.checkout_branch(task_dir, pull_branch_name)
        except Exception as e:
            logger.debug("Checkout failed with exception: %s, Trying with b=False" % e)
            github_manager.checkout_branch(task_dir, pull_branch_name, b=False)

        # Stage all changes
        github_manager.stage_all_changes(task_dir)

        try:
            # Commit and push changes
            github_manager.commit_and_push_changes(task_dir, pull_branch_name, commit_message)
        except Exception as e:
            logger.debug("Commit failed with exception: %s" % e)

        # Create a pull request
        pull_request = github_manager.create_pull_request(pull_branch_name, pull_title, pull_body)
        pull_url = pull_request.html_url
        logger.debug(
            "Task committed successfully with Title:\n%s\n\nBody:\n%s\n\nBranch:\n%s\nAt URL:\n%s\n"
            % (pull_title, pull_body, pull_branch_name, pull_url),
        )

        task.status = TaskStatus.COMMITTED
        logger.debug("Task committed successfully")
        return pull_request.html_url

    def get_task_by_id(self, task_id: str) -> Optional[AutomataTask]:
        results = self.db.get_tasks_by(
            query="SELECT task_json FROM tasks WHERE task_id = ?", params=(task_id,)
        )
        if not results:
            return None
        else:
            if len(results) != 1:
                raise Exception(f"Found multiple tasks with id {task_id}")
            result = results[0]
            result.observer = self.update_task
            return result

    def get_all_tasks(self) -> list[AutomataTask]:
        results = self.db.get_tasks_by(query="SELECT task_json FROM tasks")
        for result in results:
            result.observer = self.update_task
        return results

    def _add_task(self, task: AutomataTask) -> None:
        if self.get_task_by_id(str(task.task_id)):
            raise Exception(f"Task with id {task.task_id} already exists")
        self.db.insert_task(task)

    def _setup_task_env(self, task: AutomataTask):
        """
        Creates the environment for the task.
        """
        logger.debug("Creating task environment...")

        # Create the jobs directory if it does not exist
        TaskRegistry._setup_jobs_dir()
        task_dir = self._get_task_dir(task)
        task.task_dir = task_dir
        self.github_manager.clone_repository(task_dir)
        task.status = TaskStatus.PENDING
        log_file = os.path.join(task_dir, TaskRegistry.TASK_LOG_NAME)
        logging.config.dictConfig(get_logging_config(log_file=log_file))
        logger.debug("Task environment created successfully")

    @staticmethod
    def _get_jobs_dir() -> str:
        return os.path.join(root_path(), TaskRegistry.JOB_DIR_NAME)

    @staticmethod
    def _setup_jobs_dir() -> None:
        job_dir = TaskRegistry._get_jobs_dir()
        if not os.path.exists(job_dir):
            os.makedirs(job_dir)

    @staticmethod
    def _get_task_dir(
        task: AutomataTask,
    ) -> str:
        # Generate a unique directory name for the task
        return os.path.join(TaskRegistry._get_jobs_dir(), f"task_{task.task_id}")
