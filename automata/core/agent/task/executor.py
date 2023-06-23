import logging
import logging.config
import time

from automata.config.agent_config_builder import AutomataAgentConfigFactory
from automata.core.agent.agent import AutomataAgent
from automata.core.agent.task.task import AutomataTask
from automata.core.base.task import ITaskExecution, Task, TaskStatus

logger = logging.getLogger(__name__)


class IAutomataTaskExecution(ITaskExecution):
    """
    Class for executing general tasks.
    """

    def execute(self, task: Task) -> None:
        """
        Executes the task by creawting and running an AutomataAgent
        Incremetns the task's retry count if the task fails.

        Raises:
            Exception: If the task fails on execution
        """
        if not isinstance(task, AutomataTask):
            raise TypeError("AutomataTaskEnvironment requires an AutomataTask instance")

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
    def _build_agent(task: AutomataTask) -> AutomataAgent:
        """
        Builds the agent for the task.

        Returns:
            AutomataAgent: The agent for the task.

        TODO - Consider explicitly passing args to the ConfigFactory
               Instead of passing kwargs to the create_config method.
        """
        print("task.kwargs = ", task.kwargs)
        agent_config = AutomataAgentConfigFactory().create_config(**task.kwargs)
        agent = AutomataAgent(
            task.instructions,
            agent_config,
        )
        agent.setup()
        return agent


class AutomataTaskExecutor:
    """
    Class for executing tasks using different behaviors.
    """

    def __init__(self, execution: ITaskExecution) -> None:
        """
        Args:
            execution (ITaskExecution): The behavior to use for executing the task.
        """
        self.execution = execution

    def execute(self, task: AutomataTask) -> None:
        """
        Executes the task using the specified execution behavior.

        This method will retry the task if it fails,
        until the maximum number of retries is reached.

        Args:
            task (AutomataTask): The task to execute.

        Raises:
            Exception: If the task is not status PENDING.
            Exception: If the task fails and the maximum number of retries is reached.
        """
        if task.status != TaskStatus.PENDING:
            raise Exception(
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
        """
        Waits for a specified amount of time before retrying the task

        Args:
            attempt_number (int): The number of the current attempt.

        Returns:
            int: The amount of time to wait before retrying the task.
        """
        return 2**attempt_number  # Exponential backoff in seconds
