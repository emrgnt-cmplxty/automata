import logging
import os

from automata.config.base import ConfigCategory
from automata.core.code_handling.py.writer import PyDocWriter
from automata.core.symbol_embedding.base import JSONSymbolEmbeddingVectorDatabase
from automata.core.utils import get_config_fpath, get_root_py_fpath

logger = logging.getLogger(__name__)


def main(*args, **kwargs) -> str:
    """
    Update the symbol code embedding based on the specified SCIP index file.
    """
    doc_writer = PyDocWriter(get_root_py_fpath())

    embedding_path = os.path.join(
        get_config_fpath(), ConfigCategory.SYMBOL.value, "symbol_doc_embedding_l2.json"
    )

    embedding_db = JSONSymbolEmbeddingVectorDatabase(embedding_path)

    symbols = [embedding.symbol for embedding in embedding_db.get_ordered_embeddings()]

    docs = {symbol: embedding_db.get(symbol.dotpath) for symbol in symbols}

    doc_writer.write_documentation(docs, symbols, os.path.join(get_root_py_fpath(), "docs"))  # type: ignore
    return "Success"
