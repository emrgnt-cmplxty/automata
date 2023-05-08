import uuid

import pytest

from automata.configs.automata_agent_configs import AutomataAgentConfig
from automata.configs.config_enums import AgentConfigVersion
from automata.core.base.github_manager import RepositoryManager
from automata.core.tasks.task import AutomataTask
from automata.core.tasks.task_executor import TaskExecutor, TestExecuteBehavior


class MockRepositoryManager(RepositoryManager):
    def clone_repository(self, local_path: str):
        pass

    def create_branch(self, branch_name: str):
        pass

    def checkout_branch(self, repo_local_path: str, branch_name: str):
        pass

    def stage_all_changes(self, repo_local_path: str):
        pass

    def commit_and_push_changes(self, repo_local_path: str, branch_name: str, commit_message: str):
        pass

    def create_pull_request(self, branch_name: str, title: str, body: str):
        pass

    def branch_exists(self, branch_name: str) -> bool:
        return False


@pytest.fixture
def task():
    repo_manager = MockRepositoryManager()
    return AutomataTask(
        repo_manager, agent_config=AutomataAgentConfig.load(AgentConfigVersion.TEST)
    )


def test_create_task_env(task):
    task.create_task_env()


def test_execute(task):
    task.create_task_env()
    # Add assertions to verify that the execute() method performs as expected
    executor = TaskExecutor(TestExecuteBehavior())
    executor.execute(task)


def test_commit_task(task, mocker):
    task.create_task_env()
    executor = TaskExecutor(TestExecuteBehavior())
    executor.execute(task)

    mocker.spy(task.github_manager, "create_branch")
    mocker.spy(task.github_manager, "checkout_branch")
    mocker.spy(task.github_manager, "stage_all_changes")
    mocker.spy(task.github_manager, "commit_and_push_changes")
    mocker.spy(task.github_manager, "create_pull_request")

    task.commit_task(
        commit_message="This is a commit message",
        pull_title="This is a test",
        pull_body="I am testing this...",
        pull_branch_name="test_branch",
    )

    task.github_manager.create_branch.assert_called_once_with("test_branch")
    task.github_manager.checkout_branch.assert_called_once_with(task.task_dir, "test_branch")
    task.github_manager.stage_all_changes.assert_called_once_with(task.task_dir)
    task.github_manager.commit_and_push_changes.assert_called_once_with(
        task.task_dir, "test_branch", "This is a commit message"
    )
    task.github_manager.create_pull_request.assert_called_once_with(
        "test_branch", "This is a test", "I am testing this..."
    )


def test_deterministic_session_id():
    task_1 = AutomataTask(
        MockRepositoryManager(),
        test1="arg1",
        test2="arg2",
        priority=5,
        generate_deterministic_id=True,
        agent_config=AutomataAgentConfig.load(AgentConfigVersion.TEST),
    )

    task_2 = AutomataTask(
        MockRepositoryManager(),
        test1="arg1",
        test2="arg2",
        priority=5,
        generate_deterministic_id=True,
        agent_config=AutomataAgentConfig.load(AgentConfigVersion.TEST),
    )

    task_3 = AutomataTask(
        MockRepositoryManager(),
        test1="arg1",
        test2="arg3",
        priority=5,
        generate_deterministic_id=True,
        agent_config=AutomataAgentConfig.load(AgentConfigVersion.TEST),
    )

    task_4 = AutomataTask(
        MockRepositoryManager(),
        test1="arg1",
        test2="arg2",
        priority=5,
        generate_deterministic_id=False,
        agent_config=AutomataAgentConfig.load(AgentConfigVersion.TEST),
    )

    assert task_1.task_id == task_2.task_id
    assert task_1.task_id != task_3.task_id
    assert task_1.task_id != task_4.task_id
    assert isinstance(task_4.task_id, uuid.UUID)


def test_deterministic_vs_non_deterministic_session_id():
    task_1 = AutomataTask(
        MockRepositoryManager(),
        test1="arg1",
        test2="arg2",
        priority=5,
        generate_deterministic_id=True,
        agent_config=AutomataAgentConfig.load(AgentConfigVersion.TEST),
    )

    task_2 = AutomataTask(
        MockRepositoryManager(),
        test1="arg1",
        test2="arg2",
        priority=5,
        generate_deterministic_id=False,
        agent_config=AutomataAgentConfig.load(AgentConfigVersion.TEST),
    )
    assert task_1.task_id != task_2.task_id
