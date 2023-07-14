from ast import unparse as py_ast_unparse
from typing import Any, Callable, Dict, List, Optional, Tuple, Union

import numpy as np

from automata.embedding import EmbeddingHandler, EmbeddingSimilarityCalculator
from automata.experimental.search.rank import SymbolRank, SymbolRankConfig
from automata.singletons.py_module_loader import py_module_loader
from automata.symbol import (
    Symbol,
    SymbolGraph,
    SymbolReference,
    convert_to_ast_object,
    parse_symbol,
)

SymbolReferencesResult = Dict[str, List[SymbolReference]]
SymbolRankResult = List[Tuple[Symbol, float]]
SourceCodeResult = Optional[str]
ExactSearchResult = Dict[str, List[int]]


class SymbolSearch:
    """A class which exposes various search methods for symbols."""

    def __init__(
        self,
        symbol_graph: SymbolGraph,
        symbol_rank_config: SymbolRankConfig,
        search_embedding_handler: EmbeddingHandler,
        embedding_similarity_calculator: EmbeddingSimilarityCalculator,
        z_score_power: float = 2.0,
    ) -> None:
        """
        Raises:
            ValueError: If the code_subgraph is not a subgraph of the symbol_graph
        TODO - We should modify SymbolSearch to receive a completed instance of SymbolRank.
        """

        self.symbol_graph = symbol_graph
        self.embedding_similarity_calculator = embedding_similarity_calculator
        self.search_embedding_handler = search_embedding_handler
        self.symbol_rank_config = symbol_rank_config
        self.z_score_power = z_score_power
        self._symbol_rank = (
            None  # Create a placeholder for the lazy loaded SymbolRank
        )

    @property
    def symbol_rank(self):
        if self._symbol_rank is None:
            self._symbol_rank = SymbolRank(
                self.symbol_graph.default_rankable_subgraph,
                config=self.symbol_rank_config,
            )
        return self._symbol_rank

    def get_symbol_rank_results(self, query: str) -> SymbolRankResult:
        """Fetches the list of the SymbolRank similar symbols ordered by rank."""
        ordered_embeddings = (
            self.search_embedding_handler.get_ordered_embeddings()
        )

        query_vec = self.embedding_similarity_calculator.calculate_query_similarity_dict(
            ordered_embeddings, query
        )
        transformed_query_vec = SymbolSearch.transform_dict_values(
            query_vec, self.shifted_z_score_powered
        )
        return self.symbol_rank.get_ordered_ranks(
            query_to_symbol_similarity=transformed_query_vec
        )

    def symbol_references(self, symbol_uri: str) -> SymbolReferencesResult:
        """
        Finds all references to a module, class, method, or standalone function.

        TODO - Add parsing upstream or here to parse references
        """
        return self.symbol_graph.get_references_to_symbol(
            parse_symbol(symbol_uri)
        )

    def retrieve_source_code_by_symbol(
        self, symbol_uri: str
    ) -> SourceCodeResult:
        """Finds the raw text of a module, class, method, or standalone function."""
        node = convert_to_ast_object(parse_symbol(symbol_uri))
        return py_ast_unparse(node) if node else None

    def exact_search(self, pattern: str) -> ExactSearchResult:
        """Performs a exact search across the indexed codebase."""
        return self._find_pattern_in_modules(pattern)

    def process_query(
        self, query: str
    ) -> Union[
        SymbolReferencesResult,
        SymbolRankResult,
        SourceCodeResult,
        ExactSearchResult,
    ]:
        """
        Processes an NLP-formatted query and returns the results of the appropriate downstream search.

        Raises:
            ValueError: If the query is not formatted correctly
        """
        parts = query.split()
        if len(parts) < 2:
            raise ValueError(
                "Invalid NLP query. It must have at least two parts: 'type:...' and 'query...'"
            )

        search_type = parts[0][len("type:") :].lower()
        query_remainder = " ".join(parts[1:])

        if search_type == "symbol_references":
            return self.symbol_references(query_remainder)
        elif search_type == "symbol_rank":
            return self.get_symbol_rank_results(query_remainder)
        elif search_type == "exact":
            return self.exact_search(query_remainder)
        elif search_type == "source":
            return self.retrieve_source_code_by_symbol(query_remainder)
        else:
            raise ValueError(f"Unknown search type: {search_type}")

    def _find_pattern_in_modules(self, pattern: str) -> Dict[str, List[int]]:
        """Finds exact line matches for a given pattern string in all modules."""
        matches = {}
        for module_path, module in py_module_loader.items():
            if module:
                lines = py_ast_unparse(module).splitlines()
                line_numbers = [
                    i + 1
                    for i, line in enumerate(lines)
                    if pattern in line.strip()
                ]
                if line_numbers:
                    matches[module_path] = line_numbers
        return matches

    def shifted_z_score_powered(
        self, values: Union[List[float], np.ndarray]
    ) -> np.ndarray:
        """
        Calculates the z-score, shifts them to be positive,
        and then raises the values to the specified power.

        This method is used to transform similarity scores into a quantity that
        is more suitable for ranking. Empirically, we found that raising the values
        to the third power results in a good balance between influence from symbol
        similarity and importance (e.g. the connectivity or references to a symbol).
        """

        if not isinstance(values, np.ndarray):
            values = np.array(values)

        mean = np.mean(values)
        std_dev = np.std(values)
        zscores = [(value - mean) / std_dev for value in values]
        return (zscores - np.min(zscores)) ** self.z_score_power

    @staticmethod
    def transform_dict_values(
        dictionary: Dict[Any, float], func: Callable[[List[float]], np.ndarray]
    ) -> Dict[Any, float]:
        """Apply a function to each value in a dictionary and return a new dictionary."""
        # Apply the function to the accumulated values
        transformed_values = func([dictionary[key] for key in dictionary])

        return {key: transformed_values[i] for i, key in enumerate(dictionary)}
