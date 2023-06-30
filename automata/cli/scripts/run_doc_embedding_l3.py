import logging
import os

from tqdm import tqdm

from automata.config.base import ConfigCategory
from automata.core.base.database.vector import JSONEmbeddingVectorDatabase
from automata.core.coding.py.module_loader import py_module_loader
from automata.core.context.py.retriever import (
    PyContextRetriever,
    PyContextRetrieverConfig,
)
from automata.core.embedding.code_embedding import (
    SymbolCodeEmbeddingBuilder,
    SymbolCodeEmbeddingHandler,
)
from automata.core.embedding.doc_embedding import (
    SymbolDocEmbeddingBuilder,
    SymbolDocEmbeddingHandler,
)
from automata.core.embedding.symbol_similarity import SymbolSimilarityCalculator
from automata.core.llm.providers.openai import (
    OpenAIChatCompletionProvider,
    OpenAIEmbeddingProvider,
)
from automata.core.symbol.base import SymbolDescriptor
from automata.core.symbol.graph import SymbolGraph
from automata.core.symbol.search.rank import SymbolRankConfig
from automata.core.symbol.search.symbol_search import SymbolSearch
from automata.core.symbol.symbol_utils import get_rankable_symbols
from automata.core.utils import get_config_fpath

logger = logging.getLogger(__name__)


def main(*args, **kwargs) -> str:
    """
    Update the symbol code embedding based on the specified SCIP index file.
    """
    py_module_loader.initialize()

    logger.info("Running....")
    scip_path = os.path.join(
        get_config_fpath(), ConfigCategory.SYMBOL.value, kwargs.get("index-file", "index.scip")
    )

    code_embedding_fpath = os.path.join(
        get_config_fpath(), ConfigCategory.SYMBOL.value, "symbol_code_embedding.json"
    )
    code_embedding_db = JSONEmbeddingVectorDatabase(code_embedding_fpath)
    embedding_provider = OpenAIEmbeddingProvider()
    embedding_builder = SymbolCodeEmbeddingBuilder(embedding_provider)
    code_embedding_handler = SymbolCodeEmbeddingHandler(code_embedding_db, embedding_builder)

    # TODO - Add option for the user to modify l2 & l3  embedding path in commands.py
    embedding_path_l2 = os.path.join(
        get_config_fpath(),
        ConfigCategory.SYMBOL.value,
        kwargs.get("symbol_doc_embedding_l2_fpath", "symbol_doc_embedding_l2.json"),
    )
    embedding_db_l2 = JSONEmbeddingVectorDatabase(embedding_path_l2)

    embedding_path_l3 = os.path.join(
        get_config_fpath(),
        ConfigCategory.SYMBOL.value,
        kwargs.get("symbol_doc_embedding_l3_fpath", "symbol_doc_embedding_l3.json"),
    )

    symbol_graph = SymbolGraph(scip_path)

    embedding_db_l3 = JSONEmbeddingVectorDatabase(embedding_path_l3)

    symbol_code_similarity = SymbolSimilarityCalculator(code_embedding_handler, embedding_provider)

    symbol_rank_config = SymbolRankConfig()
    symbol_graph_subgraph = symbol_graph.get_rankable_symbol_dependency_subgraph()
    symbol_search = SymbolSearch(
        symbol_graph, symbol_code_similarity, symbol_rank_config, symbol_graph_subgraph
    )
    py_context_retriever = PyContextRetriever(
        symbol_graph, PyContextRetrieverConfig(), embedding_db_l2
    )
    chat_provider = OpenAIChatCompletionProvider()

    symbol_doc_embedding_builder = SymbolDocEmbeddingBuilder(
        embedding_provider, chat_provider, symbol_search, py_context_retriever
    )

    embedding_handler = SymbolDocEmbeddingHandler(embedding_db_l3, symbol_doc_embedding_builder)

    all_defined_symbols = symbol_graph.get_all_available_symbols()
    filtered_symbols = sorted(get_rankable_symbols(all_defined_symbols), key=lambda x: x.dotpath)
    for symbol in tqdm(filtered_symbols):
        if symbol.symbol_kind_by_suffix() == SymbolDescriptor.PyKind.Class:
            try:
                embedding_handler.process_embedding(symbol)
                embedding_db_l3.save()
            except Exception as e:
                logger.error(f"Error updating embedding for {symbol.dotpath}: {e}")

    for symbol in embedding_handler.get_all_supported_symbols():
        if symbol not in filtered_symbols:
            logger.info(f"Discarding stale symbol {symbol}...")
            embedding_db_l3.discard(symbol.dotpath)
    embedding_db_l3.save()

    logger.info("Complete.")
    return "Success"
