from unittest.mock import MagicMock, patch

import pytest
from github.MainClass import Github

from automata.singletons.github_client import GitHubClient


@pytest.fixture
def gh_client():
    with patch.object(
        Github, "get_repo", return_value=MagicMock()
    ) as mock_get_repo:
        mock_get_repo.return_value.get_git_ref.return_value.object.sha = (
            "test_sha"
        )
        mock_get_repo.return_value.create_pull.return_value = MagicMock()
        mock_get_repo.return_value.create_issue.return_value = MagicMock()

        client = GitHubClient("access_token", "remote_name")
        client.repo = mock_get_repo.return_value  # Get the mocked repo
        return client


def test_clone_repository(gh_client):
    # This test is omitted because it calls external Git and should be covered by integration tests
    pass


def test_create_branch(gh_client):
    with patch.object(gh_client.repo, "create_git_ref") as mock_create_git_ref:
        gh_client.create_branch("test_branch")
        mock_create_git_ref.assert_called_once_with(
            ref="refs/heads/test_branch", sha="test_sha"
        )


def test_checkout_branch(gh_client):
    with patch("automata.singletons.github_client.Repo") as MockRepo:
        mock_repo = MockRepo.return_value
        gh_client.checkout_branch("local_path", "test_branch")
        MockRepo.assert_called_once_with("local_path")
        mock_repo.git.checkout.assert_called_once_with("test_branch", b=True)


def test_stage_all_changes(gh_client):
    with patch("automata.singletons.github_client.Repo") as MockRepo:
        mock_repo = MockRepo.return_value
        gh_client.stage_all_changes("local_path")
        MockRepo.assert_called_once_with("local_path")
        mock_repo.git.add.assert_called_once_with(A=True)


def test_commit_and_push_changes(gh_client):
    with patch("automata.singletons.github_client.Repo") as MockRepo:
        mock_repo = MockRepo.return_value
        gh_client.commit_and_push_changes(
            "local_path", "test_branch", "test_commit"
        )
        MockRepo.assert_called_once_with("local_path")
        mock_repo.git.commit.assert_called_once_with(m="test_commit")
        mock_repo.git.push.assert_called_once_with("origin", "test_branch")


def test_create_pull_request(gh_client):
    with patch.object(
        gh_client.client, "get_repo", return_value=gh_client.repo
    ) as _:
        _ = gh_client.create_pull_request(
            "test_branch", "test_title", "test_body"
        )
        gh_client.repo.create_pull.assert_called_once_with(
            title="test_title",
            body="test_body",
            head="test_branch",
            base=gh_client.primary_branch,
        )


def test_create_issue(gh_client):
    with patch.object(
        gh_client.client, "get_repo", return_value=gh_client.repo
    ) as _:
        gh_client.create_issue("test_title", "test_body", ["label1", "label2"])
        gh_client.repo.create_issue.assert_called_once_with(
            title="test_title", body="test_body", labels=["label1", "label2"]
        )


@pytest.mark.parametrize(
    "branch, exists",
    [("existing_branch", True), ("non_existent_branch", False)],
)
def test_branch_exists(gh_client, branch, exists):
    if exists:
        gh_client.repo.get_git_ref.return_value = MagicMock()
    else:
        gh_client.repo.get_git_ref.side_effect = Exception()
    assert gh_client.branch_exists(branch) == exists


@pytest.mark.parametrize("issue_id, exists", [(1, True), (1, False)])
def test_fetch_issue(gh_client, issue_id, exists):
    if exists:
        gh_client.repo.get_issue.return_value = MagicMock()
        assert isinstance(gh_client.fetch_issue(issue_id), MagicMock)
    else:
        gh_client.repo.get_issue.side_effect = Exception()
        assert gh_client.fetch_issue(issue_id) is None
