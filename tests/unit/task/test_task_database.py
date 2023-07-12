import os

import pytest

from automata.tasks.agent_database import AutomataAgentTaskDatabase
from automata.tasks.base import TaskStatus
from automata.tasks.tasks import AutomataTask


@pytest.fixture(scope="module")
def db(tmpdir_factory):
    db_file = tmpdir_factory.mktemp("data").join("test.db")
    db = AutomataAgentTaskDatabase(str(db_file))
    yield db
    db.close()
    os.remove(str(db_file))


@pytest.fixture
def task():
    return AutomataTask("task1", instructions="instruction1")


def test_insert_task(db, task):
    db.insert_task(task)
    assert db.contains(task)


def test_update_task(db, task):
    db.cursor.execute("DELETE FROM tasks")
    db.conn.commit()

    db.insert_task(task)
    task.status = TaskStatus.SUCCESS
    db.update_task(task)
    tasks = db.get_tasks_by_query(["status"], [str(task.status.value)])
    assert len(tasks) == 1
    assert tasks[0].status == task.status


def test_get_tasks_by_query(db, task):
    db.cursor.execute("DELETE FROM tasks")
    db.conn.commit()
    db.insert_task(task)
    tasks = db.get_tasks_by_query(["status"], [str(task.status.value)])
    assert len(tasks) == 1
    assert tasks[0].status == task.status


def test_contains(db, task):
    db.cursor.execute("DELETE FROM tasks")
    db.conn.commit()

    db.insert_task(task)
    assert db.contains(task)


def test_database_lifecycle(db, task):
    db.cursor.execute("DELETE FROM tasks")
    db.conn.commit()

    # Test that the task doesn't exist yet
    assert not db.contains(task)
    tasks = db.get_tasks_by_query(["status"], [str(task.status.value)])

    # Test insertion of a task
    db.insert_task(task)
    assert db.contains(task)

    # Test updating a task
    task.status = TaskStatus.SUCCESS
    db.update_task(task)
    tasks = db.get_tasks_by_query(["status"], [str(task.status.value)])
    assert len(tasks) == 1
    assert tasks[0].status == task.status

    # Test fetching a task
    tasks = db.get_tasks_by_query(["status"], [str(task.status.value)])
    assert len(tasks) == 1
    assert tasks[0].status == task.status

    # Test multiple task handling
    task2 = AutomataTask("task2", instructions="instruction2")
    db.insert_task(task2)
    task2 = AutomataTask("task3", instructions="instruction3")
    db.insert_task(task2)
    tasks = db.get_tasks_by_query(["status"], [str(task2.status.value)])
    assert len(tasks) == 2
    assert tasks[0].status == tasks[1].status

    # Test task existence
    assert db.contains(task)
    assert db.contains(task2)
