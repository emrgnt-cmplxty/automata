# New functions
import enum
from ctypes import Union

from github import Github

from main import github


def login_github(token):
    return Github(token)


def list_repositories(github):
    repos = []
    for repo in github.get_user().get_repos():
        repos.append(repo.full_name)
    return repos


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

    for i, work_item in work_items:
        print(f"{i + 1}. {work_item.title}")

    choice = int(input("Choose a work item by its number: ")) - 1
    return work_items[choice]
