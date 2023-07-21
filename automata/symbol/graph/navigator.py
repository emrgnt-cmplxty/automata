import logging
from concurrent.futures import ProcessPoolExecutor
from functools import partial
from time import time
from typing import Any, Dict, List, Optional, Set, Tuple

import networkx as nx

from automata.config import MAX_WORKERS
from automata.core import fetch_bounding_box
from automata.singletons.py_module_loader import py_module_loader
from automata.symbol.base import Symbol, SymbolReference
from automata.symbol.symbol_utils import (
    convert_to_ast_object,
    get_rankable_symbols,
)

logger = logging.getLogger(__name__)


def process_symbol_bounds(
    loader_args: Tuple[str, str], symbol: Symbol
) -> Optional[Tuple[Symbol, Any]]:
    """Uses AST to compute the bounding box of a `Symbol`."""
    if not py_module_loader._dotpath_map:
        py_module_loader.initialize(*loader_args)
    try:
        ast_object = convert_to_ast_object(symbol)
        return symbol, fetch_bounding_box(ast_object)
    except Exception as e:
        logger.error(f"Error computing bounding box for {symbol.uri}: {e}")
        return None


class SymbolGraphNavigator:
    """Handles navigation within a symbol graph."""

    def __init__(self, graph: nx.MultiDiGraph) -> None:
        self._graph = graph
        # TODO - Find the correct way to define a bounding box
        self.bounding_box: Dict[
            Symbol, Any
        ] = {}  # Default to empty bounding boxes

    def get_sorted_supported_symbols(self) -> List[Symbol]:
        unsorted_symbols = [
            node
            for node, data in self._graph.nodes(data=True)
            if data.get("label") == "symbol"
        ]
        return sorted(unsorted_symbols, key=lambda x: x.full_dotpath)

    def get_symbol_dependencies(self, symbol: Symbol) -> Set[Symbol]:
        references_in_range = self._get_symbol_references_in_scope(symbol)
        return {ref.symbol for ref in references_in_range}

    def get_symbol_relationships(self, symbol: Symbol) -> Set[Symbol]:
        return {
            target
            for _, target, data in self._graph.out_edges(symbol, data=True)
            if data.get("label") == "relationship"
        }

    def get_references_to_symbol(
        self, symbol: Symbol
    ) -> Dict[str, List[SymbolReference]]:
        """
        Gets all references to a `Symbol`, calculated by finding out edges
        with the label "reference" and the target node being the symbol.
        """
        search_results = [
            (file_path, data.get("symbol_reference"))
            for _, file_path, data in self._graph.out_edges(symbol, data=True)
            if data.get("label") == "reference"
        ]
        result_dict: Dict[str, List[SymbolReference]] = {}

        for file_path, symbol_reference in search_results:
            if file_path in result_dict:
                result_dict[file_path].append(symbol_reference)
            else:
                result_dict[file_path] = [symbol_reference]

        return result_dict

    def get_potential_symbol_callers(
        self, symbol: Symbol
    ) -> Dict[SymbolReference, Symbol]:
        """
        Gets all references to a `Symbol`, calculated by finding out edges
        with the label "callee" and the target node being the symbol caller.
        """
        return {
            SymbolReference(
                symbol=caller,
                line_number=data.get("line_number"),
                column_number=data.get("column_number"),
                roles=data.get("roles"),
            ): callee
            for callee, caller, data in self._graph.out_edges(
                symbol, data=True
            )
            if data.get("label") == "callee"
        }

    def get_potential_symbol_callees(
        self, symbol: Symbol
    ) -> Dict[Symbol, SymbolReference]:
        """
        Gets all references to a `Symbol`, calculated by finding out edges
        with the label "caller" and the target node being the symbol callee.
        """
        return {
            callee: SymbolReference(
                symbol=caller,
                line_number=data.get("line_number"),
                column_number=data.get("column_number"),
                roles=data.get("roles"),
            )
            for caller, callee, data in self._graph.out_edges(
                symbol, data=True
            )
            if data.get("label") == "caller"
        }

    def _get_symbol_containing_file(self, symbol: Symbol) -> str:
        parent_file_list = [
            source
            for source, _, data in self._graph.in_edges(symbol, data=True)
            if data.get("label") == "contains"
        ]
        assert (
            len(parent_file_list) == 1
        ), f"{symbol.uri} should have exactly one parent file, but has {len(parent_file_list)}"
        return parent_file_list.pop()

    def _get_symbol_references_in_scope(
        self, symbol: Symbol
    ) -> List[SymbolReference]:
        """
        Gets all symbol references in the scope of a symbol.
        This is done by finding the bounding box of the symbol,
        and then finding all references in the parent module.
        Notes:
            To cache the bounding boxes before calling this function, call
            `self._pre_compute_rankable_bounding_boxes()`
            This is recommended for scenarios where this function is called
            across the entire
        """
        # bounding boxes are cached
        if len(self.bounding_box) > 0:
            bounding_box = self.bounding_box[symbol]
        else:
            ast_object = convert_to_ast_object(symbol)
            bounding_box = fetch_bounding_box(ast_object)

        (
            parent_symbol_start_line,
            parent_symbol_start_col,
            parent_symbol_end_line,
        ) = (
            bounding_box.top_left.line,
            bounding_box.top_left.column,
            bounding_box.bottom_right.line,
        )

        file_name = self._get_symbol_containing_file(symbol)
        references_in_parent_module = self._get_references_to_module(file_name)
        return [
            ref
            for ref in references_in_parent_module
            if parent_symbol_start_line
            <= ref.line_number
            < parent_symbol_end_line
            and ref.column_number >= parent_symbol_start_col
        ]

    def _get_references_to_module(
        self, module_path: str
    ) -> List[SymbolReference]:
        """Gets all references to a module in the graph."""
        reference_edges_in_module = self._graph.in_edges(
            module_path, data=True
        )
        return [
            data.get("symbol_reference")
            for _, __, data in reference_edges_in_module
            if data["label"] == "reference"
        ]

    def _pre_compute_rankable_bounding_boxes(self) -> None:
        """Pre-computes and caches the bounding boxes for all symbols in the graph."""
        now = time()
        # Bounding boxes are already loaded
        if len(self.bounding_box) > 0:
            return

        logger.info("Pre-computing bounding boxes for all rankable symbols")
        filtered_symbols = get_rankable_symbols(
            self.get_sorted_supported_symbols()
        )

        # prepare loader_args here (replace this comment with actual code)
        if not py_module_loader.initialized:
            raise ValueError(
                "Module loader must be initialized before pre-computing bounding boxes"
            )
        loader_args: Tuple[str, str] = (
            py_module_loader.root_fpath or "",
            py_module_loader.project_name or "",
        )
        bounding_boxes = {}
        with ProcessPoolExecutor(max_workers=MAX_WORKERS) as executor:
            func = partial(process_symbol_bounds, loader_args)
            results = executor.map(func, filtered_symbols)
            for result in results:
                if result is not None:
                    symbol, bounding_box = result
                    bounding_boxes[symbol] = bounding_box

        logger.info(
            f"Finished pre-computing bounding boxes for all rankable symbols in {time() - now} seconds"
        )
        self.bounding_box = bounding_boxes
