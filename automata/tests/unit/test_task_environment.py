import os
from unittest.mock import MagicMock

from automata.core.base.task import TaskStatus


class TestURL:
    html_url = "test_url"


def test_commit_task(task, mocker, environment):
    os.makedirs(task.task_dir, exist_ok=True)
    task.status = TaskStatus.SUCCESS

    environment.github_manager.create_pull_request = MagicMock(return_value=TestURL())
    environment.github_manager.branch_exists = MagicMock(return_value=False)
    mocker.spy(environment.github_manager, "create_branch")
    mocker.spy(environment.github_manager, "checkout_branch")
    mocker.spy(environment.github_manager, "stage_all_changes")
    mocker.spy(environment.github_manager, "commit_and_push_changes")
    mocker.spy(environment.github_manager, "create_pull_request")

    environment.commit_task(
        task,
        commit_message="This is a commit message",
        pull_title="This is a test",
        pull_body="I am testing this...",
        pull_branch_name="test_branch__ZZ__",
    )

    environment.github_manager.create_branch.assert_called_once_with("test_branch__ZZ__")
    environment.github_manager.checkout_branch.assert_called_once_with(
        task.task_dir, "test_branch__ZZ__"
    )
    environment.github_manager.stage_all_changes.assert_called_once_with(task.task_dir)
    environment.github_manager.commit_and_push_changes.assert_called_once_with(
        task.task_dir, "test_branch__ZZ__", "This is a commit message"
    )
    environment.github_manager.create_pull_request.assert_called_once_with(
        "test_branch__ZZ__", "This is a test", "I am testing this..."
    )
