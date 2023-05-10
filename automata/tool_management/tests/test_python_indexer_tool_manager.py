import os
from unittest.mock import MagicMock

import pytest

from automata.core.base.tool import Tool
from automata.core.utils import root_py_path
from automata.tool_management.python_indexer_tool_manager import PythonIndexerToolManager
from automata.tools.python_tools.python_indexer import PythonIndexer


@pytest.fixture
def python_indexer_tool_builder():
    path_to_here = os.path.join(root_py_path(), "tools", "tool_management", "tests")
    python_indexer = PythonIndexer(path_to_here)
    return PythonIndexerToolManager(python_indexer=python_indexer)


def test_init(python_indexer_tool_builder):
    assert isinstance(python_indexer_tool_builder.indexer, PythonIndexer)


def test_build_tools(python_indexer_tool_builder):
    tools = python_indexer_tool_builder.build_tools()
    assert len(tools) == 3
    for tool in tools:
        assert isinstance(tool, Tool)


def test_tool_execution(python_indexer_tool_builder):
    python_indexer_tool_builder.indexer.retrieve_code_without_docstrings = MagicMock(
        return_value="Sample code"
    )
    python_indexer_tool_builder.indexer.retrieve_docstring = MagicMock(
        return_value="Sample docstring"
    )

    tools = python_indexer_tool_builder.build_tools()
    assert tools[0].func(("module.path", "func")) == "Sample code"
    assert tools[1].func(("module.path", "func")) == "Sample docstring"
