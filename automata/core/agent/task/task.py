import logging
import logging.config
import os
from typing import Optional

from automata.config.agent_config_builder import AutomataAgentConfigFactory
from automata.core.agent.agent import AutomataAgent
from automata.core.base.task import Task, TaskStatus
from automata.core.utils import get_logging_config, root_py_fpath

logger = logging.getLogger(__name__)


class AutomataMissingInstructions(Exception):
    """
    Exception raised when no instructions are provided for the task.
    """

    def __init__(self):
        super().__init__("No instructions provided for the task.")


class AutomataTask(Task):
    """
    A task that is to be executed by the TaskExecutor.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.args = args
        self.kwargs = kwargs
        if "instructions" not in self.kwargs or self.kwargs["instructions"] == "":
            raise AutomataMissingInstructions()
        self.instructions = self.kwargs["instructions"]
        self.result: Optional[str] = None
        self.error: Optional[str] = None
        self.path_to_root_py = kwargs.get("path_to_root_py", root_py_fpath())

    def build_agent(self) -> AutomataAgent:
        """
        Builds the agent for the task.

        Returns:
            AutomataAgent: The agent for the task.
        """
        agent_config = AutomataAgentConfigFactory().create_config(**self.kwargs)
        agent = AutomataAgent(
            self.instructions,
            agent_config,
        )
        agent.setup()
        return agent

    def validate_pending(self):
        """
        Validates that the task can be executed.

        Raises:
            ValueError: If the task is not in the pending state.

        """
        if self.status != TaskStatus.PENDING:
            raise ValueError("Task must be in pending state to be executed.")

    def initialize_logging(self) -> None:
        """
        Initializes logging for the task by creating a log file in the task directory.
        If the task directory does not exist, it is created.
        """
        log_dir = self._get_log_dir()
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)

        log_file = os.path.join(log_dir, Task.TASK_LOG_NAME.replace("TASK_ID", str(self.task_id)))
        log_level = logging.DEBUG if self.kwargs.get("verbose") else logging.INFO
        logging.config.dictConfig(get_logging_config(log_level=log_level, log_file=log_file))
        logging.debug("Logging initialized.")

    def get_logs(self) -> str:
        """
        Gets the logs for the task.

        Returns:
            str: The logs for the task.

        Raises:
            FileNotFoundError: If the log file for the task does not exist.
        """
        log_dir = self._get_log_dir()
        log_file = os.path.join(log_dir, Task.TASK_LOG_NAME.replace("TASK_ID", str(self.task_id)))

        if not os.path.exists(log_file):
            raise FileNotFoundError(f"Log file {log_file} not found.")
        with open(log_file, "r") as f:
            log_content = f.read()
        return log_content
