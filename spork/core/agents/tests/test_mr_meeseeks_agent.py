import pytest

from spork.core import load_llm_toolkits
from spork.core.agents.mr_meeseeks_agent import MrMeeseeksAgent
from spork.core.utils import root_py_path
from spork.tools.python_tools.python_indexer import PythonIndexer


@pytest.fixture
def mr_meeseeks_agent():
    python_indexer = PythonIndexer(root_py_path())

    tool_list = ["python_indexer"]
    mock_llm_toolkits = load_llm_toolkits(tool_list)

    overview = python_indexer.get_overview()

    initial_payload = {
        "overview": overview,
    }

    agent = MrMeeseeksAgent(
        initial_payload=initial_payload,
        instructions="Test instruction.",
        llm_toolkits=mock_llm_toolkits,
    )
    return agent


def test_mr_meeseeks_agent_init(mr_meeseeks_agent):
    assert mr_meeseeks_agent is not None
    assert mr_meeseeks_agent.model == "gpt-4"
    assert mr_meeseeks_agent.session_id is not None
    assert len(mr_meeseeks_agent.toolkits.keys()) > 0


def test_mr_meeseeks_agent_iter_task(
    mr_meeseeks_agent,
):
    assert len(mr_meeseeks_agent.messages) == 3
