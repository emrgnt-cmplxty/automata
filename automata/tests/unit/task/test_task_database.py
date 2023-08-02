import os

import pytest

from automata.tasks.automata_task import AutomataTask
from automata.tasks.task_base import TaskStatus
from automata.tasks.task_database import AutomataAgentTaskDatabase
from automata.tasks.task_error import TaskStateError
from automata.tasks.task_registry import AutomataTaskRegistry


@pytest.fixture(autouse=True)
def db(tmpdir_factory):
    # generate random suffix for database file
    import random

    db_file = tmpdir_factory.mktemp("data").join(
        f"task_db_{random.randint(0, 100000)}.db"
    )
    db = AutomataAgentTaskDatabase(str(db_file))
    yield db
    db.close()
    os.remove(str(db_file))


@pytest.fixture
def task_registry(db):
    return AutomataTaskRegistry(db)


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


def test_get_tasks_by_query_with_sql_string(db, task):
    db.cursor.execute("DELETE FROM tasks")
    db.conn.commit()
    db.insert_task(task)
    tasks = db.get_tasks_by_query(
        "SELECT json FROM tasks WHERE id = ?", (str(task.session_id),)
    )
    assert tasks[0].session_id == task.session_id
    assert tasks[0].instructions == task.instructions


# test cases for AutomataAgentTaskDatabase
def test_insert_and_contains_task(db, task):
    db.insert_task(task)
    assert db.contains(task)


def test_update_task_2(db, task):
    db.insert_task(task)
    task.status = TaskStatus.SUCCESS
    db.update_task(task)
    tasks = db.get_tasks_by_query(
        "SELECT * FROM tasks WHERE status = ?", (str(task.status.value),)
    )
    assert len(tasks) == 1
    assert tasks[0].status == task.status


# test cases for AutomataTaskRegistry
def test_register_and_update_task(db, task):
    task_registry = AutomataTaskRegistry(db)
    task_registry.register(task)
    task.status = TaskStatus.SUCCESS
    task_registry.update_task(task)
    fetched_task = task_registry.fetch_task_by_id(str(task.session_id))
    assert fetched_task.status == TaskStatus.SUCCESS


def test_register_existing_task(db, task):
    task_registry = AutomataTaskRegistry(db)
    task_registry.register(task)
    with pytest.raises(TaskStateError):
        task_registry.register(task)


def test_fetch_task_by_id(db, task):
    task_registry = AutomataTaskRegistry(db)
    task_registry.register(task)
    fetched_task = task_registry.fetch_task_by_id(str(task.session_id))
    assert fetched_task.session_id == task.session_id
    assert fetched_task.instructions == task.instructions


def test_get_all_tasks(db, task):
    task_registry = AutomataTaskRegistry(db)
    tasks = task_registry.get_all_tasks()
    task_registry.register(task)
    tasks = task_registry.get_all_tasks()
    assert len(tasks) == 1
    assert tasks[0].session_id == task.session_id
    assert tasks[0].instructions == task.instructions


def test_update_nonexistent_task(task_registry, task):
    # Test that updating a nonexistent task raises an error.
    with pytest.raises(TaskStateError):
        task_registry.update_task(task)
