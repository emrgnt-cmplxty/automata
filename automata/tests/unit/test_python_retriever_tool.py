import os
from unittest.mock import MagicMock

import pytest

from automata.core.agent.tools.py_reader import PyReaderTool
from automata.core.base.tool import Tool
from automata.core.coding.py.module_loader import ModuleLoader
from automata.core.coding.py.reader import PyReader
from automata.core.utils import root_py_fpath


@pytest.fixture(autouse=True)
def module_loader():
    module_loader = ModuleLoader()
    path_to_here = os.path.join(root_py_fpath(), "tools", "tool_management", "tests")

    module_loader.set_paths(
        path_to_here,
        "tests",
    )
    yield module_loader
    module_loader.py_dir = None
    module_loader._dotpath_map = None


@pytest.fixture
def python_retriever_tool_builder():
    python_code_retriever = PyReader()
    return PyReaderTool(py_reader=python_code_retriever)


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
    assert tools[0].func(("module.path", "func")) == "Sample code"
    assert tools[1].func(("module.path", "func")) == "Sample docstring"
