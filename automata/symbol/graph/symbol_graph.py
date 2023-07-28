import logging
import pickle
from copy import deepcopy
from functools import lru_cache
from typing import Dict, List, Optional, Set

import networkx as nx
from tqdm import tqdm

from automata.embedding.data_root_settings import data_root_path
from automata.symbol.graph.graph_builder import GraphBuilder
from automata.symbol.graph.symbol_navigator import SymbolGraphNavigator
from automata.symbol.scip_pb2 import Index  # type: ignore
from automata.symbol.symbol_base import (
    ISymbolProvider,
    Symbol,
    SymbolReference,
)
from automata.symbol.symbol_utils import get_rankable_symbols

logger = logging.getLogger(__name__)


class SymbolGraph(ISymbolProvider):
    """
    A `SymbolGraph` contains the symbols and relationships between them.e
    Currently, nodes are files and symbols, and edges consist of either
    "contains", "reference", "relationship", "caller", or "callee".
    """

    def __init__(
        self,
        index_path: str,
        build_references: bool = True,
        build_relationships: bool = True,
        build_caller_relationships: bool = False,
        pickle_graph: bool = True,
    ) -> None:
        super().__init__()
        index = self._load_index_protobuf(index_path)
        builder = GraphBuilder(
            index,
            build_references,
            build_relationships,
            build_caller_relationships,
        )
        self._graph = builder.build_graph()
        self.navigator = SymbolGraphNavigator(self._graph)

        if pickle_graph:
            with open(f"{data_root_path}/symbol_graph.pkl", "wb") as f:
                pickle.dump(self._graph, f)

    def get_symbol_dependencies(self, symbol: Symbol) -> Set[Symbol]:
        return self.navigator.get_symbol_dependencies(symbol)

    def get_symbol_relationships(self, symbol: Symbol) -> Set[Symbol]:
        """
        Gets the set of symbols with relationships to the given symbol.
        # TODO: Consider the implications of using a List instead of Set.
        """
        return self.navigator.get_symbol_relationships(symbol)

    def get_potential_symbol_callers(
        self, symbol: Symbol
    ) -> Dict[SymbolReference, Symbol]:
        """
        Gets the callees of the given symbol.
        Downstream filtering must be applied to remove non-call relationships.
        """
        return self.navigator.get_potential_symbol_callers(symbol)

    def get_potential_symbol_callees(
        self, symbol: Symbol
    ) -> Dict[Symbol, SymbolReference]:
        """
        Gets the callees of the given symbol.
        Downstream filtering must be applied to remove non-callee relationships.
        """
        return self.navigator.get_potential_symbol_callees(symbol)

    def get_references_to_symbol(
        self, symbol: Symbol
    ) -> Dict[str, List[SymbolReference]]:
        return self.navigator.get_references_to_symbol(symbol)

    @property
    def default_rankable_subgraph(self) -> nx.DiGraph:
        return self._build_default_rankable_subgraph()

    @lru_cache(maxsize=1)
    def _build_default_rankable_subgraph(self) -> nx.DiGraph:
        return self._build_rankable_subgraph()

    def _build_rankable_subgraph(
        self, path_filter: Optional[str] = None
    ) -> nx.DiGraph:
        """
        Creates a subgraph of the original `SymbolGraph` which
        contains only rankable symbols. The nodes in the subgraph
        are rankable symbols, and the edges are the dependencies
        between them.

        TODO - Think of how to handle relationships here.
        """
        G = nx.DiGraph()

        filtered_symbols = get_rankable_symbols(
            self.get_sorted_supported_symbols()
        )

        if path_filter is not None:
            filtered_symbols = [
                sym for sym in filtered_symbols if sym.full_dotpath.startswith(path_filter)  # type: ignore
            ]

        self.navigator._pre_compute_rankable_bounding_boxes()

        logger.info("Building the rankable symbol subgraph...")
        for symbol in tqdm(filtered_symbols):
            try:
                dependencies = [
                    ele
                    for ele in self.get_symbol_dependencies(symbol)
                    if ele in self.get_sorted_supported_symbols()
                ]
                for dependency in dependencies:
                    G.add_edge(symbol, dependency)
                    G.add_edge(dependency, symbol)
            except Exception as e:
                logger.error(f"Error processing {symbol.uri}: {e}")

        logger.info("Built the rankable symbol subgraph")
        return G

    # ISymbolProvider methods
    def _get_sorted_supported_symbols(self) -> List[Symbol]:
        return self.navigator.get_sorted_supported_symbols()

    def filter_symbols(self, sorted_supported_symbols: List[Symbol]):
        if self._graph:
            graph_nodes_and_data = deepcopy(self._graph.nodes(data=True))
            for node, data in graph_nodes_and_data:
                if (
                    data.get("label") == "symbol"
                    and node not in sorted_supported_symbols
                ):
                    self._graph.remove_node(node)

    @staticmethod
    def _load_index_protobuf(path: str) -> Index:
        index = Index()
        with open(path, "rb") as f:
            index.ParseFromString(f.read())
        return index

    @classmethod
    def from_graph(cls, graph: nx.MultiDiGraph) -> "SymbolGraph":
        instance = cls.__new__(cls)

        instance._graph = graph

        instance.navigator = SymbolGraphNavigator(instance._graph)

        return instance
