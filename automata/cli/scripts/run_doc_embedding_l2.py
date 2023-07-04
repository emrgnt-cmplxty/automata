import logging
import os

from tqdm import tqdm

from automata.config.base import ConfigCategory
from automata.core.experimental.search.rank import SymbolRankConfig
from automata.core.experimental.search.symbol_search import SymbolSearch
from automata.core.llm.providers.openai import (
    OpenAIChatCompletionProvider,
    OpenAIEmbeddingProvider,
)
from automata.core.memory_store.symbol_code_embedding import SymbolCodeEmbeddingHandler
from automata.core.memory_store.symbol_doc_embedding import SymbolDocEmbeddingHandler
from automata.core.retrievers.py.context import (
    PyContextRetriever,
    PyContextRetrieverConfig,
)
from automata.core.singletons.py_module_loader import py_module_loader
from automata.core.symbol.base import SymbolDescriptor
from automata.core.symbol.graph import SymbolGraph
from automata.core.symbol.symbol_utils import get_rankable_symbols
from automata.core.symbol_embedding.base import JSONSymbolEmbeddingVectorDatabase
from automata.core.symbol_embedding.builders import (
    SymbolCodeEmbeddingBuilder,
    SymbolDocEmbeddingBuilder,
)
from automata.core.embedding.base import EmbeddingSimilarityCalculator
from automata.core.utils import get_config_fpath

logger = logging.getLogger(__name__)


def setup(**kwargs):
    embedding_provider = OpenAIEmbeddingProvider()
    chat_provider = OpenAIChatCompletionProvider(model=kwargs.get("model", "gpt-4"))
    embedding_similarity_calculator = EmbeddingSimilarityCalculator(embedding_provider)

    code_embedding_fpath = os.path.join(
        get_config_fpath(), ConfigCategory.SYMBOL.value, "symbol_code_embedding.json"
    )
    code_embedding_db = JSONSymbolEmbeddingVectorDatabase(code_embedding_fpath)
    code_embedding_builder = SymbolCodeEmbeddingBuilder(embedding_provider)
    code_embedding_handler = SymbolCodeEmbeddingHandler(code_embedding_db, code_embedding_builder)

    doc_embedding_path_l2 = os.path.join(
        get_config_fpath(),
        ConfigCategory.SYMBOL.value,
        kwargs.get("symbol_doc_embedding_l2_fpath", "symbol_doc_embedding_l2.json"),
    )
    doc_embedding_db_l2 = JSONSymbolEmbeddingVectorDatabase(doc_embedding_path_l2)

    scip_path = os.path.join(
        get_config_fpath(), ConfigCategory.SYMBOL.value, kwargs.get("index-file", "index.scip")
    )
    symbol_graph = SymbolGraph(scip_path)
    symbol_search = SymbolSearch(symbol_graph, SymbolRankConfig(), embedding_similarity_calculator)
    py_context_retriever = PyContextRetriever(symbol_graph, PyContextRetrieverConfig())

    symbol_doc_embedding_builder = SymbolDocEmbeddingBuilder(
        embedding_provider, chat_provider, symbol_search, py_context_retriever
    )

    embedding_handler = SymbolDocEmbeddingHandler(
        doc_embedding_db_l2, symbol_doc_embedding_builder
    )

    # sync the symbol graph with the code embedding
    graph_symbols = symbol_graph.get_sorted_supported_symbols()
    embedding_symbols = code_embedding_handler.get_sorted_supported_symbols()
    sorted_supported_symbols = set(graph_symbols).intersection(set(embedding_symbols))
    filter_digraph_by_symbols(symbol_graph.default_rankable_subgraph, sorted_supported_symbols)

    return {
        "embedding_handler": embedding_handler,
        "doc_embedding_db_l2": doc_embedding_db_l2,
        "symbol_graph": symbol_graph,
    }


def process_embeddings(embedding_handler, doc_embedding_db_l2, symbol_graph):
    all_defined_symbols = symbol_graph.get_sorted_supported_symbols()
    filtered_symbols = sorted(get_rankable_symbols(all_defined_symbols), key=lambda x: x.dotpath)

    for symbol in tqdm(filtered_symbols):
        if symbol.symbol_kind_by_suffix() == SymbolDescriptor.PyKind.Class:
            try:
                logger.info(f"Attempting update for symbol {symbol}...")
                embedding_handler.process_embedding(symbol)
                doc_embedding_db_l2.save()
            except Exception as e:
                logger.error(f"Failed to update embedding for symbol {symbol}: {e}")


def discard_stale_symbols(embedding_handler, doc_embedding_db_l2, symbol_graph):
    all_defined_symbols = symbol_graph.get_sorted_supported_symbols()
    filtered_symbols = sorted(get_rankable_symbols(all_defined_symbols), key=lambda x: x.dotpath)

    for symbol in embedding_handler.get_sorted_supported_symbols():
        if symbol not in filtered_symbols:
            logger.info(f"Discarding stale symbol {symbol}...")
            doc_embedding_db_l2.discard(symbol.dotpath)
    doc_embedding_db_l2.save()


def main(*args, **kwargs) -> str:
    py_module_loader.initialize()

    logger.info("Running....")

    setup_data = setup(**kwargs)

    process_embeddings(
        setup_data["embedding_handler"],
        setup_data["doc_embedding_db_l2"],
        setup_data["symbol_graph"],
    )


# def main(*args, **kwargs) -> str:
#     """
#     Update the symbol code embedding based on the specified SCIP index file.
#     """

#     py_module_loader.initialize()

#     logger.info("Running....")

#     embedding_provider = OpenAIEmbeddingProvider()
#     chat_provider = OpenAIChatCompletionProvider(model=kwargs.get("model", "gpt-4"))
#     embedding_similarity_calculator = EmbeddingSimilarityCalculator(embedding_provider)

#     code_embedding_fpath = os.path.join(
#         get_config_fpath(), ConfigCategory.SYMBOL.value, "symbol_code_embedding.json"
#     )
#     code_embedding_db = JSONSymbolEmbeddingVectorDatabase(code_embedding_fpath)
#     code_embedding_builder = SymbolCodeEmbeddingBuilder(embedding_provider)
#     code_embedding_handler = SymbolCodeEmbeddingHandler(code_embedding_db, code_embedding_builder)

#     # TODO - Add option for the user to modify l2 embedding path in commands.py
#     doc_embedding_path_l2 = os.path.join(
#         get_config_fpath(),
#         ConfigCategory.SYMBOL.value,
#         kwargs.get("symbol_doc_embedding_l2_fpath", "symbol_doc_embedding_l2.json"),
#     )
#     doc_embedding_db_l2 = JSONSymbolEmbeddingVectorDatabase(doc_embedding_path_l2)

#     scip_path = os.path.join(
#         get_config_fpath(), ConfigCategory.SYMBOL.value, kwargs.get("index-file", "index.scip")
#     )
#     symbol_graph = SymbolGraph(scip_path)
#     symbol_search = SymbolSearch(symbol_graph, SymbolRankConfig(), embedding_similarity_calculator)
#     py_context_retriever = PyContextRetriever(symbol_graph, PyContextRetrieverConfig())

#     symbol_doc_embedding_builder = SymbolDocEmbeddingBuilder(
#         embedding_provider, chat_provider, symbol_search, py_context_retriever
#     )

#     embedding_handler = SymbolDocEmbeddingHandler(
#         doc_embedding_db_l2, symbol_doc_embedding_builder
#     )

#     all_defined_symbols = symbol_graph.get_sorted_supported_symbols()
#     filtered_symbols = sorted(get_rankable_symbols(all_defined_symbols), key=lambda x: x.dotpath)

#     for symbol in tqdm(filtered_symbols):
#         if symbol.symbol_kind_by_suffix() == SymbolDescriptor.PyKind.Class:
#             try:
#                 logger.info(f"Attempting update for symbol {symbol}...")
#                 embedding_handler.process_embedding(symbol)
#                 doc_embedding_db_l2.save()
#             except Exception as e:
#                 logger.error(f"Failed to update embedding for symbol {symbol}: {e}")

#     for symbol in embedding_handler.get_sorted_supported_symbols():
#         if symbol not in filtered_symbols:
#             logger.info(f"Discarding stale symbol {symbol}...")
#             doc_embedding_db_l2.discard(symbol.dotpath)
#     doc_embedding_db_l2.save()

#     logger.info("Complete.")
#     return "Success"
