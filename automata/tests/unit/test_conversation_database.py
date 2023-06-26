import os

import pytest

from automata.core.agent.conversation_database import AutomataAgentConversationDatabase


@pytest.fixture(scope="module")
def db(tmpdir_factory):
    db_file = tmpdir_factory.mktemp("data").join("test.db")
    db = AutomataAgentConversationDatabase("session1", str(db_file))
    yield db
    db.close()
    os.remove(str(db_file))


@pytest.fixture
def interaction():
    return {"role": "user", "content": "Hello, world!", "function_call": {}}


def test_get_last_interaction_id_when_no_interactions(db):
    assert db.get_last_interaction_id() == 0


def test_put_message_increments_interaction_id(db, interaction):
    initial_interaction_id = db.get_last_interaction_id()
    db.put_message(**interaction)
    assert db.get_last_interaction_id() == initial_interaction_id + 1


def test_multiple_put_message_increments_interaction_id(db, interaction):
    initial_interaction_id = db.get_last_interaction_id()
    db.put_message(**interaction)
    db.put_message(**interaction)
    assert db.get_last_interaction_id() == initial_interaction_id + 2
