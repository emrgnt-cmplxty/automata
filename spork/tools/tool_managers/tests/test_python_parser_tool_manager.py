from unittest.mock import MagicMock

import pytest
from langchain.agents import Tool

from spork.tools.python_tools.python_parser import PythonParser
from spork.tools.tool_managers.python_parser_tool_manager import PythonParserToolManager


@pytest.fixture
def python_parser_tool_builder():
    python_parser = PythonParser()
    return PythonParserToolManager(python_parser)


def test_init(python_parser_tool_builder):
    assert isinstance(python_parser_tool_builder.python_parser, PythonParser)
    assert python_parser_tool_builder.logger is None


def test_build_tools(python_parser_tool_builder):
    tools = python_parser_tool_builder.build_tools()
    assert len(tools) == 2
    for tool in tools:
        assert isinstance(tool, Tool)


def test_tool_execution(python_parser_tool_builder):
    python_parser_tool_builder.python_parser.get_raw_code = MagicMock(return_value="Sample code")
    python_parser_tool_builder.python_parser.get_docstring = MagicMock(
        return_value="Sample docstring"
    )

    tools = python_parser_tool_builder.build_tools()
    assert tools[0].func("some.path") == "Sample code"
    assert tools[1].func("some.path") == "Sample docstring"
