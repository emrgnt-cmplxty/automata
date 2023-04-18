"""
This module provides functions to interact with the GitHub API, specifically to list repositories, issues, and pull requests,
choose a work item to work on, and remove HTML tags from text.
"""

from typing import List, Tuple, Union

from github import Github
from github.Issue import Issue
from github.PaginatedList import PaginatedList
from github.PullRequest import PullRequest
from github.Repository import Repository
from langchain.chains.conversational_retrieval.base import BaseConversationalRetrievalChain
from langchain.document_loaders import TextLoader
from langchain.schema import AIMessage, Document, HumanMessage


def login_github(token: str) -> Github:
    """
    Logs in to the GitHub API using a token.

    Args:
    - token: A GitHub access token.

    Returns:
    - A Github object representing the authenticated user.
    """
    return Github(token)


def list_issues(repo: Repository) -> PaginatedList:
    """
    Lists the open issues for a given repository.

    Args:
    - repo: A Github repository object.

    Returns:
    - A list of Github Issue objects representing the open issues for the repository.
    """

    return repo.get_issues(state="open")


def list_pulls(repo: Repository) -> PaginatedList:
    """
    Lists the open pull requests for a given repository.

    Args:
    - repo: A Github repository object.

    Returns:
    - A list of Github PullRequest objects representing the open pull requests for the repository.
    """

    return repo.get_pulls(state="open")


def choose_work_item(
    github_repo: Repository,
) -> Union[Issue, PullRequest]:
    """
    Asks the user whether they want to work on issues or pull requests for a given repository, lists the available
    work items, and prompts the user to choose one to work on.

    Args:
    - github_repo: A Github repository object.

    Returns:
    - A Github Issue object or PullRequest object representing the user's chosen work item.
    """

    choice = input("Do you want to work on issues or pull requests? (i/p)")
    work_items: PaginatedList

    if choice == "i":
        work_items = list_issues(github_repo)
        print("Issues:")
    elif choice == "p":
        work_items = list_pulls(github_repo)
        print("Pull requests:")
    else:
        print("Invalid choice.")
        return choose_work_item(github_repo)

    for i, work_item in enumerate(work_items):
        print(f"{i + 1}. {work_item.title}")

    choice_index = int(input("Choose a work item by its number: ")) - 1
    return work_items[choice_index]


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


def _get_chat_history(chat_history: List[Tuple[HumanMessage, AIMessage]]) -> str:
    buffer = ""
    for human_m, ai_m in chat_history:
        human = "Human: " + str(human_m)
        ai = "Assistant: " + str(ai_m)
        buffer += "\n" + "\n".join([human, ai])
    return buffer


def run_retrieval_chain_with_sources_format(
    chain: BaseConversationalRetrievalChain, q: str
) -> str:
    result = chain(q)
    answer, sources = result["answer"], result.get("source_documents", [])
    formatted_answer = f"Answer: {answer}"
    if sources:
        formatted_sources = "\n".join(
            [f"Source: {s.metadata['source']} Content: {s.page_content}" for s in sources]
        )
        formatted_answer = "\n".join([formatted_answer, formatted_sources])
    return formatted_answer


class NumberedLinesTextLoader(TextLoader):
    def load(self) -> List[Document]:
        """Load from file path."""
        with open(self.file_path, encoding=self.encoding) as f:
            lines = f.readlines()
            text = f"{self.file_path}\n"  # this helps with mapping content to file name
            for i, line in enumerate(lines):
                text += f"{i}: {line}"
        metadata = {"source": self.file_path}
        return [Document(page_content=text, metadata=metadata)]
