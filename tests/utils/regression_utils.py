from typing import List

from automata.agent import OpenAIAutomataAgent
from automata.config import AgentConfigName, OpenAIAutomataAgentConfigBuilder
from automata.llm.eval import (
    Action,
    CodeWritingEval,
    CompositeEval,
    Eval,
    EvalResult,
    OpenAIFunctionEval,
)
from automata.singletons.dependency_factory import dependency_factory
from automata.singletons.py_module_loader import py_module_loader
from automata.tasks import (
    AutomataAgentTaskDatabase,
    AutomataTask,
    AutomataTaskEnvironment,
    AutomataTaskExecutor,
    EnvironmentMode,
    IAutomataTaskExecution,
)
from automata.tasks.registry import AutomataTaskRegistry
from automata.tools.factory import AgentToolFactory


def initialize_automata():
    py_module_loader.reset()
    dependency_factory.reset()
    py_module_loader.initialize()


def run_agent_and_get_eval(
    instructions: str,
    agent_config_name: str,
    toolkit_list: List[str],
    model: str,
    max_iterations: int,
    expected_actions: List[Action],
    evaluators: List[Eval] = [
        OpenAIFunctionEval(),
        CodeWritingEval(target_variables=["x", "y", "z"]),
    ],
) -> EvalResult:
    initialize_automata()

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

    return composite_evaluator.generate_eval_result(
        task, expected_actions, task_executor
    )


def run_agent_and_get_result(
    instructions: str,
    toolkit_list: List[str],
    model: str,
    agent_config_name: str,
    max_iterations: int,
) -> str:
    initialize_automata()

    tool_dependencies = dependency_factory.build_dependencies_for_tools(
        toolkit_list
    )
    tools = AgentToolFactory.build_tools(toolkit_list, **tool_dependencies)
    config_name = AgentConfigName(agent_config_name)
    agent_config_builder = (
        OpenAIAutomataAgentConfigBuilder.from_name(config_name)
        .with_tools(tools)
        .with_model(model)
    )

    agent_config_builder = agent_config_builder.with_max_iterations(
        max_iterations
    )

    agent = OpenAIAutomataAgent(
        instructions, config=agent_config_builder.build()
    )
    result = agent.run()
    return result.replace("Execution Result:\n", "").strip()
