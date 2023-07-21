import pytest

from automata.singletons.py_module_loader import py_module_loader
from tests.utils.factories import symbol_search_live  # noqa


def get_top_n_results_desc_name(result, n=0):
    return [ele[0].descriptors[-1].name for ele in result[:n]]


def check_hits(expected_in_top_hits, found_top_hits):
    for expected_hit in expected_in_top_hits:
        expected_and_found = any(
            expected_hit in found_hit for found_hit in found_top_hits
        )
        if not expected_and_found:
            assert (
                False
            ), f"Expected to find {expected_hit} in top hits, but found {found_top_hits}"


@pytest.mark.regression
@pytest.mark.parametrize(
    "search, expected_in_top_hits",
    [
        ("SymbolGraph", ["Symbol", "SymbolGraph", "GraphBuilder"]),
        (
            "SymbolSearch",
            ["Symbol", "SymbolSearchToolkitBuilder", "SymbolSearch"],
        ),
        (
            "Embedding",
            [
                "SymbolEmbeddingHandler",
                "EmbeddingBuilder",
                "SymbolDocEmbeddingHandler",
                "SymbolEmbedding",
                "Embedding",
            ],
        ),
        (
            "OpenAI",
            [
                "OpenAIAutomataAgent",
                "OpenAIConversation",
                "OpenAIChatCompletionProvider",
            ],
        ),
        (
            "LLM",
            [
                "LLMProvider",
                "LLMConversation",
                "LLMCompletionResult",
            ],
        ),
        ("Symbol", ["Symbol", "SymbolGraph"]),
    ],
)
def test_symbol_rank_search_on_symbol(
    symbol_search_live, search, expected_in_top_hits  # noqa : F811
):
    py_module_loader.reset()
    py_module_loader.initialized = (
        False  # This is a hacky way to avoid any risk of initialization error
    )

    py_module_loader.initialize()
    results = symbol_search_live.get_symbol_rank_results(search)
    filtered_results = [
        result for result in results if ".tests." not in result[0].full_dotpath
    ]
    found_top_hits = get_top_n_results_desc_name(filtered_results, 10)
    check_hits(expected_in_top_hits, found_top_hits)


EXACT_CALLS_TO_HITS = {
    "OpenAIAutomataAgent": [
        "automata.cli.scripts.run_agent",
        "automata.agent.providers",
        "automata.singletons.toolkit_registries",
    ],
    "SymbolRank": [
        "automata.experimental.search.symbol_search",
        "automata.experimental.search.rank",
    ],
}


@pytest.mark.regression
@pytest.mark.parametrize(
    "search, expected_in_hits",
    [
        (
            "OpenAIAutomataAgent",
            [
                "automata.cli.scripts.run_agent",
                "automata.agent.providers",
                "automata.singletons.toolkit_registries",
            ],
        ),
        (
            "SymbolRank",
            [
                "automata.experimental.search.symbol_search",
                "automata.experimental.search.rank",
            ],
        ),
    ],
)
def test_exact_search(
    symbol_search_live, search, expected_in_hits  # noqa : F811
):
    py_module_loader.initialized = (
        False  # This is a hacky way to avoid any risk of initialization error
    )
    py_module_loader.initialize()
    expected_in_exact_hits = EXACT_CALLS_TO_HITS[search]
    found_in_exact_hits = list(symbol_search_live.exact_search(search).keys())
    check_hits(expected_in_exact_hits, found_in_exact_hits)


@pytest.mark.regression
@pytest.mark.parametrize(
    "search, expected_in_source",
    [
        (
            "OpenAIAutomataAgent#",
            [
                "class OpenAIAutomataAgent(Agent):\n",
                "def run",
            ],
        ),
    ],
)
def test_source_code_retrieval(
    symbol_search_live, search, expected_in_source  # noqa : F811
):
    py_module_loader.initialized = (
        False  # This is a hacky way to avoid any risk of initialization error
    )
    py_module_loader.initialize()
    symbols = symbol_search_live.symbol_graph.get_sorted_supported_symbols()

    symbol = [
        symbol
        for symbol in symbols
        if search[:-1] == symbol.descriptors[-1].name
    ][0]
    found_source_code = symbol_search_live.retrieve_source_code_by_symbol(
        symbol.uri
    )
    for source_hit in expected_in_source:
        assert (
            source_hit in found_source_code
        ), f"Expected to find {source_hit} in source code, but it was not found"
    py_module_loader.initialized = False
    py_module_loader.project_name = None
    py_module_loader.root_fpath = None
