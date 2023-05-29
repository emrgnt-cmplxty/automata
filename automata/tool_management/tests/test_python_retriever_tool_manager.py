import os
from unittest.mock import MagicMock

import pytest

from automata.core.base.tool import Tool
from automata.core.code_indexing.module_tree_map import LazyModuleTreeMap
from automata.core.code_indexing.python_code_retriever import PythonCodeRetriever
from automata.core.utils import root_py_path
from automata.tool_management.python_code_retriever_tool_manager import (
    PythonCodeRetrieverToolManager,
)


@pytest.fixture
def python_retriever_tool_builder():
    path_to_here = os.path.join(root_py_path(), "tools", "tool_management", "tests")
    python_code_retriever = PythonCodeRetriever(LazyModuleTreeMap(path_to_here))
    return PythonCodeRetrieverToolManager(python_retriever=python_code_retriever)


def test_init(python_retriever_tool_builder):
    assert isinstance(python_retriever_tool_builder.code_retriever, PythonCodeRetriever)


def test_build_tools(python_retriever_tool_builder):
    tools = python_retriever_tool_builder.build_tools()
    assert len(tools) == 3
    for tool in tools:
        assert isinstance(tool, Tool)


def test_tool_execution(python_retriever_tool_builder):
    python_retriever_tool_builder.code_retriever.get_source_code_without_docstrings = MagicMock(
        return_value="Sample code"
    )
    python_retriever_tool_builder.code_retriever.get_docstring = MagicMock(
        return_value="Sample docstring"
    )

    tools = python_retriever_tool_builder.build_tools()
    assert tools[0].func(("module.path", "func")) == "Sample code"
    assert tools[1].func(("module.path", "func")) == "Sample docstring"
