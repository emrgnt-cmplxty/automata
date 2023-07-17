import logging
from unittest.mock import MagicMock, patch

import click.testing
import pytest

import automata.cli.commands


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
