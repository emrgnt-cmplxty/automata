import logging
import os

from tqdm import tqdm

from automata_docs.configs.config_enums import ConfigCategory
from automata_docs.core.database.vector import JSONVectorDatabase
from automata_docs.core.embedding.symbol_embedding import SymbolCodeEmbeddingHandler
from automata_docs.core.symbol.graph import SymbolGraph
from automata_docs.core.symbol.symbol_utils import get_rankable_symbols
from automata_docs.core.utils import config_fpath

logger = logging.getLogger(__name__)
CHUNK_SIZE = 10


def main(*args, **kwargs):
    """
    Update the symbol code embedding based on the specified SCIP index file.
    """
    scip_path = os.path.join(
        config_fpath(), ConfigCategory.SYMBOLS.value, kwargs.get("index_file", "index.scip")
    )
    embedding_path = os.path.join(
        config_fpath(),
        ConfigCategory.SYMBOLS.value,
        kwargs.get("embedding_file", "symbol_code_embedding.json"),
    )

    symbol_graph = SymbolGraph(scip_path)

    all_defined_symbols = symbol_graph.get_all_available_symbols()
    filtered_symbols = sorted(get_rankable_symbols(all_defined_symbols), key=lambda x: x.dotpath)

    embedding_db = JSONVectorDatabase(embedding_path)
    embedding_handler = SymbolCodeEmbeddingHandler(embedding_db)

    for symbol in tqdm(filtered_symbols):
        embedding_handler.update_embedding(symbol)
        embedding_db.save()
    return "Success"
