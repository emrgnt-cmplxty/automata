import logging
import os

from tqdm import tqdm

from automata_docs.configs.config_enums import ConfigCategory
from automata_docs.core.embedding.symbol_embedding import SymbolEmbeddingMap
from automata_docs.core.symbol.symbol_graph import SymbolGraph
from automata_docs.core.symbol.symbol_utils import get_rankable_symbols
from automata_docs.core.utils import config_path

logger = logging.getLogger(__name__)
CHUNK_SIZE = 10


def main(*args, **kwargs):
    """
    Update the distance embedding based on the symbols present in the system.
    """
    scip_path = os.path.join(config_path(), ConfigCategory.SYMBOLS.value, "index.scip")
    embedding_path = os.path.join(
        config_path(), ConfigCategory.SYMBOLS.value, "symbol_embedding.json"
    )

    symbol_graph = SymbolGraph(scip_path)

    if kwargs.get("update_embedding_map") or kwargs.get("build_new_embedding_map"):
        all_defined_symbols = symbol_graph.get_all_available_symbols()
        filtered_symbols = get_rankable_symbols(all_defined_symbols)
        chunks = [
            filtered_symbols[i : i + CHUNK_SIZE]
            for i in range(0, len(filtered_symbols), CHUNK_SIZE)
        ]

        for chunk in tqdm(chunks):
            if kwargs.get("build_new_embedding_map") and chunk == chunks[0]:
                symbol_embedding = SymbolEmbeddingMap(
                    all_defined_symbols=chunk,
                    build_new_embedding_map=True,
                    embedding_path=embedding_path,
                )
            else:
                symbol_embedding = SymbolEmbeddingMap(
                    load_embedding_map=True,
                    embedding_path=embedding_path,
                )
                symbol_embedding.update_embeddings(chunk)

            symbol_embedding.save(embedding_path, overwrite=True)
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
        "--update_embedding_map",
        action="store_true",
        help="Flag to update the embedding map.",
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
