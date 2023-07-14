import logging
from unittest.mock import MagicMock, patch

import click.testing
import pytest

import automata.cli.commands


def test_reconfigure_logging_debug():
    with patch(
        "automata.cli.commands.get_logging_config"
    ) as mock_get_logging_config, patch("logging.config.dictConfig") as mock_dictConfig:
        mock_get_logging_config.return_value = {}
        automata.cli.commands.reconfigure_logging("DEBUG")
        mock_get_logging_config.assert_called_once_with(log_level=logging.DEBUG)
        mock_dictConfig.assert_called_once_with({})


def test_reconfigure_logging_info():
    with patch(
        "automata.cli.commands.get_logging_config"
    ) as mock_get_logging_config, patch("logging.config.dictConfig") as mock_dictConfig:
        mock_get_logging_config.return_value = {}
        automata.cli.commands.reconfigure_logging("INFO")
        mock_get_logging_config.assert_called_once_with(log_level=logging.INFO)
        mock_dictConfig.assert_called_once_with({})


def test_reconfigure_logging_invalid():
    with pytest.raises(ValueError):
        automata.cli.commands.reconfigure_logging("INVALID")


# FIXME: This test is failing
# def test_cli_run_code_embedding():
#     with patch('automata.cli.scripts.run_code_embedding.main') as mock_main:
#         runner = click.testing.CliRunner()
#         result = runner.invoke(automata.cli.commands.cli, ['run-doc-embedding', '--embedding-level', '2'])
#         assert result.exit_code == 0
#         mock_main.assert_called_once()
