"""Unit tests for the PythonParser module."""

from spork.tools.python_tools.python_parser import PythonParser


def test_get_raw_code():
    parser = PythonParser()
    raw_code = parser.get_raw_code(
        "spork.tools.tool_managers.tests.sample_code.sample.sample_function"
    )
    assert "def sample_function(name):" in raw_code


def test_get_docstring():
    parser = PythonParser()
    docstring = parser.get_docstring(
        "spork.tools.tool_managers.tests.sample_code.sample.sample_function"
    )
    assert "This is a sample function" in docstring


def test_get_overview():
    parser = PythonParser()
    overview = parser.get_overview()
    assert "spork.tools.tool_managers.tests.sample_code.sample" in overview
    assert "sample_function" in overview
    assert "Person" in overview
    assert "say_hello" in overview
