from unittest.mock import patch

import pytest

from automata.agent import AgentMaxIterError, OpenAIAutomataAgent


def test_build_initial_messages(automata_agent):
    formatters = {
        "user_input_instructions": "DUMMY_INSTRUCTIONS",
    }
    initial_messages = automata_agent._build_initial_messages(formatters)
    assert "assistant" == initial_messages[0].role
    assert "DUMMY_INSTRUCTIONS" in initial_messages[1].content
    assert "user" == initial_messages[1].role


@patch("openai.ChatCompletion.create")
def test_iter_step_without_api_call(mock_openai_chatcompletion_create, automata_agent):
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
    assert assistant_message.content == "The dummy_tool has been tested successfully."
    assert user_message.content, OpenAIAutomataAgent.CONTINUE_PREFIX
    assert automata_agent.iteration_count == 1


@patch("openai.ChatCompletion.create")
def test_run_with_no_completion(mock_openai_chatcompletion_create, automata_agent):
    max_iterations = 5
    automata_agent.config.max_iterations = max_iterations
    # Mock the API response
    mock_openai_chatcompletion_create.return_value = {
        "choices": [{"message": {"content": "...", "role": "assistant"}}]
    }

    with pytest.raises(AgentMaxIterError):
        automata_agent.run()

    assert automata_agent.iteration_count == max_iterations


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


@pytest.mark.parametrize("api_response", [mock_openai_response_with_completion_message()])
@patch("openai.ChatCompletion.create")
def test_run_with_completion_message(
    mock_openai_chatcompletion_create, api_response, automata_agent
):
    # Mock the API response
    mock_openai_chatcompletion_create.return_value = api_response

    # Call the iter_step method and store the result
    result = automata_agent.run()

    # Check if the result is None, indicating that the agent has completed
    assert result == f"{OpenAIAutomataAgent.EXECUTION_PREFIX}\n\nSuccess"

    # Verify that the agent's completed attribute is set to True
    assert automata_agent.completed is True


# TODO - Add test of successful non-termination function call
