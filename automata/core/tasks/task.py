import logging
import uuid
from collections.abc import Hashable
from enum import Enum
from typing import Callable, Dict, Optional

from automata.cli.cli_utils import check_kwargs, process_kwargs
from automata.core.agent.automata_agent_utils import AutomataAgentFactory
from automata.core.manager.automata_manager_factory import AutomataManagerFactory

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
        self.args = args
        self.kwargs = kwargs
        # Check that args build a valid agent
        self.validate_initialization()
        self.path_to_root_py = kwargs.get("path_to_root_py", "")
        self.result = None
        self.error: Optional[str] = None

    def build_agent_manager(self):
        """
        Builds the agent from the task args.
        """
        pass
        helper_agent_names = self.kwargs.get("helper_agent_names", None)
        has_sub_agents = helper_agent_names is not None
        if has_sub_agents:
            check_kwargs(self.kwargs)
            kwargs = process_kwargs(**self.kwargs)
            logger.info(f"Passing in instructions:\n %s" % (kwargs.get("instructions")))
            logger.info("-" * 60)

            logger.info("Creating main agent...")
            main_agent = AutomataAgentFactory.create_agent(**kwargs)

            logger.info("Creating agent manager...")
            agent_manager = AutomataManagerFactory.create_manager(
                main_agent, kwargs.get("helper_agent_configs")
            )

            return agent_manager
        else:
            return AutomataManagerFactory.create_manager(
                AutomataAgentFactory.create_agent(*self.args, **self.kwargs), {}
            )

    def validate_initialization(self):
        """
        Validates that the task can be initialized.
        """
        self.build_agent_manager()

    def validate_pending(self):
        """
        Validates that the task can be executed.
        """
        if self.task_dir is None:
            raise ValueError("Task must have a task_dir set to be executed.")
        if self.status != TaskStatus.PENDING:
            raise ValueError("Task must be in pending state to be executed.")

    def to_partial_json(self) -> Dict[str, str]:
        """
        Returns a JSON representation of key attributes of the task.
        """
        result = {
            "task_id": str(self.task_id),
            "status": self.status.value,
            "priority": self.priority,
            "max_retries": self.max_retries,
            "retry_count": self.retry_count,
            "path_to_root_py": self.path_to_root_py,
            "result": self.result,
            "error": self.error,
        }
        result["model"] = self.kwargs.get("model", "gpt-4")
        result["llm_toolkits"] = self.kwargs.get("llm_toolkits", "")
        result["instructions"] = self.kwargs.get("instructions", None)
        result["instruction_payload"] = self.kwargs.get("instruction_payload", None)
        agent_config = self.kwargs.get("agent_config", None)
        if agent_config:
            result["agent_config"] = agent_config.config_name.value
            result["instruction_config"] = agent_config.instruction_version.value
        return result
