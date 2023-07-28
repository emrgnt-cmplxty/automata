# TODO - Agent tests should depend on actions for verification, not specific output
import logging
import random

import pytest

from automata.core.run_handlers import run_setup, run_with_agent
from automata.core.utils import calculate_similarity
from automata.llm import OpenAIEmbeddingProvider
from automata.singletons.py_module_loader import py_module_loader

logger = logging.getLogger(__name__)

EMBEDDING_PROVIDER = OpenAIEmbeddingProvider()
CORE_PARAMS = "instructions, agent_config, toolkit_list, model, max_iterations"


@pytest.mark.regression
@pytest.mark.parametrize(
    f"{CORE_PARAMS}, allowable_results",
    [
        # A simple 'hello-world' style instruction
        (
            "This is a dummy instruction, return True.",
            "automata-main",
            [],  # no tool necessary, default agent has a stop execution fn.
            "gpt-3.5-turbo-16k",
            1,
            ["True"],
        ),
    ],
)
def test_basic_agent_execution(
    instructions,
    agent_config,
    toolkit_list,
    model,
    max_iterations,
    allowable_results,
):
    """Test that the agent can execute a simple instruction."""

    tools, agent_config_name = run_setup(agent_config, toolkit_list)
    agent = run_with_agent(
        instructions, agent_config_name, tools, model, max_iterations
    )
    result = agent.get_result()

    if result not in allowable_results:
        raise ValueError(
            f"Allowable results={allowable_results}, found result={result}"
        )


@pytest.mark.regression
@pytest.mark.parametrize(
    f"{CORE_PARAMS}, expected_result, min_similarity",
    [
        # Extracting source code directly from a module
        (
            "Fetch the source code for VectorDatabaseProvider.",
            "automata-main",
            ["py-reader"],
            "gpt-4",
            2,
            "class VectorDatabaseProvider(abc.ABC, Generic[K, V]):\n\n    @abc.abstractmethod\n    def __len__(self) -> int:\n        pass\n\n    @abc.abstractmethod\n    def save(self) -> None:\n        pass\n\n    @abc.abstractmethod\n    def load(self) -> None:\n        pass\n\n    @abc.abstractmethod\n    def clear(self) -> None:\n        pass\n\n    @abc.abstractmethod\n    def get_ordered_keys(self) -> List[K]:\n        pass\n\n    @abc.abstractmethod\n    def get_all_ordered_embeddings(self) -> List[V]:\n        pass\n\n    @abc.abstractmethod\n    def add(self, entry: V) -> None:\n        pass\n\n    @abc.abstractmethod\n    def batch_add(self, entries: V) -> None:\n        pass\n\n    @abc.abstractmethod\n    def update_entry(self, entry: V) -> None:\n        pass\n\n    @abc.abstractmethod\n    def batch_update(self, entries: List[V]) -> None:\n        pass\n\n    @abc.abstractmethod\n    def entry_to_key(self, entry: V) -> K:\n        pass\n\n    @abc.abstractmethod\n    def contains(self, key: K) -> bool:\n        pass\n\n    @abc.abstractmethod\n    def get(self, key: K) -> V:\n        pass\n\n    @abc.abstractmethod\n    def batch_get(self, keys: List[K]) -> List[V]:\n        pass\n\n    @abc.abstractmethod\n    def discard(self, key: K) -> None:\n        pass\n\n    @abc.abstractmethod\n    def batch_discard(self, keys: List[K]) -> None:\n        pass",
            0.85,
        ),
        # A simple context search for `SymbolSearch`
        (
            "What class should we instantiate to search the codebase for relevant symbols? Please return just the class name.",
            "automata-main",
            ["advanced-context-oracle"],
            "gpt-4",
            2,
            "SymbolSearch",
            0.85,
        ),
    ],
)
def test_agent_py_reader_and_context(
    instructions,
    agent_config,
    toolkit_list,
    model,
    max_iterations,
    expected_result,
    min_similarity,
):
    """Tests the reader and context functionality of the agent."""
    tools, agent_config_name = run_setup(agent_config, toolkit_list)
    agent = run_with_agent(
        instructions, agent_config_name, tools, model, max_iterations
    )
    result = agent.get_result()

    similarity = calculate_similarity(
        result, expected_result, EMBEDDING_PROVIDER
    )
    if similarity < min_similarity:
        raise ValueError(
            f"Found a similarity of {similarity} required {min_similarity}."
        )


random_suffix = random.randint(0, 1000000)


@pytest.mark.regression
@pytest.mark.parametrize(
    f"{CORE_PARAMS}, expected_output_module",
    [
        # Extracting source code directly from a module
        (
            f"Create a new module with a hello world function at automata.test_module_{random_suffix}",
            "automata-main",
            ["py-writer"],
            "gpt-4",
            2,
            f"automata.test_module_{random_suffix}",
        ),
    ],
)
def test_agent_py_writer(
    instructions,
    agent_config,
    toolkit_list,
    model,
    max_iterations,
    expected_output_module,
):
    """Tests the writer functionality of the agent."""

    tools, agent_config_name = run_setup(agent_config, toolkit_list)
    run_with_agent(
        instructions, agent_config_name, tools, model, max_iterations
    )

    if _ := py_module_loader.fetch_ast_module(expected_output_module):
        py_module_loader.delete_module(expected_output_module)
    else:
        raise ValueError("Failed to create expected output module")
