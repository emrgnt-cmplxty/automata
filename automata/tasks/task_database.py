import logging
import logging.config
from typing import List, Tuple

import jsonpickle

from automata.config import TASK_DB_PATH
from automata.core.base import SQLDatabase
from automata.tasks.automata_task import AutomataTask

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
        session_id = task.session_id
        task_json = jsonpickle.encode(task)
        instructions = task.instructions
        status = task.status.value
        self.insert(
            self.TABLE_NAME,
            {
                "id": str(session_id),
                "json": task_json,
                "instructions": instructions,
                "status": status,
            },
        )

    def update_task(self, task: AutomataTask) -> None:
        task_json = jsonpickle.encode(task)
        instructions = task.instructions
        status = task.status.value
        self.update_entry(
            self.TABLE_NAME,
            {
                "json": task_json,
                "instructions": instructions,
                "status": status,
            },
            {"id": str(task.session_id)},
        )

    def get_tasks_by_query(
        self, query: str, params: Tuple = ()
    ) -> List[AutomataTask]:
        """Gets the list of tasks by applying the specified query."""

        if "WHERE" in query:
            query_where = query.split("WHERE")[1].strip()
            query_conditions = query_where.split("AND")
            conditions = {
                q.split("=")[0].strip(): p
                for q, p in zip(query_conditions, params)
            }
        else:
            conditions = {}

        rows = self.select(self.TABLE_NAME, ["json"], conditions=conditions)

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

        result = self.select(
            self.TABLE_NAME, ["id"], conditions={"id": str(task.session_id)}
        )
        return len(result) > 0
