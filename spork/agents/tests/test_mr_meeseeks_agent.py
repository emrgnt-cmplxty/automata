import logging

import pytest

from spork.agents.mr_meeseeks_agent import MrMeeseeksAgent
from spork.tools.base.tool_utils import load_llm_tools
from spork.tools.python_tools.python_indexer import PythonIndexer
from spork.tools.utils import root_py_path


@pytest.fixture
def mr_meeseeks_agent():
    python_indexer = PythonIndexer(root_py_path())

    inputs = {
        "documentation_url": "https://some.documentation.url/",
        "model": "gpt-4",
    }

    tool_list = ["python_indexer"]
    inputs = {}  # Add any required inputs for the tools here
    logger = logging.getLogger(__name__)
    mock_llm_tools = load_llm_tools(tool_list, inputs, logger)

    overview = python_indexer.get_overview()

    initial_payload = {
        "overview": overview,
    }

    agent = MrMeeseeksAgent(
        initial_payload=initial_payload, instructions="Test instruction.", llm_tools=mock_llm_tools
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
