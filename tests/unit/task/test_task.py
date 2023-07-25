from unittest.mock import PropertyMock, patch

import pytest

from automata.config import AgentConfigName
from automata.tasks.automata_task import AutomataTask
from automata.tasks.base import TaskStatus
from tests.conftest import MockRepositoryClient


@pytest.fixture(autouse=True)
def mock_logging_config_dict(mocker):
    return mocker.patch("logging.config.dictConfig", return_value=None)


def test_task_inital_state(mock_logging_config_dict, task):
    assert task.status == TaskStatus.CREATED


def test_register_task(mock_logging_config_dict, task, registry):
    registry.register(task)
    assert task.status == TaskStatus.REGISTERED


def test_setup_environment(
    mock_logging_config_dict, task, environment, registry
):
    registry.register(task)
    environment.setup(task)
    assert task.observer is not None
    assert task.status == TaskStatus.PENDING


def test_setup_task_no_setup(mock_logging_config_dict, task, registry):
    with pytest.raises(Exception):
        registry.setup(task)


@patch.object(AutomataTask, "status", new_callable=PropertyMock)
def test_status_setter(mock_status, task):
    task.status = TaskStatus.RETRYING
    mock_status.assert_called_once_with(TaskStatus.RETRYING)


@patch.object(AutomataTask, "notify_observer")
def test_callback(mock_notify_observer, task, environment, registry):
    registry.register(task)
    environment.setup(task)
    # Notify observer should be called twice, once at register and once at setup
    assert mock_notify_observer.call_count == 2


def test_session_id_determinism(automata_agent_config_builder):
    common_args = {
        "test1": "arg1",
        "priority": 5,
        "config": automata_agent_config_builder,
        "helper_agent_names": "test",
        "instructions": "test1",
    }

    task_1 = AutomataTask(
        **common_args, test2="arg2", generate_deterministic_id=True
    )
    task_2 = AutomataTask(
        **common_args, test2="arg2", generate_deterministic_id=True
    )
    task_3 = AutomataTask(
        **common_args, test2="arg3", generate_deterministic_id=True
    )
    task_4 = AutomataTask(
        **common_args, test2="arg2", generate_deterministic_id=False
    )

    assert task_1.session_id == task_2.session_id
    assert task_1.session_id != task_3.session_id
    assert task_1.session_id != task_4.session_id
    assert isinstance(task_4.session_id, str)

    task_5 = AutomataTask(
        MockRepositoryClient(),
        **common_args,
        test2="arg2",
        generate_deterministic_id=False,
        config_to_load=AgentConfigName.TEST.to_path(),
    )

    assert task_1.session_id != task_5.session_id
