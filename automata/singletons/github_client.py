import os
from abc import ABC, abstractmethod
from typing import Any, List, Optional

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

from automata.core.base import Singleton


class RepositoryClient(ABC):
    """An abstract class for managing repositories"""

    @abstractmethod
    def clone_repository(self, local_path: str) -> Any:
        """Clone the repository to the local path."""
        pass

    @abstractmethod
    def create_branch(self, branch_name: str) -> Any:
        """Create a new branch in the repository."""
        pass

    @abstractmethod
    def checkout_branch(self, repo_local_path: str, branch_name: str) -> Any:
        """Checkout a branch in the repository."""
        pass

    @abstractmethod
    def stage_all_changes(self, repo_local_path: str) -> Any:
        """Stage all changes in the repository."""
        pass

    @abstractmethod
    def commit_and_push_changes(
        self, repo_local_path: str, branch_name: str, commit_message: str
    ) -> Any:
        """Commit and push all changes in the repository."""
        pass

    @abstractmethod
    def create_pull_request(
        self, branch_name: str, title: str, body: str
    ) -> Any:
        """Create a new pull request on the remote."""
        pass

    @abstractmethod
    def merge_pull_request(
        self, pull_request_number: int, commit_message: str
    ) -> PullRequestMergeStatus.PullRequestMergeStatus:
        """Merge a pull request on the remote."""
        pass

    @abstractmethod
    def branch_exists(self, branch_name: str) -> bool:
        """Check if a branch exists on the remote."""
        pass


class GitHubClient(RepositoryClient, metaclass=Singleton):
    """The GitHub manager provides an interface for interacting with GitHub repositories."""

    def __init__(
        self, access_token: str, remote_name: str, primary_branch: str = "main"
    ) -> None:
        self.access_token = access_token
        self.client = Github(access_token)
        self.remote_name = os.getenv(
            "AUTOMATA_DEFAULT_REPOSITORY", "emrgnt-cmplxty/automata"
        )
        self.repo = self.client.get_repo(self.remote_name)

        self.primary_branch = primary_branch

    # Repository Manager methods

    def clone_repository(self, local_path: str) -> None:
        """Clone the repository to the local path."""

        # Use Git to clone the repository
        clone_url = self.repo.clone_url.replace(
            "https://",
            f"https://{self.client.get_user().login}:{self.access_token}@",
        )

        Git().clone(clone_url, local_path)

    def create_branch(self, branch_name: str) -> GitRef.GitRef:
        """Create a new branch in the repository."""

        # Get the reference to the HEAD commit of the primary_branch
        base_sha = self.repo.get_git_ref(
            f"heads/{self.primary_branch}"
        ).object.sha
        # Create a new branch pointing to the HEAD commit of the primary_branch
        return self.repo.create_git_ref(
            ref=f"refs/heads/{branch_name}", sha=base_sha
        )

    def checkout_branch(
        self, repo_local_path: str, branch_name: str, b=True
    ) -> None:
        """Checkout a branch in the repository."""
        repo = Repo(repo_local_path)
        repo.git.checkout(branch_name, b=b)

    def stage_all_changes(self, repo_local_path: str) -> None:
        """Stage all changes in the repository."""
        repo = Repo(repo_local_path)
        repo.git.add(A=True)

    def commit_and_push_changes(
        self, repo_local_path: str, branch_name: str, commit_message: str
    ) -> None:
        """Commit and push all changes in the repository."""

        repo = Repo(repo_local_path)
        repo.git.commit(m=commit_message)
        repo.git.push("origin", branch_name)

    def create_pull_request(
        self, branch_name: str, title: str, body: str
    ) -> PullRequest.PullRequest:
        """Create a new pull request on GitHub."""
        repo = self.client.get_repo(self.remote_name)
        return repo.create_pull(
            title=title, body=body, head=branch_name, base=self.primary_branch
        )

    def merge_pull_request(
        self, pull_request_number: int, commit_message: str
    ) -> PullRequestMergeStatus.PullRequestMergeStatus:
        """Merge a pull request on GitHub."""
        pull_request = self.repo.get_pull(number=pull_request_number)
        return pull_request.merge(commit_message=commit_message)

    def branch_exists(self, branch_name: str) -> bool:
        """Check if a branch exists on GitHub."""

        try:
            self.repo.get_git_ref(f"heads/{branch_name}")
            return True
        except Exception:
            return False

    # Github related methods

    def get_open_issues(self) -> PaginatedList.PaginatedList:
        """Get the open issues for the remote repository."""
        return self.repo.get_issues(state="open")

    def get_open_pull_requests(
        self,
    ) -> PaginatedList.PaginatedList:
        """Get the open pull requests for the remote repository."""
        return self.repo.get_pulls(state="open")

    def create_issue(
        self, title: str, body: str, labels: List[str]
    ) -> Issue.Issue:
        """Create a new issue on GitHub"""
        repo = self.client.get_repo(self.remote_name)
        return repo.create_issue(title=title, body=body, labels=labels)

    def create_label(self, issue_number: int, label_name: str) -> None:
        """Remove a label from an issue on the remote repository."""
        issue = self.repo.get_issue(number=issue_number)
        issue.remove_from_labels(label_name)

    def add_label(self, issue_number: int, label_name: str) -> None:
        """Add a label to an issue on the remote repository."""
        issue = self.repo.get_issue(number=issue_number)
        issue.add_to_labels(label_name)

    def remove_label(self, issue_number: int, label_name: str) -> None:
        """Remove a label from an issue on the remote repository."""
        issue = self.repo.get_issue(number=issue_number)
        issue.remove_from_labels(label_name)

    def create_issue_comment(
        self, issue_number: int, comment_body: str
    ) -> IssueComment.IssueComment:
        """Add a comment to an issue on the remote repository."""
        issue = self.repo.get_issue(number=issue_number)
        return issue.create_comment(body=comment_body)

    def remove_issue_comment(self, comment_id: int) -> None:
        """Remove a comment from an issue on the remote repository."""
        comment = self.repo.get_comment(comment_id)
        comment.delete()

    def fetch_issue(self, issue_number: int) -> Optional[Issue.Issue]:
        """Fetch an issue from the remote repository if it exists, otherwise return None."""
        try:
            return self.repo.get_issue(number=issue_number)
        except Exception:
            return None

    def set_remote_name(self, remote_name: str):
        self.remote_name = remote_name
        self.repo = self.client.get_repo(self.remote_name)
