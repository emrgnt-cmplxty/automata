import pytest

from automata.core import load_llm_toolkits
from automata.core.agents.automata_agent import (
    AutomataAgentBuilder,
    AutomataAgentConfig,
    AutomataConfigVersion,
)


@pytest.fixture
def automata_agent():
    tool_list = ["python_indexer"]
    mock_llm_toolkits = load_llm_toolkits(tool_list)

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
    assert len(automata_agent.llm_toolkits.keys()) > 0


def test_automata_agent_iter_task(
    automata_agent,
):
    assert len(automata_agent.messages) == 3
