"""
Contains the `GraphBuilder` class, which builds a `SymbolGraph` from a corresponding Index.
"""

import logging
import os
import pickle
from typing import Any

import networkx as nx

from automata.config.config_base import SerializedDataCategory
from automata.symbol.graph.symbol_caller_callees import CallerCalleeProcessor
from automata.symbol.graph.symbol_references import ReferenceProcessor
from automata.symbol.graph.symbol_relationships import RelationshipProcessor
from automata.symbol.scip_pb2 import Index  # type: ignore
from automata.symbol.symbol_parser import parse_symbol
from automata.symbol.symbol_utils import load_data_path

logger = logging.getLogger(__name__)


def _load_index_protobuf(path: str) -> Index:
    """
    Loads and returns an Index protobuf object from the given file path.
    """
    index = Index()
    with open(path, "rb") as f:
        index.ParseFromString(f.read())
    return index


class GraphBuilder:
    """Builds a `SymbolGraph` from a corresponding Index."""

    def __init__(
        self,
        index_path: str,
        build_references: bool,
        build_relationships: bool,
        build_caller_relationships: bool,
    ) -> None:
        """
        Initializes a new instance of `GraphBuilder`.
        """
        self.index_path = index_path
        self.build_references = build_references
        self.build_relationships = build_relationships
        self.build_caller_relationships = build_caller_relationships
        self._graph = nx.MultiDiGraph()
        self.pickled_data_path = load_data_path()

    def build_graph(
        self, from_pickle: bool, save_graph_pickle: bool
    ) -> nx.MultiDiGraph:
        """
        Loop over all the `Documents` in the index of the graph
        and add corresponding `Symbol` nodes to the graph.
        The `Document` type, along with others, is defined in the scip_pb2.py file.
        Edges are added for relationships, references, and calls between `Symbol` nodes.
        """
        os.makedirs(self.pickled_data_path, exist_ok=True)

        graph_pickle_path = os.path.join(
            self.pickled_data_path,
            SerializedDataCategory.PICKLED_SYMBOL_GRAPH.value,
        )

        if not from_pickle or not os.path.exists(graph_pickle_path):
            self.index = (
                None if from_pickle else _load_index_protobuf(self.index_path)
            )
            if self.index is None:
                raise ValueError(
                    "Index file could not be loaded. Please check if the index file exists and is accessible."
                )

            for document in self.index.documents:
                self._add_symbol_vertices(document)
                if self.build_relationships:
                    self._process_relationships(document)
                if self.build_references:
                    self._process_references(document)
                if self.build_caller_relationships:
                    self._process_caller_callee_relationships(document)
            if save_graph_pickle:
                with open(graph_pickle_path, "wb") as f:
                    pickle.dump(self._graph, f)

        else:
            self._graph = pickle.load(open(graph_pickle_path, "rb"))

        return self._graph

    def _add_symbol_vertices(self, document: Any) -> None:
        """Add `Symbol` nodes to the graph."""
        for symbol_information in document.symbols:
            try:
                symbol = parse_symbol(symbol_information.symbol)
            except Exception as e:
                logger.error(
                    f"Parsing symbol {symbol_information.symbol} failed with error {e}"
                )
                continue

            self._graph.add_node(symbol, label="symbol")
            self._graph.add_edge(
                document.relative_path, symbol, label="contains"
            )

    def _process_relationships(self, document: Any) -> None:
        """Add edges for relationships between `Symbol` nodes."""
        for symbol_information in document.symbols:
            relationship_manager = RelationshipProcessor(
                self._graph, symbol_information
            )
            relationship_manager.process()

    def _process_references(self, document: Any) -> None:
        """Process references between `Symbol` nodes."""
        occurrence_manager = ReferenceProcessor(self._graph, document)
        occurrence_manager.process()

    def _process_caller_callee_relationships(self, document: Any) -> None:
        """Process caller-callee relationships between `Symbol` nodes."""
        caller_callee_manager = CallerCalleeProcessor(self._graph, document)
        caller_callee_manager.process()
