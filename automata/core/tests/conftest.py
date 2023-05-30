import os
import shutil
from functools import wraps

import pytest

from automata.configs.automata_agent_config_utils import AutomataAgentConfigBuilder
from automata.configs.automata_agent_configs import AutomataAgentConfig, AutomataInstructionPayload
from automata.configs.config_enums import AgentConfigName
from automata.core.agent.automata_agent_utils import AutomataAgentFactory
from automata.core.code_indexing.utils import build_repository_overview
from automata.core.utils import calculate_similarity, root_py_path
from automata.tool_management.tool_management_utils import build_llm_toolkits

current_file_dir = os.path.dirname(os.path.realpath(__file__))


@pytest.fixture
def automata_params(request):
    model = request.param.get("model")
    temperature = request.param.get("temperature")
    tool_list = request.param.get("tool_list")

    inputs = {
        "model": model,
        "temperature": temperature,
        "automata_indexer_config": AutomataAgentConfig.load(AgentConfigName.AUTOMATA_INDEXER_PROD),
        "automata_writer_config": AutomataAgentConfig.load(AgentConfigName.AUTOMATA_WRITER_PROD),
    }
    mock_llm_toolkits = build_llm_toolkits(tool_list, **inputs)

    instruction_payload = (
        generate_instruction_payload() if not request.param.get("exclude_overview") else {}
    )
    return instruction_payload, mock_llm_toolkits


def build_agent_with_params(
    automata_params,
    instructions: str,
    config_name: AgentConfigName = AgentConfigName.AUTOMATA_INDEXER_PROD,
    max_iters=2,
    temperature=0.0,
    model="gpt-3.5-turbo",
):
    instruction_payload, mock_llm_toolkits = automata_params

    agent = AutomataAgentFactory.create_agent(
        instructions,
        config=AutomataAgentConfigBuilder.from_name(config_name)
        .with_instruction_payload(instruction_payload)
        .with_llm_toolkits(mock_llm_toolkits)
        .with_verbose(True)
        .with_max_iters(max_iters)
        .with_temperature(temperature)
        .with_model(model)
        .build(),
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


def generate_instruction_payload():
    return AutomataInstructionPayload(overview=build_repository_overview(root_py_path()))


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
