from copy import deepcopy
from typing import Any, Callable, Dict, List, Optional, Set, Tuple, Union

import networkx as nx
import numpy as np

from automata.core.coding.py.module_loader import py_module_loader
from automata.core.embedding.symbol_similarity import SymbolSimilarityCalculator
from automata.core.symbol.graph import SymbolGraph
from automata.core.symbol.parser import parse_symbol
from automata.core.symbol.search.rank import SymbolRank, SymbolRankConfig
from automata.core.symbol.symbol_types import Symbol, SymbolReference
from automata.core.symbol.symbol_utils import convert_to_fst_object

SymbolReferencesResult = Dict[str, List[SymbolReference]]
SymbolRankResult = List[Tuple[Symbol, float]]
SourceCodeResult = Optional[str]
ExactSearchResult = Dict[str, List[int]]


class SymbolSearch:
    """A class which exposes various search methods for symbols."""

    def __init__(
        self,
        symbol_graph: SymbolGraph,
        symbol_code_similarity: SymbolSimilarityCalculator,
        symbol_rank_config: SymbolRankConfig,
        code_subgraph: SymbolGraph.SubGraph,
    ) -> None:
        """
        Raises:
            ValueError: If the code_subgraph is not a subgraph of the symbol_graph
        TODO - We should modify SymbolSearch to receive a completed instance of SymbolRank.
        """

        if code_subgraph.parent != symbol_graph:
            raise ValueError("code_subgraph must be a subgraph of symbol_graph")

        graph_symbols = symbol_graph.get_all_available_symbols()
        embedding_symbols = symbol_code_similarity.embedding_handler.get_all_supported_symbols()
        available_symbols = set(graph_symbols).intersection(set(embedding_symbols))
        SymbolSearch.filter_graph(code_subgraph.graph, available_symbols)

        # TODO - Do we need to filter the SymbolGraph as well?
        self.symbol_graph = symbol_graph
        self.symbol_code_similarity = symbol_code_similarity
        symbol_code_similarity.set_available_symbols(available_symbols)
        self.symbol_rank = SymbolRank(code_subgraph.graph, config=symbol_rank_config)

    def symbol_rank_search(self, query: str) -> SymbolRankResult:
        """Fetches the list of the SymbolRank similar symbols ordered by rank."""
        query_vec = self.symbol_code_similarity.calculate_query_similarity_dict(query)
        transformed_query_vec = SymbolSearch.transform_dict_values(
            query_vec, SymbolSearch.shifted_z_score_powered
        )
        return self.symbol_rank.get_ranks(query_to_symbol_similarity=transformed_query_vec)

    def symbol_references(self, symbol_uri: str) -> SymbolReferencesResult:
        """
        Finds all references to a module, class, method, or standalone function.

        TODO - Add parsing upstream or here to parse references
        """
        return self.symbol_graph.get_references_to_symbol(parse_symbol(symbol_uri))

    def retrieve_source_code_by_symbol(self, symbol_uri: str) -> SourceCodeResult:
        """Finds the raw text of a module, class, method, or standalone function."""
        node = convert_to_fst_object(parse_symbol(symbol_uri))
        return str(node) if node else None

    def exact_search(self, pattern: str) -> ExactSearchResult:
        """Performs a exact search across the indexed codebase."""
        return self._find_pattern_in_modules(pattern)

    def process_query(
        self, query: str
    ) -> Union[SymbolReferencesResult, SymbolRankResult, SourceCodeResult, ExactSearchResult,]:
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
            return self.symbol_rank_search(query_remainder)
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
                lines = module.dumps().splitlines()
                line_numbers = [i + 1 for i, line in enumerate(lines) if pattern in line.strip()]
                if line_numbers:
                    matches[module_path] = line_numbers
        return matches

    @staticmethod
    def filter_graph(graph: nx.DiGraph, available_symbols: Set[Symbol]) -> None:
        """Filters a graph to only contain nodes that are in the available_symbols set."""
        graph_nodes = deepcopy(graph.nodes())
        for symbol in graph_nodes:
            if symbol not in available_symbols:
                graph.remove_node(symbol)

    @staticmethod
    def shifted_z_score_powered(
        values: Union[List[float], np.ndarray], power: int = 3
    ) -> np.ndarray:
        """
        Shifts the values to be positive, calculates the z-score,
        and raises the values to the specified power.

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
        return (zscores - np.min(zscores)) ** power

    @staticmethod
    def transform_dict_values(
        dictionary: Dict[Any, float], func: Callable[[List[float]], np.ndarray]
    ) -> Dict[Any, float]:
        """Apply a function to each value in a dictionary and return a new dictionary."""
        # Apply the function to the accumulated values
        transformed_values = func([dictionary[key] for key in dictionary])

        return {key: transformed_values[i] for i, key in enumerate(dictionary)}
