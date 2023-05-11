import logging
import uuid
from collections.abc import Hashable
from enum import Enum
from typing import Callable, Optional

from automata.core.agent.automata_agent import AutomataAgent
from automata.core.agent.automata_agent_helpers import create_builder_from_args

logger = logging.getLogger(__name__)


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

    def __init__(self, *args, **kwargs):
        self.task_id = (
            self._deterministic_task_id(**kwargs)
            if kwargs.get("generate_deterministic_id", True)
            else uuid.uuid4()
        )
        self.priority = kwargs.get("priority", 0)
        self.max_retries = kwargs.get("max_retries", 3)
        self.observer: Optional[Callable] = None
        self.retry_count = 0

        self._task_dir: Optional[str] = None
        self._status = TaskStatus(kwargs.get("status", "setup"))

    def notify_observer(self):
        if self.observer:
            self.observer(self)

    @property
    def task_dir(self) -> Optional[str]:
        return self._task_dir

    @task_dir.setter
    def task_dir(self, new_task_dir: str) -> None:
        self._task_dir = new_task_dir
        self.notify_observer()

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
        seed = f"{kwargs_hash}"
        deterministic_uuid = uuid.uuid5(uuid.NAMESPACE_DNS, seed)

        return deterministic_uuid

    def __str__(self):
        return f"Task {self.task_id} ({self.status})"


class AutomataTask(Task):
    """
    A task that is to be executed by the TaskExecutor.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Check that we can create a builder from the args
        self.args = args
        self.kwargs = kwargs
        self.validate_initialization()
        self.rel_py_path = kwargs.get("rel_py_path", "")
        self.result = None
        self.error: Optional[str] = None

    def build_agent(self) -> AutomataAgent:
        """
        Builds the agent from the task args.
        """
        return create_builder_from_args(*self.args, **self.kwargs).build()

    def validate_initialization(self):
        """
        Validates that the task can be initialized.
        """
        create_builder_from_args(*self.args, **self.kwargs)

    def validate_pending(self):
        """
        Validates that the task can be executed.
        """
        if self.task_dir is None:
            raise ValueError("Task must have a task_dir set to be executed.")
        if self.status != TaskStatus.PENDING:
            raise ValueError("Task must be in pending state to be executed.")
