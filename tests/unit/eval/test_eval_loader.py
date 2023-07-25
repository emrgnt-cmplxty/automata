import os

import pytest

from automata.eval import EvalSetLoader


@pytest.fixture
def loader():
    file_name = os.path.join(os.path.dirname(__file__), "test_payload.json")
    return EvalSetLoader(file_name)


def test_eval_loader(loader):
    _ = loader
