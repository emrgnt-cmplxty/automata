# New functions
from github import Github


def login_github(token):
    return Github(token)


def list_repositories(github):
    repos = []
    for repo in github.get_user().get_repos():
        repos.append(repo.full_name)
    return repos


def list_issues(repo):
    issues = []
    for issue in repo.get_issues(state="open"):
        issues.append(issue)
    return issues


def choose_issue(issues):
    print("Issues:")
    for i, issue in enumerate(issues):
        print(f"{i + 1}. {issue.title}")
    choice = int(input("Choose an issue by its number: ")) - 1
    return issues[choice]
