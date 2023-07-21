import os

import pytest

from automata.llm import OpenAIChatMessage
from automata.memory_store import OpenAIAutomataConversationDatabase


@pytest.fixture(scope="module", autouse=True)
def db(tmpdir_factory):
    db_file = tmpdir_factory.mktemp("data").join("test.db")
    db = OpenAIAutomataConversationDatabase(str(db_file))
    yield db
    db.close()
    if os.path.exists(str(db_file)):
        os.remove(str(db_file))


@pytest.fixture
def interaction():
    return {"role": "user", "content": "Hello, world!", "function_call": {}}


def test_get_get_last_interaction_id_when_no_interactions(db):
    db.cursor.execute("DELETE FROM interactions")
    db.conn.commit()
    assert db._get_last_interaction_id("test_session") == 0


def test_put_message_increments_interaction_id(db, interaction):
    db.cursor.execute("DELETE FROM interactions")
    db.conn.commit()

    initial_interaction_id = db._get_last_interaction_id("test_session")
    db.save_message("test_session", OpenAIChatMessage(**interaction))
    assert (
        db._get_last_interaction_id("test_session")
        == initial_interaction_id + 1
    )


def test_multiple_put_message_increments_interaction_id(db, interaction):
    db.cursor.execute("DELETE FROM interactions")
    db.conn.commit()

    initial_interaction_id = db._get_last_interaction_id("session1")
    db.save_message("session1", OpenAIChatMessage(**interaction))
    db.save_message("session1", OpenAIChatMessage(**interaction))
    assert (
        db._get_last_interaction_id("session1") == initial_interaction_id + 2
    )


def test_get_messages_returns_single_message_for_session(db, interaction):
    db.cursor.execute("DELETE FROM interactions")
    db.conn.commit()

    # Given no initial messages
    assert len(db.get_messages("session1")) == 0

    # When a message is added
    db.save_message("session1", OpenAIChatMessage(**interaction))

    # Then get_messages should return that message
    messages = db.get_messages("session1")
    assert len(messages) == 1
    assert messages[0].role == interaction["role"]
    assert messages[0].content == interaction["content"]


def test_get_messages_returns_multiple_messages_in_order(db, interaction):
    db.cursor.execute("DELETE FROM interactions")
    db.conn.commit()

    # Given no initial messages
    assert len(db.get_messages("session1")) == 0

    # When two messages are added
    db.save_message("session1", OpenAIChatMessage(**interaction))
    db.save_message("session1", OpenAIChatMessage(**interaction))

    # Then get_messages should return both messages in the correct order
    messages = db.get_messages("session1")
    assert len(messages) == 2
    assert messages[0].role == interaction["role"]
    assert messages[0].content == interaction["content"]
    assert messages[1].role == interaction["role"]
    assert messages[1].content == interaction["content"]
