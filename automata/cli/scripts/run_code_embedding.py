import logging
import os

from tqdm import tqdm

from automata.core.utils import get_root_fpath
from automata.llm.providers.openai import OpenAIEmbeddingProvider
from automata.memory_store.symbol_code_embedding import SymbolCodeEmbeddingHandler
from automata.singletons.dependency_factory import DependencyFactory, dependency_factory
from automata.singletons.py_module_loader import py_module_loader
from automata.symbol.graph import SymbolGraph
from automata.symbol.symbol_utils import get_rankable_symbols
from automata.symbol_embedding.base import SymbolCodeEmbedding
from automata.symbol_embedding.vector_databases import (
    ChromaSymbolEmbeddingVectorDatabase,
)

logger = logging.getLogger(__name__)


def main(*args, **kwargs) -> str:
    """
    Update the symbol code embedding based on the specified SCIP index file.
    """
    root_path = kwargs.get("project_root_fpath") or get_root_fpath()
    project_name = kwargs.get("project_name") or "automata"
    rel_py_path = kwargs.get("project_rel_py_path") or project_name
    py_module_loader.initialize(root_path, rel_py_path)

    code_embedding_db = ChromaSymbolEmbeddingVectorDatabase(
        project_name,
        persist_directory=DependencyFactory.DEFAULT_CODE_EMBEDDING_FPATH,
        factory=SymbolCodeEmbedding.from_args,
    )

    symbol_graph = SymbolGraph(
        os.path.join(DependencyFactory.DEFAULT_SCIP_FPATH, f"{project_name}.scip")
    )
    embedding_provider = OpenAIEmbeddingProvider()

    dependency_factory.set_overrides(
        **{
            "symbol_graph": symbol_graph,
            "code_embedding_db": code_embedding_db,
            "embedding_provider": embedding_provider,
            "disable_synchronization": True,
        }
    )

    symbol_code_embedding_handler: SymbolCodeEmbeddingHandler = dependency_factory.get(
        "symbol_code_embedding_handler"
    )
    # Mock synchronization to allow us to build the initial embedding handler
    symbol_graph.is_synchronized = True
    symbol_code_embedding_handler.is_synchronized = True

    all_defined_symbols = symbol_graph.get_sorted_supported_symbols()
    filtered_symbols = sorted(get_rankable_symbols(all_defined_symbols), key=lambda x: x.dotpath)

    for symbol in tqdm(filtered_symbols):
        try:
            symbol_code_embedding_handler.process_embedding(symbol)
        except Exception as e:
            logger.error(f"Failed to update embedding for {symbol.dotpath}: {e}")

    symbol_code_embedding_handler.embedding_db.save()
    return "Success"
