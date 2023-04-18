"""
custom_tools.py - a module containing custom tools for Spork, an open-source Python framework for building bots.

This module contains a GithubToolManager class for interacting with Git repositories, and a requests_get_clean tool for sending GET requests and returning clean text.

Classes:
- GithubToolManager: A class for interacting with Git repositories.

Functions:
- requests_get_clean: A function for sending GET requests and returning clean text.
"""

from typing import List, Optional, Union

import git
import github
import requests
from github.Issue import Issue
from github.PullRequest import PullRequest
from github.Repository import Repository
from langchain.agents import Tool, tool

from spork.tools.tool_managers.base_tool_manager import BaseToolManager
from spork.tools.utils import PassThroughBuffer, remove_html_tags


class GithubToolManager(BaseToolManager):
    def __init__(
        self,
        github_repo: Repository,
        pygit_repo: git.Repo,
        work_item: Union[Issue, PullRequest],
        logger: Optional[PassThroughBuffer] = None,
    ):
        """
        Initializes a GithubToolManager object with the given inputs.

        Args:
        - github_repo (github.Repository): A github.Repository object representing the repository to work on.
        - pygit_repo (git.Repo): A git.Repo object representing the local copy of the repository to work on.
        - work_item (Union[Issue, PullRequest]): An Issue or PullRequest object representing the work item to work on.
        - logger (Optional[PassThroughBuffer]): An optional PassThroughBuffer object to log output.

        Returns:
        - None
        """
        self.github_repo = github_repo
        self.pygit_repo = pygit_repo
        self.work_item = work_item
        self.logger = logger

    def build_tools(self) -> List[Tool]:
        """
        Builds a list of Tool objects for interacting with Git.

        Args:
        - None

        Returns:
        - tools (List[Tool]): A list of Tool objects representing Git commands.
        """
        tools = [
            Tool(
                name="git-new-branch",
                func=lambda input_str: self._create_new_branch(input_str),
                description="Creates and checks out a new branch in the specified repository. The only input is the branch name. For example: 'my-branch'.",
                return_direct=False,
            ),
            Tool(
                name="git-commit",
                func=lambda input_str: self._commit_to_git(input_str),
                description="Takes a string of comma-separated file names and commits them to git. For example: 'file1.py,file2.py'.",
                return_direct=False,
            ),
            Tool(
                name="git-create-pull-request",
                func=lambda input_str: self._create_pull_request(input_str),
                description="Creates a pull request in the specified repository.",
                return_direct=False,
            ),
            Tool(
                name="git-checkout-existing-branch",
                func=lambda input_str: self._checkout_branch(input_str),
                description="Checks out an existing branch in the specified repository. The only input is the branch name. For example: 'my-branch'.",
                return_direct=False,
            ),
        ]
        return tools

    def _create_new_branch(self, branch_name: str) -> str:
        """
        Creates and checks out a new branch in the specified repository.

        Args:
        - branch_name (str): A string representing the name of the new branch to create.

        Returns:
        - output (str): A string representing the output of the Git command.
        """
        try:
            self.pygit_repo.git.branch(branch_name)
            self.pygit_repo.git.checkout(branch_name)
            return f"Created and checked out branch {branch_name} in {self.github_repo.name} repository."

        except Exception as e:
            return f"Error: {e}"

    def _checkout_branch(self, branch_name: str) -> str:
        """
        Checks out an existing branch in the specified repository.

        Args:
        - branch_name (str): A string representing the name of the existing branch to checkout.

        Returns:
        - output (str): A string representing the output of the Git command.
        """

        # Checkout branch
        try:
            self.pygit_repo.git.checkout(branch_name)
            self.pygit_repo.git.pull()
            return f"Checked out an existing branch {branch_name} in {self.github_repo.name} repository."
        except Exception as e:
            return f"Error: {e}"

    def _commit_to_git(self, file_names: str) -> str:
        """
        Commits specified files to Git.

        Args:
        - file_names (str): A string representing comma-separated file names to commit.

        Returns:
        - output (str): A string representing the output of the Git command.
        """
        try:
            file_names_list = file_names.split(",")
            for file_name in file_names_list:
                self.pygit_repo.git.add(file_name)

            self.pygit_repo.git.commit(m="Committing changes")
            self.pygit_repo.git.push(
                "--set-upstream", "origin", self.pygit_repo.git.branch("--show-current")
            )
            return f"Committed {file_names} to {self.github_repo.name} repository."
        except Exception as e:
            return f"Error: {e}"

    def _create_pull_request(self, body) -> str:
        """
        Creates a pull request in the specified repository.

        Args:
        - body: A string representing the body of the pull request.

        Returns:
        - output (str): A string representing the output of the Git command.
        """
        # get current branch name
        try:
            assert type(self.work_item) == Issue
            current_branch = self.pygit_repo.git.branch("--show-current")
            title = "Fix for issue #" + str(self.work_item.number)
            pull: github.PullRequest.PullRequest = self.github_repo.create_pull(
                head=current_branch,
                base=self.github_repo.default_branch,
                issue=self.work_item,
            )
            if self.logger:
                pull.create_issue_comment(self.logger.saved_output)
            return f"Created pull request for  {title} in {self.github_repo.name} repository."
        except Exception as e:
            return f"Error: {e}"


@tool
def requests_get_clean(url: str) -> str:
    """
    Sends a GET request to a specified URL and returns the clean text in the response.
    Args:
    - url (str): A string representing the URL to send a GET request to.

    Returns:
    - output (str): A string representing the clean text in the response.
    """

    response = requests.get(url)
    try:
        if response.status_code == 200:
            return remove_html_tags(response.text)
        else:
            raise Exception(f"Error: {response.status_code} {response.text}")
    except Exception as e:
        return f"Error: {e}"
