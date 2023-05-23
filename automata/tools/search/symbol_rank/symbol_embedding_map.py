import logging
import os
from typing import Dict, List

import jsonpickle
import openai

from automata.tools.search.local_types import Descriptor, StrPath, Symbol, SymbolEmbedding
from automata.tools.search.symbol_converter import SymbolConverter

logger = logging.getLogger(__name__)


class EmbeddingsProvider:
    def __init__(self):
        if not openai.api_key:
            from automata.config import OPENAI_API_KEY

            openai.api_key = OPENAI_API_KEY

    def get_embedding(self, symbol_source: str) -> List[float]:
        # wait to import get_embedding to allow easy mocking of the function in tests.
        from openai.embeddings_utils import get_embedding

        return get_embedding(symbol_source)


class SymbolEmbeddingMap:
    def __init__(
        self,
        *args,
        embedding_provider=None,
        build_new_embedding_map=False,
        load_embedding_map=False,
        **kwargs,
    ):
        """
        Initialize SymbolEmbeddingMap
        Args:
            *args: Variable length argument list
            embedding_provider (EmbeddingsProvider): EmbeddingsProvider object
            build_new_embedding_map (bool): Whether to build a new embedding map
            load_embedding_map (bool): Whether to load an existing embedding map
            **kwargs: Arbitrary keyword arguments
        Result:
            An instance of SymbolEmbeddingMap
        """
        self.embedding_provider = embedding_provider or EmbeddingsProvider()

        if build_new_embedding_map and load_embedding_map:
            raise ValueError("Cannot specify both build_new_embedding_map and load_embedding_map")

        if build_new_embedding_map:
            try:
                symbol_converter = kwargs["symbol_converter"]
                all_defined_symbols = kwargs["all_defined_symbols"]
                self.embedding_map = self._build_embedding_map(
                    symbol_converter, all_defined_symbols
                )
            except KeyError as e:
                raise ValueError(f"Missing required argument: {e}")

        elif load_embedding_map:
            try:
                # If given an embedding path, load the embedding map from that path
                # This results in calling cls constructor again with the loaded embedding map
                if "embedding_path" in kwargs:
                    self.embedding_map = SymbolEmbeddingMap.load(kwargs["embedding_path"])
                # Otherwise, load the embedding map from the kwargs
                elif "embedding_map" in kwargs:
                    self.embedding_map = kwargs["embedding_map"]
            except KeyError as e:
                raise ValueError(f"Missing required argument: {e}")

    def update_embeddings(
        self, symbol_converter: SymbolConverter, symbols_to_update: List[Symbol]
    ):
        """
        Update the embedding map with new symbols.

        Args:
            symbol_converter (SymbolConverter): SymbolConverter object
            symbols_to_update (List[Symbol]): List of symbols to update
        Result:
            None
        """
        for symbol in symbols_to_update:
            try:
                symbol_source = str(symbol_converter.convert_to_fst_object(symbol))
                if (
                    symbol not in self.embedding_map
                    or self.embedding_map[symbol].source_code != symbol_source
                ):
                    symbol_embedding = self.embedding_provider.get_embedding(symbol_source)
                    self.embedding_map[symbol] = SymbolEmbedding(
                        symbol=symbol, vector=symbol_embedding, source_code=symbol_source
                    )
                else:
                    logger.info("Symbol: %s already in embedding map" % symbol)
            except Exception as e:
                logger.error("Updating embedding for symbol: %s failed with %s" % (symbol, e))
        # TODO - Add trimming here

    def save(self, output_embedding_path: StrPath, overwrite: bool = False) -> None:
        """
        Save the built embedding map to a file.

        :param output_embedding_path: Path to output file
        """
        # Raise error if the file already exists
        if os.path.exists(output_embedding_path) and not overwrite:
            raise ValueError("output_embedding_path must be a path to a non-existing file.")
        with open(output_embedding_path, "w") as f:
            encoded_embedding = jsonpickle.encode(self.embedding_map)
            f.write(encoded_embedding)

    @classmethod
    def load(cls, input_embedding_path: StrPath) -> Dict[Symbol, SymbolEmbedding]:
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

        return embedding_map

    def _build_embedding_map(
        self, symbol_converter: SymbolConverter, defined_symbols: List[Symbol]
    ) -> Dict[Symbol, SymbolEmbedding]:
        """
        Build a map from symbol to embedding vector.
        Args:
            symbol_converter: SymbolConverter to convert symbols to FST objects
            all_defined_symbols: List of symbols to build embedding map for
        Returns:
            Map from symbol to embedding vector
        """
        print("Building embedding map")
        embedding_map: Dict[Symbol, SymbolEmbedding] = {}
        filtered_symbols = self._filter_symbols(defined_symbols)

        for symbol in filtered_symbols:
            try:
                symbol_source = str(symbol_converter.convert_to_fst_object(symbol))
                symbol_embedding = self.embedding_provider.get_embedding(symbol_source)
                embedding_map[symbol] = SymbolEmbedding(
                    symbol=symbol, vector=symbol_embedding, source_code=symbol_source
                )

            except Exception as e:
                logger.error("Building embedding for symbol: %s failed with %s" % (symbol, e))

        return embedding_map

    @staticmethod
    def _filter_symbols(symbols: List[Symbol]) -> List[Symbol]:
        """
        Filter out symbols that are not relevant for the embedding map.

        Args:
            symbols: List of symbols to filter
        Returns:
            List of filtered symbols
        """
        filtered_symbols = []
        filter_strings = ["__init__", "setup", "local", "test"]
        for symbol in symbols:
            do_continue = False
            for filter_string in filter_strings:
                if filter_string in symbol.uri:
                    do_continue = True
                    break
            if do_continue:
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
            filtered_symbols.append(symbol)
        return filtered_symbols
