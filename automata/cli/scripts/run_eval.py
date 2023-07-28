import logging
from typing import List

from automata.cli.cli_utils import initialize_py_module_loader
from automata.eval import (
    AgentEvalResultDatabase,
    AgentEvalSetLoader,
    AgentEvaluationHarness,
    CodeWritingEval,
    OpenAIFunctionEval,
)
from automata.eval.agent.agent_eval import AgentEval
from automata.singletons.dependency_factory import dependency_factory
from automata.tasks import (
    AutomataAgentTaskDatabase,
    AutomataTaskEnvironment,
    AutomataTaskExecutor,
    AutomataTaskRegistry,
    EnvironmentMode,
    IAutomataTaskExecution,
)
from automata.tools.agent_tool_factory import AgentToolFactory

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

    toolkits = kwargs.get("toolkits")
    if toolkits is not None and not isinstance(toolkits, str):
        raise ValueError("Toolkits must be a string or None.")
    elif toolkits is None:
        toolkits = []
    else:
        toolkits = toolkits.split(",")

    tool_dependencies = dependency_factory.build_dependencies_for_tools(
        toolkits
    )
    tools = AgentToolFactory.build_tools(toolkits, **tool_dependencies)

    eval_loader = AgentEvalSetLoader(
        evals_filepath,
        model=kwargs.get("model", "gpt-4"),
        config_to_load=kwargs.get("config_to_load", "automata-main"),
        tools=tools,
    )
    tasks = eval_loader.tasks
    tasks_expected_actions = eval_loader.tasks_expected_actions

    # Setup the tasks
    task_db = AutomataAgentTaskDatabase()
    task_environment = AutomataTaskEnvironment(
        environment_mode=EnvironmentMode.LOCAL_COPY
    )
    task_registry = AutomataTaskRegistry(task_db)

    for task in eval_loader.tasks:
        task_registry.register(task)
        task_environment.setup(task)

    # Create the evaluation harness
    eval_database = AgentEvalResultDatabase()
    evaluation_harness = AgentEvaluationHarness(evals, eval_database)

    # Create the executor
    execution = IAutomataTaskExecution()
    task_executor = AutomataTaskExecutor(execution)

    # Execute the evaluations
    metrics = evaluation_harness.evaluate(
        tasks, tasks_expected_actions, task_executor
    )

    # Log the metrics
    logging.info(f"Evaluation metrics: {metrics}")


def main(*args, **kwargs) -> None:
    """Main entrypoint for the run_eval script."""

    initialize_py_module_loader(**kwargs)
    run_eval_harness(**kwargs)
