import os
import uuid
from abc import ABC, abstractmethod
from collections.abc import Hashable
from enum import Enum
from typing import Any, Callable, Optional

from automata.config import TASK_OUTPUT_PATH


class TaskStatus(Enum):
    CREATED = "created"
    REGISTERED = "registered"
    PENDING = "pending"
    RUNNING = "running"
    SUCCESS = "success"
    COMMITTED = "committed"
    FAILED = "failed"
    RETRYING = "retrying"


class Task:
    """
    A generic `Task` object used by the `TaskExecutor`.

    A `Task` is responsible for storing the task id, priority, and max retries.
    It receives kwargs that are passed to the task function when the task is executed.
    It also exposes a method to generate a deterministic task id based on the hash of the hashable kwargs.
    """

    TASK_LOG_NAME = "task_SESSION_ID.log"
    TASK_LOG_REL_DIR = "logs"

    def __init__(self, *args, **kwargs) -> None:
        # sourcery skip: remove-redundant-if
        """
        Initializes a task object.

        Keyword Args:
            generate_deterministic_id (bool): Whether to generate a deterministic task id or not.
              In the case of a deterministic task id, the task id is generated based on the hash of
              the hashable kwargs. Defaults to False.
            priority (int): The priority of the task. Defaults to 0.
            max_retries (int): The maximum number of retries for the task. Defaults to 3.
        """

        if (
            "generate_deterministic_id" in kwargs
            and "session_id" not in kwargs
        ):
            self.session_id = self._deterministic_session_id(**kwargs)
        elif (
            "session_id" in kwargs
            and "generate_deterministic_id" not in kwargs
        ):
            self.session_id = kwargs["session_id"]
        elif "generate_deterministic_id" in kwargs and "session_id" in kwargs:
            raise ValueError(
                "Values for both session_id and generate_deterministic_id cannot be provided."
            )
        else:
            self.session_id = uuid.uuid4()

        self.priority = kwargs.get("priority", 0)
        self.max_retries = kwargs.get("max_retries", 3)
        self._status = TaskStatus.CREATED
        self.retry_count = 0
        self.observer: Optional[Callable] = None
        self.task_dir = self._get_task_dir(
            kwargs.get("task_dir", TASK_OUTPUT_PATH)
        )
        self.result: Optional[str] = None
        self.error: Optional[str] = None

    def __str__(self):
        return f"Task {self.session_id} ({self.status})"

    def notify_observer(self) -> None:
        """
        Used to notify the observer when the task status changes.
        """
        if self.observer:
            self.observer(self)

    @property
    def status(self) -> TaskStatus:
        """
        The status of the task is updated by the task executor as the task progresses through
        different stages of execution.
        """
        return self._status

    @status.setter
    def status(self, new_status: TaskStatus) -> None:
        """
        Sets the status of the `Task`.

        If the new status is RETRYING, the retry count is incremented
        and the task status is set to FAILED if the retry count exceeds the max retries.
        """
        if new_status == TaskStatus.RETRYING:
            self.retry_count += 1
            if self.retry_count == self.max_retries:
                self._status = TaskStatus.FAILED
            else:
                self._status = new_status
        else:
            self._status = new_status
        self.notify_observer()

    def _deterministic_session_id(self, **kwargs) -> uuid.UUID:
        """
        Returns a deterministic session id for the task which is
        generated based on the hash of the hashable kwargs.

        Keyword Args:
            kwargs (dict): The keyword arguments passed to the task.
        """
        # Generate the hash of the hashable kwargs
        hashable_items = sorted(
            [item for item in kwargs.items() if isinstance(item[1], Hashable)]
        )
        kwargs_hash = hash(tuple(hashable_items))

        # Combine the hashes and use it as a seed for generating a deterministic UUID
        return uuid.uuid5(uuid.NAMESPACE_DNS, f"{kwargs_hash}")

    def _get_task_dir(self, base_dir: str) -> str:
        """
        Gets the output directory for the task.
        Use of the session_id as the directory name ensures that the task directory is unique.
        """
        return os.path.join(base_dir, f"task_{self.session_id}")

    def _get_log_dir(self) -> str:
        """
        Gets the output directory where task logs are saved."""
        return os.path.join(self.task_dir, Task.TASK_LOG_REL_DIR)


class ITaskExecution(ABC):
    """Interface for task execution behaviors."""

    @abstractmethod
    def execute(self, task: Task) -> Any:
        pass


class TaskEnvironment(ABC):
    """An abstract base class for implementing a task environment."""

    @abstractmethod
    def setup(self, task: Task):
        """Set up the environment."""
        pass

    @abstractmethod
    def teardown(self):
        """Tear down the environment."""
        pass

    @abstractmethod
    def validate(self):
        """Validate the environment."""
        pass

    @abstractmethod
    def reset(self):
        """Reset the environment to its initial state."""
        pass
