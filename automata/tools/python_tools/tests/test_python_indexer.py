import os

import pytest

from automata.tools.python_tools.python_indexer import PythonIndexer


@pytest.fixture
def indexer():
    # get latest path
    sample_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "sample_modules")
    # Set the root directory to the folder containing test modules
    return PythonIndexer(sample_dir)


def test_retrieve_docstring_function(indexer):
    module_name = "test_module"
    object_path = "test_function"
    result = indexer.retrieve_docstring(module_name, object_path)
    expected_match = "This is my new function"
    assert result == expected_match


def test_retrieve_code_method(indexer):
    module_name = "test_module"
    object_path = "TestClass.test_method"
    result = indexer.retrieve_code(module_name, object_path)
    expected_match = "def test_method(self) -> bool:\n    return False"
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
    result = indexer.retrieve_code(module_name, object_path)
    expected_match = "class TestClass:\n\n    def __init__(self):\n        pass\n\n    def test_method(self) -> bool:\n        return False"
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
    result = indexer.retrieve_code(module_name, object_path)
    expected_match = "def test_function() -> bool:\n    return True\n\nclass TestClass:\n\n    def __init__(self):\n        pass\n\n    def test_method(self) -> bool:\n        return False"
    assert result == expected_match


def test_docstring_module(indexer):
    module_name = "test_module"
    object_path = None
    result = indexer.retrieve_docstring(module_name, object_path)
    expected_match = "This is a sample module for testing"
    assert result == expected_match
