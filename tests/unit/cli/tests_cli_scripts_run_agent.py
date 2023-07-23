from unittest.mock import Mock, patch

import pytest

from automata.cli.scripts.run_agent import main, process_issues


@pytest.fixture
def mock_github_manager():
    with patch(
        "automata.singletons.github_client.GitHubClient"
    ) as mock_github_client:
        yield mock_github_client.return_value


@pytest.mark.skip(reason="Test not implemented yet")
def test_process_issues_without_issues(mock_github_manager):
    instructions = process_issues([], mock_github_manager)
    assert instructions == []


@pytest.mark.skip(reason="Test not implemented yet")
def test_process_issues_with_issues(mock_github_manager):
    mock_github_manager.fetch_issue.side_effect = (
        lambda number: Mock(
            number=number, title=f"Title {number}", body=f"Body {number}"
        )
        if number <= 3
        else None
    )
    issue_numbers = [1, 2, 3, 4]
    expected = [
        "Issue #1: Title 1\nBody 1",
        "Issue #2: Title 2\nBody 2",
        "Issue #3: Title 3\nBody 3",
    ]
    instructions = process_issues(issue_numbers, mock_github_manager)
    assert instructions == expected


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
        mock_dependency_get.return_value = (
            Mock()
        )  # Return a mock when get is called
        mock_dependency_get.return_value.get_top_symbols.return_value = [
            ("symbol1", 1)
        ]  # Simulate the behavior of get_top_symbols

        yield


@pytest.mark.skip(reason="Test not implemented yet")
def test_main(mock_dependencies):
    with patch(
        "automata.cli.scripts.run_agent.OpenAIAutomataAgent"
    ) as mock_agent:
        mock_agent.return_value.run.return_value = "Success"
        result = main(
            instructions="Test Instructions",
            agent_name="test-agent",
            toolkit_list="context-oracle",
        )
        mock_agent.assert_called_once_with(
            "Test Instructions",
            # config=AgentConfig.from_payload({"name": "test-agent", "model": "gpt-4-0613"}),
        )
        mock_agent.return_value.run.assert_called_once()
        assert result == "Success"
