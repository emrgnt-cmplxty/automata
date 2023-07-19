import pytest

from automata.llm.eval.providers import OpenAIFunctionCallAction
from tests.utils.regression_utils import run_agent_and_get_eval


@pytest.mark.evaluation
@pytest.mark.parametrize(
    "instructions, agent_config_name, toolkit_list, model, max_iterations, expected_actions",
    [
        (
            "Fetch the source code for VectorDatabaseProvider.",
            "automata-main",
            ["py-reader"],
            "gpt-4",
            2,
            [
                OpenAIFunctionCallAction(
                    name="py-retriever-code",
                    arguments={
                        "module_path": "automata.core.base.database.vector",
                        "node_path": "VectorDatabaseProvider",
                    },
                )
            ],
        ),
    ],
)
def test_eval_read(
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

    assert (
        eval_result.full_match
    ), f"Expected actions were not fully matched.\nMatch Result: {eval_result.match_result}\nObserved Actions:{eval_result.observed_actions}\nExtra Actions: {eval_result.extra_actions}\n"


@pytest.mark.evaluation
@pytest.mark.parametrize(
    "instructions, agent_config_name, toolkit_list, model, max_iterations, expected_actions",
    [
        (
            "Create a new module with a hello world function at automata.test_module",
            "automata-main",
            ["py-writer"],
            "gpt-4",
            2,
            [
                OpenAIFunctionCallAction(
                    name="py-writer-create-new-module",
                    arguments={
                        "module_name": "automata.test_module",
                        "content": "def hello_world():\n    print('Hello, world!')",
                    },
                )
            ],
        ),
    ],
)
def test_eval_py_write(
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

    assert (
        eval_result.full_match
    ), f"Expected actions were not fully matched.\nMatch Result: {eval_result.match_result}\nExtra Actions: {eval_result.extra_actions}\n"
