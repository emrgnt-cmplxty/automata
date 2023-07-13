import pytest

from automata.config import AgentConfigName, OpenAIAutomataAgentConfig
from automata.tools.factory import AgentToolFactory

default_model = "gpt-4"
default_model_2 = "gpt-3.5-turbo"


def test_automata_agent_init(automata_agent):
    assert automata_agent is not None
    assert automata_agent.config.model == default_model
    assert automata_agent.config.session_id is not None
    assert len(automata_agent.config.tools) > 0
    assert len(automata_agent.agent_conversation_database) == 5


def test_builder_default_config(automata_agent_config_builder):
    config = automata_agent_config_builder.build()

    assert config.model == default_model
    assert config.stream is False
    assert config.verbose is True
    assert config.max_iterations == 50
    assert config.temperature == 0.8
    assert config.session_id is not None  # session id defaults if not set


def test_builder_provided_parameters_override_defaults(
    automata_agent_config_builder,
):
    config = (
        automata_agent_config_builder.with_model(default_model_2)
        .with_stream(True)
        .with_verbose(True)
        .with_max_iterations(500)
        .with_temperature(0.5)
        .with_session_id("test-session-id")
        .build()
    )

    assert config.model == default_model_2
    assert config.stream is True
    assert config.verbose is True
    assert config.max_iterations == 500
    assert config.temperature == 0.5
    assert config.session_id == "test-session-id"


def test_builder_accepts_all_fields(automata_agent_config_builder):
    toolkit_list = []

    tools = AgentToolFactory.build_tools(
        toolkit_list,
    )

    config = (
        automata_agent_config_builder.with_tools(tools)
        .with_model(default_model_2)
        .with_stream(True)
        .with_verbose(True)
        .with_max_iterations(500)
        .with_temperature(0.5)
        .with_session_id("test-session-id")
        .build()
    )
    assert config.tools == tools
    assert config.model == default_model_2
    assert config.stream is True
    assert config.verbose is True
    assert config.max_iterations == 500
    assert config.temperature == 0.5
    assert config.session_id == "test-session-id"


def test_builder_creates_proper_instance(automata_agent_config_builder):
    config = automata_agent_config_builder.build()

    assert isinstance(config, OpenAIAutomataAgentConfig)


def test_builder_invalid_input_types(automata_agent_config_builder):
    with pytest.raises(ValueError):
        automata_agent_config_builder.with_model(123)

    with pytest.raises(ValueError):
        automata_agent_config_builder.with_stream("True")

    with pytest.raises(ValueError):
        automata_agent_config_builder.with_verbose("True")

    with pytest.raises(ValueError):
        automata_agent_config_builder.with_max_iterations("500")

    with pytest.raises(ValueError):
        automata_agent_config_builder.with_temperature("0.5")

    with pytest.raises(ValueError):
        automata_agent_config_builder.with_session_id(12345)


def test_config_loading_different_versions():
    for config_name in AgentConfigName:
        if config_name == AgentConfigName.DEFAULT:
            continue
        config = OpenAIAutomataAgentConfig.load(config_name)
        assert isinstance(config, OpenAIAutomataAgentConfig)
