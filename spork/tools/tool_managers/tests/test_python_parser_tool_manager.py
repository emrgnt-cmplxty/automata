from unittest.mock import MagicMock

import pytest
from langchain.agents import Tool

from spork.tools.python_tools.python_indexer import PythonIndexer
from spork.tools.tool_managers.python_indexer_tool_manager import PythonIndexerToolManager


@pytest.fixture
def python_indexer_tool_builder():
    python_indexer = PythonIndexer("sample_code")
    return PythonIndexerToolManager(python_indexer)


def test_init(python_indexer_tool_builder):
    assert isinstance(python_indexer_tool_builder.python_indexer, PythonIndexer)
    assert python_indexer_tool_builder.logger is None


def test_build_tools(python_indexer_tool_builder):
    tools = python_indexer_tool_builder.build_tools()
    assert len(tools) == 2
    for tool in tools:
        assert isinstance(tool, Tool)


def test_tool_execution(python_indexer_tool_builder):
    python_indexer_tool_builder.python_indexer.get_raw_code = MagicMock(return_value="Sample code")
    python_indexer_tool_builder.python_indexer.get_docstring = MagicMock(
        return_value="Sample docstring"
    )

    tools = python_indexer_tool_builder.build_tools()
    assert tools[0].func("some.path") == "Sample code"
    assert tools[1].func("some.path") == "Sample docstring"
