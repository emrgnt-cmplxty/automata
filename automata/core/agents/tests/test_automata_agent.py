import textwrap
from unittest.mock import patch

import pytest

from automata.core.agents.automata_agent import AutomataAgent
from automata.tool_management.tool_management_utils import build_llm_toolkits


def test_build_tool_message(automata_agent_builder):
    tool_list = ["python_indexer", "python_writer", "codebase_oracle"]
    mock_llm_toolkits = build_llm_toolkits(tool_list)

    agent = automata_agent_builder.with_llm_toolkits(mock_llm_toolkits).build()
    messages = agent._build_tool_message()
    assert len(messages) > 1_000
    assert "python-indexer-retrieve-code" in messages
    assert "python-indexer-retrieve-docstring" in messages
    assert "python-indexer-retrieve-raw-code" in messages
    assert "python-writer-update-module" in messages
    assert "codebase-oracle-agent" in messages


def test_init_database(automata_agent):
    automata_agent._init_database()
    assert automata_agent.conn is not None
    assert automata_agent.cursor is not None


def test_save_and_load_interaction(automata_agent):
    automata_agent._init_database()
    message = {"role": "assistant", "content": "Test message."}
    automata_agent._save_interaction(message)
    # Add assertions to check if the message is saved correctly.
    automata_agent.messages = {}
    automata_agent._load_previous_interactions()
    saved_results = automata_agent.messages
    assert len(saved_results) == 4
    assert saved_results[-1]["role"] == "assistant"
    assert saved_results[-1]["content"] == "Test message."


@patch("openai.ChatCompletion.create")
def test_iter_task_without_api_call(mock_openai_chatcompletion_create, automata_agent):
    # Mock the API response
    mock_openai_chatcompletion_create.return_value = {
        "choices": [{"message": {"content": "The dummy_tool has been tested successfully."}}]
    }

    # Call the iter_task method and store the result
    result = automata_agent.iter_task()

    # Check if the result is as expected
    assistant_message, user_message = result
    assert assistant_message["content"] == "The dummy_tool has been tested successfully."
    assert user_message["content"], AutomataAgent.CONTINUE_MESSAGE
    assert len(automata_agent.messages) == 5


def mock_openai_response_with_completion_message():
    return {
        "choices": [
            {
                "message": {
                    "content": textwrap.dedent(
                        """
                        - thoughts
                          - I can now return the requested information.
                        - actions
                          - return_result_0
                            - AutomataAgent is imported in the following files: 1. tools.tool_management.automata_agent_tool_manager.py, 2. scripts.main_automata.py, 3. agents.automata_agent.py
                        """
                    )
                }
            }
        ]
    }


@pytest.mark.parametrize("api_response", [mock_openai_response_with_completion_message()])
@patch("openai.ChatCompletion.create")
def test_iter_task_with_completion_message(
    mock_openai_chatcompletion_create, api_response, automata_agent
):
    # Mock the API response
    mock_openai_chatcompletion_create.return_value = api_response

    # Call the iter_task method and store the result
    result = automata_agent.iter_task()

    # Check if the result is None, indicating that the agent has completed
    assert result is None

    # Verify that the agent's completed attribute is set to True
    assert automata_agent.completed is True

    # Check if the completion message is stored correctly
    completion_message = automata_agent.messages[-1]["content"]
    assert "AutomataAgent is imported in the following files:" in completion_message
