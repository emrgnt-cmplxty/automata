import logging
from typing import Any

import networkx as nx

from automata.symbol.graph.symbol_graph_base import GraphProcessor
from automata.symbol.graph.symbol_navigator import SymbolGraphNavigator
from automata.symbol.symbol_base import SymbolDescriptor
from automata.symbol.symbol_parser import parse_symbol

logger = logging.getLogger(__name__)


class CallerCalleeProcessor(GraphProcessor):
    """Adds edges to the `MultiDiGraph` for caller-callee relationships between `Symbol` nodes."""

    def __init__(self, graph: nx.MultiDiGraph, document: Any) -> None:
        self._graph = graph
        self.navigator = SymbolGraphNavigator(graph)
        self.document = document

    def process(self) -> None:
        """
        Adds edges in the local `MultiDiGraph` for caller-callee between `Symbol` nodes.
        One symbol is a caller of another symbol if it performs a call to that symbol.
        E.g. `foo()` is a caller of `bar()` in `foo(bar())`.
        Note - Construction is an expensive operation and should be used sparingly.
        TODO - Split this method into smaller methods.
        """
        for symbol in self.document.symbols:
            try:
                symbol_object = parse_symbol(symbol.symbol)
            except Exception as e:
                logger.error(
                    f"Parsing symbol {symbol.symbol} failed with error {e}"
                )
                continue

            if symbol_object.py_kind != SymbolDescriptor.PyKind.Method:
                continue

            try:
                references_in_scope = (
                    self.navigator._get_symbol_references_in_scope(
                        symbol_object
                    )
                )
            except Exception as e:
                logger.error(
                    f"Failed to get references in scope for symbol {symbol} with error {e}"
                )
                continue

            for ref in references_in_scope:
                try:
                    if ref.symbol.py_kind in [
                        SymbolDescriptor.PyKind.Method,
                        SymbolDescriptor.PyKind.Class,
                    ]:
                        if ref.symbol == symbol_object:
                            continue
                        # TODO - This approach will include non-call statements, like return statements
                        # unfortunately, this seems necessary to get the full set of callers
                        # e.g. omitting classes appears to remove constructor calls for X, like X()
                        # For, we filtering is done downstream with the ASTNavigator
                        # with current understanding, it seems handling will require AST awareness
                        self._graph.add_edge(
                            symbol_object,
                            ref.symbol,
                            line_number=ref.line_number,
                            column_number=ref.column_number,
                            roles=ref.roles,
                            label="caller",
                        )
                        self._graph.add_edge(
                            ref.symbol,
                            symbol_object,
                            line_number=ref.line_number,
                            column_number=ref.column_number,
                            roles=ref.roles,
                            label="callee",
                        )
                except Exception as e:
                    logger.error(
                        f"Failed to add caller-callee edge for {symbol} with error {e} "
                    )
                    continue
