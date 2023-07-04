import logging
import os

from tqdm import tqdm

from automata.config.base import ConfigCategory
from automata.core.llm.providers.openai import OpenAIEmbeddingProvider
from automata.core.memory_store.symbol_code_embedding import SymbolCodeEmbeddingHandler
from automata.core.singletons.py_module_loader import py_module_loader
from automata.core.symbol.graph import SymbolGraph
from automata.core.symbol.symbol_utils import get_rankable_symbols
from automata.core.symbol_embedding.base import JSONSymbolEmbeddingVectorDatabase
from automata.core.symbol_embedding.builders import SymbolCodeEmbeddingBuilder
from automata.core.utils import get_config_fpath

logger = logging.getLogger(__name__)


def main(*args, **kwargs) -> str:
    """
    Update the symbol code embedding based on the specified SCIP index file.
    """

    py_module_loader.initialize()

    scip_path = os.path.join(
        get_config_fpath(), ConfigCategory.SYMBOL.value, kwargs.get("index-file", "index.scip")
    )
    embedding_path = os.path.join(
        get_config_fpath(),
        ConfigCategory.SYMBOL.value,
        kwargs.get("embedding-file", "symbol_code_embedding.json"),
    )

    symbol_graph = SymbolGraph(scip_path)

    all_defined_symbols = symbol_graph.get_all_supported_symbols()
    filtered_symbols = sorted(get_rankable_symbols(all_defined_symbols), key=lambda x: x.dotpath)

    embedding_db = JSONSymbolEmbeddingVectorDatabase(embedding_path)
    embedding_provider = OpenAIEmbeddingProvider()
    embedding_builder = SymbolCodeEmbeddingBuilder(embedding_provider)
    embedding_handler = SymbolCodeEmbeddingHandler(embedding_db, embedding_builder)

    for symbol in tqdm(filtered_symbols):
        try:
            embedding_handler.process_embedding(symbol)
            embedding_db.save()
        except Exception as e:
            logger.error(f"Failed to update embedding for {symbol.dotpath}: {e}")

    for symbol in embedding_handler.get_all_supported_symbols():
        if symbol not in filtered_symbols:
            logger.info(f"Discarding stale symbol {symbol}...")
            embedding_db.discard(symbol.dotpath)
    embedding_db.save()

    return "Success"
