import pytest

from automata.llm.eval.eval_providers import OpenAIFunctionCallAction
from tests.utils.regression_utils import run_agent_and_get_eval


@pytest.mark.evaluation
@pytest.mark.parametrize(
    "instructions, agent_config_name, toolkit_list, model, max_iterations, expected_actions",
    [
        (
            "What class should we instantiate to search the codebase for relevant symbols? Please return just the class name with no extra formatting.",
            "automata-main",
            ["context-oracle"],
            "gpt-4",
            2,
            [
                OpenAIFunctionCallAction(
                    name="call_termination",
                    arguments={"result": "SymbolSearch"},
                )
            ],
        ),
    ],
)
def test_eval_context(
    instructions,
    agent_config_name,
    toolkit_list,
    model,
    max_iterations,
    expected_actions,
):
    eval_result = run_agent_and_get_eval(
        instructions,
        agent_config_name,
        toolkit_list,
        model,
        max_iterations,
        expected_actions,
    )

    # TODO - Move to utils and avoid copy pasta across eval tests
    assert (
        eval_result.full_match
    ), f"Expected actions were not fully matched. Match result: {eval_result.match_result}"
