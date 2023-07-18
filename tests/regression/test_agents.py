import logging

import pytest

from automata.agent import OpenAIAutomataAgent
from automata.config import AgentConfigName, OpenAIAutomataAgentConfigBuilder
from automata.singletons.dependency_factory import dependency_factory
from automata.tools.factory import AgentToolFactory
from tests.utils.regression_utils import initialize_automata

logger = logging.getLogger(__name__)


# Uncomment if using gpt-3.5-turbo-16k
# @pytest.mark.flaky(
#     reruns=5
# )  # allowing up to 5 retries if using gpt-3.5-turbo-16k
@pytest.mark.regression
@pytest.mark.parametrize(
    "instructions, toolkit_list, model, agent_config_name, max_iterations, allowable_results",
    [
        # A simple 'hello-world' style instruction
        (
            "This is a dummy instruction, return True.",
            ["context-oracle"],
            "gpt-3.5-turbo-16k",
            "automata-main",
            1,
            ["True"],
        ),
        # A simple context search for `SymbolSearch`
        (
            "What class should we instantiate to search the codebase for relevant symbols? Please return just the class name.",
            ["context-oracle"],
            "gpt-4",
            "automata-main",
            2,
            ["SymbolSearch", "`SymbolSearch`"],
        ),
        # A simple context search for `OpenAIAutomataAgentConfig`
        (
            "What class is responsible for building OpenAI Agent configurations? Please jsut return the class name.",
            ["context-oracle"],
            "gpt-4",
            "automata-main",
            2,
            [
                "OpenAIAutomataAgentConfigBuilder",
                "`OpenAIAutomataAgentConfigBuilder`",
                "OpenAIAutomataAgentConfig",  # this is not the correct result, but let's allow it for now
                "`OpenAIAutomataAgentConfig`",  # same
            ],
        ),
        # Extracting source code directly from a module
        (
            "Fetch the source code for the module at 'automata.core.utils'.",
            ["py-reader"],
            "gpt-4",
            "automata-main",
            2,
            [],
        ),
    ],
)
def test_agent_execution(
    instructions,
    toolkit_list,
    model,
    agent_config_name,
    max_iterations,
    allowable_results,
):
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
    result = result.replace("Execution Result:\n", "").strip()
    if result not in allowable_results:
        raise ValueError(
            f"Allowable results={allowable_results}, found result={result}"
        )
