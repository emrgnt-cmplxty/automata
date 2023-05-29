import pytest

from automata.configs.automata_agent_config_utils import AutomataAgentConfigBuilder
from automata.configs.automata_agent_configs import AgentConfigName, AutomataInstructionPayload
from automata.core.agent.automata_agent_utils import AutomataAgentFactory
from automata.tool_management.tool_management_utils import build_llm_toolkits


@pytest.fixture
def automata_agent():
    tool_list = ["python_retriever"]
    mock_llm_toolkits = build_llm_toolkits(tool_list)

    instruction_payload = AutomataInstructionPayload(agents_message="", overview="", tools="")

    instructions = "Test instruction."

    config_name = AgentConfigName.AUTOMATA_MAIN_DEV

    agent = AutomataAgentFactory.create_agent(
        instructions,
        config=AutomataAgentConfigBuilder.from_name(config_name)
        .with_instruction_payload(instruction_payload)
        .with_llm_toolkits(mock_llm_toolkits)
        .with_stream(False)
        .build(),
    )
    return agent


@pytest.fixture
def automata_agent_config_builder():
    config_name = AgentConfigName.DEFAULT
    agent_config_builder = AutomataAgentConfigBuilder.from_name(config_name)
    return agent_config_builder


@pytest.fixture
def automata_agent_with_dev_main_builder():
    config_name = AgentConfigName.AUTOMATA_MAIN_DEV
    agent_config_builder = AutomataAgentConfigBuilder.from_name(config_name)
    return agent_config_builder
