import os

import pytest

from automata.config.base import ConfigCategory
from automata.core.base.database.vector import JSONVectorDatabase
from automata.core.embedding.code_embedding import SymbolCodeEmbeddingHandler
from automata.core.embedding.symbol_similarity import SymbolSimilarity
from automata.core.llm.providers.openai import OpenAIEmbeddingProvider
from automata.core.symbol.graph import SymbolGraph
from automata.core.symbol.search.rank import SymbolRankConfig
from automata.core.symbol.search.symbol_search import SymbolSearch
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
    graph = SymbolGraph(index_path)
    return graph


@pytest.fixture
def symbol_search_live() -> SymbolSearch:
    """
    Creates a non-mock SymbolGraph object to be used for testing the search

    """
    scip_path = os.path.join(get_config_fpath(), ConfigCategory.SYMBOL.value, "index.scip")

    code_embedding_fpath = os.path.join(
        get_config_fpath(), ConfigCategory.SYMBOL.value, "symbol_code_embedding.json"
    )
    code_embedding_db = JSONVectorDatabase(code_embedding_fpath)
    code_embedding_handler = SymbolCodeEmbeddingHandler(
        code_embedding_db, OpenAIEmbeddingProvider()
    )

    symbol_graph = SymbolGraph(scip_path)

    symbol_code_similarity = SymbolSimilarity(code_embedding_handler)

    symbol_rank_config = SymbolRankConfig()
    symbol_graph_subgraph = symbol_graph.get_rankable_symbol_subgraph()
    symbol_search = SymbolSearch(
        symbol_graph, symbol_code_similarity, symbol_rank_config, symbol_graph_subgraph
    )

    return symbol_search
