import ast
import os

import pytest

from automata.core.utils import get_root_py_fpath
from automata.singletons.py_module_loader import py_module_loader


@pytest.fixture()
def root_path():
    return os.path.join(get_root_py_fpath(), "tests", "unit", "sample_modules")


@pytest.fixture()
def setup_module_loader(root_path):
    py_module_loader.reset()
    py_module_loader.initialize(root_path, "my_project")
    return py_module_loader


@pytest.fixture()
def local_module_loader(setup_module_loader):
    yield setup_module_loader


@pytest.fixture(autouse=True)
def cleanup():
    yield


def test_get_items(local_module_loader):
    assert len(local_module_loader._dotpath_map.items()) == 7


def test_dotpath_map(local_module_loader):
    # Test that we have the correct number of modules (Python files) in our DotPathMap
    assert len(local_module_loader._dotpath_map.items()) == 7

    # Test that we can correctly retrieve file paths from dotpaths
    assert (
        "sample_modules/my_project/core/calculator.py"
        in local_module_loader._dotpath_map.get_module_fpath_by_dotpath(
            "my_project.core.calculator"
        )
    )
    assert (
        "sample_modules/my_project/core/calculator2.py"
        in local_module_loader._dotpath_map.get_module_fpath_by_dotpath(
            "my_project.core.calculator2"
        )
    )
    assert (
        "sample_modules/my_project/core/extended/calculator3.py"
        in local_module_loader._dotpath_map.get_module_fpath_by_dotpath(
            "my_project.core.extended.calculator3"
        )
    )

    abs_path = os.path.join(get_root_py_fpath(), "tests", "unit")
    # Test that we can correctly retrieve dotpaths from file paths
    assert (
        "my_project.core.calculator"
        in local_module_loader._dotpath_map.get_module_dotpath_by_fpath(
            os.path.join(
                abs_path, "sample_modules/my_project/core/calculator.py"
            )
        )
    )
    assert (
        "my_project.core.calculator2"
        in local_module_loader._dotpath_map.get_module_dotpath_by_fpath(
            os.path.join(
                abs_path, "sample_modules/my_project/core/calculator2.py"
            )
        )
    )
    assert (
        "my_project.core.extended.calculator3"
        in local_module_loader._dotpath_map.get_module_dotpath_by_fpath(
            os.path.join(
                abs_path,
                "sample_modules/my_project/core/extended/calculator3.py",
            )
        )
    )


@pytest.mark.parametrize(
    "module, class_name",
    [
        ("my_project.core.calculator", "Calculator"),
        ("my_project.core.calculator2", "Calculator2"),
        ("my_project.core.extended.calculator3", "Calculator3"),
    ],
)
def test_load_module(local_module_loader, module, class_name):
    # Test that we can correctly load modules using dotpaths
    calculator_module = local_module_loader.fetch_ast_module(module)
    result = [
        node.name
        for node in ast.walk(calculator_module)
        if isinstance(node, ast.ClassDef)
    ]
    assert class_name in result


def test_invalid_dotpath(local_module_loader):
    # Test that an error is raised when trying to load a non-existent module
    assert (
        local_module_loader.fetch_ast_module("my_project.core.non_existent")
        is None
    )


def test_empty_dotpath(local_module_loader):
    # Test that an error is raised when trying to load an empty string
    assert local_module_loader.fetch_ast_module("") is None


def test_get_module_dotpath_by_fpath_for_invalid_path(local_module_loader):
    # Test that an error is raised when trying to retrieve a dotpath with a non-existent path
    with pytest.raises(KeyError):
        local_module_loader._dotpath_map.get_module_dotpath_by_fpath(
            "sample_modules/my_project/core/non_existent.py"
        )


def test_get_module_fpath_by_dotpath_for_invalid_dotpath(local_module_loader):
    # Test that an error is raised when trying to retrieve a file path with a non-existent dotpath
    with pytest.raises(KeyError):
        local_module_loader._dotpath_map.get_module_fpath_by_dotpath(
            "my_project.core.non_existent"
        )


def test_non_python_files(local_module_loader):
    # Test that non-python files are ignored by the loader
    assert "my_project.core.somefile" not in local_module_loader


def test_multiple_initializations(local_module_loader):
    # Test behavior when initialize is called more than once without setting initialized = False
    with pytest.raises(Exception):  # replace with your actual exception
        local_module_loader.initialize(
            os.path.join(
                get_root_py_fpath(), "tests", "unit", "sample_modules"
            ),
            "my_project",
        )


def test_directory_without_init(local_module_loader):
    # Test that directories without an __init__.py file are not included in the dotpath map
    assert "my_project.no_init.some_module" in local_module_loader
