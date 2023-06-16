import logging
import os

from tqdm import tqdm

from automata.config.config_types import ConfigCategory
from automata.core.database.vector import JSONVectorDatabase
from automata.core.embedding.code_embedding import SymbolCodeEmbeddingHandler
from automata.core.embedding.doc_embedding import SymbolDocEmbeddingHandler
from automata.core.embedding.embedding_types import OpenAIEmbedding
from automata.core.symbol.graph import SymbolGraph
from automata.core.symbol.symbol_types import SymbolDescriptor
from automata.core.symbol.symbol_utils import get_rankable_symbols
from automata.core.utils import config_fpath

logger = logging.getLogger(__name__)


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

    code_embedding_fpath = os.path.join(
        config_fpath(), ConfigCategory.SYMBOL.value, "symbol_code_embedding.json"
    )
    code_embedding_db = JSONVectorDatabase(code_embedding_fpath)
    code_embedding_handler = SymbolCodeEmbeddingHandler(code_embedding_db, OpenAIEmbedding())

    symbol_graph = SymbolGraph(scip_path)
    all_defined_symbols = symbol_graph.get_all_available_symbols()
    filtered_symbols = sorted(get_rankable_symbols(all_defined_symbols), key=lambda x: x.dotpath)
    embedding_db = JSONVectorDatabase(embedding_path)
    embedding_handler = SymbolDocEmbeddingHandler(
        embedding_db, OpenAIEmbedding(), code_embedding_handler
    )
    for symbol in tqdm(filtered_symbols):
        if symbol.symbol_kind_by_suffix() == SymbolDescriptor.PyKind.Class:
            embedding_handler.update_embedding(symbol)
            embedding_db.save()
    return "Success"
