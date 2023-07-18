# TODO - Agent tests should depend on actions for verification, not specific output
import ast
import logging

import pytest

from automata.core.utils import calculate_similarity
from automata.llm import OpenAIEmbeddingProvider
from automata.singletons.py_module_loader import py_module_loader
from tests.utils.regression_utils import run_agent_and_get_result

logger = logging.getLogger(__name__)

EMBEDDING_PROVIDER = OpenAIEmbeddingProvider()


@pytest.mark.regression
@pytest.mark.parametrize(
    "instructions, toolkit_list, model, agent_config_name, max_iterations, allowable_results",
    [
        # A simple 'hello-world' style instruction
        (
            "This is a dummy instruction, return True.",
            [],  # no tool necessary, default agent has a stop execution fn.
            "gpt-3.5-turbo-16k",
            "automata-main",
            1,
            ["True"],
        ),
    ],
)
def test_basic_agent_execution(
    instructions,
    toolkit_list,
    model,
    agent_config_name,
    max_iterations,
    allowable_results,
):
    result = run_agent_and_get_result(
        instructions, toolkit_list, model, agent_config_name, max_iterations
    )
    if result not in allowable_results:
        raise ValueError(
            f"Allowable results={allowable_results}, found result={result}"
        )


@pytest.mark.regression
@pytest.mark.parametrize(
    "instructions, toolkit_list, model, agent_config_name, max_iterations, expected_result, min_similarity",
    [
        # Extracting source code directly from a module
        (
            "Fetch the source code for VectorDatabaseProvider.",
            ["py-reader"],
            "gpt-4",
            "automata-main",
            2,
            "class VectorDatabaseProvider(abc.ABC, Generic[K, V]):\n\n    @abc.abstractmethod\n    def __len__(self) -> int:\n        pass\n\n    @abc.abstractmethod\n    def save(self) -> None:\n        pass\n\n    @abc.abstractmethod\n    def load(self) -> None:\n        pass\n\n    @abc.abstractmethod\n    def clear(self) -> None:\n        pass\n\n    @abc.abstractmethod\n    def get_ordered_keys(self) -> List[K]:\n        pass\n\n    @abc.abstractmethod\n    def get_ordered_embeddings(self) -> List[V]:\n        pass\n\n    @abc.abstractmethod\n    def add(self, entry: V) -> None:\n        pass\n\n    @abc.abstractmethod\n    def batch_add(self, entries: V) -> None:\n        pass\n\n    @abc.abstractmethod\n    def update_entry(self, entry: V) -> None:\n        pass\n\n    @abc.abstractmethod\n    def batch_update(self, entries: List[V]) -> None:\n        pass\n\n    @abc.abstractmethod\n    def entry_to_key(self, entry: V) -> K:\n        pass\n\n    @abc.abstractmethod\n    def contains(self, key: K) -> bool:\n        pass\n\n    @abc.abstractmethod\n    def get(self, key: K) -> V:\n        pass\n\n    @abc.abstractmethod\n    def batch_get(self, keys: List[K]) -> List[V]:\n        pass\n\n    @abc.abstractmethod\n    def discard(self, key: K) -> None:\n        pass\n\n    @abc.abstractmethod\n    def batch_discard(self, keys: List[K]) -> None:\n        pass",
            0.95,
        ),
        # A simple context search for `SymbolSearch`
        (
            "What class should we instantiate to search the codebase for relevant symbols? Please return just the class name.",
            ["context-oracle"],
            "gpt-4",
            "automata-main",
            2,
            "SymbolSearch",
            0.95,
        ),
    ],
)
def test_agent_py_reader_and_context(
    instructions,
    toolkit_list,
    model,
    agent_config_name,
    max_iterations,
    expected_result,
    min_similarity,
):
    result = run_agent_and_get_result(
        instructions, toolkit_list, model, agent_config_name, max_iterations
    )

    similarity = calculate_similarity(
        result, expected_result, EMBEDDING_PROVIDER
    )
    if similarity < min_similarity:
        raise ValueError(
            f"Found a similarity of {similarity} required {min_similarity}."
        )


@pytest.mark.regression
@pytest.mark.parametrize(
    "instructions, toolkit_list, model, agent_config_name, max_iterations, expected_output_module, expected_result, min_similarity",
    [
        # Extracting source code directly from a module
        (
            "Create a new module with a hello world function at automata.test_module",
            ["py-writer"],
            "gpt-4",
            "automata-main",
            2,
            "automata.test_output.test_module",
            "def hello_world():\n    print('Hello, world!')",
            0.9,
        ),
    ],
)
def test_agent_py_writer(
    instructions,
    toolkit_list,
    model,
    agent_config_name,
    max_iterations,
    expected_output_module,
    expected_result,
    min_similarity,
):
    _ = run_agent_and_get_result(
        instructions, toolkit_list, model, agent_config_name, max_iterations
    )

    module = py_module_loader.fetch_ast_module(expected_output_module)
    if not module:
        raise ValueError("Failed to crate expected output modle")
    result = ast.unparse(module)
    py_module_loader.delete_module(expected_output_module)

    similarity = calculate_similarity(
        result, expected_result, EMBEDDING_PROVIDER
    )
    if similarity < min_similarity:
        raise ValueError(
            f"Found a similarity of {similarity} required {min_similarity}."
        )
