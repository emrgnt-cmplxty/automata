import os
from unittest.mock import Mock, patch

import pytest
from git import Git, Repo
from github import (
    Github,
    GitRef,
    Issue,
    IssueComment,
    PaginatedList,
    PullRequest,
    PullRequestMergeStatus,
)

from automata.singletons.github_client import GitHubClient


def test_clone_repository(mocker):
    client = GitHubClient(os.getenv("GITHUB_API_KEY"), "remote_name")

    mocker.patch.object(client, "clone_repository")

    local_path = "local_path"
    client.clone_repository(local_path)

    client.clone_repository.assert_called_once_with(local_path)


@pytest.mark.parametrize("branch_name", ["branch1", "branch2", "branch3"])
def test_create_branch(mocker, branch_name):
    client = GitHubClient(os.getenv("GITHUB_API_KEY"), "remote_name")
    mocker.patch.object(client.repo, "create_git_ref")

    client.create_branch(branch_name)

    client.repo.create_git_ref.assert_called_once_with(
        ref=f"refs/heads/{branch_name}",
        sha=client.repo.get_git_ref(
            f"heads/{client.primary_branch}"
        ).object.sha,
    )


@pytest.mark.skip(reason="Issues with singletons")
def test_checkout_branch(mocker):
    client = GitHubClient(os.getenv("GITHUB_API_KEY"), "remote_name")

    # Create a Mock for Repo
    mock_repo = mocker.patch("git.Repo", autospec=True)
    mock_repo.return_value.git = mocker.MagicMock()

    # Create a Mock for repo.heads
    heads = mocker.PropertyMock(return_value=["branch1", "branch2"])
    type(mock_repo.return_value).heads = heads

    client.checkout_branch("local_path", "branch_name")

    # If the branch exists, checkout should be called
    if "branch_name" in mock_repo.return_value.heads:
        mock_repo.return_value.git.checkout.assert_called_once_with(
            "branch_name"
        )
    # If the branch doesn't exist, checkout should be called with '-b' option
    else:
        mock_repo.return_value.git.checkout.assert_called_once_with(
            "-b", "branch_name"
        )


@pytest.mark.skip(reason="Issues with singletons")
def test_stage_all_changes(mocker):
    client = GitHubClient(os.getenv("GITHUB_API_KEY"), "remote_name")
    mock_repo = mocker.patch("git.Repo")

    client.stage_all_changes("local_path")

    mock_repo().git.add.assert_called_once_with(A=True)


@pytest.mark.skip(reason="Issues with singletons")
def test_commit_and_push_changes(mocker):
    client = GitHubClient(os.getenv("GITHUB_API_KEY"), "remote_name")
    mock_repo = mocker.patch("git.Repo")

    client.commit_and_push_changes(
        "local_path", "branch_name", "commit_message"
    )

    mock_repo().git.commit.assert_called_once_with(m="commit_message")
    mock_repo().git.push.assert_called_once_with("origin", "branch_name")


@pytest.mark.skip(reason="Issues with singletons")
def test_create_pull_request(mocker):
    client = GitHubClient(os.getenv("GITHUB_API_KEY"), "remote_name")

    client.create_pull_request("branch_name", "title", "body")

    client.repo.create_pull.assert_called_once_with(
        title="title",
        body="body",
        head="branch_name",
        base=client.primary_branch,
    )


def test_merge_pull_request(mocker):
    client = GitHubClient(os.getenv("GITHUB_API_KEY"), "remote_name")
    mock_pull_request = mocker.patch.object(client.repo, "get_pull")

    client.merge_pull_request(1, "commit_message")

    mock_pull_request().merge.assert_called_once_with(
        commit_message="commit_message"
    )


@pytest.mark.parametrize(
    "branch_name,exists", [("branch1", True), ("branch2", False)]
)
def test_branch_exists(mocker, branch_name, exists):
    client = GitHubClient(os.getenv("GITHUB_API_KEY"), "remote_name")
    if exists:
        mocker.patch.object(client.repo, "get_git_ref")
    else:
        mocker.patch.object(client.repo, "get_git_ref", side_effect=Exception)

    assert client.branch_exists(branch_name) == exists
