import os

import pytest

from automata.eval import AgentEvalSetLoader


@pytest.fixture
def loader():
    file_name = os.path.join(os.path.dirname(__file__), "test_payload.json")
    return AgentEvalSetLoader(file_name)


def test_eval_loader(loader):
    assert loader.tasks, "No tasks loaded"
    assert loader.tasks_expected_actions, "No expected actions loaded"
    assert (
        loader.tasks[0].instructions == "Call Termination with result True"
    ), "Instruction not loaded correctly"
    assert (
        loader.tasks_expected_actions[0][0].name == "call-termination"
    ), "Call Termination not loaded correctly"
    assert loader.tasks_expected_actions[0][0].arguments == {
        "result": "True"
    }, "Call Termination not loaded correctly"

    assert (
        loader.tasks[1].instructions
        == "Return a markdown python snippet which when executed creates a `CodeWritingAction`."
    ), "Instruction not loaded correctly"
