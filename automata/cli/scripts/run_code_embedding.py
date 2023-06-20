import logging
import os

from tqdm import tqdm

from automata.config.config_types import ConfigCategory
from automata.core.database.vector import JSONVectorDatabase
from automata.core.embedding.code_embedding import SymbolCodeEmbeddingHandler
from automata.core.embedding.embedding_types import OpenAIEmbedding
from automata.core.symbol.graph import SymbolGraph
from automata.core.symbol.symbol_utils import get_rankable_symbols
from automata.core.utils import config_fpath

logger = logging.getLogger(__name__)


def main(*args, **kwargs) -> str:
    """
    Update the symbol code embedding based on the specified SCIP index file.
    """
    scip_path = os.path.join(
        config_fpath(), ConfigCategory.SYMBOL.value, kwargs.get("index_file", "index.scip")
    )
    embedding_path = os.path.join(
        config_fpath(),
        ConfigCategory.SYMBOL.value,
        kwargs.get("embedding_file", "symbol_code_embedding.json"),
    )

    symbol_graph = SymbolGraph(scip_path)

    all_defined_symbols = symbol_graph.get_all_available_symbols()
    filtered_symbols = sorted(get_rankable_symbols(all_defined_symbols), key=lambda x: x.dotpath)

    embedding_db = JSONVectorDatabase(embedding_path)
    embedding_handler = SymbolCodeEmbeddingHandler(embedding_db, OpenAIEmbedding())

    for symbol in tqdm(filtered_symbols):
        try:
            embedding_handler.update_embedding(symbol)
            embedding_db.save()
        except Exception as e:
            logger.error(f"Failed to update embedding for {symbol.dotpath}: {e}")
    return "Success"
