import logging
import os
import shutil
import textwrap

import pytest

from spork.configs.agent_configs import AgentVersion
from spork.core import load_llm_toolkits
from spork.core.agents.mr_meeseeks_agent import MrMeeseeksAgent
from spork.core.utils import root_py_path
from spork.tools.python_tools.python_indexer import PythonIndexer

TEST_MODEL = "gpt-3.5-turbo"


@pytest.fixture
def mr_meeseeks_indexer_params():
    python_indexer = PythonIndexer(root_py_path())

    inputs = {"model": TEST_MODEL}

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

    inputs = {"model": "gpt-3.5-turbo"}

    tool_list = ["python_writer"]
    inputs = {}  # Add any required inputs for the tools here
    logger = logging.getLogger(__name__)
    mock_llm_toolkits = load_llm_toolkits(tool_list, inputs, logger)

    overview = python_indexer.get_overview()

    initial_payload = {
        "overview": overview,
    }
    return initial_payload, mock_llm_toolkits


EXPECTED_RESPONSES = {
    "test_get_mr_meeseeks_docs": "MrMeeseeksAgent is an autonomous agent that performs the actual work of the Spork system. Meeseeks are responsible for executing instructions and reporting the results back to the master.",
    "test_get_python_writer_docs": textwrap.dedent(
        """A utility class for working with Python AST nodes.\n\nPublic Methods:\n\n    update_module(\n        source_code: str,\n        extending_module: bool,\n        module_obj (Optional[Module], keyword),\n        module_path (Optional[str], keyword)\n    ) -> None:\n        Perform an in-place extention or reduction of a module object according to the received code.\n\n    write_module(self) -> None:\n        Write the module object to a file.\n\n    Exceptions:\n        ModuleNotFound: Raised when a module cannot be found.\n        InvalidArguments: Raised when invalid arguments are passed to a method."""
    ),
    "test_write_simple_response": "def test_write_simple_response(mr_meeseeks_writer_params):\n    return True",
}


def clean_result(result: str) -> str:
    result = result.split('{"result_0": ')[1]
    result = result.replace("}", "")[1:-1]
    result = result.replace("\\n", "\n").strip()
    return result


def build_agent_with_params(mr_meeseeks_params, instructions):
    initial_payload, mock_llm_toolkits = mr_meeseeks_params

    agent = MrMeeseeksAgent(
        initial_payload=initial_payload,
        instructions=instructions,
        llm_toolkits=mock_llm_toolkits,
        verbose=True,
        max_iters=5,
        version=AgentVersion.MEESEEKS_RETRIEVER_V2,
        temperature=0.0,
    )
    return agent


# @pytest.mark.regression
# def test_get_mr_meeseeks_docs(mr_meeseeks_params):
#     agent = build_agent_with_params(
#         mr_meeseeks_params, "Fetch the docstrings for mr meeseeks agent."
#     )
#     result = clean_result(agent.run())

#     expected_content = EXPECTED_RESPONSES["test_get_mr_meeseeks_docs"].strip()
#     assert result == expected_content

# @pytest.mark.regression
# def test_get_python_writer_docs(mr_meeseeks_indexer_params):
#     agent = build_agent_with_params(
#         mr_meeseeks_indexer_params, "Fetch the docstrings for the python writer."
#     )
#     result = clean_result(agent.run())
#     expected_content = EXPECTED_RESPONSES["test_get_python_writer_docs"].strip()
#     assert result == expected_content


@pytest.mark.regression
def test_write_simple_response(mr_meeseeks_writer_params):
    agent = build_agent_with_params(
        mr_meeseeks_writer_params,
        "Write the following function - 'def test_write_simple_response(mr_meeseeks_writer_params):\n    return True' to the file core.tests.sample_code.test",
    )
    result = agent.run()
    print("result = ", result)
    # Check if the file has been created
    file_path = "spork/core/tests/sample_code/test.py"
    assert os.path.isfile(file_path)

    # Check if the content of the file is as expected
    expected_content = EXPECTED_RESPONSES["test_write_simple_response"].strip()
    with open(file_path, "r") as file:
        content = file.read().strip()

    # Delete the file after the test
    os.remove(file_path)
    assert content.strip() == expected_content.strip()

    sample_code_dir = "spork/core/tests/sample_code"
    shutil.rmtree(sample_code_dir)


# @pytest.mark.regression
# def test_write_simple_response(mr_meeseeks_writer_params):
#     agent = build_agent_with_params(
#         mr_meeseeks_writer_params,
#         "Write the following function - 'def test_write_simple_response(mr_meeseeks_writer_params):\n    return True' to the file core.tests.sample_code.test",
#     )
#     result = agent.run()
#     print("messages = ", agent.messages)
#     print("result = ", result)
#     # assert result == EXPECTED_RESPONSES["test_get_python_writer_docs"].strip()
#     assert False
