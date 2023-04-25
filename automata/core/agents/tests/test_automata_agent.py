import textwrap

import pytest

from automata.configs.agent_configs.config_type import AutomataAgentConfig, AutomataConfigVersion
from automata.core.agents.automata_agent import AutomataAgent, AutomataAgentBuilder
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


def test_extract_action():
    input_text = textwrap.dedent(
        """
        - thoughts
            - I will use the automata-indexer-retrieve-code tool to retrieve the code for the "run" function from the Automata agent.
        - actions
            - tool_query_0
                - tool
                    - automata-indexer-retrieve-code
                - inputs
                    - Retrieve the raw code for the function 'run' from the Automata agent, including all necessary imports and docstrings.
        """
    )

    result = AutomataAgent._extract_actions(input_text)
    assert result[0]["tool"] == "automata-indexer-retrieve-code"
    assert (
        result[0]["input"][0]
        == "Retrieve the raw code for the function 'run' from the Automata agent, including all necessary imports and docstrings."
    )


def test_extract_actions():
    input_text = textwrap.dedent(
        """
        - thoughts
            - I will use the automata-indexer-retrieve-code tool to retrieve the code for the "run" function from the Automata agent.
        - actions
            - tool_query_0
                - tool
                    - automata-indexer-retrieve-code
                - inputs
                    - Retrieve the raw code for the function 'run' from the Automata agent, including all necessary imports and docstrings.
            - tool_query_1
                - tool
                    - automata-writer-modify-module
                - inputs
                    - Modify the code in the Automata agent.
                    - A dummy input....
        """
    )

    result = AutomataAgent._extract_actions(input_text)
    assert result[0]["tool"] == "automata-indexer-retrieve-code"
    assert (
        result[0]["input"][0]
        == "Retrieve the raw code for the function 'run' from the Automata agent, including all necessary imports and docstrings."
    )

    assert result[1]["tool"] == "automata-writer-modify-module"
    assert result[1]["input"][0] == "Modify the code in the Automata agent."

    assert result[1]["input"][1] == "A dummy input...."


def test_extract_actions_with_code():
    input_text = textwrap.dedent(
        """
        - thoughts
            - I will use the automata-indexer-retrieve-code tool to retrieve the code for the "run" function from the Automata agent.
        - actions
            - tool_query_0
                - tool
                    - automata-indexer-retrieve-code
                - inputs
                    - Retrieve the raw code for the function 'run' from the Automata agent, including all necessary imports and docstrings.
            - tool_query_1
                - tool
                    - automata-writer-modify-module
                - inputs
                    - Modify the code in the Automata agent.
                    - python
                    ```
                    def f(x: int) -> int:
                        return 0
                    ```
        """
    )

    result = AutomataAgent._extract_actions(input_text)
    print("result = ", result)
    assert result[0]["tool"] == "automata-indexer-retrieve-code"
    assert (
        result[0]["input"][0]
        == "Retrieve the raw code for the function 'run' from the Automata agent, including all necessary imports and docstrings."
    )

    assert result[1]["tool"] == "automata-writer-modify-module"
    assert result[1]["input"][0] == "Modify the code in the Automata agent."

    assert result[1]["input"][1] == "def f(x: int) -> int:\n    return 0\n"


def test_extract_actions_with_return():
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

    extractor = AutomataAgent.ActionExtractor()
    result = extractor.extract_actions(text)

    assert result[0]["tool"] == "return_result_0"
    assert result[0]["input"][0] == "Function 'run' has been added to core.tests.sample_code.test."


def test_extract_actions_tools_and_with_return():
    text = textwrap.dedent(
        """
        *Assistant*
            - thoughts
                - Having successfully written the output file, I can now return the result.
            - actions
                - tool_query_0
                    - tool
                        - automata-indexer-retrieve-code
                    - inputs
                        - Retrieve the raw code for the function 'run' from the Automata agent, including all necessary imports and docstrings.

                - return_result_0
                    - Function 'run' has been added to core.tests.sample_code.test.
        """
    )

    extractor = AutomataAgent.ActionExtractor()
    result = extractor.extract_actions(text)
    assert result[0]["tool"] == "automata-indexer-retrieve-code"
    assert (
        result[0]["input"][0]
        == "Retrieve the raw code for the function 'run' from the Automata agent, including all necessary imports and docstrings."
    )

    assert result[1]["tool"] == "return_result_0"
    assert result[1]["input"][0] == "Function 'run' has been added to core.tests.sample_code.test."


def test_extract_actions_tools_and_with_return_processed(automata_agent):
    text = textwrap.dedent(
        """
        - thoughts
            - Having successfully written the output file, I can now return the result.
        - actions
            - tool_query_0
                - tool
                    - automata-indexer-retrieve-code
                - inputs
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


def test_iter_task_core_logic(automata_agent):
    text = textwrap.dedent(
        """
        - thoughts
            - Having successfully written the output file, I can now return the result.
        - actions
            - tool_query_0
                - tool
                    - automata-indexer-retrieve-code
                - inputs
                    - Retrieve the raw code for the function 'run' from the Automata agent, including all necessary imports and docstrings.

            - return_result_0
                - Function 'run' has been added to core.tests.sample_code.test.
        """
    )
    observations = automata_agent._generate_observations(text)
    is_return_result = automata_agent._contains_return_result(observations)

    user_observation_message = AutomataAgent._generate_user_observation_message(observations)
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
