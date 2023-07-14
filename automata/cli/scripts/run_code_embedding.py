import logging
import os

from tqdm import tqdm

from automata.cli.cli_utils import initialize_modules
from automata.llm import OpenAIEmbeddingProvider
from automata.memory_store import SymbolCodeEmbeddingHandler
from automata.singletons.dependency_factory import (
    DependencyFactory,
    dependency_factory,
)
from automata.symbol import SymbolGraph, get_rankable_symbols
from automata.symbol_embedding import (
    ChromaSymbolEmbeddingVectorDatabase,
    SymbolCodeEmbedding,
)

logger = logging.getLogger(__name__)


def initialize_resources(project_name, **kwargs):
    symbol_graph = SymbolGraph(
        os.path.join(
            DependencyFactory.DEFAULT_SCIP_FPATH, f"{project_name}.scip"
        )
    )

    code_embedding_db = ChromaSymbolEmbeddingVectorDatabase(
        project_name,
        persist_directory=DependencyFactory.DEFAULT_CODE_EMBEDDING_FPATH,
        factory=SymbolCodeEmbedding.from_args,
    )
    embedding_provider = OpenAIEmbeddingProvider()

    dependency_factory.set_overrides(
        **{
            "symbol_graph": symbol_graph,
            "code_embedding_db": code_embedding_db,
            "embedding_provider": embedding_provider,
            "disable_synchronization": True,  # We spoof synchronization locally
        }
    )

    symbol_code_embedding_handler: SymbolCodeEmbeddingHandler = (
        dependency_factory.get("symbol_code_embedding_handler")
    )

    # Mock synchronization to allow us to build the initial embedding handler
    symbol_graph.is_synchronized = True
    symbol_code_embedding_handler.is_synchronized = True

    return symbol_graph, symbol_code_embedding_handler


def collect_symbols(symbol_graph):
    all_defined_symbols = symbol_graph.get_sorted_supported_symbols()
    filtered_symbols = sorted(
        get_rankable_symbols(all_defined_symbols), key=lambda x: x.full_dotpath
    )
    return filtered_symbols


def process_embeddings(symbol_code_embedding_handler, filtered_symbols):
    for symbol in tqdm(filtered_symbols):
        try:
            symbol_code_embedding_handler.process_embedding(symbol)
        except Exception as e:
            logger.error(
                f"Failed to update embedding for {symbol.full_dotpath}: {e}"
            )

    symbol_code_embedding_handler.flush()  # Final flush for any remaining symbols that didn't form a complete batch


def main(*args, **kwargs):
    project_name = kwargs.get("project_name") or "automata"
    initialize_modules(**kwargs)

    symbol_graph, symbol_code_embedding_handler = initialize_resources(
        project_name, **kwargs
    )
    filtered_symbols = collect_symbols(symbol_graph)
    process_embeddings(symbol_code_embedding_handler, filtered_symbols)

    return "Success"
