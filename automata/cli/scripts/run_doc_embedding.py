import logging
import os

from tqdm import tqdm

from automata.config.base import ConfigCategory
from automata.context_providers.symbol_synchronization import (
    SymbolProviderSynchronizationContext,
)
from automata.core.utils import get_config_fpath
from automata.llm.providers.openai import OpenAIEmbeddingProvider
from automata.memory_store.symbol_code_embedding import SymbolCodeEmbeddingHandler
from automata.memory_store.symbol_doc_embedding import SymbolDocEmbeddingHandler
from automata.singletons.dependency_factory import dependency_factory
from automata.singletons.py_module_loader import py_module_loader
from automata.symbol.graph import SymbolGraph
from automata.symbol.symbol_utils import get_rankable_symbols
from automata.symbol_embedding.vector_databases import JSONSymbolEmbeddingVectorDatabase

logger = logging.getLogger(__name__)


def initialize_providers(embedding_level, **kwargs):
    py_module_loader.initialize()

    scip_fpath = os.path.join(
        get_config_fpath(), ConfigCategory.SYMBOL.value, kwargs.get("index-file", "index.scip")
    )
    code_embedding_fpath = os.path.join(
        get_config_fpath(),
        ConfigCategory.SYMBOL.value,
        kwargs.get("code-embedding-file", "symbol_code_embedding.json"),
    )
    doc_embedding_fpath = os.path.join(
        get_config_fpath(),
        ConfigCategory.SYMBOL.value,
        kwargs.get("doc-embedding-file", f"symbol_doc_embedding_l{embedding_level}.json"),
    )

    embedding_provider = OpenAIEmbeddingProvider()

    overrides = {
        "symbol_graph_scip_fpath": scip_fpath,
        "code_embedding_fpath": code_embedding_fpath,
        "doc_embedding_fpath": doc_embedding_fpath,
        "embedding_provider": embedding_provider,
        "disable_synchronization": True,
    }

    if embedding_level == 3:
        doc_embedding_fpath_l2 = os.path.join(
            get_config_fpath(),
            ConfigCategory.SYMBOL.value,
            kwargs.get("doc-embedding-file", "symbol_doc_embedding_l2.json"),
        )
        doc_embedding_db_l2 = JSONSymbolEmbeddingVectorDatabase(doc_embedding_fpath_l2)
        overrides["py_retriever_doc_embedding_db"] = doc_embedding_db_l2

    dependency_factory.set_overrides(**overrides)

    symbol_graph: SymbolGraph = dependency_factory.get("symbol_graph")
    symbol_code_embedding_handler: SymbolCodeEmbeddingHandler = dependency_factory.get(
        "symbol_code_embedding_handler"
    )
    symbol_doc_embedding_handler: SymbolDocEmbeddingHandler = dependency_factory.get(
        "symbol_doc_embedding_handler"
    )

    with SymbolProviderSynchronizationContext() as synchronization_context:
        synchronization_context.register_provider(symbol_graph)
        synchronization_context.register_provider(symbol_code_embedding_handler)
        synchronization_context.synchronize()

    symbol_doc_embedding_handler.is_synchronized = True

    all_defined_symbols = symbol_graph.get_sorted_supported_symbols()
    filtered_symbols = sorted(get_rankable_symbols(all_defined_symbols), key=lambda x: x.dotpath)

    return symbol_doc_embedding_handler, filtered_symbols


def main(*args, **kwargs) -> str:
    """
    Update the symbol code embedding based on the specified SCIP index file.
    """

    symbol_doc_embedding_handler, filtered_symbols = initialize_providers(**kwargs)

    logger.info("Looping over filtered symbols...")
    for symbol in tqdm(filtered_symbols):
        logger.info(f"Caching embedding for {symbol}")
        symbol_doc_embedding_handler.process_embedding(symbol)
        symbol_doc_embedding_handler.embedding_db.save()

    return "Success"
