# conftest.py
import os
import shutil
from functools import wraps

import pytest

from automata.configs.agent_configs.config_type import AutomataAgentConfig, AutomataConfigVersion
from automata.core.agents.automata_agent_builder import AutomataAgentBuilder
from automata.core.utils import calculate_similarity, root_py_path
from automata.tool_management.tool_management_utils import build_llm_toolkits
from automata.tools.python_tools.python_indexer import PythonIndexer

current_file_dir = os.path.dirname(os.path.realpath(__file__))


@pytest.fixture
def automata_params(request):
    model = request.param.get("model")
    temperature = request.param.get("temperature")
    tool_list = request.param.get("tool_list")

    inputs = {
        "model": model,
        "temperature": temperature,
        "automata_indexer_config": AutomataAgentConfig.load(
            AutomataConfigVersion.AUTOMATA_INDEXER_PROD
        ),
        "automata_writer_config": AutomataAgentConfig.load(
            AutomataConfigVersion.AUTOMATA_WRITER_PROD
        ),
    }
    mock_llm_toolkits = build_llm_toolkits(tool_list, **inputs)

    initial_payload = (
        generate_initial_payload() if not request.param.get("exclude_overview") else {}
    )
    return initial_payload, mock_llm_toolkits


def build_agent_with_params(
    automata_params,
    instructions: str,
    config_version: AutomataConfigVersion = AutomataConfigVersion.AUTOMATA_INDEXER_PROD,
    max_iters=2,
    temperature=0.0,
    model="gpt-3.5-turbo",
):
    initial_payload, mock_llm_toolkits = automata_params

    agent_config = AutomataAgentConfig.load(config_version)

    agent = (
        AutomataAgentBuilder(agent_config)
        .with_initial_payload(initial_payload)
        .with_instructions(instructions)
        .with_llm_toolkits(mock_llm_toolkits)
        .with_verbose(True)
        .with_max_iters(max_iters)
        .with_temperature(temperature)
        .with_model(model)
        .build()
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

    similarity_score = calculate_similarity(content, expected_content)
    assert similarity_score > 0.85  # Check the similarity score


def generate_initial_payload():
    return {
        "overview": PythonIndexer(root_py_path()).get_overview(),
    }


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
