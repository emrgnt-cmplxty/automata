import os

import pytest

from spork.core.utils import clean_agent_result

from .conftest import build_agent_with_params, retry

current_file_dir = os.path.dirname(os.path.realpath(__file__))

MODEL = "gpt-3.5-turbo"
TEMPERATURE = 0.0
EXPECTED_RESPONSES = {
    "test_retrieve_load_yaml_docs": "Load a YAML file and return",
    "test_retrieve_python_writer_docs": "This module provides a class for writing Python",
}


@retry(3)
@pytest.mark.regression
@pytest.mark.parametrize(
    "mr_meeseeks_params",
    [
        {
            "model": MODEL,
            "temperature": TEMPERATURE,
            "tool_list": ["python_indexer", "codebase_oracle"],
        },
        # Add more parameter sets as needed
    ],
    indirect=True,
)
def test_retrieve_load_yaml_docs(mr_meeseeks_params):
    agent = build_agent_with_params(
        mr_meeseeks_params,
        "Fetch the docstrings for the load_yaml function in the util file.",
        max_iters=2,
        temperature=TEMPERATURE,
        model=MODEL,
    )
    result = clean_agent_result(agent.run())
    expected_content = EXPECTED_RESPONSES["test_retrieve_load_yaml_docs"].strip()
    assert expected_content in result


@retry(3)
@pytest.mark.regression
@pytest.mark.parametrize(
    "mr_meeseeks_params",
    [
        {
            "model": MODEL,
            "temperature": TEMPERATURE,
            "tool_list": ["python_writer"],
        },
        # Add more parameter sets as needed
    ],
    indirect=True,
)
def test_retrieve_python_writer_docs(mr_meeseeks_params):
    agent = build_agent_with_params(
        mr_meeseeks_params,
        "Fetch the docstrings for the python writer class.",
        max_iters=2,
        temperature=TEMPERATURE,
        model=MODEL,
    )
    result = clean_agent_result(agent.run())
    expected_content = EXPECTED_RESPONSES["test_retrieve_python_writer_docs"].strip()
    assert expected_content in result
