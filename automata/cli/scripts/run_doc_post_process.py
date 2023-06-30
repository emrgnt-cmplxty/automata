import logging
import os

from automata.config.base import ConfigCategory
from automata.core.base.database.vector import JSONEmbeddingVectorDatabase
from automata.core.coding.py.writer import PyDocWriter
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

    embedding_db = JSONEmbeddingVectorDatabase(embedding_path)

    symbols = [embedding.symbol for embedding in embedding_db.get_all_entries()]

    docs = {symbol: embedding_db.get(symbol) for symbol in symbols}

    doc_writer.write_documentation(docs, symbols, os.path.join(get_root_py_fpath(), "docs"))  # type: ignore
    return "Success"
