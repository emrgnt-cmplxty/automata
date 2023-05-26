import os

import pytest

from automata.configs.config_enums import ConfigCategory
from automata.core.search.symbol_graph import SymbolGraph
from automata.core.search.symbol_rank.symbol_embedding_map import SymbolEmbeddingMap
from automata.core.search.symbol_rank.symbol_rank import SymbolRankConfig
from automata.core.search.symbol_rank.symbol_similarity import SymbolSimilarity
from automata.core.utils import config_path
from automata.tools.search.symbol_searcher import SymbolSearcher

SEARCHES_TO_HITS = {
    "Symbol": ["Symbol", "SymbolParser", "parse_symbol"],
    "AutomataAgent": [
        "AutomataAgent",
        "AutomataAgentConfig",
        "AutomataAgentConfigBuilder",
        "AutomataCoordinator",
    ],
    "Task": ["AutomataTask", "AutomataTaskRegistry", "Task"],
    "SymbolGraph": ["Symbol", "SymbolSearcher", "SymbolParser"],
    "Github": ["GitHubManager", "AutomataTaskRegistry", "RepositoryManager"],
    "Embedding": ["SymbolEmbedding", "SymbolEmbeddingMap", "EmbeddingsProvider"],
    "cli": ["cli", "initialize_task", "run_pending_task"],
    "coordinator": [
        "AutomataCoordinator",
        "AutomataAgent",
        "AutomataCoordinatorFactory",
        "AutomataTask",
    ],
    "executor": ["TaskExecutor", "AutomataExecuteBehavior", "execute"],
}


def get_top_n_results_desc_name(result, n=0):
    return [ele[0].descriptors[-1].name for ele in result[0:n]]


def check_hits(expected_in_top_hits, found_top_hits):
    for expected_hit in expected_in_top_hits:
        expected_and_found = False
        for found_hit in found_top_hits:
            if expected_hit in found_hit:
                expected_and_found = True
                break
        if not expected_and_found:
            assert (
                False
            ), f"Expected to find {expected_hit} in top hits, but found {found_top_hits}"


@pytest.fixture
def symbol_searcher() -> SymbolSearcher:
    scip_path = os.path.join(config_path(), ConfigCategory.SYMBOLS.value, "index.scip")
    embedding_path = os.path.join(
        config_path(), ConfigCategory.SYMBOLS.value, "symbol_embedding.json"
    )

    # Initialize symbol graph and get subgraph
    symbol_graph = SymbolGraph(scip_path)

    # Load symbol embedding map
    symbol_embedding_map = SymbolEmbeddingMap(
        load_embedding_map=True, embedding_path=embedding_path
    )

    # Initialize symbol similarity
    symbol_similarity = SymbolSimilarity(symbol_embedding_map)

    symbol_searcher = SymbolSearcher(
        symbol_graph, symbol_embedding_map, symbol_similarity, SymbolRankConfig()
    )

    return symbol_searcher


# Searches to run SymbolRank on and the expected hits
SR_SEARCHES_TO_HITS = {
    "Symbol": ["Symbol", "SymbolParser", "parse_symbol"],
    "AutomataAgent": [
        "AutomataAgent",
        "AutomataAgentConfig",
        "AutomataAgentConfigBuilder",
        "AutomataCoordinator",
    ],
    "Task": ["AutomataTask", "AutomataTaskRegistry", "Task"],
    "SymbolGraph": ["Symbol", "SymbolSearcher", "SymbolParser"],
    "Github": ["GitHubManager", "AutomataTaskRegistry", "RepositoryManager"],
    "Embedding": ["SymbolEmbedding", "SymbolEmbeddingMap", "EmbeddingsProvider"],
    "cli": ["cli", "initialize_task", "run_pending_task"],
    "coordinator": [
        "AutomataCoordinator",
        "AutomataAgent",
        "AutomataCoordinatorFactory",
        "AutomataTask",
    ],
    "executor": ["TaskExecutor", "AutomataExecuteBehavior", "execute"],
}


@pytest.mark.regression
def test_symbol_rank_search_on_symbol(symbol_searcher):
    for search in SR_SEARCHES_TO_HITS:
        result = symbol_searcher.symbol_rank_search(search)
        expected_in_top_hits = SR_SEARCHES_TO_HITS[search]
        found_top_hits = get_top_n_results_desc_name(result, 10)
        check_hits(expected_in_top_hits, found_top_hits)


REF_CALLS_TO_HITS = {
    "AutomataAgentConfig#": [
        "automata_agent.py",
        "automata_agent_config_utils.py",
        "automata_agent_utils.py",
    ],
    "AutomataAgent#": [
        "automata_agent.py",
        "automata_coordinator.py",
        "automata_agent_utils.py",
        "automata_manager.py",
        "automata_manager_factory.py",
    ],
    "SymbolGraph#": ["symbol_graph.py", "symbol_searcher.py"],
    "AutomataTask#": ["automata_task_executor.py", "automata_task_registry.py", "task.py"],
    "AutomataCoordinator#": ["automata_manager.py"],
}


@pytest.mark.regression
def test_symbol_references(symbol_searcher):
    for search in REF_CALLS_TO_HITS:
        found_symbol = False
        for symbol in symbol_searcher.embedding_dict.keys():
            if symbol.uri.endswith(search):
                found_symbol = True
                expected_in_references = REF_CALLS_TO_HITS[search]
                found_in_references = list(symbol_searcher.symbol_references(symbol.uri).keys())
                check_hits(expected_in_references, found_in_references)
                break
        assert (
            found_symbol
        ), f"Expected class name corresponding to {search} to be found in symbol graph, but it was not found"


# EXACT_CALLS_TO_HITS = {
#     "AutomataAgent": ["eval.py", "task.py", "automata_coordinator", "automata_agent", "automata_manager", "automata_agent_configs"],
#     "SymbolRank": ["symbol_searcher.py", "symbol_rank.py"],
#     # "AutomataAgent#": ["automata_agent.py", "automata_coordinator.py", "automata_agent_utils.py", "automata_manager.py", "automata_manager_factory.py"],
#     # "SymbolGraph#": ["symbol_graph.py", "symbol_searcher.py"],
#     # "AutomataTask#": ["automata_task_executor.py", "automata_task_registry.py", "task.py"],
#     # "AutomataCoordinator#": ["automata_manager.py"],
# }
# @pytest.mark.regression
# def test_exact_search(symbol_searcher):
#     for search in EXACT_CALLS_TO_HITS:
#         expected_in_exact_hits = EXACT_CALLS_TO_HITS[search]
#         print("searching on search", search)
#         found_in_exact_hits = list(symbol_searcher.exact_search(search).keys())
#         print("found_in_exact_hits = ", found_in_exact_hits)
#         check_hits(expected_in_exact_hits, found_in_exact_hits)

# # assert found_symbol, f"Expected class name corresponding to {search} to be found in symbol graph, but it was not found"
