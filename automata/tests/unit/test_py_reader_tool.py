import os
from unittest.mock import MagicMock

import pytest

from automata.core.code_handling.py.reader import PyReader
from automata.core.singletons.py_module_loader import py_module_loader
from automata.core.tools.base import Tool
from automata.core.tools.builders.py_reader import PyReaderToolkitBuilder
from automata.core.utils import get_root_py_fpath


@pytest.fixture(autouse=True)
def module_loader():
    py_module_loader.initialize(
        os.path.join(get_root_py_fpath(), "tools", "tool_management"),
        os.path.join(get_root_py_fpath(), "tools", "tool_management", "tests"),
    )
    yield py_module_loader
    py_module_loader._dotpath_map = None
    py_module_loader.initialized = False
    py_module_loader.py_fpath = None
    py_module_loader.root_fpath = None


@pytest.fixture
def python_retriever_tool_builder():
    python_code_retriever = PyReader()
    return PyReaderToolkitBuilder(py_reader=python_code_retriever)


def test_init(python_retriever_tool_builder):
    assert isinstance(python_retriever_tool_builder.py_reader, PyReader)


def test_build(python_retriever_tool_builder):
    tools = python_retriever_tool_builder.build()
    assert len(tools) == 3
    for tool in tools:
        assert isinstance(tool, Tool)


def test_tool_execution(python_retriever_tool_builder):
    python_retriever_tool_builder.py_reader.get_source_code_without_docstrings = MagicMock(
        return_value="Sample code"
    )
    python_retriever_tool_builder.py_reader.get_docstring = MagicMock(
        return_value="Sample docstring"
    )

    tools = python_retriever_tool_builder.build()
    assert tools[0].function(("module.path", "func")) == "Sample code"
    assert tools[1].function(("module.path", "func")) == "Sample docstring"
