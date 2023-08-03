import pytest

from automata.experimental.tools import (
    PyInterpreter,
    PyInterpreterToolkitBuilder,
)
from automata.tools.tool_base import Tool


def test_python_interpreter_init():
    interpreter = PyInterpreter()
    assert isinstance(interpreter, PyInterpreter)
    assert interpreter.execution_context == []


def test_python_interpreter_execute_code():
    interpreter = PyInterpreter()
    assert interpreter.execute_code("x = 5") == PyInterpreter.SUCCESS_STRING
    assert (
        interpreter.execute_code("y = x + 5")
        == "Execution failed with error = name 'x' is not defined"
    )


def test_python_interpreter_persistent_execute():
    interpreter = PyInterpreter()
    assert (
        interpreter.persistent_execute("x = 5") == PyInterpreter.SUCCESS_STRING
    )
    assert (
        interpreter.persistent_execute("y = x + 5")
        == PyInterpreter.SUCCESS_STRING
    )
    assert (
        interpreter.persistent_execute("z = x + y + 5")
        == PyInterpreter.SUCCESS_STRING
    )
    assert (
        interpreter.persistent_execute("z == 20")
        == PyInterpreter.SUCCESS_STRING
    )

    assert interpreter.execution_context == [
        "x = 5",
        "y = x + 5",
        "z = x + y + 5",
        "z == 20",
    ]


def test_python_interpreter_import():
    interpreter = PyInterpreter()
    assert interpreter.execute_code("import random")
    assert interpreter.execute_code("import automata")


def test_python_interpreter_clear_and_persistent_execute():
    interpreter = PyInterpreter()
    interpreter.persistent_execute("x = 5")
    assert (
        interpreter.clear_and_persistent_execute("y = 10")
        == PyInterpreter.SUCCESS_STRING
    )
    assert interpreter.execution_context == ["y = 10"]


def test_python_interpreter_clear():
    interpreter = PyInterpreter()
    interpreter.persistent_execute("x = 5")
    interpreter.clear()
    assert interpreter.execution_context == []


def test_python_interpreter_toolkit_builder_init():
    builder = PyInterpreterToolkitBuilder()
    assert isinstance(builder.python_interpreter, PyInterpreter)


def test_python_interpreter_toolkit_builder_build():
    builder = PyInterpreterToolkitBuilder()
    tools = builder.build()
    assert len(tools) == 2
    for tool in tools:
        assert isinstance(tool, Tool)


@pytest.mark.parametrize(
    "tool_name, function_name, code, expected_result",
    [
        (
            "persistent-execute-python-code",
            "persistent_execute",
            "x = 5",
            PyInterpreter.SUCCESS_STRING,
        ),
        (
            "clear-and-execute-execute-python-code",
            "clear_and_persistent_execute",
            "y = 10",
            PyInterpreter.SUCCESS_STRING,
        ),
    ],
)
def test_python_interpreter_toolkit_builder_tool_functions(
    tool_name, function_name, code, expected_result
):
    builder = PyInterpreterToolkitBuilder()
    tools = builder.build()
    for tool in tools:
        if tool.name == tool_name:
            result = tool.function(code)
            assert result == expected_result
