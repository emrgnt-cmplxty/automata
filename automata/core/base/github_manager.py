from abc import ABC, abstractmethod
from typing import Any, List, Optional

from git import Git, Repo
from github import Github, Issue, PullRequest


class RepositoryManager(ABC):
    @abstractmethod
    def clone_repository(self, local_path: str) -> None:
        pass

    @abstractmethod
    def create_branch(self, branch_name: str) -> None:
        pass

    @abstractmethod
    def checkout_branch(self, repo_local_path: str, branch_name: str) -> None:
        pass

    @abstractmethod
    def stage_all_changes(self, repo_local_path: str) -> None:
        pass

    @abstractmethod
    def commit_and_push_changes(
        self, repo_local_path: str, branch_name: str, commit_message: str
    ) -> None:
        pass

    @abstractmethod
    def create_pull_request(self, branch_name: str, title: str, body: str) -> Any:
        pass

    @abstractmethod
    def branch_exists(self, branch_name: str) -> bool:
        pass

    @abstractmethod
    def fetch_issue(self, issue_number: int) -> Any:
        pass


class GitHubManager:
    """The GitHub manager provides an interface for interacting with GitHub repositories"""

    def __init__(self, access_token: str, remote_name: str, primary_branch: str = "main") -> None:
        """
        Args:
            access_token: The GitHub access token
            remote_name: The name of the remote repository
            primary_branch: The name of the primary branch
        """
        self.access_token = access_token
        self.client = Github(access_token)
        self.remote_name = remote_name
        self.repo = self.client.get_repo(self.remote_name)

        self.primary_branch = primary_branch

    def clone_repository(self, local_path: str) -> None:
        """
        Clones the repository to the specified local path

        Args:
            local_path: The local path to clone the repository to
        """
        # Use Git to clone the repository
        clone_url = self.repo.clone_url.replace(
            "https://", f"https://{self.client.get_user().login}:{self.access_token}@"
        )

        Git().clone(clone_url, local_path)

    def create_branch(self, branch_name: str) -> None:
        """
        Creates a new branch with the specified name

        Args:
            branch_name: The name of the branch to create
        """
        # Get the reference to the HEAD commit of the primary_branch
        base_sha = self.repo.get_git_ref(f"heads/{self.primary_branch}").object.sha
        # Create a new branch pointing to the HEAD commit of the primary_branch
        self.repo.create_git_ref(ref=f"refs/heads/{branch_name}", sha=base_sha)

    def checkout_branch(self, repo_local_path: str, branch_name: str, b=True) -> None:
        """
        Checks out the specified branch

        Args:
            repo_local_path: The local path of the repository
            branch_name: The name of the branch to checkout
        """
        repo = Repo(repo_local_path)
        repo.git.checkout(branch_name, b=b)

    def stage_all_changes(self, repo_local_path: str) -> None:
        """
        Stages all changes in the repository

        Args:
            repo_local_path: The local path of the repository
        """
        repo = Repo(repo_local_path)
        repo.git.add(A=True)

    def commit_and_push_changes(
        self, repo_local_path: str, branch_name: str, commit_message: str
    ) -> None:
        """
        Commits and pushes all changes in the repository

        Args:
            repo_local_path: The local path of the repository
            branch_name: The name of the branch to commit and push to
            commit_message: The commit message
        """
        repo = Repo(repo_local_path)
        repo.git.commit(m=commit_message)
        repo.git.push("origin", branch_name)

    def create_pull_request(
        self, branch_name: str, title: str, body: str
    ) -> PullRequest.PullRequest:
        """
        Creates a new pull request on GitHub

        Args:
            branch_name: The name of the branch to create the pull request from
            title: The title of the pull request
            body: The body of the pull request

        Returns:
            The pull request object
        """
        # Create a new pull request on GitHub
        repo = self.client.get_repo(self.remote_name)
        return repo.create_pull(title=title, body=body, head=branch_name, base=self.primary_branch)

    def create_issue(self, title: str, body: str, labels: List[str]) -> None:
        """
        Creates a new issue on GitHub

        Args:
            title: The title of the issue
            body: The body of the issue
            labels: The labels to apply to the issue
        """
        # Create a new pull request on GitHub
        repo = self.client.get_repo(self.remote_name)
        repo.create_issue(title=title, body=body, labels=labels)

    def branch_exists(self, branch_name: str) -> bool:
        """
        Checks if the specified branch exists

        Args:
            branch_name: The name of the branch to check

        Returns:
            True if the branch exists, False otherwise
        """
        try:
            self.repo.get_git_ref(f"heads/{branch_name}")
            return True
        except Exception:
            return False

    def fetch_issue(self, issue_number: int) -> Optional[Issue.Issue]:
        """
        Fetches an issue by its number

        Args:
            issue_number: The number of the issue to fetch
        """
        try:
            return self.repo.get_issue(number=issue_number)
        except Exception:
            return None
