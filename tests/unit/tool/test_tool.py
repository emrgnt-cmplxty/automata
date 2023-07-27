from typing import Dict

import pytest

from automata.tools.tool_base import Tool


class TestTool(Tool):
    def run(self, tool_input: Dict[str, str]) -> str:
        return "TestTool response"


@pytest.fixture
def test_tool(request) -> TestTool:
    name = request.node.get_closest_marker("tool_name")
    description = request.node.get_closest_marker("tool_description")
    function = request.node.get_closest_marker("tool_function")

    return TestTool(
        name=name.args[0] if name else "TestTool",
        description=description.args[0]
        if description
        else "A test tool for testing purposes",
        function=function.args[0]
        if function
        else (lambda x: "TestTool response"),
    )


@pytest.mark.tool_name("TestTool")
@pytest.mark.tool_description("A test tool for testing purposes")
def test_tool_instantiation(test_tool):
    assert test_tool.name == "TestTool"
    assert test_tool.description == "A test tool for testing purposes"
    assert test_tool.function is not None


def test_tool_run(test_tool):
    tool_input = {"test": "test"}
    response = test_tool.run(tool_input)
    assert response == "TestTool response"
