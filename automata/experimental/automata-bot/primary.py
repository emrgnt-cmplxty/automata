# from github import Github
from automata.singletons.github_client import GitHubClient

if __name__ == "__main__":
    print("Running main")

    client_key = "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"
    remote_name = "emrgnt-cmplxty/Automata"

    client = GitHubClient(client_key, remote_name)

    # print("Pull Requests = ", client.get_open_pull_requests())
    prs = client.get_open_pull_requests()

    for pr in prs:
        print("pr = ", client.get_open_pull_requests())

    prs = client.get_open_pull_requests()

    for pr in prs:
        print("pr = ", pr)

    issues = client.get_open_issues()

    for issue in issues:
        print("issue = ", issue)

    # First create a Github instance using an access token
    # g = Github("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")

    # print("repos = ", g.get_user().get_repos())
    # # Then play with your Github objects
    # for repo in g.get_user().get_repos():
    #     print(repo.name)
    #     repo.edit(has_wiki=False)
    #     # to see all the available attributes and methods
    #     print(dir(repo))
