import os
from unittest.mock import MagicMock

import pytest

from automata.core.agent.tools.py_code_retriever import PyCodeRetrieverTool
from automata.core.base.tool import Tool
from automata.core.coding.py_coding.module_tree import LazyModuleTreeMap
from automata.core.coding.py_coding.retriever import PyCodeRetriever
from automata.core.utils import root_py_fpath


@pytest.fixture
def python_retriever_tool_builder():
    path_to_here = os.path.join(root_py_fpath(), "tools", "tool_management", "tests")
    python_code_retriever = PyCodeRetriever(LazyModuleTreeMap(path_to_here))
    return PyCodeRetrieverTool(py_retriever=python_code_retriever)


def test_init(python_retriever_tool_builder):
    assert isinstance(python_retriever_tool_builder.code_retriever, PyCodeRetriever)


def test_build(python_retriever_tool_builder):
    tools = python_retriever_tool_builder.build()
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

    tools = python_retriever_tool_builder.build()
    assert tools[0].func(("module.path", "func")) == "Sample code"
    assert tools[1].func(("module.path", "func")) == "Sample docstring"
