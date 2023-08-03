import os
from unittest.mock import patch

import pytest

from automata.agent.error import AgentMaxIterError
from automata.agent.openai_agent import (
    OpenAIAutomataAgent,
    OpenAIChatCompletionProvider,
    OpenAITool,
)
from automata.config import OpenAIAutomataAgentConfig
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


def test_agent_initialization(automata_agent):
    assert automata_agent._initialized
    assert automata_agent.iteration_count == 0
    assert not automata_agent.completed
    assert isinstance(automata_agent.config, OpenAIAutomataAgentConfig)


def test_invalid_config():
    with pytest.raises(Exception):
        OpenAIAutomataAgent("instructions", "InvalidConfig")  # type: ignore


def test_tool_execution(automata_agent):
    assert automata_agent.tools
    for tool in automata_agent.tools:
        assert isinstance(tool, OpenAITool)


def test_chat_provider(automata_agent):
    assert isinstance(
        automata_agent.chat_provider, OpenAIChatCompletionProvider
    )


def test_build_initial_messages(automata_agent):
    formatters = {
        "user_input_instructions": "DUMMY_INSTRUCTIONS",
    }
    initial_messages = automata_agent._build_initial_messages(formatters)
    assert "assistant" == initial_messages[0].role
    assert "DUMMY_INSTRUCTIONS" in initial_messages[1].content
    assert "user" == initial_messages[1].role


@patch("openai.ChatCompletion.create")
def test_iter_step_without_api_call(
    mock_openai_chatcompletion_create, automata_agent
):
    # Mock the API response
    mock_openai_chatcompletion_create.return_value = {
        "choices": [
            {
                "message": {
                    "role": "assistant",
                    "content": "The dummy_tool has been tested successfully.",
                }
            }
        ]
    }

    # Call the iter_step method and store the result
    result = next(automata_agent)
    # Check if the result is as expected
    assistant_message, user_message = result
    assert (
        assistant_message.content
        == "The dummy_tool has been tested successfully."
    )
    assert user_message.content, OpenAIAutomataAgent.CONTINUE_PREFIX
    assert automata_agent.iteration_count == 1


@patch("openai.ChatCompletion.create")
def test_run_with_no_completion(
    mock_openai_chatcompletion_create, automata_agent
):
    max_iterations = 5
    automata_agent.config.max_iterations = max_iterations
    # Mock the API response
    mock_openai_chatcompletion_create.return_value = {
        "choices": [{"message": {"content": "...", "role": "assistant"}}]
    }

    with pytest.raises(AgentMaxIterError):
        automata_agent.run()

    assert (
        automata_agent.iteration_count == max_iterations + 1
    )  # + 1 since the agent is allowed to return a response.


def mock_openai_response_with_completion_message():
    return {
        "choices": [
            {
                "message": {
                    "role": "assistant",
                    "function_call": {
                        "name": "call_termination",
                        "arguments": '{"result": "Success"}',
                    },
                    "content": None,
                }
            }
        ]
    }


@pytest.mark.parametrize(
    "api_response", [mock_openai_response_with_completion_message()]
)
@patch("openai.ChatCompletion.create")
def test_run_with_completion_message(
    mock_openai_chatcompletion_create, api_response, automata_agent
):
    # Mock the API response
    mock_openai_chatcompletion_create.return_value = api_response

    # Call the iter_step method and store the result
    result = automata_agent.run()

    # Check if the result is None, indicating that the agent has completed
    assert result == "Observation:\nSuccess\n"

    # Verify that the agent's completed attribute is set to True
    assert automata_agent.completed is True


def test_db_connection(db):
    assert db.conn is not None


def test_db_interaction(db):
    interaction = {"content": "x", "role": "assistant"}
    initial_interaction_id = db._get_last_interaction_id("session1")
    db.save_message(
        "session1", OpenAIChatMessage(**interaction, function_call=None)
    )
    assert (
        db._get_last_interaction_id("session1") == initial_interaction_id + 1
    )


def test_db_cleanup(db, tmpdir_factory):
    db_file = tmpdir_factory.mktemp("data").join("test.db")
    db_path = str(db_file)
    new_db = OpenAIAutomataConversationDatabase(db_path)
    new_db.close()


@pytest.mark.parametrize(
    "api_response", [mock_openai_response_with_completion_message()]
)
@patch("openai.ChatCompletion.create")
def test_agent_saves_messages_to_database(
    mock_openai_chatcompletion_create, api_response, automata_agent, db
):
    # Mock the API response
    mock_openai_chatcompletion_create.return_value = api_response

    # Call the iter_step method and store the result
    automata_agent.set_database_provider(db)

    result = automata_agent.run()

    # Check if the result is None, indicating that the agent has completed
    assert result == "Observation:\nSuccess\n"

    # Verify that the agent's completed attribute is set to True
    assert automata_agent.completed is True
    saved_messages = db.get_messages(automata_agent.session_id)

    assert saved_messages[-2].role == "assistant"
    assert saved_messages[-2].content is None
    assert saved_messages[-2].function_call.name == "call_termination"
    assert saved_messages[-2].function_call.arguments == {"result": "Success"}
    assert saved_messages[-1].role == "user"
    assert "Success" in saved_messages[-1].content
    assert saved_messages[-1].function_call is None
