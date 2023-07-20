from typing import List, Type

from automata.agent import OpenAIAgentProvider, OpenAIAutomataAgent
from automata.config import AgentConfigName, OpenAIAutomataAgentConfigBuilder
from automata.llm.eval import (
    CompositeEval,
    Eval,
    EvalResult,
    OpenAIFunctionEval,
)
from automata.singletons.dependency_factory import dependency_factory
from automata.singletons.py_module_loader import py_module_loader
from automata.tools.factory import AgentToolFactory


def initialize_automata():
    py_module_loader.reset()
    dependency_factory.reset()
    py_module_loader.initialize()


def run_agent_and_get_eval(
    instructions,
    agent_config_name,
    toolkit_list,
    model,
    max_iterations,
    expected_actions,
    evaluator_classes: List[Type[Eval]] = [OpenAIFunctionEval],
) -> EvalResult:
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
        .with_max_iterations(max_iterations)
    )
    agent_config = agent_config_builder.build()
    composite_evaluator = CompositeEval(
        agent_provider=OpenAIAgentProvider(agent_config),
        evaluator_classes=evaluator_classes,
    )

    return composite_evaluator.generate_eval_result(
        instructions, expected_actions
    )


def run_agent_and_get_result(
    instructions, toolkit_list, model, agent_config_name, max_iterations
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
