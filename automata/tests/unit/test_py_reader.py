import os

import pytest

from automata.core.code_handling.py.reader import PyReader
from automata.core.singletons.module_loader import py_module_loader


@pytest.fixture(autouse=True)
def module_loader():
    py_module_loader.initialize(
        os.path.join(os.path.dirname(os.path.abspath(__file__))),
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "sample_modules"),
    )
    yield py_module_loader
    py_module_loader._dotpath_map = None
    py_module_loader.initialized = False
    py_module_loader.py_fpath = None
    py_module_loader.root_fpath = None


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
    result = getter.get_source_code_without_docstrings(module_name, object_path)
    expected_match = 'def say_hello(self):\n        return f"Hello, I am {self.name}."\n\n    '
    assert result == expected_match


def test_get_docstring_no_docstring_class(getter):
    module_name = "sample_modules.sample"
    object_path = "Person"
    result = getter.get_docstring(module_name, object_path)
    expected_match = "This is a sample class."
    assert result == expected_match


def test_get_code_module(getter):
    module_name = "sample_modules.sample"
    object_path = None
    result = getter.get_source_code_without_docstrings(module_name, object_path)
    expected_match = 'import math\n\n\ndef sample_function(name):\n    return f"Hello, {name}! Sqrt(2) = " + str(math.sqrt(2))\n\n\nclass Person:\n\n    def __init__(self, name):\n        self.name = name\n\n    def say_hello(self):\n        return f"Hello, I am {self.name}."\n\n    def run(self) -> str:\n        return "run"\n\n\ndef f(x) -> int:\n    return x + 1\n\n\nclass EmptyClass:\n    pass\n\n\nclass OuterClass:\n    class InnerClass:\n\n        def inner_method(self):\n'
    assert result.split("\n") == expected_match.split("\n")


def test_get_docstring_multiline(getter):
    module_name = "sample_modules.sample2"
    object_path = "PythonAgentToolkit.__init__"
    result = getter.get_docstring(module_name, object_path)
    expected = "\n        Initializes a PythonAgentToolkit with the given PythonAgent.\n\n        Args:\n            python_agent (PythonAgent): A PythonAgent instance representing the agent to work with.\n        "

    assert result == expected


def test_get_code_no_docstring_no_code(getter):
    module_name = "sample_modules.sample"
    object_path = "EmptyClass"
    result = getter.get_source_code_without_docstrings(module_name, object_path)
    expected_match = "class EmptyClass:\n    pass\n\n\n"
    assert result == expected_match


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
