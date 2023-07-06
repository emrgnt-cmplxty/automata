import logging
import os

from tqdm import tqdm

from automata.config.base import ConfigCategory
from automata.core.utils import get_config_fpath
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

    scip_fpath = os.path.join(
        get_config_fpath(), ConfigCategory.SYMBOL.value, kwargs.get("index-file", "index.scip")
    )
    code_embedding_fpath = os.path.join(
        get_config_fpath(),
        ConfigCategory.SYMBOL.value,
        kwargs.get("code-embedding-file", "symbol_code_embedding.json"),
    )
    embedding_provider = OpenAIEmbeddingProvider()

    dependency_factory.set_overrides(
        **{
            "symbol_graph_scip_fpath": scip_fpath,
            "code_embedding_fpath": code_embedding_fpath,
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
            symbol_code_embedding_handler.embedding_db.save()
        except Exception as e:
            logger.error(f"Failed to update embedding for {symbol.dotpath}: {e}")

    return "Success"
