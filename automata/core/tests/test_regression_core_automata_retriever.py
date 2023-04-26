import os
import textwrap

import pytest

from automata.core.utils import calculate_similarity

from .conftest import build_agent_with_params

current_file_dir = os.path.dirname(os.path.realpath(__file__))

MODEL = "gpt-4"
TEMPERATURE = 0.7
EXPECTED_RESPONSES = {
    "test_retrieve_load_yaml_docs": "Loads a YAML file.",
    "test_retrieve_python_writer_docs": textwrap.dedent(
        """A utility class for working with Python AST nodes.

Public Methods:

update_module(
    source_code: str,
    extending_module: bool,
    module_obj (Optional[Module], keyword),
    module_path (Optional[str], keyword)
) -> None:
    Perform an in-place extention or reduction of a module object according to the received code.

write_module(self) -> None:
    Write the module object to a file.

Exceptions:
    ModuleNotFound: Raised when a module cannot be found.
    InvalidArguments: Raised when invalid arguments are passed to a method.
"""
    ),
}


@pytest.mark.regression
@pytest.mark.parametrize(
    "automata_params",
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
def test_retrieve_load_yaml_docs(automata_params):
    agent = build_agent_with_params(
        automata_params,
        "Fetch the docstrings for the load_yaml function in the util file.",
        max_iters=2,
        temperature=TEMPERATURE,
        model=MODEL,
    )
    result = agent.run()
    expected_content = EXPECTED_RESPONSES["test_retrieve_load_yaml_docs"].strip()
    assert calculate_similarity(expected_content, result) > 0.8


@pytest.mark.regression
@pytest.mark.parametrize(
    "automata_params",
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
def test_retrieve_python_writer_docs(automata_params):
    agent = build_agent_with_params(
        automata_params,
        "Fetch the docstrings for the python writer class.",
        max_iters=2,
        temperature=TEMPERATURE,
        model=MODEL,
    )
    result = agent.run()
    expected_content = EXPECTED_RESPONSES["test_retrieve_python_writer_docs"].strip()
    assert calculate_similarity(expected_content, result) > 0.8
