import os
import ast
import pytest
from spork.tools.python_tools.python_ast_indexer import PythonASTIndexer


@pytest.fixture
def indexer():
    # get latest path
    root_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "sample_modules")
    # Set the root directory to the folder containing test modules
    return PythonASTIndexer(root_dir)


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
    print("result = ", result)
    expected_match = "def test_function() -> bool:\n    return True\n\nclass TestClass:\n\n    def __init__(self):\n        pass\n\n    def test_method(self) -> bool:\n        return False"
    assert result == expected_match


def test_docstring_module(indexer):
    module_name = "test_module"
    object_path = None
    result = indexer.retrieve_docstring(module_name, object_path)
    print("result = ", result)
    expected_match = "This is a sample module for testing"
    assert result == expected_match


# def test_search_code_no_result(searcher):
#     search_term = "non_existent_function"
#     module_name = "test_module"

#     results = searcher.search_code(search_term, module_name)
#     assert len(results) == 0


# def test_search_docstrings(searcher):
#     search_term = "Sample docstring"
#     module_name = "test_module"

#     results = searcher.search_docstrings(search_term, module_name)
#     assert len(results) == 1
#     assert isinstance(results[0], ast.FunctionDef)
#     assert search_term in ast.get_docstring(results[0])


# def test_search_docstrings_no_result(searcher):
#     search_term = "Non-existent docstring"
#     module_name = "test_module"

#     results = searcher.search_docstrings(search_term, module_name)
#     assert len(results) == 0
