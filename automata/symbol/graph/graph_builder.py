import logging
from typing import Any

import networkx as nx

from automata.symbol.graph.caller_callees import CallerCalleeProcessor
from automata.symbol.graph.references import ReferenceProcessor
from automata.symbol.graph.relationships import RelationshipProcessor
from automata.symbol.parser import parse_symbol
from automata.symbol.scip_pb2 import Index  # type: ignore

logger = logging.getLogger(__name__)


class GraphBuilder:
    """Builds a `SymbolGraph` from a corresponding Index."""

    def __init__(
        self,
        index: Index,
        build_references: bool,
        build_relationships: bool,
        build_caller_relationships: bool,
    ) -> None:
        self.index = index
        self.build_references = build_references
        self.build_relationships = build_relationships
        self.build_caller_relationships = build_caller_relationships
        self._graph = nx.MultiDiGraph()

    def build_graph(self) -> nx.MultiDiGraph:
        """
        Loop over all the `Documents` in the index of the graph
        and add corresponding `Symbol` nodes to the graph.
        The `Document` type, along with others, is defined in the scip_pb2.py file.
        Edges are added for relationships, references, and calls between `Symbol` nodes.
        """
        for document in self.index.documents:
            self._add_symbol_vertices(document)
            if self.build_relationships:
                self._process_relationships(document)
            if self.build_references:
                self._process_references(document)
            if self.build_caller_relationships:
                self._process_caller_callee_relationships(document)

        return self._graph

    def _add_symbol_vertices(self, document: Any) -> None:
        for symbol_information in document.symbols:
            try:
                symbol = parse_symbol(symbol_information.symbol)
            except Exception as e:
                logger.error(f"Parsing symbol {symbol_information.symbol} failed with error {e}")
                continue

            self._graph.add_node(symbol, label="symbol")
            self._graph.add_edge(document.relative_path, symbol, label="contains")

    def _process_relationships(self, document: Any) -> None:
        for symbol_information in document.symbols:
            relationship_manager = RelationshipProcessor(self._graph, symbol_information)
            relationship_manager.process()

    def _process_references(self, document: Any) -> None:
        occurrence_manager = ReferenceProcessor(self._graph, document)
        occurrence_manager.process()

    def _process_caller_callee_relationships(self, document: Any) -> None:
        caller_callee_manager = CallerCalleeProcessor(self._graph, document)
        caller_callee_manager.process()
