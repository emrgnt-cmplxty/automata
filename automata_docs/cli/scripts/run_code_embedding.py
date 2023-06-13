import logging
import os

from tqdm import tqdm

from automata_docs.configs.config_enums import ConfigCategory
from automata_docs.core.database.vector import JSONVectorDatabase
from automata_docs.core.embedding.symbol_embedding import SymbolCodeEmbeddingHandler
from automata_docs.core.symbol.symbol_graph import SymbolGraph
from automata_docs.core.symbol.symbol_utils import get_rankable_symbols
from automata_docs.core.utils import config_path

logger = logging.getLogger(__name__)
CHUNK_SIZE = 10


def main(*args, **kwargs):
    """
    Update the distance embedding based on the symbols present in the system.
    """
    scip_path = os.path.join(
        config_path(), ConfigCategory.SYMBOLS.value, kwargs.get("index_file", "index.scip")
    )
    embedding_path = os.path.join(
        config_path(),
        ConfigCategory.SYMBOLS.value,
        kwargs.get("embedding_file", "symbol_code_embedding.json"),
    )

    symbol_graph = SymbolGraph(scip_path)

    all_defined_symbols = symbol_graph.get_all_available_symbols()
    filtered_symbols = sorted(get_rankable_symbols(all_defined_symbols), key=lambda x: x.path)

    embedding_db = JSONVectorDatabase(embedding_path)
    embedding_handler = SymbolCodeEmbeddingHandler(embedding_db)

    for symbol in tqdm(filtered_symbols):
        embedding_handler.update_embedding(symbol)
        embedding_db.save()
    return "Success"


if __name__ == "__main__":
    # Setup argument parser
    import argparse

    # Create the parser
    parser = argparse.ArgumentParser(
        description="Update the distance embedding based on the symbols present in the system."
    )

    # Add the arguments
    parser.add_argument(
        "--index_file",
        default="index.scip",
        help="Which index file to use for the embedding modifications.",
    )
    # Add the arguments
    parser.add_argument(
        "--embedding_file",
        default="symbol_code_embedding.json",
        help="Which embedding file to save to.",
    )

    parser.add_argument(
        "--build_new_embedding_map",
        action="store_true",
        help="Flag to build a new embedding map.",
    )

    # Parse the arguments
    args = parser.parse_args()

    # Call the main function with parsed arguments
    main(**vars(args))
