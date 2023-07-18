import os

import pytest

from automata.code_parsers.py.reader import PyReader
from automata.singletons.py_module_loader import py_module_loader


@pytest.fixture(autouse=True)
def module_loader():
    py_module_loader.reset()
    py_module_loader.initialize(
        os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."),
        "sample_modules",
    )


@pytest.fixture
def getter():
    return PyReader()


def test_get_docstring_function(getter):
    module_name = "sample_modules.sample"
    object_path = "sample_function"

    result = getter.get_docstring(module_name, object_path)
    expected_match = "This is a sample function."
    assert result == expected_match


def test_get_code_no_docstring_method(getter):
    module_name = "sample_modules.sample"
    object_path = "Person.say_hello"
    result = getter.get_source_code_without_docstrings(
        module_name, object_path
    )
    expected_match = (
        "def say_hello(self):\n    return f'Hello, I am {self.name}.'"
    )
    assert result.strip() == expected_match.strip()


def test_get_docstring_no_docstring_class(getter):
    module_name = "sample_modules.sample"
    object_path = "Person"
    result = getter.get_docstring(module_name, object_path)
    expected_match = "This is a sample class."
    assert result == expected_match


def test_get_code_module(getter):
    module_name = "sample_modules.sample"
    object_path = None
    result = getter.get_source_code_without_docstrings(
        module_name, object_path
    )
    expected_match = [
        "import math",
        "",
        "def sample_function(name):",
        "    return f'Hello, {name}! Sqrt(2) = {str(math.sqrt(2))}'",
        "",
        "class Person:",
        "",
        "    def __init__(self, name):",
        "        self.name = name",
        "",
        "    def say_hello(self):",
        "        return f'Hello, I am {self.name}.'",
        "",
        "    def run(self) -> str:",
        "        return 'run'",
        "",
        "def f(x) -> int:",
        "    return x + 1",
        "",
        "class EmptyClass:",
        "    pass",
        "",
        "class OuterClass:",
        "",
        "    class InnerClass:",
        "",
        "        def inner_method(self):",
    ]

    assert result.split("\n") == expected_match


def test_get_docstring_multiline(getter):
    module_name = "sample_modules.sample2"
    object_path = "PythonAgentToolkit.__init__"
    result = getter.get_docstring(module_name, object_path).strip()
    expected = "\n        Initializes a PythonAgentToolkit with the given PythonAgent.\n\nArgs:\n    python_agent (PythonAgent): A PythonAgent instance representing the agent to work with.\n        ".strip()
    assert result == expected


def test_get_code_no_docstring_no_code(getter):
    module_name = "sample_modules.sample"
    object_path = "EmptyClass"
    result = getter.get_source_code_without_docstrings(
        module_name, object_path
    )
    expected_match = "class EmptyClass:\n    pass"
    assert result.strip() == expected_match.strip()


def test_get_docstring_nested_class(getter):
    module_name = "sample_modules.sample"
    object_path = "OuterClass.InnerClass"
    result = getter.get_docstring(module_name, object_path)
    expected_match = "Inner doc strings"
    assert result == expected_match


def test_get_docstring_nested_class_method(getter):
    module_name = "sample_modules.sample"
    object_path = "OuterClass.InnerClass.inner_method"
    result = getter.get_docstring(module_name, object_path)
    expected_match = "Inner method doc strings"
    assert result == expected_match
