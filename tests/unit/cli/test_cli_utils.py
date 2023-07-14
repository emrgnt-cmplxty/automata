from unittest.mock import patch

import pytest

from automata.cli.cli_utils import initialize_modules
from automata.core.utils import get_root_fpath
from automata.singletons.py_module_loader import py_module_loader


@pytest.fixture
def default_args():
    return {
        "project_root_fpath": get_root_fpath(),
        "project_name": "automata",
        "project_rel_py_path": "automata",
    }


@patch("automata.singletons.py_module_loader.py_module_loader.initialize")
def test_initialize_modules_defaults(mock_initialize, default_args):
    initialize_modules()
    mock_initialize.assert_called_once_with(
        default_args["project_root_fpath"], default_args["project_rel_py_path"]
    )


@patch("automata.singletons.py_module_loader.py_module_loader.initialize")
def test_initialize_modules_custom_args(mock_initialize):
    custom_args = {
        "project_root_fpath": "/custom/root/path",
        "project_name": "custom_project",
        "project_rel_py_path": "custom_path",
    }
    initialize_modules(**custom_args)
    mock_initialize.assert_called_once_with(
        custom_args["project_root_fpath"], custom_args["project_rel_py_path"]
    )
