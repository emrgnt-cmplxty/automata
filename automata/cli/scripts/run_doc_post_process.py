"""
Runs symbol doc embedding post processing for the given symbol graph.
"""

import logging
import os

from automata.cli.cli_utils import initialize_py_module_loader
from automata.code_writers.py.py_doc_writer import PyDocWriter
from automata.core.utils import get_root_fpath
from automata.singletons.dependency_factory import DependencyFactory
from automata.symbol_embedding import (
    ChromaSymbolEmbeddingVectorDatabase,
    SymbolDocEmbedding,
)

logger = logging.getLogger(__name__)


def main(*args, **kwargs) -> str:
    """
    Update the symbol code embedding based on the specified SCIP index file.
    """

    project_name = kwargs.get("project_name") or "automata"
    initialize_py_module_loader(**kwargs)

    doc_writer = PyDocWriter(get_root_fpath())

    doc_embedding_db = ChromaSymbolEmbeddingVectorDatabase(
        project_name,
        persist_directory=DependencyFactory.DEFAULT_DOC_EMBEDDING_FPATH,
        factory=SymbolDocEmbedding.from_args,
    )

    symbols = [
        embedding.symbol
        for embedding in doc_embedding_db.get_all_ordered_embeddings()
    ]

    docs = {
        symbol: doc_embedding_db.get(symbol.full_dotpath) for symbol in symbols
    }

    doc_writer.write_documentation(docs, symbols, os.path.join(get_root_fpath(), "docs"))  # type: ignore
    return "Success"
