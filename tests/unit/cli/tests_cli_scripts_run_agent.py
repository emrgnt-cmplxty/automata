from unittest.mock import Mock, patch

import pytest

from automata.cli.scripts.run_agent import (
    DEFAULT_ISSUES_PROMPT_PREFIX,
    DEFAULT_ISSUES_PROMPT_SUFFIX,
    build_agent_config,
    process_instructions,
)
from automata.config import AgentConfig


@pytest.fixture
def mock_github_manager():
    with patch("automata.singletons.github_client.GitHubClient") as mock_github_client:
        yield mock_github_client.return_value


def test_process_instructions_without_issues(mock_github_manager):
    instructions = process_instructions({}, mock_github_manager)
    assert instructions == "This is a dummy instruction, return True."


@patch("automata.cli.scripts.run_agent.process_issues")
def test_process_instructions_with_issues(mock_process_issues, mock_github_manager):
    mock_process_issues.return_value = ["issue1", "issue2"]
    instructions = process_instructions({"fetch_issues": "1,2"}, mock_github_manager)
    assert (
        instructions
        == DEFAULT_ISSUES_PROMPT_PREFIX
        + "\n".join(["issue1", "issue2"])
        + DEFAULT_ISSUES_PROMPT_SUFFIX
    )


@pytest.fixture
def mock_dependencies():
    with patch(
        "automata.singletons.dependency_factory.dependency_factory.build_dependencies_for_tools"
    ) as mock_build_dependencies, patch(
        "automata.tools.factory.AgentToolFactory.build_tools"
    ) as mock_build_tools, patch(
        "automata.singletons.dependency_factory.dependency_factory.get"
    ) as mock_dependency_get:
        mock_build_dependencies.return_value = {}
        mock_build_tools.return_value = []
        mock_dependency_get.return_value = Mock()  # Return a mock when get is called
        mock_dependency_get.return_value.get_top_symbols.return_value = [
            ("symbol1", 1)
        ]  # Simulate the behavior of get_top_symbols

        yield


def test_build_agent_config(mock_dependencies, mock_github_manager):
    config = build_agent_config({"toolkit_list": "tool1,tool2"})
    assert isinstance(config, AgentConfig)
