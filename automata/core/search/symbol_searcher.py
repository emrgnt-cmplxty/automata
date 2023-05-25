from copy import deepcopy
from typing import Dict, List, Optional, Tuple, Union

import networkx as nx

from automata.core.search.symbol_converter import SymbolConverter
from automata.core.search.symbol_graph import SymbolGraph
from automata.core.search.symbol_parser import parse_symbol
from automata.core.search.symbol_rank.symbol_embedding_map import SymbolEmbeddingMap
from automata.core.search.symbol_rank.symbol_rank import SymbolRank, SymbolRankConfig
from automata.core.search.symbol_rank.symbol_similarity import SymbolSimilarity
from automata.core.search.symbol_types import StrPath, Symbol, SymbolEmbedding, SymbolReference
from automata.core.search.symbol_utils import (
    find_and_replace_in_modules,
    find_pattern_in_modules,
    shifted_z_score_sq,
    sync_graph_and_dict,
    transform_dict_values,
)

SymbolReferencesResult = Dict[StrPath, List[SymbolReference]]
SymbolRankResult = List[Tuple[str, float]]
SourceCodeResult = Optional[str]
ExactSearchResult = Dict[str, List[int]]
FindAndReplaceResult = int


class SymbolSearcher:
    def __init__(
        self,
        symbol_converter: SymbolConverter,
        symbol_graph: SymbolGraph,
        symbol_embedding_map: SymbolEmbeddingMap,
        symbol_similarity: SymbolSimilarity,
        symbol_rank_config: Optional[SymbolRankConfig],
        code_subgraph: Optional[nx.DiGraph] = None,
        embedding_dict: Optional[Dict[Symbol, SymbolEmbedding]] = None,
        *args,
        **kwargs,
    ):
        self.converter = symbol_converter
        self.symbol_graph = symbol_graph
        self.symbol_similarity = symbol_similarity

        if not code_subgraph:
            code_subgraph = symbol_graph.get_rankable_symbol_subgraph(
                kwargs.get("flow_rank", "bidirectional")
            )
        if not embedding_dict:
            embedding_dict = deepcopy(symbol_embedding_map.get_embedding_dict())

        code_subgraph, embedding_dict = sync_graph_and_dict(code_subgraph, embedding_dict)

        self.symbol_rank = SymbolRank(code_subgraph, config=symbol_rank_config)
        self.code_subgraph = code_subgraph
        self.embedding_dict = embedding_dict

    def symbol_rank_search(self, query: str) -> SymbolRankResult:
        """
        Fetches the list of the SymbolRank similar symbols ordered by rank

        Args:
            query (str): The query to search for

        Returns:
            A list of tuples of the form (symbol_uri, rank)
        """

        query_vec = self.symbol_similarity.get_query_similarity_dict(query)
        transformed_query_vec = transform_dict_values(query_vec, shifted_z_score_sq)
        ranks = self.symbol_rank.get_ranks(symbol_similarity=transformed_query_vec)
        return ranks

    def symbol_references(self, symbol_uri: str) -> SymbolReferencesResult:
        """
        Gets the list a symbol-based search

        Args:
            symbol_uri (str): The symbol to search for

        Returns:
            A dict of paths to files that contain the symbol and corresponding line numbers
        """
        # TODO - Add parsing upstream or here to parse references
        return self.symbol_graph.get_references_to_symbol(parse_symbol(symbol_uri))

    def retrieve_source_code_by_symbol(self, symbol_uri: str) -> SourceCodeResult:
        """
        Finds the raw text of a module, class, method, or standalone function

        Args:
            symbol_uri (str): The symbol to retrieve

        Returns:
            The raw text of the symbol or None if not found
        """
        node = self.converter.convert_to_fst_object(parse_symbol(symbol_uri))
        return str(node) if node is not None else None

    def exact_search(self, pattern: str) -> ExactSearchResult:
        """
        Performs a exact search across the indexed codebase

        Args:
            pattern (str): The pattern to search for

        Returns:
            A dict of paths to files that contain the pattern and corresponding line numbers
        """
        return find_pattern_in_modules(self.converter, pattern)

    def find_and_replace(self, find: str, replace: str, do_write: bool) -> FindAndReplaceResult:
        """
        Performs a exact replace on the in-memory codebase and write the result

        Args:
            find (str): The string to find
            replace (str): The string to replace
            do_write (bool): Whether to write the result to disk

        Returns:
            The number of replacements made
        """
        return find_and_replace_in_modules(self.converter, find, replace, do_write)

    def process_query(
        self, query: str
    ) -> Union[
        SymbolReferencesResult,
        SymbolRankResult,
        SourceCodeResult,
        ExactSearchResult,
        FindAndReplaceResult,
    ]:
        """
        Processes an NLP-formatted query and return the results of the appropriate search

        Args:
            query: The query to process

        Returns:
            The results of the search
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
        elif search_type == "replace":
            find, replace, do_write = query_remainder.split(" ")
            assert do_write in ["True", "False"]
            return self.find_and_replace(find, replace, do_write == "True")
        else:
            raise ValueError(f"Unknown search type: {search_type}")
