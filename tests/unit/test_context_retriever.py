import os

import pytest

from automata.code_parsers.py import PyContextRetriever, PyContextRetrieverConfig
from automata.core.utils import get_root_fpath
from automata.singletons.py_module_loader import py_module_loader


# TODO - Unify module loader fixture
@pytest.fixture(autouse=True)
def local_module_loader():
    # FIXME - This can't be a good pattern, let's cleanup later.
    py_module_loader.reset()
    py_module_loader.initialize(
        os.path.join(get_root_fpath(), "tests", "unit", "sample_modules"), "my_project"
    )
    yield py_module_loader


@pytest.fixture
def context_retriever():
    return PyContextRetriever(PyContextRetrieverConfig())


# def test_retrieve(context_retriever, local_module_loader):
#     print("local_module_loader = ", local_module_loader._dotpath_map.items())
#     assert False
