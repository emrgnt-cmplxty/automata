import os

import pytest

from automata.tools.python_tools.python_indexer import PythonIndexer


@pytest.fixture
def indexer():
    # get latest path
    sample_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "sample_modules")
    # Set the root directory to the folder containing test modules
    return PythonIndexer(sample_dir)


def test_build_overview():
    sample_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "sample_modules")
    result = PythonIndexer.build_overview(sample_dir)
    first_module_overview = "test_module\n     - func test_function\n     - cls TestClass\n       - func __init__\n       - func test_method"
    assert result.startswith(
        first_module_overview
    )  # the other module gets randomly overwritten each time


def test_retrieve_docstring_function(indexer):
    module_name = "test_module"
    object_path = "test_function"
    result = indexer.retrieve_docstring(module_name, object_path)
    expected_match = "This is my new function"
    assert result == expected_match


def test_retrieve_code_method(indexer):
    module_name = "test_module"
    object_path = "TestClass.test_method"
    result = indexer.retrieve_code_without_docstrings(module_name, object_path)
    expected_match = "def test_method(self) -> bool:\n        return False\n"
    assert result == expected_match


def test_retrieve_docstring_method(indexer):
    module_name = "test_module"
    object_path = "TestClass.test_method"
    result = indexer.retrieve_docstring(module_name, object_path)
    expected_match = "This is my test method"
    assert result == expected_match


def test_retrieve_code_class(indexer):
    module_name = "test_module"
    object_path = "TestClass"
    result = indexer.retrieve_code_without_docstrings(module_name, object_path)

    expected_match = "class TestClass:\n\n    def __init__(self):\n        pass\n\n    def test_method(self) -> bool:\n        return False\n"
    assert result == expected_match


def test_retrieve_docstring_class(indexer):
    module_name = "test_module"
    object_path = "TestClass"
    result = indexer.retrieve_docstring(module_name, object_path)
    expected_match = "This is my test class"
    assert result == expected_match


def test_retrieve_code_module(indexer):
    module_name = "test_module"
    object_path = None
    result = indexer.retrieve_code_without_docstrings(module_name, object_path)
    expected_match = "\n\ndef test_function() -> bool:\n    return True\n\n\nclass TestClass:\n\n    def __init__(self):\n        pass\n\n    def test_method(self) -> bool:\n        return False\n"
    assert result == expected_match


def test_docstring_module(indexer):
    module_name = "test_module"
    object_path = None
    result = indexer.retrieve_docstring(module_name, object_path)
    expected_match = "This is a sample module for testing"
    assert result == expected_match


def test_retrieve_code_by_line(indexer):
    module_name = "test_module"
    line_number = 4
    result = indexer.retrieve_parent_code_by_line(module_name, line_number)
    expected_match = '"""This is a sample module for testing"""\n...\ndef test_function() -> bool:\n    """This is my new function"""\n    return True\n'

    assert result == expected_match

    line_number = 18
    result = indexer.retrieve_parent_code_by_line(module_name, line_number)

    expected_match = '"""This is a sample module for testing"""\n...\ndef test_function() -> bool:\n    """This is my new function"""\n...\nclass TestClass:\n    """This is my test class"""\n...\n    def __init__(self):\n    """This initializes TestClass"""\n...\n    def test_method(self) -> bool:\n        """This is my test method"""\n        return False\n'
    assert result == expected_match


def test_find_expression_context(indexer):
    expression = "test_function"
    result = indexer.find_expression_context(expression)
    expected_match = 'test_module.test_function\nL2-6\n```\n\ndef test_function() -> bool:\n    """This is my new function"""\n    return True```\n\n'
    assert result == expected_match
