import os

import pytest

from automata.config.base import ConfigCategory
from automata.core.experimental.search.rank import SymbolRankConfig
from automata.core.experimental.search.symbol_search import SymbolSearch
from automata.core.llm.providers.openai import OpenAIEmbeddingProvider
from automata.core.memory_store.symbol_code_embedding import SymbolCodeEmbeddingHandler
from automata.core.symbol.graph import SymbolGraph
from automata.core.symbol_embedding.base import JSONSymbolEmbeddingVectorDatabase
from automata.core.symbol_embedding.builders import SymbolCodeEmbeddingBuilder
from automata.core.embedding.base import EmbeddingSimilarityCalculator
from automata.core.utils import get_config_fpath


@pytest.fixture
def symbol_graph_static_test() -> SymbolGraph:
    """
    Creates a non-mock SymbolGraph object for testing the graph

    Note:
        Subgraphs produced from this graph can change as the underlying code evolves in automata/
        This is because the graph is loading up indices that point to the actual code.
    """
    # assuming the path to a valid index protobuf file, you should replace it with your own file path
    file_dir = os.path.dirname(os.path.abspath(__file__))
    index_path = os.path.join(file_dir, "..", "index.scip")
    return SymbolGraph(index_path)


@pytest.fixture
def symbol_search_live() -> SymbolSearch:
    """
    Creates a non-mock SymbolGraph object to be used for testing the search

    """
    scip_path = os.path.join(get_config_fpath(), ConfigCategory.SYMBOL.value, "index.scip")

    code_embedding_fpath = os.path.join(
        get_config_fpath(), ConfigCategory.SYMBOL.value, "symbol_code_embedding.json"
    )
    embedding_provider = OpenAIEmbeddingProvider()

    symbol_graph = SymbolGraph(scip_path)

    embedding_similarity_calculator = EmbeddingSimilarityCalculator(embedding_provider)

    symbol_rank_config = SymbolRankConfig()

    return SymbolSearch(symbol_graph, symbol_rank_config, embedding_similarity_calculator)
