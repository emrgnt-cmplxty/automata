import logging
import logging.config
from typing import List, Optional, Tuple

import jsonpickle

from automata.agent.error import AgentTaskGeneralError, AgentTaskStateError
from automata.config import TASK_DB_PATH
from automata.core.base.database.relational import SQLDatabase
from automata.tasks.base import TaskStatus
from automata.tasks.tasks import AutomataTask

logger = logging.getLogger(__name__)


class AutomataAgentTaskDatabase(SQLDatabase):
    """The database creates a local store for all tasks."""

    TABLE_NAME = "tasks"
    TABLE_FIELDS = {
        "id": "TEXT PRIMARY KEY",
        "json": "TEXT",
        "instructions": "TEXT",
        "status": "TEXT",
    }

    def __init__(self, db_path: str = TASK_DB_PATH):
        self.connect(db_path)
        self.create_table(self.TABLE_NAME, self.TABLE_FIELDS)

    def insert_task(self, task: AutomataTask) -> None:
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
        task_json = jsonpickle.encode(task)
        instructions = task.instructions
        status = task.status.value
        self.update_database(
            self.TABLE_NAME,
            {"json": task_json, "instructions": instructions, "status": status},
            {"id": str(task.task_id)},
        )

    def get_tasks_by_query(self, query: str, params: Tuple = ()) -> List[AutomataTask]:
        """Gets the list of tasks by applying the specified query."""
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
        """Checks if a task exists in the database."""
        result = self.select(self.TABLE_NAME, ["id"], conditions={"id": str(task.task_id)})
        return len(result) > 0


class AutomataTaskRegistry:
    """The registry manages storing and retrieving tasks."""

    def __init__(self, db: AutomataAgentTaskDatabase) -> None:
        self.db = db

    def register(self, task: AutomataTask) -> None:
        """
        Initializes a task by adding it to the registry and setting its status to REGISTERED.

        Raises:
            Exception: If the task is not status CREATED.
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
        results = self.db.get_tasks_by_query(query="SELECT json FROM tasks")
        for result in results:
            result.observer = self.update_task
        return results
