import pytest

from automata.llm import FunctionCall


def test_tool_run(test_tool):
    tool_input = {"test": "test"}
    response = test_tool.run(tool_input)
    assert response == "TestTool response"


def test_tool_execution(tool_execution, function_call):
    response = tool_execution.execute(function_call)
    assert response == "TestTool response"


def test_tool_executor(tool_executor, function_call):
    response = tool_executor.execute(function_call)
    assert response == "TestTool response"


def test_tool_execution_no_tool_found(tool_execution):
    function_call = FunctionCall(
        name="NonExistentTool", arguments={"test": "test"}
    )
    with pytest.raises(
        Exception, match=r"No tool found for function call: NonExistentTool"
    ):
        tool_execution.execute(function_call)


def test_tool_executor_no_tool_found(tool_executor):
    function_call = FunctionCall(
        name="NonExistentTool", arguments={"test": "test"}
    )
    with pytest.raises(
        Exception, match=r"No tool found for function call: NonExistentTool"
    ):
        tool_executor.execute(function_call)
