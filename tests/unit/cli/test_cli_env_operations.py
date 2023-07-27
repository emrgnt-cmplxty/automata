from unittest.mock import mock_open, patch, call

import pytest

from automata.cli.env_operations import (
    delete_key_value,
    get_key,
    load_env_vars,
    replace_key,
    show_key_value,
    update_key_value,
)


@pytest.fixture
def dotenv_path():
    return ".env"


@pytest.fixture
def default_keys():
    return {
        "GITHUB_API_KEY": "your_github_api_key",
        "OPENAI_API_KEY": "your_openai_api_key",
    }


def test_get_key(dotenv_path):
    with patch(
        "builtins.open", new_callable=mock_open, read_data="KEY=test\n"
    ) as mock_file:
        value = get_key(dotenv_path, "KEY")
        assert value == "test"
        mock_file.assert_called_once_with(dotenv_path, "r")


def test_replace_key(dotenv_path):
    with patch(
        "builtins.open", new_callable=mock_open, read_data="KEY=old\n"
    ) as mock_file:
        replace_key(dotenv_path, "KEY", "new")
        mock_file.assert_any_call(dotenv_path, "r")
        mock_file.assert_any_call(dotenv_path, "w")
        handle = mock_file()
        handle.writelines.assert_called_once_with(["KEY=new\n"])


def test_load_env_vars(dotenv_path, default_keys):
    with patch(
        "automata.cli.env_operations.get_key",
        return_value="your_github_api_key",
    ), patch(
        "automata.cli.env_operations.replace_key"
    ) as mock_replace_key, patch(
        "automata.cli.env_operations.input", return_value="new"
    ), patch(
        "dotenv.load_dotenv"
    ):
        load_env_vars(dotenv_path, default_keys)
    calls = [call(dotenv_path, "GITHUB_API_KEY", "new"), call(dotenv_path, "OPENAI_API_KEY", "your_github_api_key")]
    mock_replace_key.assert_has_calls(calls, any_order=True)



def test_show_key_value(dotenv_path):
    with patch(
        "automata.cli.env_operations.get_key", return_value="value"
    ), patch("automata.cli.env_operations.log_cli_output") as mock_log:
        show_key_value(dotenv_path, "KEY")
        mock_log.assert_called_once_with("The value of KEY is: value")


def test_update_key_value(dotenv_path):
    with patch("automata.cli.env_operations.input", return_value="new"), patch(
        "automata.cli.env_operations.replace_key"
    ) as mock_replace_key, patch(
        "automata.cli.env_operations.log_cli_output"
    ) as mock_log:
        update_key_value(dotenv_path, "KEY")
        mock_replace_key.assert_called_once_with(dotenv_path, "KEY", "new")
        mock_log.assert_called_once_with("The value of KEY has been updated.")


def test_delete_key_value(dotenv_path):
    with patch("automata.cli.env_operations.input", return_value="y"), patch(
        "automata.cli.env_operations.replace_key"
    ) as mock_replace_key, patch(
        "automata.cli.env_operations.log_cli_output"
    ) as mock_log:
        delete_key_value(dotenv_path, "KEY")
        mock_replace_key.assert_called_once_with(dotenv_path, "KEY", "")
        mock_log.assert_called_once_with("The value of KEY has been deleted.")
