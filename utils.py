# New functions
from typing import Union
import github
from github import Github


def login_github(token):
    return Github(token)


def list_repositories(github):
    repos = []
    for repo in github.get_user().get_repos(sort="updated", direction="desc"):
        repos.append(repo.full_name)
    return repos[:5]


def list_issues(repo):
    return repo.get_issues(state="open")


def list_pulls(repo):
    return repo.get_pulls(state="open")


def choose_work_item(
    github_repo,
) -> Union[github.Issue.Issue, github.PullRequest.PullRequest]:
    choice = input("Do you want to work on issues or pull requests? (i/p)")
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

    choice = int(input("Choose a work item by its number: ")) - 1
    return work_items[choice]

# this is probably not a good idea but it works for now
class PassThroughBuffer:
    def __init__(self, buffer):
        self.saved_output = ''
        self.original_buffer = buffer

    def write(self, message):
        self.saved_output += message
        self.original_buffer.write(message)

    def __getattr__(self, attr):
        return getattr(self.original_buffer, attr)
