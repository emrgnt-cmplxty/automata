import logging

from tqdm import tqdm

from automata.llm.providers.openai import OpenAIEmbeddingProvider
from automata.memory_store.symbol_code_embedding import SymbolCodeEmbeddingHandler
from automata.singletons.dependency_factory import dependency_factory
from automata.singletons.py_module_loader import py_module_loader
from automata.symbol.graph import SymbolGraph
from automata.symbol.symbol_utils import get_rankable_symbols

logger = logging.getLogger(__name__)


def main(*args, **kwargs) -> str:
    """
    Update the symbol code embedding based on the specified SCIP index file.
    """
    py_module_loader.initialize()

    embedding_provider = OpenAIEmbeddingProvider()

    dependency_factory.set_overrides(
        **{
            "embedding_provider": embedding_provider,
            "disable_synchronization": True,
        }
    )

    symbol_graph: SymbolGraph = dependency_factory.get("symbol_graph")
    symbol_code_embedding_handler: SymbolCodeEmbeddingHandler = dependency_factory.get(
        "symbol_code_embedding_handler"
    )
    # Mock synchronization to allow us to build the initial embedding handler
    symbol_graph.is_synchronized = True
    symbol_code_embedding_handler.is_synchronized = True

    all_defined_symbols = symbol_graph.get_sorted_supported_symbols()
    filtered_symbols = sorted(get_rankable_symbols(all_defined_symbols), key=lambda x: x.dotpath)

    for symbol in tqdm(filtered_symbols):
        try:
            symbol_code_embedding_handler.process_embedding(symbol)
        except Exception as e:
            logger.error(f"Failed to update embedding for {symbol.dotpath}: {e}")

    symbol_code_embedding_handler.embedding_db.save()
    return "Success"
