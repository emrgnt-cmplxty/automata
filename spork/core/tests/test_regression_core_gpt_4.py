import logging
import os
import shutil
import textwrap
from functools import wraps

import pytest

from spork.configs.agent_configs import AgentVersion
from spork.core import load_llm_toolkits
from spork.core.agents.mr_meeseeks_agent import MrMeeseeksAgent
from spork.core.utils import root_py_path
from spork.tools.python_tools.python_indexer import PythonIndexer

current_file_dir = os.path.dirname(os.path.realpath(__file__))
MODEL = "gpt-4"


@pytest.fixture
def mr_meeseeks_indexer_params():
    python_indexer = PythonIndexer(root_py_path())

    inputs = {"model": MODEL}

    tool_list = ["python_indexer", "codebase_oracle"]
    inputs = {}  # Add any required inputs for the tools here
    logger = logging.getLogger(__name__)
    mock_llm_toolkits = load_llm_toolkits(tool_list, inputs, logger)

    overview = python_indexer.get_overview()

    initial_payload = {
        "overview": overview,
    }
    return initial_payload, mock_llm_toolkits


@pytest.fixture
def mr_meeseeks_writer_params():
    python_indexer = PythonIndexer(root_py_path())

    inputs = {"model": MODEL}

    tool_list = ["python_writer"]
    inputs = {}  # Add any required inputs for the tools here
    logger = logging.getLogger(__name__)
    mock_llm_toolkits = load_llm_toolkits(tool_list, inputs, logger)

    overview = python_indexer.get_overview()

    initial_payload = {
        "overview": overview,
    }
    return initial_payload, mock_llm_toolkits


@pytest.fixture
def mr_meeseeks_master_params():
    inputs = {"model": MODEL}

    tool_list = ["meeseeks_indexer", "meeseeks_writer"]
    inputs = {}  # Add any required inputs for the tools here
    logger = logging.getLogger(__name__)
    mock_llm_toolkits = load_llm_toolkits(tool_list, inputs, logger)

    initial_payload = {}
    return initial_payload, mock_llm_toolkits


EXPECTED_RESPONSES = {
    "test_get_mr_meeseeks_docs": "MrMeeseeksAgent is an autonomous agent that performs the actual work of the Spork system. Meeseeks are responsible for executing instructions and reporting the results back to the master.",
    "test_get_python_writer_docs": textwrap.dedent(
        """A utility class for working with Python AST nodes.\n\nPublic Methods:\n\n    update_module(\n        source_code: str,\n        extending_module: bool,\n        module_obj (Optional[Module], keyword),\n        module_path (Optional[str], keyword)\n    ) -> None:\n        Perform an in-place extention or reduction of a module object according to the received code.\n\n    write_module(self) -> None:\n        Write the module object to a file.\n\n    Exceptions:\n        ModuleNotFound: Raised when a module cannot be found.\n        InvalidArguments: Raised when invalid arguments are passed to a method."""
    ),
    "test_simple_writer_example": "def test_write_simple_response(mr_meeseeks_writer_params) -> bool:\n    return True",
    "test_advanced_writer_example": textwrap.dedent(
        '''
        """This is a sample module for testing"""

        def test_function() -> bool:
            """This is my new function"""
            return True


        class TestClass:
            """This is my test class"""

            def __init__(self):
                """This initializes TestClass"""
                pass

            def test_method(self) -> bool:
                """This is my test method"""
                return False
        '''
    ),
    "test_fetch_run_and_write_out": textwrap.dedent(
        '''
        def run(self) -> str:
            """Run until the initial instruction terminates."""

            while True:
                self.iter_task()

                if MrMeeseeksAgent.is_completion_message(self.messages[-1]["content"]):
                    return self.messages[-1]["content"]
                # Check the previous previous message to see if it is a completion message
                if MrMeeseeksAgent.is_completion_message(self.messages[-2]["content"]):
                    return self.messages[-2]["content"]
                # Each iteration produces two messages, so the check below is for equalling the max_iters
                if (len(self.messages) - MrMeeseeksAgent.NUM_DEFAULT_MESSAGES) >= self.max_iters * 2:
                    return "Result was not captured before iterations exceeded max limit."
        '''
    ),
}


def build_agent_with_params(
    mr_meeseeks_params,
    instructions: str,
    version: AgentVersion = AgentVersion.MEESEEKS_RETRIEVER_V2,
    max_iters=2,
    model="gpt-4",
):
    print("Building with version = %s" % (version))
    initial_payload, mock_llm_toolkits = mr_meeseeks_params
    agent = MrMeeseeksAgent(
        initial_payload=initial_payload,
        instructions=instructions,
        llm_toolkits=mock_llm_toolkits,
        verbose=True,
        max_iters=max_iters,
        version=version,
        temperature=0.7,
        model=model,
    )
    return agent


def cleanup_and_check(expected_content: str) -> None:
    # Check if the file has been created
    file_path = os.path.join(current_file_dir, "sample_code", "test.py")
    assert os.path.isfile(file_path), "File does not exist"

    # Check if the content of the file is as expected

    with open(file_path, "r") as file:
        content = file.read()
    print("content = ", content)
    # Delete the whole "sample_code" directory after the test
    sample_code_dir = os.path.join(current_file_dir, "sample_code")
    # shutil.rmtree(sample_code_dir)
    assert content.strip() == expected_content.strip()


def retry(num_attempts: int):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for _ in range(num_attempts - 1):
                try:
                    return func(*args, **kwargs)
                except AssertionError:
                    pass
            return func(*args, **kwargs)

        return wrapper

    return decorator


# @pytest.mark.regression
# @retry(3)
# def test_get_mr_meeseeks_docs(mr_meeseeks_indexer_params):
#     agent = build_agent_with_params(
#         mr_meeseeks_indexer_params, "Fetch the docstrings for mr meeseeks agent."
#     )
#     result = clean_result(agent.run())

#     expected_content = EXPECTED_RESPONSES["test_get_mr_meeseeks_docs"].strip()
#     assert result == expected_content


# @pytest.mark.regression
# @retry(3)
# def test_get_python_writer_docs(mr_meeseeks_indexer_params):
#     agent = build_agent_with_params(
#         mr_meeseeks_indexer_params, "Fetch the docstrings for the python writer."
#     )
#     result = clean_result(agent.run())
#     expected_content = EXPECTED_RESPONSES["test_get_python_writer_docs"].strip()
#     assert result == expected_content


# @pytest.mark.regression
# @retry(3)
# def test_simple_writer_example(mr_meeseeks_writer_params):
#     expected_content = EXPECTED_RESPONSES["test_simple_writer_example"].strip()

#     agent = build_agent_with_params(
#         mr_meeseeks_writer_params,
#         f"Write the following function - '{expected_content}' to the file core.tests.sample_code.test",
#         AgentVersion.MEESEEKS_WRITER_V2,
#     )
#     agent.run()
#     cleanup_and_check(expected_content)


"""
# TODO - FIX THE CODE TO MAKE THIS TEST PASS
# @pytest.mark.regression
# # @retry(3)
# def test_advanced_writer_example(mr_meeseeks_writer_params):
#     expected_content = EXPECTED_RESPONSES["test_advanced_writer_example"].strip()
#     agent = build_agent_with_params(
#         mr_meeseeks_writer_params,
#         f"Write the following module - '{expected_content}' to the file core.tests.sample_code.test",
#     )
#     agent.run()
#     print("agent.messages = ", agent.messages)

#     cleanup_and_check(expected_content)
"""


@pytest.mark.regression
# @retry(3)
def test_fetch_run_and_write_out(mr_meeseeks_master_params):
    agent = build_agent_with_params(
        mr_meeseeks_master_params,
        f'1. Retrieve the code for the function "run" from the mr meeseeks agent.\n'
        f"2. NEXT, write the retrieved code into the file core.tests.sample_code.test, as other methods within this file are dependent on it.\n"
        f'Do not return a "result" until you have successfuly written the output file.',
        version=AgentVersion.MEESEEKS_MASTER_V3,
        max_iters=4,
    )

    next_steps = (
        {
            "role": "assistant",
            "content": 'Thought: I will use the meeseeks-indexer-retrieve-code tool to retrieve the code for the "run" function from the Mr. Meeseeks agent.\nAction:\n{\n  "tool": "meeseeks-indexer-retrieve-code",\n  "input": "Retrieve the code for the function \'run\' from the Mr. Meeseeks agent, including all necessary imports and docstrings."\n}',
        },
        {
            "role": "user",
            "content": "Observation:\n{\n\"output_0\": \"The code for the 'run' function in Mr. Meeseeks agent is:\n\ndef run(self) -> str:\n    while True:\n        self.iter_task()\n        if MrMeeseeksAgent.is_completion_message(self.messages[-2]['content']):\n            return self.messages[-2]['content']\n        if len(self.messages) - MrMeeseeksAgent.NUM_DEFAULT_MESSAGES >= self.max_iters * 2:\n            return 'Result was not captured before iterations exceeded max limit.'\n\nNote: No docstring was found for this function.\"\", \n}",
        },
    )
    agent.messages.extend(next_steps)
    result = agent.run()
    print("agent.messages = ", agent.messages)
    print("result = ", result)
    expected_content = EXPECTED_RESPONSES["test_fetch_run_and_write_out"].strip()
    print("expected_content = ", expected_content)
    cleanup_and_check(expected_content)
