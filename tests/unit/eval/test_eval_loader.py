import os

import pytest

from automata.eval import EvalSetLoader


@pytest.fixture
def loader():
    file_name = os.path.join(os.path.dirname(__file__), "test_payload.json")
    return EvalSetLoader(file_name)


def test_eval_loader(loader):
    assert loader.tasks, "No tasks loaded"
    assert loader.expected_actions, "No expected actions loaded"
    assert (
        loader.tasks[0].instructions == "Call Termination with result True"
    ), "Instruction not loaded correctly"
    assert (
        loader.expected_actions[0][0].name == "call_termination"
    ), "Call Termination not loaded correctly"
    assert loader.expected_actions[0][0].arguments == {
        "result": "True"
    }, "Call Termination not loaded correctly"
