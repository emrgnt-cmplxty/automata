import logging
import os
from typing import Dict, List

import jsonpickle
import openai

from automata.tools.search.local_types import Descriptor, StrPath, Symbol, SymbolEmbedding
from automata.tools.search.symbol_converter import SymbolConverter

logger = logging.getLogger(__name__)


class SymbolEmbeddingMap:
    def __init__(self, *args, **kwargs):
        """
        Initialize SymbolEmbeddingMap

        :param load_embedding_map: Should the embedding map be loaded from a file?
        :param embedding_path: Path to embedding map file, used when loading

        """
        # Check if openai key has been set
        if not openai.api_key:
            from automata.config import OPENAI_API_KEY

            openai.api_key = OPENAI_API_KEY

        if "build_new_embedding_map" in kwargs and "load_embedding_map" in kwargs:
            raise ValueError("Cannot specify both build_new_embedding_map and load_embedding_map")

        if kwargs.get("build_new_embedding_map"):
            symbol_converter: SymbolConverter = kwargs["symbol_converter"]
            all_defined_symbols: List[Symbol] = kwargs["all_defined_symbols"]
            self.embedding_map = self._build_embedding_map(symbol_converter, all_defined_symbols)
        elif kwargs.get("load_embedding_map"):
            self.embedding_map = kwargs["embedding_map"]

    def _build_embedding_map(
        self, symbol_converter: SymbolConverter, all_defined_symbols: List[Symbol]
    ) -> Dict[Symbol, SymbolEmbedding]:
        """
        Build a map from symbol to embedding vector.
        """
        # wait to import get_embedding to allow easy mocking of the function in tests.
        from openai.embeddings_utils import get_embedding

        embedding_map = {}
        for symbol in all_defined_symbols:
            if "__init__" in symbol.uri:
                continue
            if "setup" in symbol.uri:
                continue
            if "local" in symbol.uri:
                continue
            if "test" in symbol.uri:
                continue
            symbol_kind = symbol.symbol_kind_by_suffix()
            if (
                symbol_kind == Descriptor.PythonKinds.Local
                or symbol_kind == Descriptor.PythonKinds.Value
                or symbol_kind == Descriptor.PythonKinds.Meta
                or symbol_kind == Descriptor.PythonKinds.Macro
                or symbol_kind == Descriptor.PythonKinds.Parameter
                or symbol_kind == Descriptor.PythonKinds.TypeParameter
            ):
                continue

            try:
                symbol_source = str(symbol_converter.convert_to_fst_object(symbol))
                symbol_embedding = get_embedding(symbol_source)
                embedding_map[symbol] = SymbolEmbedding(
                    symbol=symbol, vector=symbol_embedding, source_code=symbol_source
                )

            except Exception as e:
                logger.error("Building embedding for symbol: %s failed with %s" % (symbol, e))

        return embedding_map

    def update_embeddings(
        self, symbol_converter: SymbolConverter, symbols_to_update: List[Symbol]
    ):
        # wait to import get_embedding to allow easy mocking of the function in tests.
        from openai.embeddings_utils import get_embedding

        for symbol in symbols_to_update:
            try:
                symbol_source = str(symbol_converter.convert_to_fst_object(symbol))
                if (
                    symbol not in self.embedding_map
                    or self.embedding_map[symbol].source_code != symbol_source
                ):
                    symbol_embedding = get_embedding(symbol_source)
                    self.embedding_map[symbol] = SymbolEmbedding(
                        symbol=symbol, vector=symbol_embedding, source_code=symbol_source
                    )
            except Exception as e:
                logger.error("Updating embedding for symbol: %s failed with %s" % (symbol, e))

    def save(self, output_embedding_path: StrPath):
        """
        Save the built embedding map to a file.

        :param output_embedding_path: Path to output file
        """
        # Raise error if the file already exists
        if os.path.exists(output_embedding_path):
            raise ValueError("output_embedding_path must be a path to a non-existing file.")
        with open(output_embedding_path, "w") as f:
            encoded_embedding = jsonpickle.encode(self.embedding_map)
            f.write(encoded_embedding)

    @classmethod
    def load(cls, input_embedding_path: StrPath) -> "SymbolEmbeddingMap":
        """
        Load a saved embedding map from a local file.

        :param input_embedding_path: Path to input file
        """
        # Raise error if the file does not exist
        if not os.path.exists(input_embedding_path):
            raise ValueError("input_embedding_path must be a path to an existing file.")

        embedding_map = {}
        with open(input_embedding_path, "r") as f:
            embedding_map_str_keys = jsonpickle.decode(f.read())
            embedding_map = {
                Symbol.from_string(key): value for key, value in embedding_map_str_keys.items()
            }

        print("embedding_map = ", embedding_map)
        return cls(load_embedding_map=True, embedding_map=embedding_map)
