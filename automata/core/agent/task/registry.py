import logging
import logging.config
from typing import List, Optional, Tuple

import jsonpickle

from automata.config import TASK_DB_PATH
from automata.core.agent.error import AgentTaskGeneralError, AgentTaskStateError
from automata.core.agent.task.task import AutomataTask
from automata.core.base.database.relational import SQLDatabase
from automata.core.base.task import TaskStatus

logger = logging.getLogger(__name__)


class AutomataTaskDatabase(SQLDatabase):
    """The database creates a local store for all tasks."""

    # TODO - Implement custom errors and implement more robust handling
    # around database creation and connection

    TABLE_NAME = "tasks"
    TABLE_FIELDS = {
        "id": "TEXT PRIMARY KEY",
        "json": "TEXT",
        "instructions": "TEXT",
        "status": "TEXT",
    }

    def __init__(self, db_path: str = TASK_DB_PATH):
        """
        Args:
            db_path (str): The path to the database file.
        """
        self.connect(db_path)
        self.create_table(self.TABLE_NAME, self.TABLE_FIELDS)

    def insert_task(self, task: AutomataTask) -> None:
        """
        Inserts a task into the database.

        Args:
            task (AutomataTask): The task to insert.
        """
        task_id = task.task_id
        task_json = jsonpickle.encode(task)
        instructions = task.instructions
        status = task.status.value
        self.insert(
            self.TABLE_NAME,
            {
                "id": str(task_id),
                "json": task_json,
                "instructions": instructions,
                "status": status,
            },
        )

    def update_task(self, task: AutomataTask) -> None:
        """
        Updates a task in the database.

        Args:
            task (AutomataTask): The task to update.
        """
        task_json = jsonpickle.encode(task)
        instructions = task.instructions
        status = task.status.value
        self.update(
            self.TABLE_NAME,
            {"json": task_json, "instructions": instructions, "status": status},
            {"id": str(task.task_id)},
        )

    def get_tasks_by_query(self, query: str, params: Tuple = ()) -> List[AutomataTask]:
        """
        Gets the tasks by the specified query.

        This works by getting the json for each task and then decoding it.

        Args:
            query (str): The query to use for getting the tasks.
            params (Tuple): The parameters to use for the query.
        """
        rows = self.select(self.TABLE_NAME, ["json"], conditions=dict(zip(query, params)))
        tasks = []
        for row in rows:
            task_json = row[0]
            try:
                task = jsonpickle.decode(task_json)
                tasks.append(task)
            except Exception as e:
                logger.error(f"Failed to decode task with error: {e}")

        return tasks

    def contains(self, task: AutomataTask) -> bool:
        """
        Checks if a task exists in the database.

        Args:
            task (AutomataTask): The task to check for existence.
        """
        result = self.select(self.TABLE_NAME, ["id"], conditions={"id": str(task.task_id)})
        return len(result) > 0


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
