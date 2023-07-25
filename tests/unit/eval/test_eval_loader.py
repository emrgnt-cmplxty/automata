import os

import pytest

from automata.eval import EvalTaskLoader


@pytest.fixture
def loader():
    file_name = os.path.join(os.path.dirname(__file__), "test_payload.json")
    return EvalTaskLoader(file_name)


def test_eval_loader(loader):
    print("loader = ", loader)

    assert False
