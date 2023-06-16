import logging
import os

from automata_docs.config.config_enums import ConfigCategory
from automata_docs.core.database.vector import JSONVectorDatabase
from automata_docs.core.embedding.code_embedding import SymbolCodeEmbeddingHandler
from automata_docs.core.embedding.doc_embedding import SymbolDocEmbeddingHandler
from automata_docs.core.embedding.embedding_types import OpenAIEmbedding
from automata_docs.core.symbol.graph import SymbolGraph
from automata_docs.core.symbol.symbol_types import SymbolDescriptor
from automata_docs.core.symbol.symbol_utils import get_rankable_symbols
from automata_docs.core.utils import config_fpath
from tqdm import tqdm

logger = logging.getLogger(__name__)


def main(*args, **kwargs):
    """
    Update the symbol code embedding based on the specified SCIP index file.
    """
    print("We are in run doc embedding l3....")
    scip_path = os.path.join(
        config_fpath(), ConfigCategory.SYMBOL.value, kwargs.get("index_file", "index.scip")
    )

    code_embedding_fpath = os.path.join(
        config_fpath(), ConfigCategory.SYMBOL.value, "symbol_code_embedding.json"
    )
    code_embedding_db = JSONVectorDatabase(code_embedding_fpath)
    code_embedding_handler = SymbolCodeEmbeddingHandler(code_embedding_db, OpenAIEmbedding())

    embedding_path_l2 = os.path.join(
        config_fpath(),
        ConfigCategory.SYMBOL.value,
        kwargs.get("embedding_file", "symbol_doc_embedding_l2.json"),
    )
    embedding_db_l2 = JSONVectorDatabase(embedding_path_l2)

    embedding_path_l3 = os.path.join(
        config_fpath(),
        ConfigCategory.SYMBOL.value,
        kwargs.get("embedding_file", "symbol_doc_embedding_l3.json"),
    )
    embedding_db_l3 = JSONVectorDatabase(embedding_path_l3)
    embedding_handler = SymbolDocEmbeddingHandler(
        embedding_db_l3, OpenAIEmbedding(), code_embedding_handler, embedding_db_l2
    )

    symbol_graph = SymbolGraph(scip_path)
    all_defined_symbols = symbol_graph.get_all_available_symbols()
    filtered_symbols = sorted(get_rankable_symbols(all_defined_symbols), key=lambda x: x.dotpath)
    for symbol in tqdm(filtered_symbols):
        if symbol.symbol_kind_by_suffix() == SymbolDescriptor.PyKind.Class:
            embedding_handler.update_embedding(symbol)
            embedding_db_l3.save()
    return "Success"
