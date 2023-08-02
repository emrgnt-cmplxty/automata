from unittest.mock import patch

import pytest

from automata.cli.cli_utils import ask_choice, initialize_py_module_loader
from automata.core.utils import get_root_fpath


@pytest.fixture
def default_args():
    return {
        "project_root_fpath": get_root_fpath(),
        "project_name": "automata",
        "project_project_name": "automata",
    }


@pytest.fixture
def mock_os():
    with patch("automata.cli.cli_utils.os") as mock_os:
        yield mock_os


@pytest.fixture
def mock_shutil():
    with patch("automata.cli.cli_utils.shutil") as mock_shutil:
        yield mock_shutil


@pytest.fixture
def mock_logger():
    with patch("automata.cli.cli_utils.logger") as mock_logger:
        yield mock_logger


@patch("automata.singletons.py_module_loader.py_module_loader.initialize")
def test_initialize_modules_defaults(mock_initialize, default_args):
    initialize_py_module_loader()
    mock_initialize.assert_called_once_with(
        default_args["project_root_fpath"],
        default_args["project_project_name"],
    )


@patch("automata.singletons.py_module_loader.py_module_loader.initialize")
def test_initialize_modules_custom_args(mock_initialize):
    custom_args = {
        "project_root_fpath": "/custom/root/path",
        "project_name": "custom_project",
        "project_project_name": "custom_path",
    }
    initialize_py_module_loader(**custom_args)
    mock_initialize.assert_called_once_with(
        custom_args["project_root_fpath"], custom_args["project_project_name"]
    )


@patch("automata.cli.cli_utils.prompt")
def test_ask_choice(mock_prompt):
    mock_prompt.return_value = {"choice": "Selected choice"}

    result = ask_choice("Test question", ["Choice 1", "Choice 2"])

    assert result == "Selected choice"
    mock_prompt.assert_called_once()
