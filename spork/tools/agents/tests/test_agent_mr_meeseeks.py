import os
import tempfile
from typing import List
from unittest.mock import MagicMock

import openai
import pytest
from langchain.tools import BaseTool

from spork.config import *  # noqa F403

# Replace imports with appropriate paths for your project
from ..agent_mr_meeseeks import AgentMrMeeseeks


@pytest.fixture
def mocked_openai_api():
    original_api_method = openai.ChatCompletion.create
    openai.ChatCompletion.create = MagicMock(
        return_value={"choices": [{"message": {"content": "Test response from Assistant"}}]}
    )

    yield

    openai.ChatCompletion.create = original_api_method


@pytest.fixture
def temporary_database():
    # Create a temporary file for the SQLite database
    db_file = tempfile.NamedTemporaryFile(delete=False)

    # Set the SQLite connection string to use the temporary file
    original_db_path = CONVERSATION_DB_NAME  # noqa F405
    AgentMrMeeseeks.DB_PATH = f"sqlite:///{db_file.name}"

    yield

    # Close and remove the temporary file after the test is finished
    db_file.close()
    os.unlink(db_file.name)

    # Reset the SQLite connection string to the original value
    AgentMrMeeseeks.DB_PATH = original_db_path


def test_order_preservation(temporary_database, mocked_openai_api):
    initial_payload = {"overview": "Test overview"}
    initial_instructions = [
        {
            "role": "assistant",
            "content": '{"tool": "meeseeks-initializer", "input": "Hello, I am Mr. Meeseeks, look at me."}',
        },
        {"role": "user", "content": "Test instruction"},
    ]
    tools: List[BaseTool] = []

    # Create an agent and save interactions
    agent = AgentMrMeeseeks(initial_payload, initial_instructions, tools)
    agent.iter_task()
    agent._save_interaction({"role": "user", "content": "Test instruction 2"})
    agent.iter_task()

    session_id = agent.session_id

    # Create a new agent with the same session ID to replay the interactions
    replay_agent = AgentMrMeeseeks(
        initial_payload, initial_instructions, tools, session_id=session_id
    )

    assert replay_agent.messages == agent.messages


if __name__ == "__main__":
    pytest.main(["-v", "test_agent_meeseeks.py"])
