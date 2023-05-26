import os
from unittest.mock import MagicMock

import pytest

from automata.core.base.tool import Tool
from automata.core.code_indexing.python_ast_indexer import PythonASTIndexer
from automata.core.code_indexing.python_code_inspector import PythonCodeInspector
from automata.core.utils import root_py_path
from automata.tool_management.python_inspector_tool_manager import PythonInspectorToolManager


@pytest.fixture
def python_inspector_tool_builder():
    path_to_here = os.path.join(root_py_path(), "tools", "tool_management", "tests")
    python_inspector = PythonCodeInspector(PythonASTIndexer(path_to_here))
    return PythonInspectorToolManager(python_inspector=python_inspector)


def test_init(python_inspector_tool_builder):
    assert isinstance(python_inspector_tool_builder.inspector, PythonCodeInspector)


def test_build_tools(python_inspector_tool_builder):
    tools = python_inspector_tool_builder.build_tools()
    assert len(tools) == 3
    for tool in tools:
        assert isinstance(tool, Tool)


def test_tool_execution(python_inspector_tool_builder):
    python_inspector_tool_builder.inspector.get_source_code_without_docstrings = MagicMock(
        return_value="Sample code"
    )
    python_inspector_tool_builder.inspector.get_docstring = MagicMock(
        return_value="Sample docstring"
    )

    tools = python_inspector_tool_builder.build_tools()
    assert tools[0].func(("module.path", "func")) == "Sample code"
    assert tools[1].func(("module.path", "func")) == "Sample docstring"
