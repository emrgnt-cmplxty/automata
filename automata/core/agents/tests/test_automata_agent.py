import textwrap
from unittest.mock import patch

import pytest

from automata.configs.agent_configs.config_type import AutomataAgentConfig, AutomataConfigVersion
from automata.core.agents.automata_agent import AutomataAgent
from automata.core.agents.automata_agent_builder import AutomataAgentBuilder
from automata.core.agents.automata_agent_helpers import (
    ActionExtractor,
    generate_user_observation_message,
    retrieve_completion_message,
)
from automata.tool_management.tool_management_utils import build_llm_toolkits


@pytest.fixture
def automata_agent():
    tool_list = ["python_indexer"]
    mock_llm_toolkits = build_llm_toolkits(tool_list)

    initial_payload = {}

    instructions = "Test instruction."

    config_version = AutomataConfigVersion.DEFAULT
    agent_config = AutomataAgentConfig.load(config_version)

    agent = (
        AutomataAgentBuilder(agent_config)
        .with_initial_payload(initial_payload)
        .with_instructions(instructions)
        .with_llm_toolkits(mock_llm_toolkits)
        .build()
    )
    return agent


def test_automata_agent_init(automata_agent):
    assert automata_agent is not None
    assert automata_agent.model == "gpt-4"
    assert automata_agent.session_id is not None
    tool_list = ["python_indexer", "python_writer", "codebase_oracle"]
    build_llm_toolkits(tool_list)

    assert len(automata_agent.llm_toolkits.keys()) > 0


def test_automata_agent_iter_task(
    automata_agent,
):
    assert len(automata_agent.messages) == 3


def test_builder_default_config():
    config_version = AutomataConfigVersion.DEFAULT
    agent_config = AutomataAgentConfig.load(config_version)
    agent = AutomataAgentBuilder(agent_config).build()

    assert agent.model == "gpt-4"
    assert agent.stream is False
    assert agent.verbose is False
    assert agent.max_iters == 1_000_000
    assert agent.temperature == 0.7
    assert agent.session_id is not None  # session id defaults if not set


def test_builder_provided_parameters_override_defaults():
    config_version = AutomataConfigVersion.DEFAULT
    agent_config = AutomataAgentConfig.load(config_version)
    agent = (
        AutomataAgentBuilder(agent_config)
        .with_model("gpt-3.5-turbo")
        .with_stream(True)
        .with_verbose(True)
        .with_max_iters(500)
        .with_temperature(0.5)
        .with_session_id("test-session-id")
        .build()
    )

    assert agent.model == "gpt-3.5-turbo"
    assert agent.stream is True
    assert agent.verbose is True
    assert agent.max_iters == 500
    assert agent.temperature == 0.5
    assert agent.session_id == "test-session-id"


def test_builder_accepts_all_fields():
    config_version = AutomataConfigVersion.DEFAULT
    agent_config = AutomataAgentConfig.load(config_version)
    initial_payload = {}
    tool_list = ["python_indexer", "python_writer", "codebase_oracle"]
    mock_llm_toolkits = build_llm_toolkits(tool_list)
    instructions = "Test instructions."

    agent = (
        AutomataAgentBuilder(agent_config)
        .with_initial_payload(initial_payload)
        .with_llm_toolkits(mock_llm_toolkits)
        .with_instructions(instructions)
        .with_model("gpt-3.5-turbo")
        .with_stream(True)
        .with_verbose(True)
        .with_max_iters(500)
        .with_temperature(0.5)
        .with_session_id("test-session-id")
        .build()
    )
    assert agent.initial_payload == initial_payload
    assert agent.llm_toolkits == mock_llm_toolkits
    assert agent.instructions == instructions
    assert agent.model == "gpt-3.5-turbo"
    assert agent.stream is True
    assert agent.verbose is True
    assert agent.max_iters == 500
    assert agent.temperature == 0.5
    assert agent.session_id == "test-session-id"


def test_builder_creates_proper_instance():
    config_version = AutomataConfigVersion.DEFAULT
    agent_config = AutomataAgentConfig.load(config_version)
    agent = AutomataAgentBuilder(agent_config).build()

    assert isinstance(agent, AutomataAgent)


def test_builder_invalid_input_types():
    config_version = AutomataConfigVersion.DEFAULT
    agent_config = AutomataAgentConfig.load(config_version)
    builder = AutomataAgentBuilder(agent_config)

    with pytest.raises(ValueError):
        builder.with_model(123)

    with pytest.raises(ValueError):
        builder.with_stream("True")

    with pytest.raises(ValueError):
        builder.with_verbose("True")

    with pytest.raises(ValueError):
        builder.with_max_iters("500")

    with pytest.raises(ValueError):
        builder.with_temperature("0.5")

    with pytest.raises(ValueError):
        builder.with_session_id(12345)


def test_config_loading_different_versions():
    for config_version in AutomataConfigVersion:
        agent_config = AutomataAgentConfig.load(config_version)
        assert isinstance(agent_config, AutomataAgentConfig)


def test_builder_gets_default_params_from_test_config():
    config_version = AutomataConfigVersion.TEST
    agent_config = AutomataAgentConfig.load(config_version)
    agent = AutomataAgentBuilder(agent_config).build()

    assert agent.instructions == "Test instructions."
    assert agent.model == "gpt-4"
    assert agent.stream is False
    assert agent.verbose is True
    assert agent.max_iters == 100
    assert agent.temperature == 0.8
    assert agent.session_id == "test-session-id"


def test_extract_actions_0():
    input_text = textwrap.dedent(
        """
        - thoughts
            - I will use the automata-indexer-retrieve-code tool to retrieve the code for the "run" function from the Automata agent.
        - actions
            - tool_query_0
                - tool_name
                    - automata-indexer-retrieve-code
                - tool_args
                    - Retrieve the raw code for the function 'run' from the Automata agent, including all necessary imports and docstrings.
        """
    )

    result = ActionExtractor.extract_actions(input_text)
    assert result[0]["tool_name"] == "automata-indexer-retrieve-code"
    assert (
        result[0]["tool_args"][0]
        == "Retrieve the raw code for the function 'run' from the Automata agent, including all necessary imports and docstrings."
    )


def test_extract_actions_1():
    input_text = textwrap.dedent(
        """
        - thoughts
            - I will use the automata-indexer-retrieve-code tool to retrieve the code for the "run" function from the Automata agent.
        - actions
            - tool_query_0
                - tool_name
                    - automata-indexer-retrieve-code
                - tool_args
                    - Retrieve the raw code for the function 'run' from the Automata agent, including all necessary imports and docstrings.
            - tool_query_1
                - tool_name
                    - automata-writer-modify-module
                - tool_args
                    - Modify the code in the Automata agent.
                    - A dummy input....
        """
    )

    result = ActionExtractor.extract_actions(input_text)
    assert result[0]["tool_name"] == "automata-indexer-retrieve-code"
    assert (
        result[0]["tool_args"][0]
        == "Retrieve the raw code for the function 'run' from the Automata agent, including all necessary imports and docstrings."
    )

    assert result[1]["tool_name"] == "automata-writer-modify-module"
    assert result[1]["tool_args"][0] == "Modify the code in the Automata agent."

    assert result[1]["tool_args"][1] == "A dummy input...."


def test_extract_actions_2():
    input_text = textwrap.dedent(
        """
        - thoughts
            - I will use the automata-indexer-retrieve-code tool to retrieve the code for the "run" function from the Automata agent.
        - actions
            - tool_query_0
                - tool_name
                    - automata-indexer-retrieve-code
                - tool_args
                    - Retrieve the raw code for the function 'run' from the Automata agent, including all necessary imports and docstrings.
            - tool_query_1
                - tool_name
                    - automata-writer-modify-module
                - tool_args
                    - Modify the code in the Automata agent.
                    - python
                    ```
                    def f(x: int) -> int:
                        return 0
                    ```
        """
    )

    result = ActionExtractor.extract_actions(input_text)
    assert result[0]["tool_name"] == "automata-indexer-retrieve-code"
    assert (
        result[0]["tool_args"][0]
        == "Retrieve the raw code for the function 'run' from the Automata agent, including all necessary imports and docstrings."
    )

    assert result[1]["tool_name"] == "automata-writer-modify-module"
    assert result[1]["tool_args"][0] == "Modify the code in the Automata agent."

    assert result[1]["tool_args"][1] == "def f(x: int) -> int:\n    return 0\n"


def test_extract_actions_3():
    text = textwrap.dedent(
        """
        *Assistant*
            - thoughts
                - Having successfully written the output file, I can now return the result.
            - actions
                - return_result_0
                    - Function 'run' has been added to core.tests.sample_code.test.
        """
    )

    extractor = ActionExtractor()
    result = extractor.extract_actions(text)

    assert result[0]["tool_name"] == "return_result_0"
    assert (
        result[0]["tool_args"][0]
        == "Function 'run' has been added to core.tests.sample_code.test."
    )


def test_extract_actions_4():
    text = textwrap.dedent(
        """
        *Assistant*
            - thoughts
                - Having successfully written the output file, I can now return the result.
            - actions
                - tool_query_0
                    - tool_name
                        - automata-indexer-retrieve-code
                    - tool_args
                        - Retrieve the raw code for the function 'run' from the Automata agent, including all necessary imports and docstrings.

                - return_result_0
                    - Function 'run' has been added to core.tests.sample_code.test.
        """
    )

    extractor = ActionExtractor()
    result = extractor.extract_actions(text)
    assert result[0]["tool_name"] == "automata-indexer-retrieve-code"
    assert (
        result[0]["tool_args"][0]
        == "Retrieve the raw code for the function 'run' from the Automata agent, including all necessary imports and docstrings."
    )

    assert result[1]["tool_name"] == "return_result_0"
    assert (
        result[1]["tool_args"][0]
        == "Function 'run' has been added to core.tests.sample_code.test."
    )


def test_extract_actions_5(automata_agent):
    text = textwrap.dedent(
        """
        - thoughts
            - Having successfully written the output file, I can now return the result.
        - actions
            - tool_query_0
                - tool_name
                    - automata-indexer-retrieve-code
                - tool_args
                    - Retrieve the raw code for the function 'run' from the Automata agent, including all necessary imports and docstrings.

            - return_result_0
                - Function 'run' has been added to core.tests.sample_code.test.
        """
    )
    processed_input = automata_agent._generate_observations(text)
    assert (
        processed_input["output_0"]
        == """Error: Tool 'automata-indexer-retrieve-code' not found."""
    )
    assert (
        processed_input["return_result_0"]
        == """Function 'run' has been added to core.tests.sample_code.test."""
    )


def test_extract_actions_6(automata_agent):
    text = textwrap.dedent(
        """
        - thoughts
            - Having successfully written the output file, I can now return the result.
        - actions
            - tool_query_0
                - tool_name
                    - automata-indexer-retrieve-code
                - tool_args
                    - Retrieve the raw code for the function 'run' from the Automata agent, including all necessary imports and docstrings.

            - return_result_0
                - Function 'run' has been added to core.tests.sample_code.test.
        """
    )
    observations = automata_agent._generate_observations(text)
    is_return_result = retrieve_completion_message(observations)

    user_observation_message = generate_user_observation_message(observations)
    assert is_return_result
    expected_observations = textwrap.dedent(
        """-  observations
    - output_0
      - Error: Tool 'automata-indexer-retrieve-code' not found.
    - return_result_0
      - Function 'run' has been added to core.tests.sample_code.test.
        """
    )
    assert user_observation_message.strip() == expected_observations.strip()


def test_build_tool_message(automata_agent):
    "".join(
        [
            f"\n{tool.name}: {tool.description}\n"
            for toolkit in automata_agent.llm_toolkits.values()
            for tool in toolkit.tools
        ]
    )
    config_version = AutomataConfigVersion.DEFAULT
    agent_config = AutomataAgentConfig.load(config_version)
    initial_payload = {}
    tool_list = ["python_indexer", "python_writer", "codebase_oracle"]
    mock_llm_toolkits = build_llm_toolkits(tool_list)
    instructions = "Test instructions."

    agent = (
        AutomataAgentBuilder(agent_config)
        .with_initial_payload(initial_payload)
        .with_llm_toolkits(mock_llm_toolkits)
        .with_instructions(instructions)
        .with_model("gpt-3.5-turbo")
        .with_stream(True)
        .with_verbose(True)
        .with_max_iters(500)
        .with_temperature(0.5)
        .with_session_id("test-session-id")
        .build()
    )
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


def mock_openai_response():
    return {
        "choices": [
            {"message": {"content": "The python_indexer tool has been tested successfully."}}
        ]
    }


@pytest.mark.parametrize("api_response", [mock_openai_response()])
@patch("openai.ChatCompletion.create")
def test_iter_task_without_api_call(
    mock_openai_chatcompletion_create, api_response, automata_agent
):
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
