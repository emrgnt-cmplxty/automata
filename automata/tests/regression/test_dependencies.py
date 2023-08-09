import logging
import os

import pytest

import automata.core.utils  # pylint: disable=unused-import
from automata.core.run_handlers import initialize_automata
from automata.singletons.dependency_factory import (
    DependencyFactory,
    dependency_factory,
)
from automata.symbol.graph import SymbolGraph
from automata.symbol_embedding.symbol_embedding_base import (
    SymbolCodeEmbedding,
    SymbolDocEmbedding,
)
from automata.symbol_embedding.vector_databases import (
    ChromaSymbolEmbeddingVectorDatabase,
)

logger = logging.getLogger(__name__)


@pytest.mark.regression
@pytest.mark.parametrize(
    "classes_to_build",
    [
        ["symbol_graph"],
        ["symbol_code_embedding_handler"],
        ["symbol_code_embedding_handler", "symbol_graph"],
        ["symbol_code_embedding_handler", "symbol_doc_embedding_handler"],
        ["symbol_doc_embedding_handler", "symbol_graph"],
        ["symbol_search"],
        ["symbol_rank"],
    ],
)
def test_build_automata_class_dependencies(classes_to_build):
    initialize_automata()
    # sourcery skip: no-loop-in-tests
    for class_to_build in classes_to_build:
        dependency_factory.get(class_to_build)


@pytest.mark.regression
@pytest.mark.parametrize(
    "toolkits_to_build",
    [
        ["symbol-search"],
        ["advanced-context-oracle"],
        ["document-oracle"],
        ["py-reader"],
        ["py-writer"],
        ["py-interpreter"],
        ["agent-search"],
    ],
)
def test_build_automata_tools(toolkits_to_build):
    initialize_automata()
    dependency_factory.build_dependencies_for_tools(toolkits_to_build)


@pytest.mark.regression
def test_automata_symbol_providers():
    initialize_automata()
    project_name = "automata"
    # SYMBOL GRAPH
    symbol_graph = SymbolGraph(
        os.path.join(
            DependencyFactory.DEFAULT_SCIP_FPATH, f"{project_name}.scip"
        )
    )
    symbol_graph.is_synchronized = True  # mock initialization
    supported_symbol_graph_embeddings = (
        symbol_graph.get_sorted_supported_symbols()
    )
    last_symbol_graph_embedding_symbol = supported_symbol_graph_embeddings[-1]

    # CODE EMBEDDING
    code_embedding_db = ChromaSymbolEmbeddingVectorDatabase(
        project_name,
        persist_directory=DependencyFactory.DEFAULT_CODE_EMBEDDING_FPATH,
        factory=SymbolCodeEmbedding.from_args,
    )

    ordered_code_embeddings = list(
        code_embedding_db.get_all_ordered_embeddings()
    )
    last_code_embedding_symbol = ordered_code_embeddings[-1].symbol

    # DOC EMBEDDING
    doc_embedding_db = ChromaSymbolEmbeddingVectorDatabase(
        project_name,
        persist_directory=DependencyFactory.DEFAULT_DOC_EMBEDDING_FPATH,
        factory=SymbolDocEmbedding.from_args,
    )

    ordered_doc_embeddings = list(
        doc_embedding_db.get_all_ordered_embeddings()
    )
    last_doc_embedding_symbol = ordered_doc_embeddings[-1].symbol
    if last_code_embedding_symbol.package != last_doc_embedding_symbol.package:
        raise ValueError(
            f"Last code embedding symbol {last_code_embedding_symbol} package does not match last doc embedding symbol {last_doc_embedding_symbol} package."
        )
    elif (
        last_code_embedding_symbol.package
        != last_symbol_graph_embedding_symbol.package
    ):
        raise ValueError(
            f"Last code embedding symbol {last_code_embedding_symbol} package does not match last symbol graph embedding symbol {last_symbol_graph_embedding_symbol} package."
        )
