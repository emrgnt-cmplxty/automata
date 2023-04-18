"""
This module provides functions to interact with the GitHub API, specifically to list repositories, issues, and pull requests,
choose a work item to work on, and remove HTML tags from text.
"""

import logging
import os
from typing import Dict, List, Union

import regex as re
import yaml
from bs4 import BeautifulSoup
from github import Github
from github.Issue import Issue
from github.PaginatedList import PaginatedList
from github.PullRequest import PullRequest
from github.Repository import Repository
from langchain.chains.conversational_retrieval.base import BaseConversationalRetrievalChain
from langchain.document_loaders import TextLoader
from langchain.schema import Document


def load_yaml(filename: str) -> Dict:
    with open(filename, "r") as f:
        return yaml.safe_load(f)


def home_path() -> str:
    """
    Returns the path to the home folder.

    Returns:
    - A path object in string form

    """
    script_dir = os.path.dirname(os.path.realpath(__file__))
    data_folder = os.path.join(script_dir, "..", "..")
    return data_folder


def format_config_path(config_dir: str, config_path: str) -> str:
    """
    Returns the path to a config file.
    Args:
    - config_dir (str): The name of the directory the config file is in.
    - config_path (str): The name of the config file.
    Returns:
    - The path to the config file.
    """
    return os.path.join(
        home_path(),
        "spork",
        "agents",
        config_dir,
        config_path,
    )


def login_github(token: str) -> Github:
    """
    Logs in to the GitHub API using a token.

    Args:
    - token: A GitHub access token.

    Returns:
    - A Github object representing the authenticated user.
    """
    return Github(token)


def list_repositories(github: Github) -> List[str]:
    """
    Lists the five most recently updated repositories for the authenticated user.
    Args:
    - github: A Github object representing the authenticated user.

    Returns:
    - A list of strings, each string representing a repository's full name.
    """

    repos = []
    for repo in github.get_user().get_repos(sort="updated", direction="desc"):
        repos.append(repo.full_name)
    return repos[:5]


def list_issues(repo: Repository) -> PaginatedList:
    """
    Lists the open issues for a given repository.

    Args:
    - repo: A Github repository object.

    Returns:
    - A list of Github Issue object representing the open issues for the repository.
    """

    return repo.get_issues(state="open")


def list_pulls(repo: Repository) -> PaginatedList:
    """
    Lists the open pull requests for a given repository.

    Args:
    - repo: A Github repository object.

    Returns:
    - A list of Github PullRequest object representing the open pull requests for the repository.
    """

    return repo.get_pulls(state="open")


def choose_work_item(github_repo: Repository, choice: str = "") -> Union[Issue, PullRequest]:
    """
    Asks the user whether they want to work on issues or pull requests for a given repository, lists the available
    work items, and prompts the user to choose one to work on.

    Args:
    - github_repo: A Github repository object.

    Returns:
    - A Github Issue object or PullRequest object representing the user's chosen work item.
    """

    work_items = []
    if choice == "":
        choice = input("Do you want to work on issues or pull requests (issues/pulls)? ")
    if choice == "issues":
        work_items = list_issues(github_repo)
        print("Issues:")
    elif choice == "pulls":
        work_items = list_pulls(github_repo)
        print("Pull requests:")
    else:
        print("Invalid choice.")
        return choose_work_item(github_repo)

    for i, work_item in enumerate(work_items):
        print(f"{i + 1}. {work_item.title}")

    choice_index = int(input("Choose a work item by its number: ")) - 1
    return work_items[choice_index]


def remove_html_tags(text: str) -> str:
    """
    Removes HTML tags from a given string of text.

    Args:
    - text: A string of text that may contain HTML tags.

    Returns:
    - A string of text with all HTML tags removed.
    """

    clean = re.compile("<.*?>")
    soup = BeautifulSoup(text, "html.parser")
    raw_text = soup.get_text(strip=True, separator="\n")
    clean_text = re.sub(clean, "", raw_text)
    return clean_text


def get_logging_config(log_level=logging.INFO) -> dict:
    """Returns logging configuration."""

    logging_config = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "default": {
                "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            },
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "formatter": "default",
                "level": log_level,
            },
        },
        "root": {
            "handlers": ["console"],
            "level": log_level,
        },
    }
    return logging_config


def run_retrieval_chain_with_sources_format(
    chain: BaseConversationalRetrievalChain, q: str
) -> str:
    result = chain(q)
    return f'Answer: {result["answer"]}.\n\n Sources: {result.get("source_documents", [])}'


class NumberedLinesTextLoader(TextLoader):
    def load(self) -> List[Document]:
        """Load from file path."""
        with open(self.file_path, encoding=self.encoding) as f:
            lines = f.readlines()
            text = f"{self.file_path}"  # this helps with mapping content to file name
            for i, line in enumerate(lines):
                text += f"{i}: {line}"
        metadata = {"source": self.file_path}
        return [Document(page_content=text, metadata=metadata)]


# this is probably not a good idea but it works for now
class PassThroughBuffer:
    def __init__(self, buffer):
        self.saved_output = ""
        self.original_buffer = buffer

    def write(self, message):
        self.saved_output += message
        self.original_buffer.write(message)

    def __getattr__(self, attr):
        return getattr(self.original_buffer, attr)
