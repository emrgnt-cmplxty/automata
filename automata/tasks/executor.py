import logging
import logging.config
import time

from automata.agent import (
    AgentTaskGeneralError,
    AgentTaskStateError,
    OpenAIAutomataAgent,
)
from automata.config import OpenAIAutomataAgentConfigBuilder
from automata.memory_store import OpenAIAutomataConversationDatabase
from automata.tasks.automata_task import AutomataTask
from automata.tasks.base import ITaskExecution, Task, TaskStatus

logger = logging.getLogger(__name__)


class IAutomataTaskExecution(ITaskExecution):
    """Class for executing general tasks."""

    def execute(self, task: Task) -> None:
        """
        Executes the task by creating and running an AutomataAgent.
        Eachtime the execution fails, the task's retry count is incremented.
        After the maximum number of retries is reached, the task is marked as failed.

        Raises:
            Exception: If the task fails on execution
        """
        if not isinstance(task, AutomataTask):
            raise AgentTaskGeneralError(
                "AutomataTaskEnvironment requires an AutomataTask instance"
            )
        task.status = TaskStatus.RUNNING
        try:
            agent = IAutomataTaskExecution._build_agent(task)
            result = agent.run()
            task.result = result
            task.status = TaskStatus.SUCCESS
        except Exception as e:
            logger.exception(f"AutomataTask failed: {e}")
            task.error = str(e)
            task.status = TaskStatus.FAILED
            task.retry_count += 1
            raise e

    @staticmethod
    def _build_agent(task: AutomataTask) -> OpenAIAutomataAgent:
        """
        Uses the task's arguments to build an AutomataAgent from
        the OpenAIAutomataAgentConfigBuilder.
        TODO - Consider explicitly passing args to the ConfigFactory
               Instead of passing kwargs to the create_config method.
        """
        agent_config = OpenAIAutomataAgentConfigBuilder.create_from_args(
            session_id=str(task.task_id), **task.kwargs
        )

        agent = OpenAIAutomataAgent(
            task.instructions,
            agent_config,
        )

        if task.record_conversation:
            # Initialize the OpenAIAutomataConversationDatabase and set it to the agent
            db_provider = OpenAIAutomataConversationDatabase(
                session_id=str(task.task_id)
            )
            agent.set_database_provider(db_provider)

        return agent


class AutomataTaskExecutor:
    """A class for using ITaskExecution behavior to execute a task."""

    def __init__(self, execution: ITaskExecution) -> None:
        self.execution = execution

    def execute(self, task: AutomataTask) -> None:
        """
        Executes the task using the specified execution behavior.

        This method will retry the task if it fails,
        until the maximum number of retries is reached.

        Raises Exception:
            If the task is not status PENDING.
            If the task fails and the maximum number of retries is reached.
        """
        if task.status != TaskStatus.PENDING:
            raise AgentTaskStateError(
                f"Cannot execute task because task is not in PENDING state. Task status = {task.status}"
            )
        for attempt in range(task.max_retries):
            try:
                logger.debug(f"Executing task {task.task_id}")
                task.status = TaskStatus.RUNNING
                self.execution.execute(task)
                task.status = TaskStatus.SUCCESS
                logger.info(f"Task {task.task_id} executed successfully.")
                break

            except Exception as e:
                logging.exception(f"AutomataTask failed: {e}")
                task.status = TaskStatus.RETRYING
                task.error = str(e)

                # If we've used up all retries, re-raise the exception
                if attempt == task.max_retries - 1:
                    raise e

                # Otherwise, wait before retrying
                time.sleep(AutomataTaskExecutor._exponential_backoff(attempt))

    @staticmethod
    def _exponential_backoff(attempt_number: int) -> int:
        return 2**attempt_number  # Exponential backoff in seconds
