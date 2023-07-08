import logging

from tqdm import tqdm

from automata.context_providers.symbol_synchronization import (
    SymbolProviderSynchronizationContext,
)
from automata.llm.providers.openai import OpenAIEmbeddingProvider
from automata.memory_store.symbol_code_embedding import SymbolCodeEmbeddingHandler
from automata.memory_store.symbol_doc_embedding import SymbolDocEmbeddingHandler
from automata.singletons.dependency_factory import dependency_factory
from automata.singletons.py_module_loader import py_module_loader
from automata.symbol.graph import SymbolGraph
from automata.symbol.symbol_utils import get_rankable_symbols

logger = logging.getLogger(__name__)


def initialize_providers(embedding_level, **kwargs):
    py_module_loader.initialize()

    embedding_provider = OpenAIEmbeddingProvider()

    overrides = {
        "embedding_provider": embedding_provider,
        "disable_synchronization": True,
    }

    if embedding_level == 3:
        raise NotImplementedError("Embedding level 3 is not supported at this moment.")

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
