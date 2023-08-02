from unittest.mock import patch

import pytest
import responses

from automata.singletons.github_client import GitHubClient

GITHUB_REQUEST_BASE = "https://api.github.com:443/repos/user/repo"
GITHUB_URL_BASE = "https://api.github.com/repos/user/repo"
GITHUB_REQUEST_JSON = {
    "name": "repo",
    "owner": {"login": "user"},
    "url": GITHUB_URL_BASE,
}


@responses.activate
@patch("os.getenv")
def test_create_issue(mock_getenv):
    mock_getenv.return_value = "user/repo"
    responses.add(
        responses.GET,
        GITHUB_REQUEST_BASE,
        json=GITHUB_REQUEST_JSON,
        status=200,
    )

    responses.add(
        responses.POST,
        f"{GITHUB_REQUEST_BASE}/issues",
        json={
            "number": 1,
            "title": "Test",
            "body": "Test issue",
            "labels": [],
        },
        status=201,
    )

    client = GitHubClient("MOCK_TOKEN", "user/repo")
    issue = client.create_issue("Test", "Test issue", [])

    assert issue.number == 1
    assert issue.title == "Test"
    assert issue.body == "Test issue"
    assert issue.labels == []


@responses.activate
def test_create_pull_request():
    responses.add(
        responses.GET,
        GITHUB_REQUEST_BASE,
        json={
            "name": "repo",
            "owner": {"login": "user"},
            "url": GITHUB_URL_BASE,
        },
        status=200,
    )

    responses.add(
        responses.POST,
        f"{GITHUB_REQUEST_BASE}/pulls",
        json={
            "number": 1,
            "title": "Test",
            "body": "Test PR",
        },
        status=201,
    )

    client = GitHubClient("MOCK_TOKEN", "user/repo")
    pull_request = client.create_pull_request("test-branch", "Test", "Test PR")

    assert pull_request.number == 1
    assert pull_request.title == "Test"
    assert pull_request.body == "Test PR"


@responses.activate
def test_merge_pull_request():
    responses.add(
        responses.GET,
        f"{GITHUB_REQUEST_BASE}/pulls/1",
        json={
            "number": 1,
            "title": "Test",
            "body": "Test PR",
            "url": GITHUB_URL_BASE,
        },
        status=200,
    )

    responses.add(
        responses.PUT,
        f"{GITHUB_REQUEST_BASE}/merge",
        json={
            "sha": "6dcb09b5b57875f334f61aebed695e2e4193db5e",
            "merged": True,
            "message": "Pull Request successfully merged",
        },
        status=200,
    )
    client = GitHubClient("MOCK_TOKEN", "user/repo")
    merge_status = client.merge_pull_request(1, "Merging PR")

    assert merge_status.merged
    assert merge_status.message == "Pull Request successfully merged"


@responses.activate
def test_get_open_issues():
    responses.add(
        responses.GET,
        GITHUB_REQUEST_BASE,
        json={
            "url": f"{GITHUB_URL_BASE}",
        },
        status=200,
    )

    responses.add(
        responses.GET,
        f"{GITHUB_REQUEST_BASE}/issues?state=open",
        json=[
            {
                "number": 1,
                "title": "Test issue",
                "body": "This is a test issue",
                "state": "open",
            },
            {
                "number": 2,
                "title": "Another test issue",
                "body": "This is another test issue",
                "state": "open",
            },
        ],
        status=200,
    )

    client = GitHubClient("MOCK_TOKEN", "user/repo")
    issues = client.get_open_issues()

    assert len(list(issues)) == 2
    assert issues[0].number == 1
    assert issues[0].title == "Test issue"
    assert issues[0].body == "This is a test issue"
    assert issues[0].state == "open"


@responses.activate
def test_branch_exists():
    responses.add(
        responses.GET,
        f"{GITHUB_REQUEST_BASE}/git/refs/heads/test-branch",
        json={
            "ref": "refs/heads/test-branch",
            "url": f"{GITHUB_URL_BASE}/git/refs/heads/test-branch",
        },
        status=200,
    )

    client = GitHubClient("MOCK_TOKEN", "user/repo")
    assert client.branch_exists("test-branch")


@responses.activate
def test_get_open_pull_requests():
    responses.add(
        responses.GET,
        f"{GITHUB_REQUEST_BASE}/pulls",
        json=[
            {
                "number": 1,
                "title": "Test PR",
                "body": "This is a test PR",
                "state": "open",
            },
            {
                "number": 2,
                "title": "Another test PR",
                "body": "This is another test PR",
                "state": "open",
            },
        ],
        status=200,
    )

    client = GitHubClient("MOCK_TOKEN", "user/repo")
    pull_requests = client.get_open_pull_requests()

    assert len(list(pull_requests)) == 2
    assert pull_requests[0].number == 1
    assert pull_requests[0].title == "Test PR"
    assert pull_requests[0].body == "This is a test PR"
    assert pull_requests[0].state == "open"


@responses.activate
def test_create_issue_comment():
    responses.add(
        responses.GET,
        GITHUB_REQUEST_BASE,
        json={
            "number": 1,
            "title": "Test issue",
            "body": "This is a test issue",
            "state": "open",
            "url": "https://api.github.com/repos/user/repo",
        },
        status=200,
    )

    responses.add(
        responses.GET,
        f"{GITHUB_REQUEST_BASE}/issues/1",
        json={
            "id": 1,
            "body": "Test comment",
            "url": f"{GITHUB_URL_BASE}/issues/1",
        },
        status=201,
    )

    responses.add(
        responses.POST,
        f"{GITHUB_REQUEST_BASE}/issues/1/comments",
        json={
            "id": 1,
            "body": "Test comment",
            "url": f"{GITHUB_URL_BASE}/issues/1/comments",
        },
        status=201,
    )

    client = GitHubClient("MOCK_TOKEN", "user/repo")
    comment = client.create_issue_comment(1, "Test comment")

    assert comment.id == 1
    assert comment.body == "Test comment"


@pytest.mark.skip(reason="Not implemented")
@responses.activate
def test_remove_issue_comment():
    pass


@responses.activate
def test_fetch_issue():
    responses.add(
        responses.GET,
        f"{GITHUB_REQUEST_BASE}/issues/1",
        json={
            "number": 1,
            "title": "Test issue",
            "body": "This is a test issue",
            "state": "open",
        },
        status=200,
    )

    client = GitHubClient("MOCK_TOKEN", "user/repo")
    issue = client.fetch_issue(1)

    assert issue.number == 1
    assert issue.title == "Test issue"
    assert issue.body == "This is a test issue"
    assert issue.state == "open"


@responses.activate
def test_fetch_issue_not_found():
    responses.add(
        responses.GET,
        f"{GITHUB_REQUEST_BASE}/issues/999",
        json={
            "message": "Not Found",
            "documentation_url": "https://docs.github.com/rest/reference/issues#get-an-issue",
        },
        status=404,
    )

    client = GitHubClient("MOCK_TOKEN", "user/repo")
    issue = client.fetch_issue(999)

    assert issue is None
