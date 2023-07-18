import logging
from unittest.mock import MagicMock, patch

import click.testing
import pytest

import automata.cli.commands


@pytest.fixture()
def mock_logger():
    with patch("automata.cli.commands.logger") as mock_logger:
        yield mock_logger


@pytest.fixture()
def mock_ask_choice():
    with patch("automata.cli.commands.ask_choice") as mock_ask_choice:
        yield mock_ask_choice


@pytest.fixture()
def runner():
    return click.testing.CliRunner()


def test_reconfigure_logging_debug():
    with patch(
        "automata.cli.commands.get_logging_config"
    ) as mock_get_logging_config, patch(
        "logging.config.dictConfig"
    ) as mock_dictConfig:
        mock_get_logging_config.return_value = {}
        automata.cli.commands.reconfigure_logging("DEBUG")
        mock_get_logging_config.assert_called_once_with(
            log_level=logging.DEBUG
        )
        mock_dictConfig.assert_called_once_with({})


def test_reconfigure_logging_info():
    with patch(
        "automata.cli.commands.get_logging_config"
    ) as mock_get_logging_config, patch(
        "logging.config.dictConfig"
    ) as mock_dictConfig:
        mock_get_logging_config.return_value = {}
        automata.cli.commands.reconfigure_logging("INFO")
        mock_get_logging_config.assert_called_once_with(log_level=logging.INFO)
        mock_dictConfig.assert_called_once_with({})


def test_reconfigure_logging_invalid():
    with pytest.raises(ValueError):
        automata.cli.commands.reconfigure_logging("INVALID")


def test_cli_run_code_embedding():
    with patch(
        "automata.cli.scripts.run_code_embedding.main"
    ) as mock_main, patch(
        "automata.cli.commands.reconfigure_logging"
    ) as mock_reconfigure_logging, patch(
        "logging.getLogger"
    ) as mock_getLogger:
        mock_getLogger.return_value = MagicMock(spec=logging.Logger)

        runner = click.testing.CliRunner()
        result = runner.invoke(
            automata.cli.commands.cli, ["run-code-embedding"]
        )

        assert result.exit_code == 0
        mock_reconfigure_logging.assert_called_once_with("DEBUG")
        mock_main.assert_called_once()


def test_cli_run_doc_embedding():
    with patch(
        "automata.cli.scripts.run_doc_embedding.main"
    ) as mock_main, patch(
        "automata.cli.commands.reconfigure_logging"
    ) as mock_reconfigure_logging, patch(
        "logging.getLogger"
    ) as mock_getLogger:
        mock_getLogger.return_value = MagicMock(spec=logging.Logger)
        mock_main.return_value = "doc_embedding_result"

        runner = click.testing.CliRunner()
        result = runner.invoke(
            automata.cli.commands.cli,
            ["run-doc-embedding", "--embedding-level", "2"],
        )

        assert result.exit_code == 0
        mock_reconfigure_logging.assert_called_once_with("DEBUG")
        assert mock_main.called


def test_cli_run_doc_post_process():
    with patch(
        "automata.cli.scripts.run_doc_post_process.main"
    ) as mock_main, patch(
        "automata.cli.commands.reconfigure_logging"
    ) as mock_reconfigure_logging, patch(
        "logging.getLogger"
    ) as mock_getLogger:
        mock_getLogger.return_value = MagicMock(spec=logging.Logger)

        runner = click.testing.CliRunner()
        result = runner.invoke(
            automata.cli.commands.cli, ["run-doc-post-process"]
        )

        assert result.exit_code == 0
        mock_reconfigure_logging.assert_called_once_with("DEBUG")
        mock_main.assert_called_once()


def test_cli_run_agent():
    with patch("automata.cli.scripts.run_agent.main") as mock_main, patch(
        "automata.cli.commands.reconfigure_logging"
    ) as mock_reconfigure_logging, patch(
        "logging.getLogger"
    ) as mock_getLogger:
        mock_getLogger.return_value = MagicMock(spec=logging.Logger)

        runner = click.testing.CliRunner()
        result = runner.invoke(
            automata.cli.commands.cli, ["run-agent", "--fetch-issues", "1,2,3"]
        )

        assert result.exit_code == 0
        mock_reconfigure_logging.assert_called_once_with("DEBUG")
        assert mock_main.called


def test_configure_setup_files_called(runner, mock_logger):
    with patch("automata.cli.commands.setup_files") as mock_setup_files:
        runner.invoke(automata.cli.commands.cli, ["configure"])
        mock_setup_files.assert_called_once_with(
            SCRIPTS_PATH="scripts/", DOTENV_PATH=".env"
        )


def test_configure_load_env_vars_called(runner, mock_logger):
    with patch("automata.cli.commands.load_env_vars") as mock_load_env_vars:
        runner.invoke(automata.cli.commands.cli, ["configure"])
        mock_load_env_vars.assert_called_once_with(
            DOTENV_PATH=".env",
            DEFAULT_KEYS={
                "GITHUB_API_KEY": "your_github_api_key",
                "OPENAI_API_KEY": "your_openai_api_key",
            },
        )


def test_configure_ask_choice_called(runner, mock_ask_choice, mock_logger):
    mock_ask_choice.return_value = "GITHUB_API_KEY"
    runner.invoke(automata.cli.commands.cli, ["configure"])
    assert mock_ask_choice.call_count == 2



@pytest.mark.parametrize(
    "operation_choice, expected_function",
    [
        ("Show", "show_key_value"),
        ("Update", "update_key_value"),
        ("Delete", "delete_key_value"),
    ],
)
def test_configure_operation_choice(
    runner, mock_ask_choice, operation_choice, expected_function, mock_logger
):
    mock_ask_choice.side_effect = ["GITHUB_API_KEY", operation_choice]
    with patch(f"automata.cli.commands.{expected_function}") as mock_func:
        runner.invoke(automata.cli.commands.cli, ["configure"])
        mock_func.assert_called_once_with(".env", "GITHUB_API_KEY")


def test_reconfigure_logging_quiet_libraries():
    with patch(
        "automata.cli.commands.get_logging_config"
    ) as mock_get_logging_config, patch(
        "logging.config.dictConfig"
    ) as mock_dictConfig, patch(
        "logging.getLogger"
    ) as mock_getLogger:
        mock_get_logging_config.return_value = {}
        mock_logger = MagicMock(spec=logging.Logger)
        mock_getLogger.return_value = mock_logger

        automata.cli.commands.reconfigure_logging("DEBUG")

        mock_get_logging_config.assert_called_once_with(
            log_level=logging.DEBUG
        )
        mock_dictConfig.assert_called_once_with({})
        assert (
            mock_getLogger.call_count == 5
        )  # 4 for external libraries, 1 for __name__

        mock_logger.setLevel.assert_called_with(logging.INFO)
