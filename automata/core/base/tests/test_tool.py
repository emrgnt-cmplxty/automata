from typing import Optional, Tuple

import pytest

from automata.core.base.tool import InvalidTool, Tool, Toolkit, ToolkitType, tool


class TestTool(Tool):
    def _run(self, tool_input: Tuple[Optional[str], ...]) -> str:
        return "TestTool response"

    async def _arun(self, tool_input: Tuple[Optional[str], ...]) -> str:
        return "TestTool async response"


@pytest.fixture
def test_tool():
    return TestTool(
        name="TestTool",
        description="A test tool for testing purposes",
        func=lambda x: "TestTool response",
    )


def test_tool_instantiation(test_tool):
    assert test_tool.name == "TestTool"
    assert test_tool.description == "A test tool for testing purposes"
    assert test_tool.func is not None


def test_tool_run(test_tool):
    tool_input = ("test",)
    response = test_tool.run(tool_input)
    assert response == "TestTool response"


@pytest.mark.asyncio
async def test_tool_arun(test_tool):
    tool_input = ("test",)
    response = await test_tool.arun(tool_input)
    assert response == "TestTool async response"


def test_invalid_tool():
    invalid_tool = InvalidTool()
    response = invalid_tool.run(("InvalidToolName",))
    assert response == "('InvalidToolName',) is not a valid tool, try another one."


@pytest.mark.asyncio
async def test_invalid_tool_async():
    invalid_tool = InvalidTool()
    response = await invalid_tool.arun(("InvalidToolName",))
    assert response == "InvalidToolName is not a valid tool, try another one."


def test_tool_decorator():
    @tool
    def example_tool(input: str) -> str:
        """Example tool for testing."""
        return f"example_tool: {input}"

    assert isinstance(example_tool, Tool)
    assert example_tool.name == "example_tool"
    assert example_tool.description.startswith("example_tool")


def test_tool_decorator_with_name():
    @tool("custom_tool_name")
    def example_tool(input: str) -> str:
        """Example tool for testing."""
        return f"example_tool: {input}"

    assert isinstance(example_tool, Tool)
    assert example_tool.name == "custom_tool_name"
    assert example_tool.description.startswith("custom_tool_name")


def test_toolkit():
    tools = [
        TestTool(
            name="TestTool",
            description="A test tool for testing purposes",
            func=lambda x: "TestTool response",
        )
    ]
    toolkit = Toolkit(tools)
    assert len(toolkit.tools) == 1
    assert isinstance(toolkit.tools[0], TestTool)
    assert toolkit.tools[0].name == "TestTool"


def test_toolkit_type():
    assert len(ToolkitType) == 3
    assert ToolkitType.PYTHON_INSPECTOR.name == "PYTHON_INSPECTOR"
    assert ToolkitType.PYTHON_WRITER.name == "PYTHON_WRITER"
    assert ToolkitType.COVERAGE_PROCESSOR.name == "COVERAGE_PROCESSOR"
