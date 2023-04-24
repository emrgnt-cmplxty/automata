import pytest

from automata.core.base.tool import Tool
from automata.tool_management.documentation_gpt_tool_manager import DocumentationGPTToolManager
from automata.tools.documentation.documentation_gpt import DocumentationGPT


@pytest.fixture
def doc_gpt_tool_builder():
    documentation_gpt = DocumentationGPT(
        url="https://python.langchain.com/en/latest/index.html",
        model="gpt-4",
        temperature=0.7,
        verbose=True,
    )
    return DocumentationGPTToolManager(documentation_gpt=documentation_gpt)


def test_init():
    documentation_gpt = DocumentationGPT(
        url="https://python.langchain.com/en/latest/index.html",
        model="gpt-4",
        temperature=0.7,
        verbose=True,
    )
    documentation_gpt_tool_manager = DocumentationGPTToolManager(
        documentation_gpt=documentation_gpt
    )
    assert documentation_gpt_tool_manager.documentation_gpt == documentation_gpt


def test_build_tools(doc_gpt_tool_builder):
    tools = doc_gpt_tool_builder.build_tools()

    assert len(tools) == 1
    for tool in tools:
        assert isinstance(tool, Tool)


# TODO - Revive this test to track doc gpt liveliness
# def test_tool_execution(doc_gpt_tool_builder):
# from unittest.mock import MagicMock
#     doc_gpt_tool_builder.documentation_gpt_lookup = MagicMock(return_value="Vec Result")
#     tools = doc_gpt_tool_builder.build_tools()
#     assert tools[0].func("Vec Lookup") == "Vec Result"
