import inspect
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
    python_parser = PythonParser(relative_dir=f"spork/tools/python_tools/tests/sample_code")
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


# Check that we can bootstrap a new module "sample2.py" with a new function "f(x) -> x + 1"
def test_bootstrap_module_with_new_function(python_writer_tool_builder):
    current_file = inspect.getframeinfo(inspect.currentframe()).filename
    absolute_path = os.sep.join(os.path.abspath(current_file).split(os.sep)[:-1])

    tools = python_writer_tool_builder.build_tools()
    (code_writer, disk_writer) = (tools[0], tools[1])
    function_def = "def f(x):\n    return x + 1"
    package = "sample_code"
    module = "sample2"

    file_py_path = f"{package}.{module}"
    file_rel_path = os.path.join(package, f"{module}.py")
    file_abs_path = os.path.join(absolute_path, file_rel_path)

    code_writer.func(f"{file_py_path},{function_def}")
    disk_writer.func()

    new_sample_text = None
    with open(file_abs_path, "r", encoding="utf-8") as f:
        new_sample_text = f.read()
    assert new_sample_text.strip() == function_def
    os.remove(file_abs_path)


# Check that we can extend existing module "sample.py" with a new function "f(x) -> x + 1"
def test_extend_module_with_new_function(python_writer_tool_builder):
    current_file = inspect.getframeinfo(inspect.currentframe()).filename
    absolute_path = os.sep.join(os.path.abspath(current_file).split(os.sep)[:-1])
    prev_text = None
    with open(os.path.join(absolute_path, "sample_code", "sample.py"), "r", encoding="utf-8") as f:
        prev_text = f.read()
    assert prev_text is not None, "Could not read sample.py"

    tools = python_writer_tool_builder.build_tools()
    (code_writer, disk_writer) = (tools[0], tools[1])
    function_def = "def f(x):\n    return x + 1"
    package = "sample_code"
    module = "sample"

    file_py_path = f"{package}.{module}"
    file_rel_path = os.path.join(package, f"{module}.py")
    file_abs_path = os.path.join(absolute_path, file_rel_path)

    code_writer.func(f"{file_py_path},{function_def}")
    disk_writer.func()

    new_sample_text = None
    with open(file_abs_path, "r", encoding="utf-8") as f:
        new_sample_text = f.read()

    assert function_def in new_sample_text
    with open(file_abs_path, "w", encoding="utf-8") as f:
        f.write(prev_text)
