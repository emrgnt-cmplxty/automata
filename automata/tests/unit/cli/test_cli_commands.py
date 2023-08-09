import logging
from unittest.mock import MagicMock, patch

import click.testing
import pytest
from click.testing import CliRunner

import automata.cli.commands

DOTENV_PATH = ".env"
SCRIPTS_PATH = "scripts/"
DEFAULT_KEYS = {
    "GITHUB_API_KEY": "your_github_api_key",
    "OPENAI_API_KEY": "your_openai_api_key",
    "GRAPH_TYPE": "dynamic",
    "DATA_ROOT_PATH": "automata-embedding-data",
}


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


def test_configure_logging_debug():
    with patch(
        "automata.cli.commands.get_logging_config"
    ) as mock_get_logging_config, patch(
        "logging.config.dictConfig"
    ) as mock_dictConfig:
        mock_get_logging_config.return_value = {}
        automata.cli.commands.configure_logging("DEBUG")
        mock_get_logging_config.assert_called_once_with(
            log_level=logging.DEBUG
        )
        mock_dictConfig.assert_called_once_with({})


def test_configure_logging_info():
    with patch(
        "automata.cli.commands.get_logging_config"
    ) as mock_get_logging_config, patch(
        "logging.config.dictConfig"
    ) as mock_dictConfig:
        mock_get_logging_config.return_value = {}
        automata.cli.commands.configure_logging("INFO")
        mock_get_logging_config.assert_called_once_with(log_level=logging.INFO)
        mock_dictConfig.assert_called_once_with({})


def test_configure_logging_invalid():
    with pytest.raises(ValueError):
        automata.cli.commands.configure_logging("INVALID")


def test_cli_run_code_embedding():
    with patch(
        "automata.cli.scripts.run_code_embedding.main"
    ) as mock_main, patch(
        "automata.cli.commands.configure_logging"
    ) as mock_configure_logging, patch(
        "logging.getLogger"
    ) as mock_getLogger:
        mock_getLogger.return_value = MagicMock(spec=logging.Logger)

        runner = click.testing.CliRunner()
        result = runner.invoke(
            automata.cli.commands.cli, ["run-code-embedding"]
        )

        assert result.exit_code == 0
        mock_configure_logging.assert_called_once_with(log_level_str="INFO")
        mock_main.assert_called_once()


def test_cli_run_doc_embedding():
    with patch(
        "automata.cli.scripts.run_doc_embedding.main"
    ) as mock_main, patch(
        "automata.cli.commands.configure_logging"
    ) as mock_configure_logging, patch(
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
        mock_configure_logging.assert_called_once_with(log_level_str="INFO")
        assert mock_main.called


def test_cli_run_doc_post_process():
    with patch(
        "automata.cli.scripts.run_doc_post_process.main"
    ) as mock_main, patch(
        "automata.cli.commands.configure_logging"
    ) as mock_configure_logging, patch(
        "logging.getLogger"
    ) as mock_getLogger:
        mock_getLogger.return_value = MagicMock(spec=logging.Logger)

        runner = click.testing.CliRunner()
        result = runner.invoke(
            automata.cli.commands.cli, ["run-doc-post-process"]
        )

        assert result.exit_code == 0
        mock_configure_logging.assert_called_once_with(log_level_str="INFO")
        mock_main.assert_called_once()


def test_cli_run_agent():
    with patch("automata.cli.scripts.run_agent.main") as mock_main, patch(
        "automata.cli.commands.configure_logging"
    ) as mock_configure_logging, patch("logging.getLogger") as mock_getLogger:
        mock_getLogger.return_value = MagicMock(spec=logging.Logger)

        runner = click.testing.CliRunner()
        result = runner.invoke(
            automata.cli.commands.cli, ["run-agent", "--fetch-issues", "1,2,3"]
        )

        assert result.exit_code == 0
        mock_configure_logging.assert_called_once_with(log_level_str="INFO")
        assert mock_main.called


@patch("automata.cli.commands.setup_files")
def test_configure_setup_files_called(setup_files_mock):
    runner = CliRunner()
    runner.invoke(automata.cli.commands.cli, ["configure"])

    setup_files_mock.assert_called_once_with(
        scripts_path=SCRIPTS_PATH, dotenv_path=DOTENV_PATH
    )


@patch("automata.cli.commands.load_env_vars")
def test_configure_load_env_vars_called(load_env_vars_mock):
    runner = CliRunner()
    runner.invoke(automata.cli.commands.cli, ["configure"])
    load_env_vars_mock.assert_called_with(
        dotenv_path=DOTENV_PATH, default_keys=DEFAULT_KEYS
    )


def test_configure_logging_quiet_libraries():
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

        automata.cli.commands.configure_logging("DEBUG")

        mock_get_logging_config.assert_called_once_with(
            log_level=logging.DEBUG
        )
        mock_dictConfig.assert_called_once_with({})
        assert (
            mock_getLogger.call_count == 7
        )  # 6 for external libraries, 1 for __name__

        mock_logger.setLevel.assert_called_with(logging.INFO)
