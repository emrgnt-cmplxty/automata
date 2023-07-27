import os
from unittest.mock import MagicMock

import pytest

from automata.tasks.task_base import TaskStatus


class TestURL:
    html_url = "test_url"


@pytest.fixture
def github_manager_mock(mocker):
    mock = MagicMock()
    mock.create_pull_request.return_value = TestURL()
    mock.branch_exists.return_value = False
    mocker.spy(mock, "create_branch")
    mocker.spy(mock, "checkout_branch")
    mocker.spy(mock, "stage_all_changes")
    mocker.spy(mock, "commit_and_push_changes")
    mocker.spy(mock, "create_pull_request")
    return mock


def test_commit_task(tasks, mocker, task_environment, github_manager_mock):
    task = tasks[0]

    os.makedirs(task.task_dir, exist_ok=True)
    task.status = TaskStatus.SUCCESS

    task_environment.github_manager.create_pull_request = MagicMock(
        return_value=TestURL()
    )
    task_environment.github_manager.branch_exists = MagicMock(
        return_value=False
    )
    mocker.spy(task_environment.github_manager, "create_branch")
    mocker.spy(task_environment.github_manager, "checkout_branch")
    mocker.spy(task_environment.github_manager, "stage_all_changes")
    mocker.spy(task_environment.github_manager, "commit_and_push_changes")
    mocker.spy(task_environment.github_manager, "create_pull_request")

    task_environment.commit_task(
        task,
        commit_message="This is a commit message",
        pull_title="This is a test",
        pull_body="I am testing this...",
        pull_branch_name="test_branch__ZZ__",
    )

    task_environment.github_manager.create_branch.assert_called_once_with(
        "test_branch__ZZ__"
    )
    task_environment.github_manager.checkout_branch.assert_called_once_with(
        task.task_dir, "test_branch__ZZ__"
    )
    task_environment.github_manager.stage_all_changes.assert_called_once_with(
        task.task_dir
    )
    task_environment.github_manager.commit_and_push_changes.assert_called_once_with(
        task.task_dir, "test_branch__ZZ__", "This is a commit message"
    )
    task_environment.github_manager.create_pull_request.assert_called_once_with(
        "test_branch__ZZ__", "This is a test", "I am testing this..."
    )
