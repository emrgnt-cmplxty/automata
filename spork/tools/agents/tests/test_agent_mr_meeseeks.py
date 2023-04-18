import json
from unittest.mock import patch

import pytest
from langchain.agents import Tool

from spork.tools.agents.agent_mr_meeseeks import AgentMrMeeseeks
from spork.tools.python_tools.python_parser import PythonParser


@pytest.fixture
def agent_mr_meeseeks():
    python_parser = PythonParser()

    exec_tools = [
        Tool(
            name="test-tool",
            func=lambda x: x,
            description=f"Test tool",
            return_direct=True,
            verbose=True,
        )
    ]

    overview = python_parser.get_overview()

    initial_payload = {
        "overview": overview,
    }

    agent = AgentMrMeeseeks(
        initial_payload=initial_payload, instructions="Test instruction.", tools=exec_tools
    )
    return agent


def test_agent_mr_meeseeks_init(agent_mr_meeseeks):
    assert agent_mr_meeseeks is not None
    assert agent_mr_meeseeks.model == "gpt-4"
    assert agent_mr_meeseeks.session_id is not None
    assert len(agent_mr_meeseeks.tools) > 0


@patch("spork.tools.agents.agent_mr_meeseeks.openai.ChatCompletion.create")
def test_agent_mr_meeseeks_iter_task(mock_chatcompletion_create, agent_mr_meeseeks):
    mock_chatcompletion_create.return_value = {
        "choices": [{"message": {"content": '{"tool": "test-tool", "input": "test input"}'}}]
    }

    next_instruction = agent_mr_meeseeks.iter_task()
    assert len(next_instruction) == 1
    assert next_instruction[0] == "test input"


@patch("spork.tools.agents.agent_mr_meeseeks.openai.ChatCompletion.create")
def test_agent_mr_meeseeks_iter_task_no_outputs(mock_chatcompletion_create, agent_mr_meeseeks):
    mock_chatcompletion_create.return_value = {"choices": [{"message": {"content": "No outputs"}}]}

    next_instruction = agent_mr_meeseeks.iter_task()
    assert next_instruction is None


def test_agent_mr_meeseeks_extract_json_objects(agent_mr_meeseeks):
    input_str = """
        This is a sample string with some JSON objects.
        {"tool": "tool1", "input": "input1"}
        {"tool": "tool2", "input": "input2"}
    """

    json_objects = agent_mr_meeseeks._extract_json_objects(input_str)
    assert len(json_objects) == 2
    assert json.loads(json_objects[0]) == {"tool": "tool1", "input": "input1"}
    assert json.loads(json_objects[1]) == {"tool": "tool2", "input": "input2"}


def test_agent_mr_meeseeks_extract_json_objects_single_quotes(agent_mr_meeseeks):
    input_str = """
        This is a sample string with some JSON objects.
        {"tool": 'tool1', "input": 'input1'}
        {"tool": 'tool2', "input": 'input2'}
    """

    json_objects = agent_mr_meeseeks._extract_json_objects(input_str)
    assert len(json_objects) == 2
    assert json.loads(json_objects[0]) == {"tool": "tool1", "input": "input1"}
    assert json.loads(json_objects[1]) == {"tool": "tool2", "input": "input2"}
