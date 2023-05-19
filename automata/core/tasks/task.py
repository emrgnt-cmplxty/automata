import logging
import os
import uuid
from collections.abc import Hashable
from enum import Enum
from typing import Callable, Dict, Optional

from automata.cli.cli_utils import check_kwargs, create_instructions_and_config_from_kwargs
from automata.config import TASKS_DIR_PATH
from automata.core.agent.automata_agent_utils import AutomataAgentFactory
from automata.core.manager.automata_manager_factory import AutomataManagerFactory
from automata.core.utils import get_logging_config, root_path

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

    TASK_LOG_NAME = "task_TASK_ID.log"
    TASK_LOG_REL_DIR = "logs"

    def __init__(self, *args, **kwargs):
        self.task_id = (
            self._deterministic_task_id(**kwargs)
            if kwargs.get("generate_deterministic_id", True)
            else uuid.uuid4()
        )
        self.priority = kwargs.get("priority", 0)
        self.max_retries = kwargs.get("max_retries", 3)
        self._status = TaskStatus(kwargs.get("status", "setup"))
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
        seed = f"{kwargs_hash}"
        deterministic_uuid = uuid.uuid5(uuid.NAMESPACE_DNS, seed)

        return deterministic_uuid

    def _get_task_dir(self) -> str:
        # Generate a unique directory name for the task
        return os.path.join(Task._get_tasks_dir(), f"task_{self.task_id}")

    @staticmethod
    def _get_tasks_dir() -> str:
        return (
            TASKS_DIR_PATH
            if TASKS_DIR_PATH != "tasks"
            else os.path.join(root_path(), TASKS_DIR_PATH)
        )

    @staticmethod
    def _get_log_dir() -> str:
        # Generate a unique directory name for the task
        return os.path.join(Task._get_tasks_dir(), Task.TASK_LOG_REL_DIR)

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
        helper_agent_names = self.kwargs.get("helper_agent_names", None)
        has_sub_agents = helper_agent_names is not None
        # Set the session id to the task id
        self.kwargs["session_id"] = str(self.task_id)
        instructions, main_config = create_instructions_and_config_from_kwargs(**self.kwargs)
        if has_sub_agents:
            check_kwargs(self.kwargs)
            logger.debug(f"Passing in instructions:\n %s" % (instructions))
            logger.debug("-" * 60)

            logger.debug("Creating main agent...")
            main_agent = AutomataAgentFactory.create_agent(
                instructions=instructions, config=main_config
            )

            logger.debug("Creating agent manager...")
            agent_manager = AutomataManagerFactory.create_manager(
                main_agent, main_config.helper_agent_configs
            )

            return agent_manager
        else:
            return AutomataManagerFactory.create_manager(
                AutomataAgentFactory.create_agent(instructions=instructions, config=main_config),
                {},
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
        result["llm_toolkits"] = self.kwargs.get("llm_toolkits", "").split(",")
        result["instructions"] = self.kwargs.get("instructions", None)
        result["instruction_payload"] = self.kwargs.get("instruction_payload", None)
        main_config = self.kwargs.get("main_config", None)
        if main_config:
            result["main_config"] = main_config.config_name.value
            result["instruction_config"] = main_config.instruction_version.value

        main_config_name = self.kwargs.get("main_config_name", None)
        if main_config_name:
            result["main_config"] = main_config_name
            result["instruction_config"] = create_instructions_and_config_from_kwargs(
                **self.kwargs
            )[1].instruction_version.value

        helper_agent_configs = self.kwargs.get("helper_agent_configs", None)
        if helper_agent_configs:
            result["helper_agent_names"] = [
                main_config.config_name.value for main_config in helper_agent_configs.values()
            ]

        helper_agent_names = self.kwargs.get("helper_agent_names", None)
        if helper_agent_names:
            result["helper_agent_names"] = helper_agent_names
        return result

    def initialize_logging(self) -> None:
        log_dir = self._get_log_dir()
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)

        log_file = os.path.join(log_dir, Task.TASK_LOG_NAME.replace("TASK_ID", str(self.task_id)))
        log_level = logging.DEBUG if self.kwargs.get("verbose") else logging.INFO
        logging.config.dictConfig(get_logging_config(log_level=log_level, log_file=log_file))
        logging.debug("Logging initialized.")

    def get_logs(self) -> str:
        log_dir = self._get_log_dir()
        log_file = os.path.join(log_dir, Task.TASK_LOG_NAME.replace("TASK_ID", str(self.task_id)))

        if os.path.exists(log_file):
            with open(log_file, "r") as f:
                log_content = f.read()
            return log_content
        else:
            raise FileNotFoundError(f"Log file {log_file} not found.")
