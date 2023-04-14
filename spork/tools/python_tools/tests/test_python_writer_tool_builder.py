import os
from unittest.mock import MagicMock

import pytest
from langchain.agents import Tool

from spork.tools.python_tools.python_parser import PythonParser
from spork.tools.python_tools.python_writer import PythonWriter
from spork.tools.python_tools.python_writer_tool_builder import PythonWriterToolBuilder


@pytest.fixture
def python_writer_tool_builder(tmpdir):
    temp_directory = tmpdir.mkdir("temp_code")
    os.chdir(temp_directory)

    python_parser = PythonParser()
    python_writer = PythonWriter(python_parser)
    return PythonWriterToolBuilder(python_writer)


def test_init(python_writer_tool_builder):
    assert isinstance(python_writer_tool_builder.python_writer, PythonWriter)
    assert python_writer_tool_builder.logger is None


def test_build_tools(python_writer_tool_builder):
    tools = python_writer_tool_builder.build_tools()
    assert len(tools) == 2
    for tool in tools:
        assert isinstance(tool, Tool)


def test_tool_execution(python_writer_tool_builder):
    python_writer_tool_builder.python_writer.modify_code_state = MagicMock()
    python_writer_tool_builder.python_writer.write_to_disk = MagicMock()

    tools = python_writer_tool_builder.build_tools()
    tools[0].func("some.path, sample_code")
    tools[1].func()

    python_writer_tool_builder.python_writer.modify_code_state.assert_called_once_with(
        "some.path", "sample_code"
    )
    python_writer_tool_builder.python_writer.write_to_disk.assert_called_once()


def test_tool_execution_real(python_writer_tool_builder):
    tools = python_writer_tool_builder.build_tools()
    code_writer, disk_writer = tools[0], tools[1]
    code_writer.func("spork.tools.python_tools.tests.sample_code_2, def f(x):\n    return x + 1")
    # disk_writer.func()
