import pytest

from automata.tests.utils.factories import symbol_search_live  # noqa


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


# Searches to run SymbolRank on and the expected hits
SR_SEARCHES_TO_HITS = {
    "Symbol": [
        "Symbol",
        "SymbolEmbedding",
        "SymbolReference",
        "SymbolDocEmbedding",
        "SymbolCodeEmbedding",
    ],
    "AutomataAgent": [
        "AutomataAgent",
        "AutomataAgentConfig",
        "AutomataCoordinator",
        "AutomataAgentConfigBuilder",
        "AutomataInstance",
    ],
    "SymbolGraph": ["SymbolGraph", "Symbol", "SubGraph", "GraphBuilder", "SymbolSearch"],
    "Embedding": [
        "SymbolEmbedding",
        "SymbolDocEmbedding",
        "SymbolCodeEmbedding",
        "EmbeddingProvider",
        "SymbolCodeEmbeddingHandler",
        "SymbolDocEmbeddingHandler",
    ],
    "cli": [
        "cli",
        "run_doc_embedding_l2",
        "run_doc_embedding_l3",
        "run_code_embedding",
        "run_agent",
    ],
    "database": [
        "JSONVectorDatabase",
        "AutomataAgentDatabase",
        "SymbolDatabaseProvider",
        "VectorDatabaseProvider",
    ],
    "python": [
        "PyCodeWriter",
        "PyCodeRetriever",
        "PyCodeWriterTool",
        "PyCodeRetrieverTool",
        "PyContextRetriever",
        "PyDocWriter",
    ],
    "code": ["PyCodeWriter", "PyCodeRetriever", "SymbolCodeEmbedding"],
}


@pytest.mark.regression
def test_symbol_rank_search_on_symbol(symbol_search_live):  # noqa
    for search in SR_SEARCHES_TO_HITS:
        results = symbol_search_live.symbol_rank_search(search)
        filtered_results = [result for result in results if ".tests." not in result[0].dotpath]
        expected_in_top_hits = SR_SEARCHES_TO_HITS[search]
        found_top_hits = get_top_n_results_desc_name(filtered_results, 10)
        check_hits(expected_in_top_hits, found_top_hits)
