from unittest.mock import MagicMock

import pytest

from automata.config.config_types import AgentConfigName, AutomataAgentConfig
from automata.core.agent.tool.tool_utils import build_llm_tool_managers


def test_automata_agent_init(automata_agent):
    assert automata_agent is not None
    assert automata_agent.config.model == "gpt-4"
    assert automata_agent.config.session_id is not None
    assert len(automata_agent.config.llm_toolkits.keys()) > 0


def test_automata_agent_iter_step(
    automata_agent,
):
    assert len(automata_agent.messages) == 3


def test_builder_default_config(automata_agent_config_builder):
    config = automata_agent_config_builder.build()

    assert config.model == "gpt-4"
    assert config.stream is False
    assert config.verbose is True
    assert config.max_iters == 100
    assert config.temperature == 0.8
    assert config.session_id is not None  # session id defaults if not set


def test_builder_provided_parameters_override_defaults(automata_agent_config_builder):
    config = (
        automata_agent_config_builder.with_model("gpt-3.5-turbo")
        .with_stream(True)
        .with_verbose(True)
        .with_max_iters(500)
        .with_temperature(0.5)
        .with_session_id("test-session-id")
        .build()
    )

    assert config.model == "gpt-3.5-turbo"
    assert config.stream is True
    assert config.verbose is True
    assert config.max_iters == 500
    assert config.temperature == 0.5
    assert config.session_id == "test-session-id"


def test_builder_accepts_all_fields(automata_agent_config_builder):
    tool_list = ["py_reader", "py_writer"]
    from automata.core.coding.py.reader import PyReader
    from automata.core.coding.py.writer import PyWriter

    mock_llm_toolkits = build_llm_tool_managers(
        tool_list,
        py_reader=MagicMock(spec=PyReader),
        py_writer=MagicMock(spec=PyWriter),
    )

    config = (
        automata_agent_config_builder.with_llm_toolkits(mock_llm_toolkits)
        .with_model("gpt-3.5-turbo")
        .with_stream(True)
        .with_verbose(True)
        .with_max_iters(500)
        .with_temperature(0.5)
        .with_session_id("test-session-id")
        .build()
    )
    assert config.llm_toolkits == mock_llm_toolkits
    assert config.model == "gpt-3.5-turbo"
    assert config.stream is True
    assert config.verbose is True
    assert config.max_iters == 500
    assert config.temperature == 0.5
    assert config.session_id == "test-session-id"


def test_builder_creates_proper_instance(automata_agent_config_builder):
    config = automata_agent_config_builder.build()

    assert isinstance(config, AutomataAgentConfig)


def test_builder_invalid_input_types(automata_agent_config_builder):
    with pytest.raises(ValueError):
        automata_agent_config_builder.with_model(123)

    with pytest.raises(ValueError):
        automata_agent_config_builder.with_stream("True")

    with pytest.raises(ValueError):
        automata_agent_config_builder.with_verbose("True")

    with pytest.raises(ValueError):
        automata_agent_config_builder.with_max_iters("500")

    with pytest.raises(ValueError):
        automata_agent_config_builder.with_temperature("0.5")

    with pytest.raises(ValueError):
        automata_agent_config_builder.with_session_id(12345)


def test_config_loading_different_versions():
    for config_name in AgentConfigName:
        if config_name == AgentConfigName.DEFAULT:
            continue
        elif config_name == AgentConfigName.AUTOMATA_INITIALIZER:
            continue
        main_config = AutomataAgentConfig.load(config_name)
        assert isinstance(main_config, AutomataAgentConfig)
