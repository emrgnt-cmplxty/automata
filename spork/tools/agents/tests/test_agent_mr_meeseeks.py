import textwrap
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
    input_str = '''
        This is a sample string with some JSON objects.
        {"tool": "tool1", "input": "input1"}
        {"tool": "tool2", "input": """"input2""""}
    '''

    json_objects = agent_mr_meeseeks._parse_input_string(input_str)
    assert len(json_objects) == 2
    assert json_objects[0] == {"tool": "tool1", "input": "input1"}
    assert json_objects[1] == {"tool": "tool2", "input": '"""input2"""'}


def test_agent_mr_meeseeks_extract_json_objects_single_quotes(agent_mr_meeseeks):
    input_str = """
        This is a sample string with some JSON objects.
        {"tool": "tool1", "input": "input1"}
        {"tool": "tool2", "input": 'input2'}
    """
    json_objects = agent_mr_meeseeks._parse_input_string(input_str)
    assert len(json_objects) == 2
    assert json_objects[0]["tool"] == "tool1"
    assert json_objects[0]["input"] == "input1"
    assert json_objects[1] == {"tool": "tool2", "input": "input2"}


def test_agent_mr_meeseeks_parse_example_0(agent_mr_meeseeks):
    input_str = textwrap.dedent(
        """{
  "tool": "python-writer-modify-code-state",
  "input": "spork.tools.tool_managers.tests.test_agent_mr_meeseeks_tool_manager,import pytest
from spork.tools.agents.agent_mr_meeseeks import AgentMrMeeseeks
from spork.tools.tool_managers.agent_mr_meeseeks_tool_manager import AgentMrMeeseeksToolManager
from spork.tools.utils import PassThroughBuffer

def test_init():
    agent_mr_meeseeks = AgentMrMeeseeks()
    tool_manager = AgentMrMeeseeksToolManager(agent_mr_meeseeks)
    assert tool_manager.agent_mr_meeseeks == agent_mr_meeseeks
    assert tool_manager.logger is None

def test_build_tools():
    agent_mr_meeseeks = AgentMrMeeseeks()
    tool_manager = AgentMrMeeseeksToolManager(agent_mr_meeseeks)
    tools = tool_manager.build_tools()
    assert len(tools) == 1
    assert tools[0].name == 'mr-meeseeks-task'

def test_tool_execution():
    agent_mr_meeseeks = AgentMrMeeseeks()
    tool_manager = AgentMrMeeseeksToolManager(agent_mr_meeseeks)
    tools = tool_manager.build_tools()
    agent_mr_meeseeks.run = MagicMock(return_value='Task completed')
    tool = tools[0]
    result = tool.func()
    assert result == 'Task completed'"
}

{
  "tool": "python-writer-write-to-disk"
}"""
    )
    json_objects = agent_mr_meeseeks._parse_input_string(input_str)
    assert len(json_objects) == 2


def test_agent_mr_meeseeks_parse_example_1(agent_mr_meeseeks):
    input_str = textwrap.dedent(
        """{
  "tool": "python-writer-modify-code-state",
  "input": "spork.main_meeseeks.main,from spork.tools.tool_managers.agent_mr_meeseeks_tool_manager import AgentMrMeeseeksToolManager

def main():
    parser.add_argument('--instructions', type=str, help='The initial instructions for the agent.')
    parser.add_argument('--version', type=AgentVersion, default=AgentVersion.MEESEEKS_V1, help='The version of the agent.')
    parser.add_argument('--model', type=str, default='gpt-4', help='The model to be used for the agent.')
    parser.add_argument('--session_id', type=str, default=None, help='The session id for the agent.')
    parser.add_argument('--stream', type=bool, default=True, help='Should we stream the responses?')
    logging_config = get_logging_config()
    logging.config.dictConfig(logging_config)
    logger = logging.getLogger(__name__)
    args = parser.parse_args()
    python_parser = PythonParser()
    python_writer = PythonWriter(python_parser)
    exec_tools = []
    exec_tools += build_tools(PythonParserToolManager(python_parser))
    exec_tools += build_tools(PythonWriterToolManager(python_writer))
    overview = python_parser.get_overview()
    initial_payload = {'overview': overview}
    logger.info('Passing in instructions: %s', args.instructions)
    logger.info('-' * 100)
    agent = AgentMrMeeseeks(initial_payload=initial_payload, instructions=args.instructions, tools=exec_tools, version=args.version, model=args.model, session_id=args.session_id, stream=args.stream)
    agent_mr_meeseeks_tool_manager = AgentMrMeeseeksToolManager(agent)
    exec_tools += build_tools(agent_mr_meeseeks_tool_manager)
    logger.info('Running the agent now...')
    agent.run()
    while True:
        user_input = input('Do you have any further instructions or feedback? Type \'exit\' to terminate: ')
        if user_input.lower() == 'exit':
            break
        else:
            instructions = [{'role': 'user', 'content': user_input}]
            agent.extend_last_instructions(instructions)
            agent.iter_task()"
}

Now, I will write the modifications to disk.

{
  "tool": "python-writer-write-to-disk"
}"""
    )
    json_objects = agent_mr_meeseeks._parse_input_string(input_str)
    assert len(json_objects) == 2
