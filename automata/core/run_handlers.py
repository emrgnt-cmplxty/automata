from typing import List, Optional, Tuple

from automata.agent import OpenAIAutomataAgent
from automata.config import AgentConfigName, OpenAIAutomataAgentConfigBuilder
from automata.core.utils import get_root_fpath
from automata.singletons.dependency_factory import dependency_factory
from automata.singletons.py_module_loader import py_module_loader
from automata.tasks import (
    AutomataTask,
    AutomataTaskEnvironment,
    AutomataTaskExecutor,
    IAutomataTaskExecution,
    ITaskExecution,
)
from automata.tasks.registry import AutomataTaskRegistry
from automata.tools import Tool
from automata.tools.factory import AgentToolFactory


def initialize_automata(
    root_fpath: str = get_root_fpath(), project_name: str = "automata"
):
    """Initialize the automata environment."""

    py_module_loader.reset()
    dependency_factory.reset()
    py_module_loader.initialize(root_fpath, project_name)


def run_setup(
    agent_config: str,
    toolkit_list: Optional[List[str]] = None,
    root_fpath: str = get_root_fpath(),
    project_name: str = "automata",
) -> Tuple[List[Tool], AgentConfigName]:
    """Setup the automata environment."""

    initialize_automata(root_fpath, project_name)
    agent_config_name = AgentConfigName(agent_config)

    if toolkit_list is None:
        toolkit_list = []

    tool_dependencies = dependency_factory.build_dependencies_for_tools(
        toolkit_list
    )
    tools = AgentToolFactory.build_tools(toolkit_list, **tool_dependencies)

    return tools, agent_config_name


def run_with_agent(
    instructions: str,
    config_name: AgentConfigName,
    tools: List[Tool],
    model: str,
    max_iterations: int,
) -> OpenAIAutomataAgent:
    """Run an agent with the given parameters."""

    agent_config_builder = (
        OpenAIAutomataAgentConfigBuilder.from_name(config_name)
        .with_tools(tools)
        .with_model(model)
        .with_max_iterations(max_iterations)
    )

    agent = OpenAIAutomataAgent(
        instructions, config=agent_config_builder.build()
    )
    agent.run()
    return agent


def create_task(
    instructions: str,
    config_name: AgentConfigName,
    tools: List[Tool],
    model: str,
    max_iterations: int,
    task_registry: AutomataTaskRegistry,
    task_environment: AutomataTaskEnvironment,
) -> AutomataTask:
    """Create a task with the given parameters."""

    task = AutomataTask(
        instructions=instructions,
        config_to_load=config_name,
        model=model,
        max_iterations=max_iterations,
        tools=tools,
    )

    # Register and setup task
    task_registry.register(task)
    task_environment.setup(task)

    return task


def run_with_task(
    instructions: str,
    config_name: AgentConfigName,
    tools: List[Tool],
    model: str,
    max_iterations: int,
    task_registry: AutomataTaskRegistry,
    task_environment: AutomataTaskEnvironment,
    task_execution: ITaskExecution = IAutomataTaskExecution(),
) -> AutomataTask:
    """Run a task with the given parameters."""

    task = create_task(
        instructions,
        config_name,
        tools,
        model,
        max_iterations,
        task_registry,
        task_environment,
    )

    # Create the executor and execute the task
    task_executor = AutomataTaskExecutor(task_execution)
    task_executor.execute(task)
    return task
