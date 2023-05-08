# TODO - Make sure the registry and database work as expected
# They have not been tested yet and are already out of date
# so some work is expected to bring them up to speed
import sqlite3
from typing import Optional

from automata.config import GITHUB_API_KEY
from automata.core.base.github_manager import GitHubManager
from automata.core.tasks.task import AutomataTask, TaskStatus


class TaskDatabase:
    def __init__(self, db_name: str):
        self.conn = sqlite3.connect(db_name)
        self.create_table()

    def create_table(self) -> None:
        cursor = self.conn.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS tasks (
                task_id TEXT PRIMARY KEY,
                priority INTEGER,
                status TEXT,
                result TEXT,
                error TEXT,
                retry_count INTEGER,
                remote_url TEXT,
                primary_branch TEXT
            )
        """
        )
        self.conn.commit()

    def insert_task(self, task: AutomataTask) -> None:
        cursor = self.conn.cursor()
        cursor.execute(
            """
            INSERT INTO tasks (task_id, priority, status, result, error, retry_count, remote_url, primary_branch)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
            (
                task.task_id,
                task.priority,
                task.status.value,
                task.result,
                task.error,
                task.retry_count,
                task.github_manager.remote_name,
                task.github_manager.primary_branch,
            ),
        )
        self.conn.commit()

    def update_task(self, task: AutomataTask) -> None:
        cursor = self.conn.cursor()
        cursor.execute(
            """
            UPDATE tasks SET
                priority = ?,
                status = ?,
                result = ?,
                error = ?,
                retry_count = ?,
                remote_name = ?,
                primary_branch = ?
            WHERE task_id = ?
        """,
            (
                task.priority,
                task.status.value,
                task.result,
                task.error,
                task.retry_count,
                task.github_manager.remote_name,
                task.github_manager.primary_branch,
                task.task_id,
            ),
        )
        self.conn.commit()

    def get_task(self, task_id: str) -> Optional[AutomataTask]:
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM tasks WHERE task_id = ?", (task_id,))
        row = cursor.fetchone()

        if row:
            github_manager = GitHubManager(
                access_token=GITHUB_API_KEY, remote_url=row[7], primary_branch=row[8]
            )
            task = AutomataTask(github_manager=github_manager)
            task.task_id = row[0]
            task.priority = row[1]
            task.status = TaskStatus(row[2])
            task.result = row[3]
            task.error = row[4]
            task.retry_count = row[5]
            return task
        else:
            return None


class TaskRegistry:
    def __init__(self, db: TaskDatabase):
        self.db = db

    def add_task(self, task: AutomataTask) -> None:
        self.db.insert_task(task)

    def get_task(self, task_id) -> Optional[AutomataTask]:
        return self.db.get_task(task_id)
