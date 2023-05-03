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


def test_retrieve_code_by_line(indexer):
    module_name = "test_module"
    line_number = 4
    result = indexer.retrieve_outer_code_by_line(module_name, line_number)
    expected_match = '4: def test_function() -> bool:    <------\n5:     """This is my new function"""\n6:     return True'
    assert result == expected_match

    line_number = 18
    result = indexer.retrieve_outer_code_by_line(module_name, line_number)
    expected_match = '9: class TestClass:\n10:     """This is my test class"""\n11: \n12:     def __init__(self):\n13:         """This initializes TestClass"""\n14:         pass\n15: \n16:     def test_method(self) -> bool:\n17:         """This is my test method"""\n18:         return False    <------'
    assert result == expected_match
