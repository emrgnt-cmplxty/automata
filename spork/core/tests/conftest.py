# conftest.py
import os
import shutil
from functools import wraps

import pytest

from spork.configs.agent_configs import AgentVersion
from spork.core import load_llm_toolkits
from spork.core.agents.mr_meeseeks_agent import MrMeeseeksAgent
from spork.core.utils import root_py_path
from spork.tools.python_tools.python_indexer import PythonIndexer

current_file_dir = os.path.dirname(os.path.realpath(__file__))


def build_agent_with_params(
    mr_meeseeks_params,
    instructions: str,
    version: AgentVersion = AgentVersion.MEESEEKS_RETRIEVER_V2,
    max_iters=2,
    temperature=0.0,
    model="gpt-3.5-turbo",
):
    initial_payload, mock_llm_toolkits = mr_meeseeks_params
    agent = MrMeeseeksAgent(
        initial_payload=initial_payload,
        instructions=instructions,
        llm_toolkits=mock_llm_toolkits,
        verbose=True,
        max_iters=max_iters,
        version=version,
        temperature=temperature,
        model=model,
    )
    return agent


def cleanup_and_check(expected_content: str, file_name: str) -> None:
    # Check if the file has been created
    file_path = os.path.join(current_file_dir, "sample_code", file_name)
    assert os.path.isfile(file_path), "File does not exist"

    # Check if the content of the file is as expected
    with open(file_path, "r") as file:
        content = file.read()

    # Delete the whole "sample_code" directory after the test
    sample_code_dir = os.path.join(current_file_dir, "sample_code")
    shutil.rmtree(sample_code_dir)

    assert (
        content.strip().split("\n")[0:5] == expected_content.strip().split("\n")[0:5]
    )  # Check the first 5 lines


def generate_initial_payload():
    return {
        "overview": PythonIndexer(root_py_path()).get_overview(),
    }


@pytest.fixture
def mr_meeseeks_params(request):
    model = request.param.get("model")
    temperature = request.param.get("temperature")
    tool_list = request.param.get("tool_list")

    inputs = {"model": model, "temperature": temperature}
    mock_llm_toolkits = load_llm_toolkits(tool_list, **inputs)

    initial_payload = generate_initial_payload()
    return initial_payload, mock_llm_toolkits


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
