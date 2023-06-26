import logging
import logging.config
import sqlite3
import textwrap
from typing import List, Optional, Tuple

import jsonpickle

from automata.config import TASK_DB_PATH
from automata.core.agent.error import AgentTaskGeneralError, AgentTaskStateError
from automata.core.agent.task.task import AutomataTask
from automata.core.base.task import TaskStatus

logger = logging.getLogger(__name__)


class AutomataTaskDatabase:
    """The database creates a local store for all tasks."""

    # TODO - Implement custom errors and implement more robust handling
    # around database creation and connection

    CREATE_TABLE_QUERY = textwrap.dedent(
        """
        CREATE TABLE IF NOT EXISTS tasks (
            id TEXT PRIMARY KEY,
            json TEXT,
            instructions TEXT,
            status TEXT
        )
        """
    )

    INSERT_TASK_QUERY = textwrap.dedent(
        """
        INSERT INTO tasks (id, json, instructions, status)
        VALUES (?, ?, ?, ?)
        """
    )

    UPDATE_TASK_QUERY = textwrap.dedent(
        """
        UPDATE tasks SET json = ?, instructions = ?, status = ?
        WHERE id = ?
    """
    )

    SELECT_TASK_QUERY = textwrap.dedent(
        """
        SELECT id FROM tasks WHERE id = ?
        """
    )

    def __init__(self, db_path: str = TASK_DB_PATH):
        """
        Args:
            db_path (str): The path to the database file.
        """
        self.conn = sqlite3.connect(db_path)
        self.create_table()

    def create_table(self, create_table_query: str = CREATE_TABLE_QUERY) -> None:
        """
        Creates the table for storing tasks.

        Args:
            create_table_query (str): The query to use for creating the table.
        """
        cursor = self.conn.cursor()
        cursor.execute(create_table_query)
        self.conn.commit()

    def insert_task(self, task: AutomataTask, insert_task_query: str = INSERT_TASK_QUERY) -> None:
        """
        Inserts a task into the database.

        Args:
            task (AutomataTask): The task to insert.
            insert_task_query (str): The query to use for inserting the task.
        """
        cursor = self.conn.cursor()
        task_id = task.task_id
        task_json = jsonpickle.encode(task)
        instructions = task.instructions
        status = task.status.value
        cursor.execute(
            insert_task_query,
            (str(task_id), task_json, instructions, status),
        )
        self.conn.commit()

    def update_task(self, task: AutomataTask, update_task_query: str = UPDATE_TASK_QUERY) -> None:
        """
        Updates a task in the database.

        Args:
            task (AutomataTask): The task to update.
            update_task_query (str): The query to use for updating the task.
        """
        cursor = self.conn.cursor()
        task_json = jsonpickle.encode(task)
        instructions = task.instructions
        status = task.status.value
        cursor.execute(
            update_task_query,
            (task_json, instructions, status, str(task.task_id)),
        )
        self.conn.commit()

    def get_tasks_by_query(self, query: str, params: Tuple = ()) -> List[AutomataTask]:
        """
        Gets the tasks by the specified query.

        This works by getting the json for each task and then decoding it.

        Args:
            query (str): The query to use for getting the tasks.
            params (Tuple): The parameters to use for the query.
        """
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

    def contains(self, task: AutomataTask, contains_task_query: str = SELECT_TASK_QUERY) -> bool:
        """
        Checks if a task exists in the database.

        Args:
            task (AutomataTask): The task to check for existence.
        """
        cursor = self.conn.cursor()
        cursor.execute(contains_task_query, (str(task.task_id),))
        result = cursor.fetchone()
        return result is not None


class AutomataTaskRegistry:
    """The registry manages storing and retrieving tasks."""

    def __init__(self, db: AutomataTaskDatabase) -> None:
        """
        Args:
            db (AutomataTaskDatabase): The database to use for storing tasks.
        """
        self.db = db

    def register(self, task: AutomataTask) -> None:
        """
        Initializes a task by adding it to the registry,
        the task must have already been set up.
        setting the observer, and setting the status to pending.

        Raises:
            Exception: If the task is not status REGISTERED.

        """
        if task.status != TaskStatus.CREATED:
            raise AgentTaskStateError(
                f"Cannot register task because task is not in CREATED state. Task status = {task.status}"
            )
        task.observer = self.update_task
        if self.fetch_task_by_id(str(task.task_id)):
            raise AgentTaskGeneralError(f"Task with id {task.task_id} already exists")
        self.db.insert_task(task)
        task.status = TaskStatus.REGISTERED
        logger.info(f"Task {task.task_id} registered successfully.")

    def update_task(self, task: AutomataTask) -> None:
        """
        Updates a task in the registry.

        Raises:
            Exception: If the task does not exist in the registry.
        """
        if not self.db.contains(task):
            raise AgentTaskStateError(f"Task with id {task.task_id} does not exist")
        task.observer = None
        self.db.update_task(task)
        task.observer = self.update_task

    def fetch_task_by_id(self, task_id: str) -> Optional[AutomataTask]:
        """
        Fetches a task by its id.

        Args:
            task_id (str): The id of the task to fetch.

        Returns:
            Optional[AutomataTask]: The task if it exists, otherwise None.

        Raises:
            Exception: If multiple tasks are found with the same id.
        """
        results = self.db.get_tasks_by_query(
            query="SELECT json FROM tasks WHERE id = ?", params=(task_id,)
        )
        if not results:
            return None
        if len(results) != 1:
            raise AgentTaskGeneralError(f"Found multiple tasks with id {task_id}")
        task = results[0]
        task.observer = self.update_task
        return task

    def get_all_tasks(self) -> List[AutomataTask]:
        """
        Gets all tasks in the registry.

        Returns:
            List[AutomataTask]: The list of tasks.
        """
        results = self.db.get_tasks_by_query(query="SELECT json FROM tasks")
        for result in results:
            result.observer = self.update_task
        return results
