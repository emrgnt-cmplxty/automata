import pytest

from automata.config import AgentConfigName, OpenAIAutomataAgentConfigBuilder
from automata.llm.eval.providers import OpenAIEval, OpenAIFunctionCallAction
from automata.singletons.dependency_factory import dependency_factory
from automata.tools.factory import AgentToolFactory
from tests.utils.regression_utils import initialize_automata


@pytest.mark.evaluation
@pytest.mark.parametrize(
    "instructions, toolkit_list, expected_actions, model, agent_config_name, max_iterations",
    [
        # A simple instruction set with expected actions
        (
            "This is a dummy instruction, return True.",
            [],
            [
                OpenAIFunctionCallAction(
                    name="call_termination", arguments={"value": "True"}
                )
            ],  # expected action
            "gpt-3.5-turbo-16k",
            "automata-main",
            1,
        ),
    ],
)
def test_eval(
    instructions,
    toolkit_list,
    expected_actions,
    model,
    agent_config_name,
    max_iterations,
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

    evaluator = OpenAIEval(config=agent_config_builder.build())
    eval_result = evaluator.generate_eval_result(
        instructions, expected_actions
    )

    # check if all expected actions were performed
    assert (
        eval_result.full_match
    ), f"Expected actions were not fully matched. Match result: {eval_result.match_result}"

    # check if no extra actions were performed
    assert (
        not eval_result.extra_actions
    ), f"Extra actions were performed: {eval_result.extra_actions}"
