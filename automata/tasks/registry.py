from typing import List, Optional

from automata.tasks.automata_task import AutomataTask
from automata.tasks.base import TaskStatus
from automata.tasks.error import TaskGeneralError, TaskStateError
from automata.tasks.task_database import AutomataAgentTaskDatabase, logger


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
            raise TaskStateError(
                f"Cannot register task because task is not in CREATED state. Task status = {task.status}"
            )
        task.observer = self.update_task
        if self.fetch_task_by_id(str(task.session_id)):
            raise TaskGeneralError(
                f"Task with id {task.session_id} already exists"
            )
        self.db.insert_task(task)
        task.status = TaskStatus.REGISTERED
        logger.info(f"Task {task.session_id} registered successfully.")

    def update_task(self, task: AutomataTask) -> None:
        """
        Updates a task in the registry.

        Raises:
            Exception: If the task does not exist in the registry.
        """

        if not self.db.contains(task):
            raise TaskStateError(
                f"Task with id {task.session_id} does not exist"
            )
        task.observer = None
        self.db.update_task(task)
        task.observer = self.update_task

    def fetch_task_by_id(self, session_id: str) -> Optional[AutomataTask]:
        """
        Fetches a taks by the recorded session id.

        Raises:
            Exception: If multiple tasks are found with the same id.
        """

        results = self.db.get_tasks_by_query(
            query="SELECT json FROM tasks WHERE id = ?", params=(session_id,)
        )
        if not results:
            return None
        if len(results) != 1:
            raise TaskGeneralError(
                f"Found multiple tasks with id {session_id}"
            )
        task = results[0]
        task.observer = self.update_task
        return task

    def get_all_tasks(self) -> List[AutomataTask]:
        """Gets all tasks in the registry."""
        results = self.db.get_tasks_by_query(query="SELECT json FROM tasks")
        for result in results:
            result.observer = self.update_task
        return results
