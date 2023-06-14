import logging
import os

from tqdm import tqdm

from automata_docs.config.config_enums import ConfigCategory
from automata_docs.core.database.vector import JSONVectorDatabase
from automata_docs.core.embedding.symbol_embedding import SymbolDocEmbeddingHandler
from automata_docs.core.symbol.graph import SymbolGraph
from automata_docs.core.symbol.symbol_types import SymbolDescriptor
from automata_docs.core.symbol.symbol_utils import get_rankable_symbols
from automata_docs.core.utils import config_fpath

logger = logging.getLogger(__name__)
CHUNK_SIZE = 10


def main(*args, **kwargs):
    """
    Update the symbol code embedding based on the specified SCIP index file.
    """
    print("We are in run doc embedding l2....")
    scip_path = os.path.join(
        config_fpath(), ConfigCategory.SYMBOL.value, kwargs.get("index_file", "index.scip")
    )
    embedding_path = os.path.join(
        config_fpath(),
        ConfigCategory.SYMBOL.value,
        kwargs.get("embedding_file", "symbol_doc_embedding_l2.json"),
    )
    print("embedding_path = ", embedding_path)

    symbol_graph = SymbolGraph(scip_path)
    all_defined_symbols = symbol_graph.get_all_available_symbols()
    filtered_symbols = sorted(get_rankable_symbols(all_defined_symbols), key=lambda x: x.dotpath)
    print("filtered_symbols[0:10] = ", filtered_symbols[0:10])
    embedding_db = JSONVectorDatabase(embedding_path)
    print("embedding db loaded...")
    embedding_handler = SymbolDocEmbeddingHandler(embedding_db)
    print("embedding handler loaded...")
    print("Calling update embedding...")
    for symbol in tqdm(filtered_symbols):
        if symbol.symbol_kind_by_suffix() == SymbolDescriptor.PyKind.Class:
            print("Updating symbol = ", symbol)
            embedding_handler.update_embedding(symbol)
            embedding_db.save()
    return "Success"
