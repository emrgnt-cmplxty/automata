import click
import pytest

from automata.cli.options import common_options


@pytest.fixture
def command_with_options():
    @click.command()
    def dummy_command():
        pass

    return common_options(dummy_command)


def test_common_options_length(command_with_options):
    assert len(command_with_options.params) == 4


def test_common_options_project_rel_py_path(command_with_options):
    project_rel_py_path_option = command_with_options.params[0]
    assert project_rel_py_path_option.name == "project_rel_py_path"
    assert project_rel_py_path_option.default is None


def test_common_options_project_root_fpath(command_with_options):
    project_root_fpath_option = command_with_options.params[1]
    assert project_root_fpath_option.name == "project_root_fpath"
    assert project_root_fpath_option.default is None


def test_common_options_project_name(command_with_options):
    project_name_option = command_with_options.params[2]
    assert project_name_option.name == "project_name"
    assert project_name_option.default == "automata"


def test_common_options_log_level(command_with_options):
    log_level_option = command_with_options.params[3]
    assert log_level_option.name == "log_level"
    assert log_level_option.default == "DEBUG"
