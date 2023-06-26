from typing import Optional, Tuple

import pytest

from automata.core.base.tool import Tool, Toolkit, ToolkitType


class TestTool(Tool):
    def run(self, tool_input: Tuple[Optional[str], ...]) -> str:
        return "TestTool response"

    async def arun(self, tool_input: Tuple[Optional[str], ...]) -> str:
        return "TestTool async response"


@pytest.fixture
def test_tool():
    return TestTool(
        name="TestTool",
        description="A test tool for testing purposes",
        function=lambda x: "TestTool response",
    )


def test_tool_instantiation(test_tool):
    assert test_tool.name == "TestTool"
    assert test_tool.description == "A test tool for testing purposes"
    assert test_tool.function is not None


def test_tool_run(test_tool):
    tool_input = ("test",)
    response = test_tool.run(tool_input)
    assert response == "TestTool response"


@pytest.mark.asyncio
async def test_tool_arun(test_tool):
    tool_input = ("test",)
    response = await test_tool.arun(tool_input)
    assert response == "TestTool async response"


def test_toolkit():
    tools = [
        TestTool(
            name="TestTool",
            description="A test tool for testing purposes",
            function=lambda x: "TestTool response",
        )
    ]
    toolkit = Toolkit(tools)
    assert len(toolkit.tools) == 1
    assert isinstance(toolkit.tools[0], TestTool)
    assert toolkit.tools[0].name == "TestTool"


def test_toolkit_type():
    assert len(ToolkitType) == 4
    assert ToolkitType.PY_READER.name == "PY_READER"
    assert ToolkitType.PY_WRITER.name == "PY_WRITER"
    assert ToolkitType.SYMBOL_SEARCH.name == "SYMBOL_SEARCH"
    assert ToolkitType.CONTEXT_ORACLE.name == "CONTEXT_ORACLE"
