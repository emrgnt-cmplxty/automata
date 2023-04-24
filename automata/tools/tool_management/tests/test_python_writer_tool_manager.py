import inspect
import os
import shutil
import textwrap

import pytest

from automata.core.base.tool import Tool
from automata.core.utils import root_py_path
from automata.tools.python_tools.python_indexer import PythonIndexer
from automata.tools.python_tools.python_writer import PythonWriter
from automata.tools.tool_management.python_writer_tool_manager import PythonWriterToolManager


@pytest.fixture
def python_writer_tool_builder(tmpdir):
    temp_directory = tmpdir.mkdir("temp_code")
    os.chdir(temp_directory)
    path_to_here = os.path.join(root_py_path(), "tools", "tool_management", "tests")
    python_indexer = PythonIndexer(path_to_here)

    python_writer = PythonWriter(python_indexer)
    return PythonWriterToolManager(python_writer=python_writer)


def test_init(python_writer_tool_builder):
    assert isinstance(python_writer_tool_builder.writer, PythonWriter)


def test_build_tools(python_writer_tool_builder):
    tools = python_writer_tool_builder.build_tools()
    assert len(tools) == 1
    for tool in tools:
        assert isinstance(tool, Tool)


# Check that we can bootstrap a new module "sample3.py" with a new function "f(x) -> x + 1"
def test_bootstrap_module_with_new_function(python_writer_tool_builder):
    current_file = inspect.getframeinfo(inspect.currentframe()).filename
    absolute_path = os.sep.join(os.path.abspath(current_file).split(os.sep)[:-1])

    tools = python_writer_tool_builder.build_tools()
    code_writer = tools[0]
    function_def = "def f(x):\n    return x + 1"
    package = "sample_code"
    module = "sample3"

    file_py_path = f"{package}.{module}"
    file_abs_path = os.path.join(absolute_path, package, f"{module}.py")
    code_writer.func(f"{file_py_path},,{function_def}")

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
    code_writer = tools[0]
    function_def = "def f(x):\n    return x + 1"
    package = "sample_code"
    module = "sample"

    file_py_path = f"{package}.{module}"
    file_rel_path = os.path.join(package, f"{module}.py")
    file_abs_path = os.path.join(absolute_path, file_rel_path)
    code_writer.func(f"{file_py_path},,{function_def}")

    new_sample_text = None
    with open(file_abs_path, "r", encoding="utf-8") as f:
        new_sample_text = f.read()
    assert function_def in new_sample_text
    with open(file_abs_path, "w", encoding="utf-8") as f:
        f.write(prev_text)


# Check that we can extend existing module "sample.py" with a new function
# that has documentation and type hints, e.g. "f(x) -> int;    return x + 1"
def test_extend_module_with_documented_new_function(python_writer_tool_builder):
    current_file = inspect.getframeinfo(inspect.currentframe()).filename
    absolute_path = os.sep.join(os.path.abspath(current_file).split(os.sep)[:-1])
    prev_text = None
    with open(os.path.join(absolute_path, "sample_code", "sample.py"), "r", encoding="utf-8") as f:
        prev_text = f.read()
    assert prev_text is not None, "Could not read sample.py"

    tools = python_writer_tool_builder.build_tools()
    code_writer = tools[0]
    function_def = 'def f(x) -> int:\n    """This is my new function"""\n    return x + 1'
    package = "sample_code"
    module = "sample"

    file_py_path = f"{package}.{module}"
    file_rel_path = os.path.join(package, f"{module}.py")
    file_abs_path = os.path.join(absolute_path, file_rel_path)

    code_writer.func(f"{file_py_path},,{function_def}")

    new_sample_text = None
    with open(file_abs_path, "r", encoding="utf-8") as f:
        new_sample_text = f.read()
    with open(file_abs_path, "w", encoding="utf-8") as f:
        f.write(prev_text)

    assert function_def in new_sample_text


# Check that we can extend existing module "sample.py" with a new function
# that has documentation and type hints, e.g. "f(x) -> int;    return x + 1"
def test_extend_module_with_documented_new_class(python_writer_tool_builder):
    class_str = textwrap.dedent(
        '''from typing import List

from automata.core.base.tool import Tool

from automata.tools.python_tools.python_agent import PythonAgent


class PythonAgentToolBuilder:
    """A class for building tools to interact with PythonAgent."""

    def __init__(self, python_agent: PythonAgent):
        """
        Initializes a PythonAgentToolBuilder with the given PythonAgent.

        Args:
            python_agent (PythonAgent): A PythonAgent instance representing the agent to work with.
        """
        self.python_agent = python_agent

    def build_tools(self) -> List:
        """
        Builds a list of Tool objects for interacting with PythonAgent.

        Args:
            - None

        Returns:
            - tools (List[Tool]): A list of Tool objects representing PythonAgent commands.
        """

        def python_agent_python_task():
            """A sample task that utilizes PythonAgent."""
            pass

        tools = [
            Tool(
                "mr-automata-task",
                python_agent_python_task,
                "Execute a Python task using the PythonAgent. Provide the task description in plain English.",
            )
        ]
        return tools
    '''
    )
    current_file = inspect.getframeinfo(inspect.currentframe()).filename
    absolute_path = os.sep.join(os.path.abspath(current_file).split(os.sep)[:-1])
    package = "sample_code"
    module = "sample4"

    tools = python_writer_tool_builder.build_tools()
    code_writer = tools[0]

    file_py_path = f"{package}.{module}"
    file_rel_path = os.path.join(package, f"{module}.py")
    file_abs_path = os.path.join(absolute_path, file_rel_path)
    code_writer.func(f"{file_py_path},PythonAgentToolBuilder,{class_str}")
    new_sample_text = None
    with open(file_abs_path, "r", encoding="utf-8") as f:
        new_sample_text = f.read()

    file2_rel_path = os.path.join(package, f"sample2.py")
    file2_abs_path = os.path.join(absolute_path, file2_rel_path)

    with open(file2_abs_path, "r", encoding="utf-8") as f:
        old_sample_text = f.read().replace("# type: ignore\n", "")
    # assert class_str.strip() == new_sample_text.strip()
    assert old_sample_text.strip() == new_sample_text.strip()
    os.remove(file_abs_path)


def test_extend_module_with_documented_new_module(python_writer_tool_builder):
    combo_str = textwrap.dedent(
        """temp_code.python_agent_tool_builder,,from typing import List, Optional
from automata.buffer import PassThroughBuffer
from automata.tools.tool import Tool
from automata.tools.python_tools.python_agent import PythonAgent

class PythonAgentToolBuilder:

    def __init__(self, python_agent: PythonAgen):
        self.python_agent = python_agent

    def build_tools(self) -> List[Tool]:
        tools = [Tool(name='mr-automata-task', func=lambda task: self.python_agent.run_agent(task), description=f'A single function that uses PythonAgent to perform a given task.', return_direct=True)]
        return tools"""
    )
    tools = python_writer_tool_builder.build_tools()
    code_writer = tools[0]
    code_writer.func(combo_str)
    # # Why?
    shutil.rmtree(os.path.join(root_py_path(), "tools", "tool_management", "tests", "temp_code"))
