import os

import pytest

from automata.core.coding.py_coding.module_tree import LazyModuleTreeMap
from automata.core.coding.py_coding.py_utils import build_repository_overview
from automata.core.coding.py_coding.retriever import PyCodeRetriever


@pytest.fixture
def module_map():
    # get latest path
    sample_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "sample_modules")
    # Set the root directory to the folder containing test modules
    return LazyModuleTreeMap(sample_dir)


@pytest.fixture
def getter(module_map):
    return PyCodeRetriever(module_map)


def test_build_overview():
    sample_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "sample_modules")
    result = build_repository_overview(sample_dir)
    first_module_overview = "sample\n     - func sample_function\n     - cls Person\n       - func __init__\n       - func say_hello\n       - func run\n     - func f\n     - cls EmptyClass\n     - cls OuterClass\n       - cls InnerClass\n         - func inner_method\nsample2\n     - cls PythonAgentToolBuilder\n       - func __init__\n       - func build\n         - func python_agent_python_task"

    assert first_module_overview in result


def test_get_docstring_function(getter):
    module_name = "sample"
    object_path = "sample_function"

    result = getter.get_docstring(module_name, object_path)
    expected_match = "This is a sample function."
    assert result == expected_match


def test_get_code_no_docstring_method(getter):
    module_name = "sample"
    object_path = "Person.say_hello"
    result = getter.get_source_code_without_docstrings(module_name, object_path)
    expected_match = 'def say_hello(self):\n        return f"Hello, I am {self.name}."\n\n    '
    assert result == expected_match


def test_get_docstring_no_docstring_class(getter):
    module_name = "sample"
    object_path = "Person"
    result = getter.get_docstring(module_name, object_path)
    expected_match = "This is a sample class."
    assert result == expected_match


def test_get_code_module(getter):
    module_name = "sample"
    object_path = None
    result = getter.get_source_code_without_docstrings(module_name, object_path)
    expected_match = 'import math\n\n\ndef sample_function(name):\n    return f"Hello, {name}! Sqrt(2) = " + str(math.sqrt(2))\n\n\nclass Person:\n\n    def __init__(self, name):\n        self.name = name\n\n    def say_hello(self):\n        return f"Hello, I am {self.name}."\n\n    def run(self) -> str:\n        ...\n\n\ndef f(x) -> int:\n    return x + 1\n\n\nclass EmptyClass:\n    pass\n\n\nclass OuterClass:\n    class InnerClass:\n\n        def inner_method(self):\n'

    assert result == expected_match


def test_get_docstring_multiline(getter):
    module_name = "sample2"
    object_path = "PythonAgentToolBuilder.__init__"
    result = getter.get_docstring(module_name, object_path)
    expected = "\n        Initializes a PythonAgentToolBuilder with the given PythonAgent.\n\n        Args:\n            python_agent (PythonAgent): A PythonAgent instance representing the agent to work with.\n        "

    assert result == expected


def test_get_code_no_docstring_no_code(getter):
    module_name = "sample"
    object_path = "EmptyClass"
    result = getter.get_source_code_without_docstrings(module_name, object_path)
    expected_match = "class EmptyClass:\n    pass\n\n\n"
    assert result == expected_match


def test_get_docstring_nested_class(getter):
    module_name = "sample"
    object_path = "OuterClass.InnerClass"
    result = getter.get_docstring(module_name, object_path)
    expected_match = "Inner doc strings"
    assert result == expected_match


def test_get_docstring_nested_class_method(getter):
    module_name = "sample"
    object_path = "OuterClass.InnerClass.inner_method"
    result = getter.get_docstring(module_name, object_path)
    expected_match = "Inner method doc strings"
    assert result == expected_match
