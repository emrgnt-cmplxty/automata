import logging
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Set

import networkx as nx
from google.protobuf.json_format import MessageToDict
from tqdm import tqdm

from automata_docs.core.symbol.scip_pb2 import Index, SymbolRole
from automata_docs.core.symbol.symbol_parser import parse_symbol
from automata_docs.core.symbol.symbol_types import (
    Symbol,
    SymbolDescriptor,
    SymbolFile,
    SymbolReference,
)
from automata_docs.core.symbol.symbol_utils import convert_to_fst_object, get_rankable_symbols

logger = logging.getLogger(__name__)


class _RelationshipManager:
    """
    Manages the relationships between symbols in a graph.
    """

    def __init__(self, graph: nx.MultiDiGraph, symbol_information: Any):
        self._graph = graph
        self.symbol_information = symbol_information

    def process(self):
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


class _OccurrenceManager:
    """
    Manages the occurrences of a symbol in a graph.
    """

    def __init__(self, graph: nx.MultiDiGraph, document: Any):
        self._graph = graph
        self.document = document

    def process(self):
        for occurrence in self.document.occurrences:
            try:
                occurrence_symbol = parse_symbol(occurrence.symbol)
            except Exception as e:
                logger.error(f"Parsing symbol {occurrence.symbol} failed with error {e}")
                continue

            occurrence_range = tuple(occurrence.range)
            occurrence_roles = _OccurrenceManager._process_symbol_roles(occurrence.symbol_roles)
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
        result = {}
        for role_name, role_value in SymbolRole.items():
            if (role & role_value) > 0:
                result[role_name] = (role & role_value) > 0
        return result


class _CallerCalleeManager:
    """
    Manages the caller-callee relationships of a symbol in a graph.
    """

    def __init__(self, graph: nx.MultiDiGraph, document: Any):
        self._graph = graph
        self.navigator = _SymbolGraphNavigator(graph)
        self.document = document

    def process(self):
        for symbol in self.document.symbols:
            try:
                symbol_object = parse_symbol(symbol.symbol)
            except Exception as e:
                logger.error(f"Parsing symbol {symbol.symbol} failed with error {e}")
                continue

            if symbol_object.symbol_kind_by_suffix() != SymbolDescriptor.PythonKinds.Method:
                continue

            try:
                references_in_scope = self.navigator._get_symbol_references_in_scope(symbol_object)
            except Exception as e:
                print(f"Failed to get references in scope for symbol {symbol} with error {e}")
                continue

            for ref in references_in_scope:
                try:
                    if (
                        ref.symbol.symbol_kind_by_suffix() == SymbolDescriptor.PythonKinds.Method
                        or ref.symbol.symbol_kind_by_suffix() == SymbolDescriptor.PythonKinds.Class
                    ):
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
                    print(f"Failed to add caller-callee edge for {symbol} with error {e} ")
                    continue


class GraphBuilder:
    """
    Builds a symbol graph from an Index.
    """

    def __init__(self, index: Index, build_caller_relationships: bool = False):
        self.index = index
        self.build_caller_relationships = build_caller_relationships
        self._graph = nx.MultiDiGraph()

    def build_graph(self):
        for document in self.index.documents:
            self._add_file_vertices(document)
            self._add_symbol_vertices(document)
            self._process_relationships(document)
            self._process_occurrences(document)
            if self.build_caller_relationships:
                self._process_caller_callee_relationships(document)

        return self._graph

    def _add_file_vertices(self, document: Any):
        self._graph.add_node(
            document.relative_path,
            file=SymbolFile(document.relative_path, occurrences=document.occurrences),
            label="file",
        )

    def _add_symbol_vertices(self, document: Any):
        for symbol_information in document.symbols:
            try:
                symbol = parse_symbol(symbol_information.symbol)
            except Exception as e:
                logger.error(f"Parsing symbol {symbol_information.symbol} failed with error {e}")
                continue

            self._graph.add_node(symbol, label="symbol")
            self._graph.add_edge(document.relative_path, symbol, label="contains")

    def _process_relationships(self, document: Any):
        for symbol_information in document.symbols:
            relationship_manager = _RelationshipManager(self._graph, symbol_information)
            relationship_manager.process()

    def _process_occurrences(self, document: Any):
        occurrence_manager = _OccurrenceManager(self._graph, document)
        occurrence_manager.process()

    def _process_caller_callee_relationships(self, document: Any):
        caller_callee_manager = _CallerCalleeManager(self._graph, document)
        caller_callee_manager.process()


class _SymbolGraphNavigator:
    """
    Handles navigation of a symbol graph.
    """

    def __init__(self, graph: nx.MultiDiGraph):
        self._graph = graph

    def get_all_files(self) -> List[SymbolFile]:
        return [
            data.get("file")
            for _, data in self._graph.nodes(data=True)
            if data.get("label") == "file"
        ]

    def get_all_available_symbols(self) -> List[Symbol]:
        return [
            node for node, data in self._graph.nodes(data=True) if data.get("label") == "symbol"
        ]

    def get_symbol_dependencies(self, symbol: Symbol) -> Set[Symbol]:
        references_in_range = self._get_symbol_references_in_scope(symbol)
        symbols_in_range = set([ref.symbol for ref in references_in_range])
        return symbols_in_range

    def get_symbol_relationships(self, symbol: Symbol) -> Set[Symbol]:
        related_symbol_nodes = set(
            [
                target
                for _, target, data in self._graph.out_edges(symbol, data=True)
                if data.get("label") == "relationship"
            ]
        )
        return related_symbol_nodes

    def get_references_to_symbol(self, symbol: Symbol) -> Dict[str, List[SymbolReference]]:
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
        TODO - Remove non-call statements from this return object
        """
        callers = {
            SymbolReference(
                symbol=caller,
                line_number=data.get("line_number"),
                column_number=data.get("column_number"),
                roles=data.get("roles"),
            ): callee
            for callee, caller, data in self._graph.out_edges(symbol, data=True)
            if data.get("label") == "callee"
        }
        return callers

    def get_potential_symbol_callees(self, symbol: Symbol) -> Dict[Symbol, SymbolReference]:
        callees = {
            callee: SymbolReference(
                symbol=caller,
                line_number=data.get("line_number"),
                column_number=data.get("column_number"),
                roles=data.get("roles"),
            )
            for caller, callee, data in self._graph.out_edges(symbol, data=True)
            if data.get("label") == "caller"
        }
        return callees

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
        file_name = self._get_symbol_containing_file(symbol)
        fst_object = convert_to_fst_object(symbol)

        # RedBaron POSITIONS ARE 1 INDEXED AND SCIP ARE 0!!!!
        parent_symbol_start_line, parent_symbol_start_col, parent_symbol_end_line = (
            fst_object.absolute_bounding_box.top_left.line - 1,
            fst_object.absolute_bounding_box.top_left.column - 1,
            fst_object.absolute_bounding_box.bottom_right.line - 1,
        )

        references_in_parent_module = self._get_references_to_module(file_name)
        references_in_range = [
            ref
            for ref in references_in_parent_module
            if parent_symbol_start_line <= ref.line_number < parent_symbol_end_line
            and ref.column_number >= parent_symbol_start_col
        ]

        return references_in_range

    def _get_references_to_module(self, module_name: str) -> List[SymbolReference]:
        reference_edges_in_module = self._graph.in_edges(module_name, data=True)
        result = []
        for _, __, data in reference_edges_in_module:
            if data["label"] == "reference":
                result.append(data.get("symbol_reference"))

        return result


class SymbolGraph:
    @dataclass
    class SubGraph:
        parent: "SymbolGraph"
        graph: nx.DiGraph

    def __init__(self, index_path: str, build_caller_relationships: bool = False):
        """
        Initializes SymbolGraph with the path of an index protobuf file.

        Args:
            index_path (str): Path to index protobuf file
        Returns:
            SymbolGraph instance
        """
        index = self._load_index_protobuf(index_path)
        builder = GraphBuilder(index, build_caller_relationships)
        self._graph = builder.build_graph()
        self.navigator = _SymbolGraphNavigator(self._graph)

    def get_all_files(self) -> List[SymbolFile]:
        """
        Gets all file nodes in the graph.

        Args:
            None
        Returns:
            List of all defined symbols.
        """
        return self.navigator.get_all_files()

    def get_all_available_symbols(self) -> List[Symbol]:
        """
        Gets all symbols defined in the graph.

        Args:
            None
        Returns:
            List[Symbol]: List of all defined symbols.
        """
        return list(set(self.navigator.get_all_available_symbols()))

    def get_symbol_dependencies(self, symbol: Symbol) -> Set[Symbol]:
        """
        Gets all symbols which contain a specified partial path

        Args:
            partial_py_path (PyPath): The partial path to explain
        Returns:
            Set[Symbol]: Set of symbols that follow the partial path
        """
        return self.navigator.get_symbol_dependencies(symbol)

    def get_symbol_relationships(self, symbol: Symbol) -> Set[Symbol]:
        """
        Gets the set of symbols with relationships to the given symbol.

        Args:
            symbol (Symbol): The symbol to get relationships for.
        Returns:
            Set[Symbol]: The list of relationships for the symbol.

        # TODO: Consider implications of using list instead of set
        """
        return self.navigator.get_symbol_relationships(symbol)

    def get_potential_symbol_callers(self, symbol: Symbol) -> Dict[SymbolReference, Symbol]:
        """
        Gets the (potential) callers of the given symbol.
        Requires downstream filtering to remove non-call statements.

        Args:
            symbol (Symbol): The symbol to get callers for.
        Returns:
            Dict[Symbol]: The map of callers to callees for the symbol.
        """

        return self.navigator.get_potential_symbol_callers(symbol)

    def get_potential_symbol_callees(self, symbol: Symbol) -> Dict[Symbol, SymbolReference]:
        """
        Gets the callers of the given symbol.
        Requires downstream filtering to remove non-call statements.

        Args:
            symbol (Symbol): The symbol to get callees for.
        Returns:
            Dict[Symbol]: The map of callees to callers for the symbol.
        """
        return self.navigator.get_potential_symbol_callees(symbol)

    def get_references_to_symbol(self, symbol: Symbol) -> Dict[str, List[SymbolReference]]:
        """
        Gets all references to a given module in the symbol graph.

        Args:
            module (Symbol): The module to locate references for
        Returns:
            List[SymbolReference]: List of symbol references
        """
        return self.navigator.get_references_to_symbol(symbol)

    def get_rankable_symbol_subgraph(
        self, flow_rank="to_dependents", path_filter: Optional[str] = None
    ) -> SubGraph:
        """
        Gets a detailed subgraph of rankable symbols.

        Args:
            symbol (str): The symbol in the form 'module`/ClassOrMethod#'

        Returns:
            List[str]: The list of dependencies for the symbol.
        TODO: Can thi sbe made more efficient?
        TODO: Can we better handle edge cases that are not handled in obvious ways
        """
        G = nx.DiGraph()

        # Filter the symbols based on the provided path filter

        filtered_symbols = get_rankable_symbols(self.get_all_available_symbols())

        if path_filter is not None:
            filtered_symbols = [
                sym for sym in filtered_symbols if sym.path.startswith(path_filter)  # type: ignore
            ]

        for symbol in tqdm(filtered_symbols):
            try:
                dependencies = self.get_symbol_dependencies(symbol)
                relationships = self.get_symbol_relationships(symbol)
                filtered_related_symbols = get_rankable_symbols(
                    list(dependencies.union(relationships))
                )
                for dependency in filtered_related_symbols:
                    if flow_rank == "to_dependents":
                        G.add_edge(symbol, dependency)
                    elif flow_rank == "from_dependents":
                        G.add_edge(dependency, symbol)
                    elif flow_rank == "bidirectional":
                        G.add_edge(symbol, dependency)
                        G.add_edge(dependency, symbol)
                    else:
                        raise ValueError(
                            "flow_rank must be one of 'to_dependents', 'from_dependents', or 'bidirectional'"
                        )

            except Exception as e:
                logger.error(f"Error processing {symbol.uri}: {e}")

        return SymbolGraph.SubGraph(graph=G, parent=self)

    @staticmethod
    def _load_index_protobuf(path: str) -> Index:
        index = Index()
        with open(path, "rb") as f:
            index.ParseFromString(f.read())
        return index
