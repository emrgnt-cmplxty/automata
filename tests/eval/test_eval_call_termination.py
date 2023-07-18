import pytest

from automata.llm.eval.providers import OpenAIFunctionCallAction
from tests.utils.regression_utils import run_agent_and_get_eval


@pytest.mark.evaluation
@pytest.mark.parametrize(
    "instructions, agent_config_name, toolkit_list, model, max_iterations, expected_actions",
    [
        # A simple instruction set with expected actions
        (
            "This is a dummy instruction, return True.",
            "automata-main",
            [],
            "gpt-3.5-turbo-16k",
            1,
            [
                OpenAIFunctionCallAction(
                    name="call_termination", arguments={"result": "True"}
                )
            ],
        ),
    ],
)
def test_eval(
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
    # check if all expected actions were performed
    assert (
        eval_result.full_match
    ), f"Expected actions were not fully matched. Match result: {eval_result.match_result}"

    # check if no extra actions were performed
    assert (
        not eval_result.extra_actions
    ), f"Extra actions were performed: {eval_result.extra_actions}"
