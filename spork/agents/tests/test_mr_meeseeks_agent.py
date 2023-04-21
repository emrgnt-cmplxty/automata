import textwrap
from unittest.mock import patch

import pytest

from spork.agents.mr_meeseeks_agent import MrMeeseeksAgent
from spork.tools import Tool
from spork.tools.python_tools.python_indexer import PythonIndexer
from spork.tools.utils import root_py_path


@pytest.fixture
def mr_meeseeks_agent():
    python_indexer = PythonIndexer(root_py_path())

    exec_tools = [
        Tool(
            name="test-tool",
            func=lambda x: x,
            description=f"Test tool",
            return_direct=True,
            verbose=True,
        )
    ]

    overview = python_indexer.get_overview()

    initial_payload = {
        "overview": overview,
    }

    agent = MrMeeseeksAgent(
        initial_payload=initial_payload, instructions="Test instruction.", tools=exec_tools
    )
    return agent


def test_mr_meeseeks_agent_init(mr_meeseeks_agent):
    assert mr_meeseeks_agent is not None
    assert mr_meeseeks_agent.model == "gpt-4"
    assert mr_meeseeks_agent.session_id is not None
    assert len(mr_meeseeks_agent.tools) > 0


@patch("spork.agents.mr_meeseeks_agent.openai.ChatCompletion.create")
def test_mr_meeseeks_agent_iter_task(mock_chatcompletion_create, mr_meeseeks_agent):
    mock_chatcompletion_create.return_value = {
        "choices": [{"message": {"content": '{"tool": "test-tool", "input": "test input"}'}}]
    }

    next_instruction = mr_meeseeks_agent.iter_task()
    assert len(next_instruction) == 1
    assert next_instruction[0] == "test input"


@patch("spork.agents.mr_meeseeks_agent.openai.ChatCompletion.create")
def test_mr_meeseeks_agent_iter_task_no_outputs(mock_chatcompletion_create, mr_meeseeks_agent):
    mock_chatcompletion_create.return_value = {"choices": [{"message": {"content": "No outputs"}}]}

    next_instruction = mr_meeseeks_agent.iter_task()
    assert next_instruction is None


def test_mr_meeseeks_agent_extract_json_objects(mr_meeseeks_agent):
    input_str = '''
        This is a sample string with some JSON objects.
        {"tool": "tool1", "input": "input1"}
        {"tool": "tool2", "input": """"input2""""}
    '''

    json_objects = mr_meeseeks_agent._parse_input_string(input_str)
    assert len(json_objects) == 2
    assert json_objects[0] == {"tool": "tool1", "input": "input1"}
    assert json_objects[1] == {"tool": "tool2", "input": '"""input2"""'}


def test_mr_meeseeks_agent_extract_json_objects_single_quotes(mr_meeseeks_agent):
    input_str = """
        This is a sample string with some JSON objects.
        {"tool": "tool1", "input": "input1"}
        {"tool": "tool2", "input": 'input2'}
    """
    json_objects = mr_meeseeks_agent._parse_input_string(input_str)
    assert len(json_objects) == 2
    assert json_objects[0]["tool"] == "tool1"
    assert json_objects[0]["input"] == "input1"
    assert json_objects[1] == {"tool": "tool2", "input": "input2"}


def test_mr_meeseeks_agent_parse_example_0(mr_meeseeks_agent):
    input_str = textwrap.dedent(
        """{
  "tool": "python-writer-update-module",
  "input": "spork.tools.tool_managers.tests.test_mr_meeseeks_agent_tool_manager,import pytest
from spork.agents.mr_meeseeks_agent import MrMeeseeksAgent
from spork.tools.tool_managers.mr_meeseeks_agent_tool_manager import MrMeeseeksAgentToolManager
from spork.tools.utils import PassThroughBuffer

def test_init():
    mr_meeseeks_agent = MrMeeseeksAgent()
    tool_manager = MrMeeseeksAgentToolManager(mr_meeseeks_agent)
    assert tool_manager.mr_meeseeks_agent == mr_meeseeks_agent
    assert tool_manager.logger is None

def test_build_tools():
    mr_meeseeks_agent = MrMeeseeksAgent()
    tool_manager = MrMeeseeksAgentToolManager(mr_meeseeks_agent)
    tools = tool_manager.build_tools()
    assert len(tools) == 1
    assert tools[0].name == 'mr-meeseeks-task'

def test_tool_execution():
    mr_meeseeks_agent = MrMeeseeksAgent()
    tool_manager = MrMeeseeksAgentToolManager(mr_meeseeks_agent)
    tools = tool_manager.build_tools()
    mr_meeseeks_agent.run = MagicMock(return_value='Task completed')
    tool = tools[0]
    result = tool.func()
    assert result == 'Task completed'"
}

{
  "tool": "python-writer-write-to-disk"
}"""
    )
    json_objects = mr_meeseeks_agent._parse_input_string(input_str)
    assert len(json_objects) == 2


def test_mr_meeseeks_agent_parse_example_1(mr_meeseeks_agent):
    input_str = textwrap.dedent(
        """{
  "tool": "python-writer-update-module",
  "input": "spork.main_meeseeks.main,from spork.tools.tool_managers.mr_meeseeks_agent_tool_manager import MrMeeseeksAgentToolManager

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
    python_indexer = PythonIndexer(root_py_path())
    python_writer = PythonASTManipulator(python_indexer)
    exec_tools = []
    exec_tools += build_tools(PythonIndexerToolManager(python_indexer))
    exec_tools += build_tools(PythonASTManipulatorToolManager(python_writer))
    overview = python_parser.get_overview()
    initial_payload = {'overview': overview}
    logger.info('Passing in instructions: %s', args.instructions)
    logger.info('-' * 100)
    agent = MrMeeseeksAgent(initial_payload=initial_payload, instructions=args.instructions, tools=exec_tools, version=args.version, model=args.model, session_id=args.session_id, stream=args.stream)
    mr_meeseeks_agent_tool_manager = MrMeeseeksAgentToolManager(agent)
    exec_tools += build_tools(mr_meeseeks_agent_tool_manager)
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
    json_objects = mr_meeseeks_agent._parse_input_string(input_str)
    assert len(json_objects) == 2
