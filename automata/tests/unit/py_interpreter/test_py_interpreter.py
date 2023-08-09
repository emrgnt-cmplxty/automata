from automata.experimental.tools import (
    PyInterpreter,
    PyInterpreterOpenAIToolkitBuilder,
    PyInterpreterToolkitBuilder,
)
from automata.llm import OpenAITool
from automata.tools.tool_base import Tool


def test_python_interpreter_init():
    interpreter = PyInterpreter()
    assert isinstance(interpreter, PyInterpreter)
    assert (
        interpreter.code_context
        == PyInterpreter.DEFAULT_CODE_CONTEXT.split("\n")
    )
    assert (
        interpreter.test_context
        == PyInterpreter.DEFAULT_TEST_CONTEXT.split("\n")
    )


def test_python_interpreter_set_code():
    interpreter = PyInterpreter()
    status, result = interpreter.set_code("```python\nx = 5```")
    assert status
    assert result == PyInterpreter.SUCCESS_STRING
    assert "x = 5" in interpreter.code_context


def test_python_interpreter_set_code_invalid_code():
    interpreter = PyInterpreter()
    status, result = interpreter.set_code("```python\nx = 5 / 0```")
    assert not status
    assert "Execution failed with error" in result


def test_python_interpreter_set_tests():
    interpreter = PyInterpreter()
    result = interpreter.set_tests("```python\nassert x == 5```")
    assert result == PyInterpreter.SUCCESS_STRING
    assert "assert x == 5" in interpreter.test_context


def test_python_interpreter_set_tests_invalid_code():
    interpreter = PyInterpreter()
    result = interpreter.set_tests("```python\nx = / 5```")  # invalid syntax
    assert (
        "Execution failed with error 'invalid syntax (<unknown>, line 2)'"
        in result
    )


def test_python_interpreter_set_code_and_run_tests():
    interpreter = PyInterpreter()
    interpreter.set_tests("```python\nassert x == 5```")
    result = interpreter.set_code_and_run_tests("```python\nx = 5```")
    assert PyInterpreter.SUCCESS_STRING in result
    assert "x = 5" in interpreter.code_context
    assert "assert x == 5" in interpreter.test_context


def test_python_interpreter_set_code_and_run_tests_fail():
    interpreter = PyInterpreter()
    interpreter.set_tests("```python\nassert x == 5```")
    result = interpreter.set_code_and_run_tests("```python\nx = 4```")
    assert "Execution failed with error" in result
    assert "x = 4" in interpreter.code_context
    assert "assert x == 5" in interpreter.test_context


def test_python_interpreter_empty_code_and_tests():
    interpreter = PyInterpreter()
    status, result = interpreter.set_code("```python\n\n```")
    assert status
    assert result == PyInterpreter.SUCCESS_STRING
    result = interpreter.set_tests("```python\n\n```")
    assert result == PyInterpreter.SUCCESS_STRING


def test_python_interpreter_non_python_code():
    interpreter = PyInterpreter()
    status, result = interpreter.set_code(
        "```python\nThis is not Python code.```"
    )
    assert not status
    assert (
        "Execution failed with error 'invalid syntax (<string>, line 4)'"
        in result
    )


def test_python_interpreter_runtime_error():
    interpreter = PyInterpreter()
    status, result = interpreter.set_code("```python\nx = 5 / 0```")
    assert not status
    assert "Execution failed with error 'division by zero'" in result


def test_python_interpreter_assertion_error():
    interpreter = PyInterpreter()
    interpreter.set_tests("```python\nassert x == 0```")
    result = interpreter.set_code_and_run_tests("```python\nx = 5```")
    assert "Execution failed with error" in result


def test_python_interpreter_large_code_block():
    interpreter = PyInterpreter()
    large_code = "```python\n" + "x = 5\n" * 10000 + "```"
    result = interpreter.set_code(large_code)
    assert result == (True, PyInterpreter.SUCCESS_STRING)


def test_python_interpreter_set_code_no_overwrite():
    interpreter = PyInterpreter()
    status, result = interpreter.set_code("```python\nx = 5```")
    assert status
    assert "x = 5" in interpreter.code_context
    status, result = interpreter.set_code(
        "```python\ny = 10```", overwrite=False
    )
    assert status
    assert "y = 10" in interpreter.code_context
    assert len(interpreter.code_context) > len(
        PyInterpreter.DEFAULT_CODE_CONTEXT.split("\n")
    )


def test_python_interpreter_set_tests_no_overwrite():
    interpreter = PyInterpreter()
    interpreter.set_tests("```python\nassert x == 5```")
    assert "assert x == 5" in interpreter.test_context
    interpreter.set_tests("```python\nassert y == 10```", overwrite=False)
    assert "assert y == 10" in interpreter.test_context
    assert len(interpreter.test_context) > len(
        PyInterpreter.DEFAULT_TEST_CONTEXT.split("\n")
    )


def test_python_interpreter_capture_output():
    interpreter = PyInterpreter()
    status, result = interpreter.set_code(
        "```python\nprint('Hello, world!')```"
    )
    assert status
    assert "Hello, world!" in result


def test_python_interpreter_capture_multiple_outputs():
    interpreter = PyInterpreter()
    status, result = interpreter.set_code(
        "```python\nprint('Hello,'); print('world!')```"
    )
    assert status
    assert "Hello,\nworld!" in result


def test_pyinterpreter_toolkit_builder_build():
    py_interpreter = PyInterpreter()
    toolkit_builder = PyInterpreterToolkitBuilder(py_interpreter)

    tools = toolkit_builder.build()

    assert len(tools) == 2
    assert isinstance(tools[0], Tool)
    assert isinstance(tools[1], Tool)

    assert tools[0].name == "py-set-tests"
    assert tools[1].name == "py-set-code-and-run-tests"

    # Testing the function is a bit tricky as we'd have to provide a valid code snippet
    # Here we just check that it's callable
    assert callable(tools[0].function)
    assert callable(tools[1].function)


def test_python_interpreter_context_persistence():
    interpreter = PyInterpreter()
    status, result = interpreter.set_code(
        "```python\ndef add(a, b): return a + b```"
    )
    assert status
    status, result = interpreter.set_code(
        "```python\nresult = add(5, 10)```", overwrite=False
    )
    assert status
    interpreter.set_tests("```python\nassert result == 15```")
    result = interpreter._run_tests()
    assert result == PyInterpreter.SUCCESS_STRING


def test_pyinterpreter_toolkit_builder_build_for_open_ai():
    py_interpreter = PyInterpreter()
    toolkit_builder = PyInterpreterOpenAIToolkitBuilder(py_interpreter)

    tools = toolkit_builder.build_for_open_ai()

    assert len(tools) == 2
    assert isinstance(tools[0], OpenAITool)
    assert isinstance(tools[1], OpenAITool)

    assert tools[0].name == "py-set-tests"
    assert tools[1].name == "py-set-code-and-run-tests"

    # Testing the function is a bit tricky as we'd have to provide a valid code snippet
    # Here we just check that it's callable
    assert callable(tools[0].function)
    assert callable(tools[1].function)

    # Check the properties and required fields
    assert (
        tools[0].properties
        == tools[1].properties
        == {
            "code": {
                "type": "string",
                "description": "The given Python code to execute, formatted as a markdown snippet, e.g. ```python\\n[CODE]``` and with newlines separated by the double-escaped newline char '\\n'.",
            },
            "overwrite": {
                "type": "bool",
                "description": "Specifies whether or not the given code should overwrite the existing code in the interpreter.",
                "default": "True",
            },
        }
    )
    assert tools[0].required == tools[1].required == ["code"]
