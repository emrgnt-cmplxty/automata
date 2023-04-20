import os
from unittest.mock import MagicMock

import pytest
from langchain.agents import Tool

from spork.tools.python_tools.python_indexer import PythonIndexer
from spork.tools.tool_managers.python_indexer_tool_manager import PythonIndexerToolManager
from spork.tools.utils import root_py_path


@pytest.fixture
def python_indexer_tool_builder():
    path_to_here = os.path.join(root_py_path(), "tools", "tool_managers", "tests")
    python_indexer = PythonIndexer(path_to_here)
    return PythonIndexerToolManager(python_indexer)


def test_init(python_indexer_tool_builder):
    assert isinstance(python_indexer_tool_builder.python_indexer, PythonIndexer)


def test_build_tools(python_indexer_tool_builder):
    tools = python_indexer_tool_builder.build_tools()
    assert len(tools) == 2
    for tool in tools:
        assert isinstance(tool, Tool)


def test_tool_execution(python_indexer_tool_builder):
    python_indexer_tool_builder.python_indexer.retrieve_code = MagicMock(
        return_value="Sample code"
    )
    python_indexer_tool_builder.python_indexer.retrieve_docstring = MagicMock(
        return_value="Sample docstring"
    )

    tools = python_indexer_tool_builder.build_tools()
    assert tools[0].func("module.path,func") == "Sample code"
    assert tools[1].func("module.path,func") == "Sample docstring"
