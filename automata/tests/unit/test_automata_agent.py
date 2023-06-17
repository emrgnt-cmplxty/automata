import textwrap
import uuid
from unittest.mock import patch

import pytest

from automata.config.config_types import AutomataInstructionPayload
from automata.core.agent.agent import AutomataAgent
from automata.core.agent.memories import AutomataMemoryDatabase
from automata.core.agent.tools.tool_utils import build_llm_toolkits
from automata.core.base.openai import OpenAIChatMessage


def test_build_tool_message(automata_agent_config_builder):
    tool_list = ["py_retriever", "py_writer"]
    mock_llm_toolkits = build_llm_toolkits(tool_list)

    config = automata_agent_config_builder.with_llm_toolkits(mock_llm_toolkits).build()
    tools_messages = config._build_tool_message()
    assert len(tools_messages) > 1_000
    assert "python-indexer-retrieve-code" in tools_messages
    assert "python-indexer-retrieve-docstring" in tools_messages
    assert "python-indexer-retrieve-raw-code" in tools_messages
    assert "python-writer-update-module" in tools_messages


def test_build_initial_messages(automata_agent):
    formatters = {
        "user_input_instructions": "DUMMY_INSTRUCTIONS",
    }
    initial_messages = automata_agent._build_initial_messages(formatters)
    assert AutomataAgent.INITIALIZER_DUMMY in initial_messages[0].content
    assert "assistant" == initial_messages[0].role
    assert "DUMMY_INSTRUCTIONS" in initial_messages[1].content
    assert "user" == initial_messages[1].role


def test_init_database(automata_agent):
    automata_agent_db = AutomataMemoryDatabase(session_id=0)
    assert automata_agent_db.conn is not None
    assert automata_agent_db.cursor is not None


def test_save_and_load_interaction(automata_agent):
    # automata_agent._init_database()
    session_id = str(uuid.uuid4())
    automata_agent_db = AutomataMemoryDatabase(session_id=session_id)

    automata_agent_db.put_message("assistant", "Test message.", session_id)
    # Add assertions to check if the message is saved correctly.
    automata_agent.messages = automata_agent_db.get_conversations()

    saved_results = automata_agent.messages
    assert len(saved_results) == 1
    assert saved_results[-1].role == "assistant"
    assert saved_results[-1].content == "Test message."


@patch("openai.ChatCompletion.create")
def test_iter_step_without_api_call(mock_openai_chatcompletion_create, automata_agent):
    # Mock the API response
    mock_openai_chatcompletion_create.return_value = {
        "choices": [{"message": {"content": "The dummy_tool has been tested successfully."}}]
    }

    # Call the iter_step method and store the result
    result = automata_agent.iter_step()

    # Check if the result is as expected
    assistant_message, user_message = result
    assert assistant_message.content == "The dummy_tool has been tested successfully."
    assert user_message.content, AutomataAgent.CONTINUE_MESSAGE
    assert len(automata_agent.messages) == 5


@patch("openai.ChatCompletion.create")
def test_max_iters_without_api_call(mock_openai_chatcompletion_create, automata_agent):
    max_iters = 5
    automata_agent.config.max_iters = max_iters
    # Mock the API response
    mock_openai_chatcompletion_create.return_value = {
        "choices": [{"message": {"content": "invalid tool name"}}]
    }

    result = automata_agent.run()
    assert (
        result
        == f"Result was not found before iterations exceeded configured max limit: {max_iters}. Debug summary: invalid tool name"
    )
    assert len(automata_agent.messages) == max_iters * 2 + AutomataAgent.NUM_DEFAULT_MESSAGES + 1


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
def test_iter_step_with_completion_message(
    mock_openai_chatcompletion_create, api_response, automata_agent
):
    # Mock the API response
    mock_openai_chatcompletion_create.return_value = api_response

    # Call the iter_step method and store the result
    result = automata_agent.iter_step()

    # Check if the result is None, indicating that the agent has completed
    assert result is None

    # Verify that the agent's completed attribute is set to True
    assert automata_agent.completed is True

    # Check if the completion message is stored correctly
    completion_message = automata_agent.messages[-1].content
    assert "AutomataAgent is imported in the following files:" in completion_message


def mock_openai_response_with_completion_tool_message_to_parse():
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
                            - {tool_output_0}
                        """
                    )
                }
            }
        ]
    }


@pytest.mark.parametrize(
    "api_response", [mock_openai_response_with_completion_tool_message_to_parse()]
)
@patch("openai.ChatCompletion.create")
def test_iter_step_with_parsed_completion_message(
    mock_openai_chatcompletion_create, api_response, automata_agent
):
    observation = textwrap.dedent(
        """
        - observations
          - tool_output_0
            - task_0
                - Please carry out the following instruction Test instruction..
        """
    )
    automata_agent.messages.append(OpenAIChatMessage("user", observation))
    # Mock the API response
    mock_openai_chatcompletion_create.return_value = api_response
    automata_agent.iter_step()
    completion_message = automata_agent.messages[-1].content
    stripped_completion_message = [ele.strip() for ele in completion_message.split("\n")]
    assert stripped_completion_message[0] == "task_0"
    assert (
        stripped_completion_message[1]
        == "- Please carry out the following instruction Test instruction.."
    )


def mock_openai_response_with_completion_agent_message_to_parse():
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
                            - {agent_query_0}
                        """
                    )
                }
            }
        ]
    }


@pytest.mark.parametrize(
    "api_response", [mock_openai_response_with_completion_agent_message_to_parse()]
)
@patch("openai.ChatCompletion.create")
def test_iter_step_with_parsed_completion_message_2(
    mock_openai_chatcompletion_create,
    api_response,
    automata_agent_with_dev_main_builder,
):
    instructions = "This is a test instruction."
    automata_agent_config = (
        automata_agent_with_dev_main_builder.with_instruction_version("agent_introduction")
        .with_stream(False)
        .with_instruction_payload(
            AutomataInstructionPayload(agents_message="", overview="", tools="")
        )
        .build()
    )

    automata_agent = AutomataAgent(instructions=instructions, config=automata_agent_config)
    automata_agent.setup()

    # Mock the API response
    mock_openai_chatcompletion_create.return_value = api_response
    automata_agent.iter_step()

    completion_message = automata_agent.messages[-1].content
    stripped_completion_message = [ele.strip() for ele in completion_message.split("\n")]
    assert stripped_completion_message[0] == "{agent_query_0}"


@pytest.mark.parametrize(
    "api_response", [mock_openai_response_with_completion_agent_message_to_parse()]
)
@patch("openai.ChatCompletion.create")
def test_iter_step_with_parsed_completion_message_main_2(
    mock_openai_chatcompletion_create,
    api_response,
    automata_agent_with_dev_main_builder,
):
    instructions = "This is a test instruction."
    automata_agent_config = (
        automata_agent_with_dev_main_builder.with_instruction_version("agent_introduction")
        .with_stream(False)
        .with_instruction_payload(
            AutomataInstructionPayload(agents_message="", overview="", tools="")
        )
        .build()
    )

    automata_agent = AutomataAgent(instructions=instructions, config=automata_agent_config)
    automata_agent.setup()

    # Mock the API response
    mock_openai_chatcompletion_create.return_value = api_response
    automata_agent.iter_step()

    completion_message = automata_agent.messages[-1].content
    stripped_completion_message = [ele.strip() for ele in completion_message.split("\n")]
    assert stripped_completion_message[0] == "{agent_query_0}"
