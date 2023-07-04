import logging
import os

from tqdm import tqdm

from automata.config.base import ConfigCategory
from automata.core.context_providers.symbol_synchronization import (
    SymbolProviderSynchronizationContext,
)
from automata.core.llm.providers.openai import OpenAIEmbeddingProvider
from automata.core.memory_store.symbol_code_embedding import SymbolCodeEmbeddingHandler
from automata.core.memory_store.symbol_doc_embedding import SymbolDocEmbeddingHandler
from automata.core.singletons.dependency_factory import dependency_factory
from automata.core.singletons.py_module_loader import py_module_loader
from automata.core.symbol.base import SymbolDescriptor
from automata.core.symbol.graph import SymbolGraph
from automata.core.symbol.symbol_utils import get_rankable_symbols
from automata.core.utils import get_config_fpath

logger = logging.getLogger(__name__)


def main(*args, **kwargs) -> str:
    """
    Update the symbol code embedding based on the specified SCIP index file.
    """

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
        kwargs.get("doc-embedding-file", "symbol_doc_embedding_l2.json"),
    )
    embedding_provider = OpenAIEmbeddingProvider()

    dependency_factory.set_overrides(
        **{
            "symbol_graph_scip_fpath": scip_fpath,
            "code_embedding_fpath": code_embedding_fpath,
            "doc_embedding_fpath": doc_embedding_fpath,
            "embedding_provider": embedding_provider,
        }
    )

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

    # # Mock synchronization to allow us to build the initial doc embedding handler
    symbol_doc_embedding_handler.is_synchronized = True

    all_defined_symbols = symbol_graph.get_sorted_supported_symbols()
    filtered_symbols = sorted(get_rankable_symbols(all_defined_symbols), key=lambda x: x.dotpath)

    for symbol in tqdm(filtered_symbols):
        if symbol.symbol_kind_by_suffix() == SymbolDescriptor.PyKind.Class:
            symbol_doc_embedding_handler.process_embedding(symbol)
            symbol_doc_embedding_handler.embedding_db.save()

    for symbol in symbol_doc_embedding_handler.get_sorted_supported_symbols():
        if symbol not in filtered_symbols:
            logger.info(f"Discarding stale symbol {symbol}...")
            symbol_doc_embedding_handler.embedding_db.discard(symbol.dotpath)
    symbol_doc_embedding_handler.embedding_db.save()

    return "Success"
