import os
import textwrap

import pytest

from automata.core.code_indexing.python_ast_indexer import PythonASTIndexer
from automata.core.code_indexing.python_code_getter import PythonCodeInspector


@pytest.fixture
def indexer():
    # get latest path
    sample_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "sample_modules")
    # Set the root directory to the folder containing test modules
    return PythonASTIndexer(sample_dir)


@pytest.fixture
def getter(indexer):
    # get latest path
    python_getter = PythonCodeInspector(indexer)
    # Set the root directory to the folder containing test modules
    return python_getter


def test_build_overview():
    sample_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "sample_modules")
    result = PythonASTIndexer.build_repository_overview(sample_dir)
    first_module_overview = textwrap.dedent(
        """local_module_2
     - cls JSztF
       - func __init__
       - func method
     - func TtAsi
local_module
     - func test_function
     - cls TestClass
       - func __init__
       - func test_method"""
    )
    assert first_module_overview in result


def test_get_docstring_function(getter):
    module_name = "local_module"
    object_path = "test_function"
    result = getter.get_docstring(module_name, object_path)
    expected_match = "This is my new function"
    assert result == expected_match


def test_get_code_no_docstring_method(getter):
    module_name = "local_module"
    object_path = "TestClass.test_method"
    result = getter.get_source_code_without_docstrings(module_name, object_path)
    expected_match = "def test_method(self) -> bool:\n        return False\n"
    assert result == expected_match


def test_get_docstring_no_docstring_class(getter):
    module_name = "local_module"
    object_path = "TestClass"
    result = getter.get_docstring(module_name, object_path)
    expected_match = "This is my test class"
    assert result == expected_match


def test_get_code_module(getter):
    module_name = "local_module"
    object_path = None
    result = getter.get_source_code_without_docstrings(module_name, object_path)
    expected_match = "\n\ndef test_function() -> bool:\n    return True\n\n\nclass TestClass:\n\n    def __init__(self):\n        pass\n\n    def test_method(self) -> bool:\n        return False\n"
    assert result == expected_match


def test_get_code_by_line(getter):
    module_name = "local_module"
    line_number = 4
    result = getter.get_parent_code_by_line(module_name, line_number)
    expected_match = '"""This is a sample module for testing"""\n...\ndef test_function() -> bool:\n    """This is my new function"""\n    return True\n'

    assert result == expected_match

    line_number = 18
    result = getter.get_parent_code_by_line(module_name, line_number)

    expected_match = '"""This is a sample module for testing"""\n...\ndef test_function() -> bool:\n    """This is my new function"""\n...\nclass TestClass:\n    """This is my test class"""\n...\n    def __init__(self):\n    """This initializes TestClass"""\n...\n    def test_method(self) -> bool:\n        """This is my test method"""\n        return False\n'
    assert result == expected_match


def test_find_expression_context(getter):
    expression = "test_function"
    result = getter.get_expression_context(expression)
    expected_match = 'local_module.test_function\nL2-6\n```\n\ndef test_function() -> bool:\n    """This is my new function"""\n    return True```\n\n'
    assert result == expected_match


def test_get_docstring_multiline(getter):
    module_name = "local_module_3"
    object_path = "multi_line_doc_function"
    result = getter.get_docstring(module_name, object_path)
    expected_match = """This is a function with a multi-line docstring.
    
    It should be handled correctly by the get_docstring method."""
    assert result == expected_match


def test_get_code_no_docstring_no_code(getter):
    module_name = "local_module_5"
    object_path = "EmptyClass"
    result = getter.get_source_code_without_docstrings(module_name, object_path)
    expected_match = "class EmptyClass:\n    pass\n"
    assert result == expected_match


def test_get_docstring_nested_class(getter):
    module_name = "local_module_6"
    object_path = "OuterClass.InnerClass"
    result = getter.get_docstring(module_name, object_path)
    expected_match = "Inner doc strings"
    assert result == expected_match


def test_get_docstring_nested_class_method(getter):
    module_name = "local_module_6"
    object_path = "OuterClass.InnerClass.inner_method"
    result = getter.get_docstring(module_name, object_path)
    expected_match = "Inner method doc strings"
    assert result == expected_match
