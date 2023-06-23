import os
import uuid
from collections.abc import Hashable
from enum import Enum
from typing import Callable, Optional

from automata.config import TASK_OUTPUT_PATH
from automata.core.utils import root_fpath


class TaskStatus(Enum):
    SETUP = "setup"
    PENDING = "pending"
    RUNNING = "running"
    SUCCESS = "success"
    COMMITTED = "committed"
    FAILED = "failed"
    RETRYING = "retrying"


class Task:
    """
    A generic task object.
    """

    TASK_LOG_NAME = "task_TASK_ID.log"
    TASK_LOG_REL_DIR = "logs"

    def __init__(self, *args, **kwargs):
        """
        Initializes a task object.

        Keyword Args:
            generate_deterministic_id (bool): Whether to generate a deterministic task id or not.
              In the case of a deterministic task id, the task id is generated based on the hash of
              the hashable kwargs. Defaults to False.
            priority (int): The priority of the task. Defaults to 0.
            max_retries (int): The maximum number of retries for the task. Defaults to 3.
        """
        self.task_id = (
            self._deterministic_task_id(**kwargs)
            if kwargs.get("generate_deterministic_id", False)
            else uuid.uuid4()
        )
        self.priority = kwargs.get("priority", 0)
        self.max_retries = kwargs.get("max_retries", 3)
        self._status = TaskStatus.SETUP
        self.retry_count = 0
        self.observer: Optional[Callable] = None
        self.task_dir = self._get_task_dir()

    def notify_observer(self):
        if self.observer:
            self.observer(self)

    @property
    def status(self) -> TaskStatus:
        return self._status

    @status.setter
    def status(self, new_status) -> None:
        if new_status == TaskStatus.RETRYING:
            self.retry_count += 1
            if self.retry_count == self.max_retries:
                self._status = TaskStatus.FAILED
            else:
                self._status = new_status
        else:
            self._status = new_status
        self.notify_observer()

    def _deterministic_task_id(self, **kwargs):
        """
        Returns a deterministic session id for the task.
        """
        # Generate the hash of the hashable kwargs
        hashable_items = sorted([item for item in kwargs.items() if isinstance(item[1], Hashable)])
        kwargs_hash = hash(tuple(hashable_items))

        # Combine the hashes and use it as a seed for generating a deterministic UUID
        return uuid.uuid5(uuid.NAMESPACE_DNS, f"{kwargs_hash}")

    def _get_task_dir(self) -> str:
        # Generate a unique directory name for the task
        return os.path.join(Task._get_tasks_dir(), f"task_{self.task_id}")

    @staticmethod
    def _get_tasks_dir() -> str:
        return (
            TASK_OUTPUT_PATH
            if TASK_OUTPUT_PATH != "tasks"
            else os.path.join(root_fpath(), TASK_OUTPUT_PATH)
        )

    @staticmethod
    def _get_log_dir() -> str:
        # Generate a unique directory name for the task
        return os.path.join(Task._get_tasks_dir(), Task.TASK_LOG_REL_DIR)

    def __str__(self):
        return f"Task {self.task_id} ({self.status})"
