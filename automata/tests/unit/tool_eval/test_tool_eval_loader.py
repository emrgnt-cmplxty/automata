import os

import pytest

from automata.eval import ToolEvalSetLoader


@pytest.fixture
def loader():
    file_name = os.path.join(
        os.path.dirname(__file__), "test_tool_payload.json"
    )
    return ToolEvalSetLoader(file_name)


def test_tool_eval_loader(loader):
    assert loader.input_functions, "No function calls loaded"
    assert loader.expected_actions, "No expected actions loaded"
    assert (
        loader.input_functions[0].name == "call_termination"
    ), "Function call not loaded correctly"
    assert loader.input_functions[0].arguments == {
        "result": "True"
    }, "Function call arguments not loaded correctly"

    assert (
        loader.expected_actions[0].query == "GitHubClient"
    ), "Expected action not loaded correctly"
