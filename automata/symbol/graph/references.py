import logging
from typing import Any, Dict

import networkx as nx

from automata.symbol.base import SymbolReference
from automata.symbol.graph.base import GraphProcessor
from automata.symbol.parser import parse_symbol

from ..scip_pb2 import SymbolRole  # type: ignore

logger = logging.getLogger(__name__)


class ReferenceProcessor(GraphProcessor):
    """Adds edges to the `MultiDiGraph` for references between `Symbol` nodes."""

    def __init__(self, graph: nx.MultiDiGraph, document: Any) -> None:
        self._graph = graph
        self.document = document

    def process(self) -> None:
        """
        Adds edges in the local `MultiDiGraph` for references between `Symbol` nodes.
        A reference is the usage of a symbol in a particular context.
        For example, a reference can be a function call, a variable usage,
        or a class instantiation.
        """
        for occurrence in self.document.occurrences:
            try:
                occurrence_symbol = parse_symbol(occurrence.symbol)
            except Exception as e:
                logger.error(
                    f"Parsing symbol {occurrence.symbol} failed with error {e}"
                )
                continue

            occurrence_range = tuple(occurrence.range)
            occurrence_roles = ReferenceProcessor._process_symbol_roles(
                occurrence.symbol_roles
            )
            occurrence_reference = SymbolReference(
                symbol=occurrence_symbol,
                line_number=occurrence_range[0],
                column_number=occurrence_range[1],
                roles=occurrence_roles,
            )
            self._graph.add_edge(
                occurrence_symbol,
                self.document.relative_path,
                symbol_reference=occurrence_reference,
                label="reference",
            )
            if occurrence_roles.get(SymbolRole.Name(SymbolRole.Definition)):
                # TODO this is gross
                incorrect_contains_edges = [
                    (source, target)
                    for source, target, data in self._graph.in_edges(
                        occurrence_symbol, data=True
                    )
                    if data.get("label") == "contains"
                ]
                for source, target in incorrect_contains_edges:
                    self._graph.remove_edge(source, target)

                self._graph.add_edge(
                    self.document.relative_path,
                    occurrence_symbol,
                    label="contains",
                )

    @staticmethod
    def _process_symbol_roles(role: int) -> Dict[str, bool]:
        return {
            role_name: (role & role_value) > 0
            for role_name, role_value in SymbolRole.items()
            if (role & role_value) > 0
        }
