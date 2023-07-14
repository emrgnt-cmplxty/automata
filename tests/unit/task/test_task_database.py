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
