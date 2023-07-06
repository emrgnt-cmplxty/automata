import logging
from abc import ABC, abstractmethod
from concurrent.futures import ProcessPoolExecutor
from functools import lru_cache, partial
from time import time
from typing import Any, Dict, List, Optional, Set, Tuple

import networkx as nx
from google.protobuf.json_format import MessageToDict  # type: ignore
from tqdm import tqdm

from automata.config import MAX_WORKERS
from automata.core.utils import filter_multi_digraph_by_symbols
from automata.singletons.py_module_loader import py_module_loader
from automata.symbol.base import (
    ISymbolProvider,
    Symbol,
    SymbolDescriptor,
    SymbolReference,
)
from automata.symbol.parser import parse_symbol
from automata.symbol.scip_pb2 import Index, SymbolRole  # type: ignore
from automata.symbol.symbol_utils import convert_to_fst_object, get_rankable_symbols

logger = logging.getLogger(__name__)


class GraphProcessor(ABC):
    """Abstract base class for processing edges in the `MultiDiGraph`."""

    @abstractmethod
    def process(self) -> None:
        """Adds new edges of the specified type to the graph."""
        pass


class _RelationshipProcessor(GraphProcessor):
    """Adds edges to the `MultiDiGraph` for relationships between `Symbol` nodes."""

    def __init__(self, graph: nx.MultiDiGraph, symbol_information: Any) -> None:
        self._graph = graph
        self.symbol_information = symbol_information

    def process(self) -> None:
        """
        Adds edges in the local `MultiDiGraph` for relationships between `Symbol` nodes.

        Two `Symbols` are related if they share an inheritance relationship.

        See below for example - the `Dog` class inherits from the `Animal` class,
        so the `Dog` class is related to the `Animal` class.

        When resolving "Find references", this field documents what other symbols
        should be included together with this symbol. For example, consider the
        following TypeScript code that defines two symbols `Animal#sound()` and
        `Dog#sound()`:
        ```ts
        interface Animal {
                  ^^^^^^ definition Animal#
          sound(): string
          ^^^^^ definition Animal#sound()
        }
        class Dog implements Animal {
              ^^^ definition Dog#, relationships = [{symbol: "Animal#", is_implementation: true}]
          public sound(): string { return "woof" }
                 ^^^^^ definition Dog#sound(), references_symbols = Animal#sound(), relationships = [{symbol: "Animal#sound()", is_implementation:true, is_reference: true}]
        }
        const animal: Animal = new Dog()
                      ^^^^^^ reference Animal#
        console.log(animal.sound())
                           ^^^^^ reference Animal#sound()
        ```
        Doing "Find references" on the symbol `Animal#sound()` should return
        references to the `Dog#sound()` method as well. Vice-versa, doing "Find
        references" on the `Dog#sound()` method should include references to the
        `Animal#sound()` method as well.
        """
        for relationship in self.symbol_information.relationships:
            relationship_labels = MessageToDict(relationship)
            relationship_labels.pop("symbol")
            related_symbol = parse_symbol(relationship.symbol)
            self._graph.add_edge(
                self.symbol_information.symbol,
                related_symbol,
                label="relationship",
                **relationship_labels,
            )


class _ReferenceProcessor(GraphProcessor):
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
                logger.error(f"Parsing symbol {occurrence.symbol} failed with error {e}")
                continue

            occurrence_range = tuple(occurrence.range)
            occurrence_roles = _ReferenceProcessor._process_symbol_roles(occurrence.symbol_roles)
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
                    for source, target, data in self._graph.in_edges(occurrence_symbol, data=True)
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


class _CallerCalleeProcessor(GraphProcessor):
    """Adds edges to the `MultiDiGraph` for caller-callee relationships between `Symbol` nodes."""

    def __init__(self, graph: nx.MultiDiGraph, document: Any) -> None:
        self._graph = graph
        self.navigator = _SymbolGraphNavigator(graph)
        self.document = document

    def process(self) -> None:
        """
        Adds edges in the local `MultiDiGraph` for caller-callee between `Symbol` nodes.

        One symbol is a caller of another symbol if it performs a call to that symbol.
        E.g. `foo()` is a caller of `bar()` in `foo(bar())`.

        Note - Construction is an expensive operation and should be used sparingly.
        """
        for symbol in self.document.symbols:
            try:
                symbol_object = parse_symbol(symbol.symbol)
            except Exception as e:
                logger.error(f"Parsing symbol {symbol.symbol} failed with error {e}")
                continue

            if symbol_object.symbol_kind_by_suffix() != SymbolDescriptor.PyKind.Method:
                continue

            try:
                references_in_scope = self.navigator._get_symbol_references_in_scope(symbol_object)
            except Exception as e:
                logger.error(
                    f"Failed to get references in scope for symbol {symbol} with error {e}"
                )
                continue

            for ref in references_in_scope:
                try:
                    if ref.symbol.symbol_kind_by_suffix() in [
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
                    logger.error(f"Failed to add caller-callee edge for {symbol} with error {e} ")
                    continue


class GraphBuilder:
    """Builds a `SymbolGraph` from a corresponding Index."""

    def __init__(self, index: Index, build_caller_relationships: bool = False) -> None:
        self.index = index
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
            self._process_relationships(document)
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
            relationship_manager = _RelationshipProcessor(self._graph, symbol_information)
            relationship_manager.process()

    def _process_references(self, document: Any) -> None:
        occurrence_manager = _ReferenceProcessor(self._graph, document)
        occurrence_manager.process()

    def _process_caller_callee_relationships(self, document: Any) -> None:
        caller_callee_manager = _CallerCalleeProcessor(self._graph, document)
        caller_callee_manager.process()


def process_symbol_bounds(
    loader_args: Tuple[str, str], symbol: Symbol
) -> Optional[Tuple[Symbol, Any]]:
    """Uses RedBaron FST to compute the bounding box of a `Symbol`."""
    if not py_module_loader._dotpath_map:
        py_module_loader.initialize(*loader_args)
    try:
        fst_object = convert_to_fst_object(symbol)
        bounding_box = fst_object.absolute_bounding_box
        return symbol, bounding_box
    except Exception as e:
        logger.error(f"Error computing bounding box for {symbol.uri}: {e}")
        return None


class _SymbolGraphNavigator:
    """Handles navigation within a symbol graph."""

    def __init__(self, graph: nx.MultiDiGraph) -> None:
        self._graph = graph
        # TODO - Find the correct way to define a bounding box
        self.bounding_box: Dict[Symbol, Any] = {}  # Default to empty bounding boxes

    def get_sorted_supported_symbols(self) -> List[Symbol]:
        unsorted_symbols = [
            node for node, data in self._graph.nodes(data=True) if data.get("label") == "symbol"
        ]
        return sorted(unsorted_symbols, key=lambda x: x.dotpath)

    def get_symbol_dependencies(self, symbol: Symbol) -> Set[Symbol]:
        references_in_range = self._get_symbol_references_in_scope(symbol)
        return {ref.symbol for ref in references_in_range}

    def get_symbol_relationships(self, symbol: Symbol) -> Set[Symbol]:
        return {
            target
            for _, target, data in self._graph.out_edges(symbol, data=True)
            if data.get("label") == "relationship"
        }

    def get_references_to_symbol(self, symbol: Symbol) -> Dict[str, List[SymbolReference]]:
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

    def get_potential_symbol_callers(self, symbol: Symbol) -> Dict[SymbolReference, Symbol]:
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
            for callee, caller, data in self._graph.out_edges(symbol, data=True)
            if data.get("label") == "callee"
        }

    def get_potential_symbol_callees(self, symbol: Symbol) -> Dict[Symbol, SymbolReference]:
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
            for caller, callee, data in self._graph.out_edges(symbol, data=True)
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

    def _get_symbol_references_in_scope(self, symbol: Symbol) -> List[SymbolReference]:
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
            fst_object = convert_to_fst_object(symbol)
            bounding_box = fst_object.absolute_bounding_box

        # RedBaron POSITIONS ARE 1 INDEXED AND SCIP ARE 0!!!!
        parent_symbol_start_line, parent_symbol_start_col, parent_symbol_end_line = (
            bounding_box.top_left.line - 1,
            bounding_box.top_left.column - 1,
            bounding_box.bottom_right.line - 1,
        )

        file_name = self._get_symbol_containing_file(symbol)
        references_in_parent_module = self._get_references_to_module(file_name)
        return [
            ref
            for ref in references_in_parent_module
            if parent_symbol_start_line <= ref.line_number < parent_symbol_end_line
            and ref.column_number >= parent_symbol_start_col
        ]

    def _get_references_to_module(self, module_name: str) -> List[SymbolReference]:
        """Gets all references to a module in the graph."""
        reference_edges_in_module = self._graph.in_edges(module_name, data=True)
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
        filtered_symbols = get_rankable_symbols(self.get_sorted_supported_symbols())

        # prepare loader_args here (replace this comment with actual code)
        if not py_module_loader.initialized:
            raise ValueError(
                "Module loader must be initialized before pre-computing bounding boxes"
            )
        loader_args: Tuple[str, str] = (
            py_module_loader.root_fpath or "",
            py_module_loader.py_fpath or "",
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


class SymbolGraph(ISymbolProvider):
    """
    A SymbolGraph contains the symbols and relationships between them.
    Currently, nodes are files and symbols, and edges consist of either
    "contains", "reference", "relationship", "caller", or "callee".
    """

    def __init__(self, index_path: str, build_caller_relationships: bool = False) -> None:
        super().__init__()
        index = self._load_index_protobuf(index_path)
        builder = GraphBuilder(index, build_caller_relationships)
        self._graph = builder.build_graph()
        self.navigator = _SymbolGraphNavigator(self._graph)

    def get_symbol_dependencies(self, symbol: Symbol) -> Set[Symbol]:
        return self.navigator.get_symbol_dependencies(symbol)

    def get_symbol_relationships(self, symbol: Symbol) -> Set[Symbol]:
        """
        Gets the set of symbols with relationships to the given symbol.
        # TODO: Consider the implications of using a List instead of Set.
        """
        return self.navigator.get_symbol_relationships(symbol)

    def get_potential_symbol_callers(self, symbol: Symbol) -> Dict[SymbolReference, Symbol]:
        """
        Gets the callees of the given symbol.
        Downstream filtering must be applied to remove non-call relationships.
        """
        return self.navigator.get_potential_symbol_callers(symbol)

    def get_potential_symbol_callees(self, symbol: Symbol) -> Dict[Symbol, SymbolReference]:
        """
        Gets the callees of the given symbol.
        Downstream filtering must be applied to remove non-callee relationships.
        """
        return self.navigator.get_potential_symbol_callees(symbol)

    def get_references_to_symbol(self, symbol: Symbol) -> Dict[str, List[SymbolReference]]:
        return self.navigator.get_references_to_symbol(symbol)

    @property
    def default_rankable_subgraph(self) -> nx.DiGraph:
        return self._build_default_rankable_subgraph()

    @lru_cache(maxsize=1)
    def _build_default_rankable_subgraph(self) -> nx.DiGraph:
        return self._build_rankable_subgraph()

    def _build_rankable_subgraph(self, path_filter: Optional[str] = None) -> nx.DiGraph:
        """
        Creates a subgraph of the original `SymbolGraph` which
        contains only rankable symbols. The nodes in the subgraph
        are rankable symbols, and the edges are the dependencies
        between them.

        TODO - Think of how to handle relationships here.
        """
        G = nx.DiGraph()

        filtered_symbols = get_rankable_symbols(self.get_sorted_supported_symbols())

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
            filter_multi_digraph_by_symbols(self._graph, sorted_supported_symbols)

    @staticmethod
    def _load_index_protobuf(path: str) -> Index:
        index = Index()
        with open(path, "rb") as f:
            index.ParseFromString(f.read())
        return index
