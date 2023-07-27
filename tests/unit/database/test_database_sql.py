import os
import sqlite3

import pytest

from automata.core.base.database.relational_database import (  # replace "your_module" with the module where SQLDatabase is defined
    SQLDatabase,
)


@pytest.fixture
def db():
    db_path = "test.db"
    db = SQLDatabase()
    db.connect(db_path)
    yield db
    db.close()
    os.remove(db_path)


def test_connect_close(db):
    conn = sqlite3.connect(db.db_path)
    cursor = conn.cursor()

    assert isinstance(db.conn, type(conn))
    assert isinstance(db.cursor, type(cursor))

    db.close()

    assert db.conn is None
    assert db.cursor is None


def test_create_table(db):
    table_name = "test_table"
    fields = {"id": "INTEGER", "name": "TEXT"}
    db.create_table(table_name, fields)

    db.cursor.execute(f"PRAGMA table_info({table_name})")
    columns = [column[1] for column in db.cursor.fetchall()]

    assert "id" in columns
    assert "name" in columns


def test_insert_select(db):
    table_name = "test_table"
    fields = {"id": "INTEGER", "name": "TEXT"}
    db.create_table(table_name, fields)

    data = {"id": 1, "name": "Test"}
    db.insert(table_name, data)

    result = db.select(table_name, ["id", "name"])

    assert result == [(1, "Test")]


def test_update_entry(db):
    table_name = "test_table"
    fields = {"id": "INTEGER", "name": "TEXT"}
    db.create_table(table_name, fields)

    data = {"id": 1, "name": "Test"}
    db.insert(table_name, data)

    updated_data = {"name": "Updated"}
    db.update_entry(table_name, updated_data, {"id": 1})

    result = db.select(table_name, ["id", "name"])

    assert result == [(1, "Updated")]


def test_delete(db):
    table_name = "test_table"
    fields = {"id": "INTEGER", "name": "TEXT"}
    db.create_table(table_name, fields)

    data = {"id": 1, "name": "Test"}
    db.insert(table_name, data)

    db.delete(table_name, {"id": 1})

    result = db.select(table_name, ["id", "name"])

    assert result == []
