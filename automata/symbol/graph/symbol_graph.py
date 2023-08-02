"""
Contains the `SymbolGraph` class and all logic related to building symbol graphs and subgraphs.
"""


import logging
import os
import pickle
from copy import deepcopy
from functools import lru_cache
from typing import Dict, List, Optional, Set

import networkx as nx
from tqdm import tqdm

from automata.config import GRAPH_TYPE
from automata.config.config_base import SerializedDataCategory
from automata.symbol.graph.graph_builder import GraphBuilder
from automata.symbol.graph.symbol_navigator import SymbolGraphNavigator
from automata.symbol.scip_pb2 import Index  # type: ignore
from automata.symbol.symbol_base import (
    ISymbolProvider,
    Symbol,
    SymbolReference,
)
from automata.symbol.symbol_utils import get_rankable_symbols, load_data_path

logger = logging.getLogger(__name__)


def _load_index_protobuf(path: str) -> Index:
    """
    Loads and returns an Index protobuf object from the given file path.
    """
    index = Index()
    with open(path, "rb") as f:
        index.ParseFromString(f.read())
    return index


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
        from_pickle: bool = GRAPH_TYPE == "static",
        save_graph_pickle: bool = True,
    ) -> None:
        """
        Initializes a new instance of `SymbolGraph`.
        """
        super().__init__()
        index = _load_index_protobuf(index_path)
        builder = GraphBuilder(
            index,
            build_references,
            build_relationships,
            build_caller_relationships,
        )
        self._graph = builder.build_graph(from_pickle, save_graph_pickle)
        self.navigator = SymbolGraphNavigator(self._graph)
        self.from_pickle = from_pickle
        self.pickled_data_path = load_data_path()
        self.subgraph_pickle_path = os.path.join(
            self.pickled_data_path,
            SerializedDataCategory.PICKLED_SYMBOL_SUBGRAPH.value,
        )
        self.save_graph_pickle = save_graph_pickle

    def get_symbol_dependencies(self, symbol: Symbol) -> Set[Symbol]:
        """
        Returns the set of symbols that the given symbol depends on. This means any symbols that the input symbol
        directly references or uses.
        """
        return self.navigator.get_symbol_dependencies(symbol)

    def get_symbol_relationships(self, symbol: Symbol) -> Set[Symbol]:
        """
        Returns the set of symbols with relationships to the given symbol. In this context, a "relationship" refers to
        any type of connection between the input symbol and other symbols, including dependencies, usages, references, etc.

        # TODO: Consider the implications of using a List instead of Set.
        """
        return self.navigator.get_symbol_relationships(symbol)

    def get_potential_symbol_callers(
        self, symbol: Symbol
    ) -> Dict[SymbolReference, Symbol]:
        """
        Gets the potential callers of the given symbol. This includes any symbols that might be making a call
        to the given symbol. Downstream filtering must be applied to remove non-call relationships.

        """
        return self.navigator.get_potential_symbol_callers(symbol)

    def get_potential_symbol_callees(
        self, symbol: Symbol
    ) -> Dict[Symbol, SymbolReference]:
        """
        Gets potential callees of the given symbol. This includes any symbols that the given symbol might be calling.
        Downstream filtering must be applied to remove relationships that are not 'calls'.
        """
        return self.navigator.get_potential_symbol_callees(symbol)

    def get_references_to_symbol(
        self, symbol: Symbol
    ) -> Dict[str, List[SymbolReference]]:
        """
        Gets the references to the given symbol in the graph. This includes all places in the codebase where
        the given symbol is used or called.
        """
        return self.navigator.get_references_to_symbol(symbol)

    @property
    def default_rankable_subgraph(self) -> nx.DiGraph:
        """
        Gets the default rankable subgraph. This subgraph contains only the nodes and edges of the original
        graph that can be ranked. This may be a cached version of the graph for faster loading.
        """
        return self._build_default_rankable_subgraph()

    @lru_cache(maxsize=1)
    def _build_default_rankable_subgraph(self) -> nx.DiGraph:
        """
        Creates a subgraph of the original `SymbolGraph`
        """
        os.makedirs(self.pickled_data_path, exist_ok=True)

        if not self.from_pickle or not os.path.exists(
            self.subgraph_pickle_path
        ):
            subgraph = self._build_rankable_subgraph()

            if self.save_graph_pickle:
                with open(self.subgraph_pickle_path, "wb") as f:
                    pickle.dump(subgraph, f)

        else:
            subgraph = pickle.load(open(self.subgraph_pickle_path, "rb"))

        return subgraph

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
        graph = nx.DiGraph()

        filtered_symbols = get_rankable_symbols(
            self.get_sorted_supported_symbols()
        )

        if path_filter is not None:
            filtered_symbols = [
                sym for sym in filtered_symbols if sym.dotpath.startswith(path_filter)  # type: ignore
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
                    graph.add_edge(symbol, dependency)
                    graph.add_edge(dependency, symbol)
            except Exception as e:
                logger.error(f"Error processing {symbol.uri}: {e}")

        logger.info("Built the rankable symbol subgraph")
        return graph

    # ISymbolProvider methods
    def _get_sorted_supported_symbols(self) -> List[Symbol]:
        return self.navigator.get_sorted_supported_symbols()

    def filter_symbols(self, sorted_supported_symbols: List[Symbol]) -> None:
        """
        Modifies the graph in-place by removing all symbol nodes that are not present in
        the given list, 'sorted_supported_symbols'. The list should contain
        symbol instances that are a part of the graph. If the graph doesn't exist, this function does nothing.
        """
        if self._graph:
            graph_nodes_and_data = deepcopy(self._graph.nodes(data=True))
            for node, data in graph_nodes_and_data:
                if (
                    data.get("label") == "symbol"
                    and node not in sorted_supported_symbols
                ):
                    self._graph.remove_node(node)

    @classmethod
    def from_graph(cls, graph: nx.MultiDiGraph) -> "SymbolGraph":
        """
        Creates a new `SymbolGraph` instance from an existing networkx MultiDiGraph object.
        """
        instance = cls.__new__(cls)

        instance._graph = graph

        instance.navigator = SymbolGraphNavigator(instance._graph)

        return instance
