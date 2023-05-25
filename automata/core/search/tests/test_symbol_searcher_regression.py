import os

import pytest

from automata.configs.config_enums import ConfigCategory
from automata.core.search.symbol_graph import SymbolGraph
from automata.core.search.symbol_rank.symbol_embedding_map import SymbolEmbeddingMap
from automata.core.search.symbol_rank.symbol_rank import SymbolRankConfig
from automata.core.search.symbol_rank.symbol_similarity import SymbolSimilarity
from automata.core.search.symbol_searcher import SymbolSearcher
from automata.core.utils import config_path

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
    for hit in expected_in_top_hits:
        assert hit in found_top_hits, f"Expected {hit} in top hits, but found {found_top_hits}"


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


@pytest.mark.regression
def test_symbol_rank_search_on_symbol(symbol_searcher):
    for search in SEARCHES_TO_HITS:
        result = symbol_searcher.symbol_rank_search(search)
        expected_in_top_hits = SEARCHES_TO_HITS[search]
        found_top_hits = get_top_n_results_desc_name(result, 10)
        check_hits(expected_in_top_hits, found_top_hits)
