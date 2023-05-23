import logging
import os

import numpy as np
from tqdm import tqdm

from automata.configs.config_enums import ConfigCategory
from automata.tools.search.symbol_converter import SymbolConverter
from automata.tools.search.symbol_graph import SymbolGraph
from automata.tools.search.symbol_rank.symbol_embedding_map import SymbolEmbeddingMap

logger = logging.getLogger(__name__)
CHUNK_SIZE = 10


def main(*args, **kwargs):
    """
    Regenerate the distance embedding based on the symbols present in the system.
    """
    file_dir = os.path.dirname(os.path.abspath(__file__))
    scip_path = os.path.join(
        file_dir, "..", "..", "configs", ConfigCategory.SYMBOLS.value, "index.scip"
    )
    embedding_path = os.path.join(
        file_dir, "..", "..", "configs", ConfigCategory.SYMBOLS.value, "symbol_embedding.json"
    )

    symbol_converter = SymbolConverter()
    symbol_graph = SymbolGraph(scip_path, symbol_converter)
    all_defined_symbols = symbol_graph.get_all_defined_symbols()
    filtered_symbols = SymbolEmbeddingMap._filter_symbols(all_defined_symbols)

    np.random.shuffle(filtered_symbols)

    chunks = [
        filtered_symbols[i : i + CHUNK_SIZE] for i in range(0, len(filtered_symbols), CHUNK_SIZE)
    ]

    for chunk in tqdm(chunks):
        print("Processing chunk of length %d" % len(chunk))
        if kwargs.get("build_new_embedding_map"):
            symbol_embedding = SymbolEmbeddingMap(
                symbol_converter=symbol_converter,
                all_defined_symbols=chunk,
                build_new_embedding_map=True,
                embedding_path=embedding_path,
            )
        else:
            symbol_embedding = SymbolEmbeddingMap(
                load_embedding_map=True,
                embedding_path=embedding_path,
            )
            symbol_embedding.update_embeddings(symbol_converter, chunk)

        symbol_embedding.save(embedding_path, overwrite=True)


if __name__ == "__main__":
    main()