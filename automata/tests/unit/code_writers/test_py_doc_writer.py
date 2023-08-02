from unittest.mock import MagicMock, mock_open, patch

import pytest

from automata.code_parsers import DirectoryManager
from automata.code_writers.py import (  # Replace with actual import path
    PyDocWriter,
)


def test_init():
    writer = PyDocWriter("/path/to/project")
    assert writer.base_path == "/path/to/project"
    assert isinstance(writer.directory_manager, DirectoryManager)


@pytest.mark.parametrize(
    "name, expected",
    [
        ("myVariable", "my_variable"),
        ("AnotherVariable", "another_variable"),
    ],
)
def test_camel_to_snake(name, expected):
    result = PyDocWriter.camel_to_snake(name)
    assert result == expected


@pytest.mark.parametrize(
    "name, expected",
    [
        ("myVariable", True),
        ("MyVariable", True),
        ("my_variable", False),
        ("My_Variable", False),
        ("MYVARIABLE", False),
        ("myvariable", False),
    ],
)
def test_check_camel_case(name, expected):
    result = PyDocWriter.check_camel_case(name)
    assert result == expected


@patch("builtins.open", new_callable=mock_open)
def test_generate_module_summary(mock_file):
    writer = PyDocWriter("/path/to/project")
    writer.directory_manager.get_files_in_dir = MagicMock(
        return_value=["file1.rst", "file2.rst", "index.rst"]
    )
    writer.generate_summary = MagicMock(return_value="Summary")
    writer.generate_module_summary("/path/to/module")
    mock_file.assert_called_with("/path/to/module/index.rst", "a")


@patch("builtins.open", new_callable=mock_open)
def test_write_documentation(mock_file):
    writer = PyDocWriter("/path/to/project")
    writer.generate_rst_files = MagicMock()
    writer.generate_index_files = MagicMock()
    writer.write_documentation({}, [], "/path/to/docs")
    writer.generate_rst_files.assert_called_once()
    writer.generate_index_files.assert_called_once()
