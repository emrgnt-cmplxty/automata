import logging
from typing import List

from automata.config import AgentConfigName
from automata.eval import (
    Action,
    AgentEval,
    AgentEvalSetLoader,
    AgentEvaluationHarness,
    CodeWritingEval,
    OpenAIFunctionEval,
)
from automata.eval.composite import CompositeAgentEval
from automata.singletons.dependency_factory import dependency_factory
from automata.singletons.py_module_loader import py_module_loader
from automata.tasks import (
    AutomataAgentTaskDatabase,
    AutomataTask,
    AutomataTaskEnvironment,
    AutomataTaskExecutor,
    AutomataTaskRegistry,
    EnvironmentMode,
    IAutomataTaskExecution,
)
from automata.tools.factory import AgentToolFactory

logger = logging.getLogger(__name__)


def run_eval_harness(
    evals_filepath: str,
    evals: List[AgentEval] = [OpenAIFunctionEval(), CodeWritingEval()],
    *args,
    **kwargs,
) -> None:
    """
    Run evaluation for a list of tasks specified in a JSON file.

    Args:
        evals_filepath (str): Filepath to the JSON file containing evals.

    Returns:
        None
    """

    # Load the tasks and expected actions
    logger.info(f"Loading evals from {evals_filepath}...")
    eval_loader = AgentEvalSetLoader(evals_filepath)
    tasks = eval_loader.tasks
    tasks_expected_actions = eval_loader.tasks_expected_actions

    # Setup the tasks
    task_db = AutomataAgentTaskDatabase()
    environment = AutomataTaskEnvironment(
        environment_mode=EnvironmentMode.LOCAL_COPY
    )

    for task in eval_loader.tasks:
        registry = AutomataTaskRegistry(task_db)
        registry.register(task)
        environment.setup(task)

    # Create the evaluation harness
    evaluation_harness = AgentEvaluationHarness(evals)

    # Create the executor
    execution = IAutomataTaskExecution()
    task_executor = AutomataTaskExecutor(execution)

    # # Execute the evaluations
    metrics = evaluation_harness.evaluate(
        tasks, tasks_expected_actions, task_executor
    )

    # Log the metrics
    logging.info(f"Evaluation metrics: {metrics}")
