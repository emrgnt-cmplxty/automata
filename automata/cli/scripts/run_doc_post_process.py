import logging
import os

from automata.code_handling.py.writer import PyDocWriter
from automata.config import ConfigCategory
from automata.core.utils import get_config_fpath, get_root_fpath
from automata.symbol_embedding import JSONSymbolEmbeddingVectorDatabase

logger = logging.getLogger(__name__)


def main(*args, **kwargs) -> str:
    """
    Update the symbol code embedding based on the specified SCIP index file.
    """
    doc_writer = PyDocWriter(get_root_fpath())

    embedding_path = os.path.join(
        get_config_fpath(),
        ConfigCategory.SYMBOL.to_path(),
        "symbol_doc_embedding_l2.json",
    )

    embedding_db = JSONSymbolEmbeddingVectorDatabase(embedding_path)

    symbols = [
        embedding.symbol for embedding in embedding_db.get_ordered_embeddings()
    ]

    docs = {
        symbol: embedding_db.get(symbol.full_dotpath) for symbol in symbols
    }

    doc_writer.write_documentation(docs, symbols, os.path.join(get_root_fpath(), "docs"))  # type: ignore
    return "Success"
