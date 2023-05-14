import logging
import logging.config
import os
import sqlite3
from typing import Dict, List, Optional, Tuple

import jsonpickle

from automata.core.base.github_manager import GitHubManager
from automata.core.tasks.task import AutomataTask, TaskStatus

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
                id TEXT PRIMARY KEY,
                json TEXT,
                instructions TEXT,
                status TEXT
            )
        """
        )
        self.conn.commit()

    def insert_task(self, task: AutomataTask) -> None:
        cursor = self.conn.cursor()
        task_id = task.task_id
        task_json = jsonpickle.encode(task)
        instructions = task.kwargs.get("instructions", "")
        status = task.status.value
        cursor.execute(
            """
            INSERT INTO tasks (id, json, instructions, status)
            VALUES (?, ?, ?, ?)
        """,
            (str(task_id), task_json, instructions, status),
        )
        self.conn.commit()

    def update_task(self, task: AutomataTask) -> None:
        cursor = self.conn.cursor()
        task_json = jsonpickle.encode(task)
        instructions = task.kwargs.get("instructions", "")
        status = task.status.value
        cursor.execute(
            """
            UPDATE tasks SET json = ?, instructions = ?, status = ?
            WHERE id = ?
        """,
            (task_json, instructions, status, str(task.task_id)),
        )
        self.conn.commit()

    def get_tasks_by(self, query: str, params: Tuple = ()) -> List[AutomataTask]:
        cursor = self.conn.cursor()
        cursor.execute(query, params)
        rows = cursor.fetchall()

        tasks = []
        for row in rows:
            task_json = row[0]
            try:
                task = jsonpickle.decode(task_json)
                tasks.append(task)
            except Exception as e:
                logger.error(f"Failed to decode task with error: {e}")

        return tasks

    def get_task_summaries_by(self, query: str, params: Tuple = ()) -> List[Tuple[str, str, str]]:
        cursor = self.conn.cursor()
        cursor.execute(query, params)
        rows = cursor.fetchall()

        tasks_summary = []
        for row in rows:
            task_id = row[0]
            task_instructions = row[1]
            task_status = row[2]
            tasks_summary.append((task_id, task_instructions, task_status))

        return tasks_summary


class AutomataTaskRegistry:
    def __init__(self, db: AutomataTaskDatabase, github_manager: GitHubManager):
        self.db = db
        self.github_manager = github_manager

    def initialize_task(self, task):
        task.observer = self.update_task
        self._add_task(task)
        self._setup_task_env(task)

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

        if task.status != TaskStatus.SUCCESS:
            raise Exception(
                "Cannot commit task to repository because the task has not been successfully executed."
            )
        if not os.path.exists(task.task_dir):
            raise Exception(
                "Cannot commit task to repository because the task directory has not been created."
            )
        # Check if the branch already exists, if not create it
        if not github_manager.branch_exists(pull_branch_name):
            github_manager.create_branch(pull_branch_name)
        # Checkout the new branch
        try:
            github_manager.checkout_branch(task.task_dir, pull_branch_name)
        except Exception as e:
            logger.debug("Checkout failed with exception: %s, Trying with b=False" % e)
            github_manager.checkout_branch(task.task_dir, pull_branch_name, b=False)

        # Stage all changes
        github_manager.stage_all_changes(task.task_dir)

        try:
            # Commit and push changes
            github_manager.commit_and_push_changes(task.task_dir, pull_branch_name, commit_message)
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
            query="SELECT json FROM tasks WHERE id = ?", params=(task_id,)
        )
        if not results:
            return None
        else:
            if len(results) != 1:
                raise Exception(f"Found multiple tasks with id {task_id}")
            task = results[0]
            task.initialize_logging()
            task.observer = self.update_task
            return task

    def get_all_tasks(self) -> list[AutomataTask]:
        results = self.db.get_tasks_by(query="SELECT json FROM tasks")
        for result in results:
            result.observer = self.update_task
        return results

    def get_all_task_summaries(self) -> List[Dict[str, str]]:
        results = self.db.get_task_summaries_by(query="SELECT id, instructions, status FROM tasks")
        return [
            {"task_id": result[0], "instructions": result[1], "status": result[2]}
            for result in results
        ]

    def _add_task(self, task: AutomataTask) -> None:
        if self.get_task_by_id(str(task.task_id)):
            raise Exception(f"Task with id {task.task_id} already exists")
        self.db.insert_task(task)

    def _setup_task_env(self, task: AutomataTask):
        """
        Creates the environment for the task.
        """
        logger.debug("Creating task environment...")
        self.github_manager.clone_repository(task.task_dir)

        task.status = TaskStatus.PENDING
        logger.debug("Task environment created successfully")
