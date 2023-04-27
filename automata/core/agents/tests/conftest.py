import pytest

from automata.configs.config_types import AgentConfigVersion, AutomataAgentConfig
from automata.core.agents.automata_agent_builder import AutomataAgentBuilder
from automata.tool_management.tool_management_utils import build_llm_toolkits


@pytest.fixture
def automata_agent():
    tool_list = ["python_indexer"]
    mock_llm_toolkits = build_llm_toolkits(tool_list)

    initial_payload = {}

    instructions = "Test instruction."

    config_version = AgentConfigVersion.DEFAULT
    agent_config = AutomataAgentConfig.load(config_version)

    agent = (
        AutomataAgentBuilder(agent_config)
        .with_initial_payload(initial_payload)
        .with_instructions(instructions)
        .with_llm_toolkits(mock_llm_toolkits)
        .build()
    )
    return agent


@pytest.fixture
def automata_agent_builder():
    config_version = AgentConfigVersion.DEFAULT
    agent_config = AutomataAgentConfig.load(config_version)
    agent_builder = AutomataAgentBuilder(agent_config)
    return agent_builder
