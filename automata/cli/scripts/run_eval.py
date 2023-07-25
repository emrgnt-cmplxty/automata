from typing import List

from automata.config import AgentConfigName
from automata.eval import (
    Action,
    CodeWritingEval,
    CompositeEval,
    EvalResultDatabase,
    OpenAIFunctionEval,
)
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


def initialize_automata():
    py_module_loader.reset()
    dependency_factory.reset()
    py_module_loader.initialize()


if __name__ == "__main__":
    initialize_automata()

    instructions = """Return True"""
    agent_config_name = "automata-main"
    toolkit_list = ["py-writer"]
    model = "gpt-3.5-turbo"
    max_iterations = 2
    evaluators = [OpenAIFunctionEval(), CodeWritingEval()]
    expected_actions: List[Action] = []

    # Create a task
    tool_dependencies = dependency_factory.build_dependencies_for_tools(
        toolkit_list
    )
    tools = AgentToolFactory.build_tools(toolkit_list, **tool_dependencies)

    config_name = AgentConfigName(agent_config_name)

    task = AutomataTask(
        instructions=instructions,
        config_to_load=config_name,
        model=model,
        max_iterations=max_iterations,
        tools=tools,
    )

    # Register and setup task
    task_db = AutomataAgentTaskDatabase()
    registry = AutomataTaskRegistry(task_db)
    registry.register(task)

    environment = AutomataTaskEnvironment(
        environment_mode=EnvironmentMode.LOCAL_COPY
    )
    environment.setup(task)

    # Create the executor
    execution = IAutomataTaskExecution()
    task_executor = AutomataTaskExecutor(execution)

    composite_evaluator = CompositeEval(
        evaluators,
    )

    result = composite_evaluator.generate_eval_result(
        task, expected_actions, task_executor
    )

    # Write result to database
    eval_db = EvalResultDatabase()
    print(f"Result = {result}")
    eval_db.write_result(result)
