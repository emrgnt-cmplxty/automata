import pytest

from automata.core.singletons.py_module_loader import py_module_loader
from automata.tests.utils.factories import symbol_search_live  # noqa


def get_top_n_results_desc_name(result, n=0):
    return [ele[0].descriptors[-1].name for ele in result[0:n]]


def check_hits(expected_in_top_hits, found_top_hits):
    for expected_hit in expected_in_top_hits:
        expected_and_found = any(expected_hit in found_hit for found_hit in found_top_hits)
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
    "SymbolGraph": ["SymbolGraph", "Symbol", "GraphBuilder", "SymbolSearch"],
    "Embedding": [
        "SymbolEmbedding",
        "SymbolDocEmbedding",
        "SymbolCodeEmbedding",
        "EmbeddingVectorProvider",
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
        "JSONSymbolEmbeddingVectorDatabase",
        "AgentConversationDatabase",
        "SymbolDatabaseProvider",
        "VectorDatabaseProvider",
    ],
    "python": [
        "PyWriter",
        "PyReader",
        "PyWriterTool",
        "PyReaderTool",
        "PyContextRetriever",
        "PyDocWriter",
    ],
    "code": ["PyWriter", "PyReader", "SymbolCodeEmbedding"],
}


@pytest.mark.regression
@pytest.mark.parametrize(
    "search, expected_in_top_hits",
    [
        ("PyReader", ["PyReader", "PyWriter", "create_py_reader"]),
        ("PyWriter", ["PyWriter", "PyReader", "create_py_writer"]),
        ("SymbolGraph", ["Symbol", "SymbolGraph", "GraphBuilder"]),
        ("SymbolSearch", ["Symbol", "SymbolSearchToolkitBuilder", "SymbolSearch"]),
        ("Embedding", ["SymbolCodeEmbedding", "SymbolDocEmbedding"]),
        (
            "OpenAI",
            [
                "OpenAIAutomataAgent",
                "OpenAIConversation",
                "OpenAIEmbeddingProvider",
                "OpenAIChatCompletionProvider",
            ],
        ),
        ("LLM", ["LLMProvider", "LLMChatMessage", "LLMConversation", "LLMCompletionResult"]),
        ("Symbol", ["Symbol", "SymbolGraph", "JSONSymbolEmbeddingVectorDatabase"]),
    ],
)
def test_symbol_rank_search_on_symbol(
    symbol_search_live, search, expected_in_top_hits  # noqa : F811
):
    py_module_loader.initialize()
    results = symbol_search_live.symbol_rank_search(search)
    filtered_results = [result for result in results if ".tests." not in result[0].dotpath]
    found_top_hits = get_top_n_results_desc_name(filtered_results, 10)
    check_hits(expected_in_top_hits, found_top_hits)
    py_module_loader.initialized = False


# FIXME - Revive tests ASAP
# EXACT_CALLS_TO_HITS = {
#     "OpenAIAutomataAgent": [
#         "automata.core.cli.scripts.run_agent",
#         "automata.core.agent.providers",
#     ],
#     # "SymbolRank": [
#     #     "automata.core.experimental.search.symbol_search",
#     #     "automata.core.experimental.search.rank",
#     #     "automata.core.toolss.symbol_search",
#     #     "automata.core.toolss.factory",
#     # ],
# }


# @pytest.mark.regression
# def test_exact_search(symbol_search_live):  # noqa : F811
#     py_module_loader.initialize()

#     print("py_module_loader.items() = ", py_module_loader.items())
#     for search in EXACT_CALLS_TO_HITS:
#         expected_in_exact_hits = EXACT_CALLS_TO_HITS[search]
#         found_in_exact_hits = list(symbol_search_live.exact_search(search).keys())
#         check_hits(expected_in_exact_hits, found_in_exact_hits)
#     py_module_loader.initialized = False


# # SOURCE_CODE_HITS = {
# #     "AutomataAgent#": ["class AutomataAgent", "def run"],
# # }


# # @pytest.mark.regression
# # def test_source_code_retrieval(symbol_search_live):  # noqa : F811
# #     symbols = symbol_search_live.symbol_graph.get_sorted_supported_symbols()

# #     for search in SOURCE_CODE_HITS:
# #         symbol = [symbol for symbol in symbols if search[:-1] == symbol.descriptors[-1].name][0]
# #         found_source_code = symbol_search_live.retrieve_source_code_by_symbol(symbol.uri)
# #         expected_in_source = SOURCE_CODE_HITS[search]
# #         for source_hit in expected_in_source:
# #             assert (
# #                 source_hit in found_source_code
# #             ), f"Expected to find {source_hit} in source code, but it was not found"
