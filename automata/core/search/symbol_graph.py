import logging
from typing import Dict, List, Set, cast

import networkx as nx
from google.protobuf.json_format import MessageToDict
from tqdm import tqdm

from automata.core.search.scip_pb2 import Index, SymbolRole
from automata.core.search.symbol_converter import SymbolConverter
from automata.core.search.symbol_parser import parse_symbol
from automata.core.search.symbol_types import File, PyPath, StrPath, Symbol, SymbolReference
from automata.core.search.symbol_utils import get_rankable_symbols

logger = logging.getLogger(__name__)


class SymbolGraph:
    def __init__(self, index_path: str, symbol_converter: SymbolConverter):
        """
        Initializes SymbolGraph with the path of an index protobuf file.

        Args:
            index_path (str): Path to index protobuf file
            symbol_converter (SymbolConverter): SymbolConverter instance
        Returns:
            SymbolGraph instance
        """
        self.converter = symbol_converter

        self._index = self._load_index_protobuf(index_path)
        self._graph = self._build_symbol_info_graph(self._index)

    def get_all_files(self) -> List[File]:
        """
        Gets all file nodes in the graph.

        Args:
            None
        Returns:
            List of all defined symbols.
        """
        return [
            data.get("file")
            for _, data in self._graph.nodes(data=True)
            if data.get("label") == "file"
        ]

    def get_all_defined_symbols(self) -> List[Symbol]:
        """
        Gets all symbols defined in the graph.

        Args:
            None
        Returns:
            List[Symbol]: List of all defined symbols.
        """
        return [
            node for node, data in self._graph.nodes(data=True) if data.get("label") == "symbol"
        ]

    def get_defined_symbols_along_path(self, partial_py_path: PyPath) -> Set[Symbol]:
        """
        Gets all symbols which contain a specified partial path

        Args:
            partial_py_path (PyPath): The partial path to explain
        Returns:
            Set[Symbol]: Set of symbols that follow the partial path
        """
        obs_symbols = set()
        symbols = self.get_all_defined_symbols()
        for symbol in symbols:
            if partial_py_path in symbol.uri:
                obs_symbols.add(symbol)
        return obs_symbols

    def get_rankable_symbol_subgraph(self, flow_rank="to_dependents") -> nx.DiGraph:
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

        filtered_symbols = get_rankable_symbols(self.get_all_defined_symbols())

        for symbol in tqdm(filtered_symbols):
            try:
                dependencies = self._get_symbol_dependencies(symbol)
                relationships = self._get_symbol_relationships(symbol)
                for dependency in dependencies.union(relationships):
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

        return G

    def get_references_to_module(self, module_name: str) -> List[SymbolReference]:
        """
        Gets all references to a given module in the symbol graph.

        Args:
            module (Symbol): The module to locate references for
        Returns:
            List[SymbolReference]: List of symbol references
        """
        reference_edges_in_module = self._graph.in_edges(module_name, data=True)
        result = []
        for _, __, data in reference_edges_in_module:
            if data["label"] == "reference":
                result.append(data.get("symbol_reference"))

        return result

    def get_references_to_symbol(self, symbol: Symbol) -> Dict[StrPath, List[SymbolReference]]:
        """
        Gets all references to a given symbol in the symbol graph.

        Args:
            symbol (Symbol): The symbol to locate references for
        Returns:
            Dict of file paths to lists of symbol references
        """
        search_results = [
            (file_path, data.get("symbol_reference"))
            for _, file_path, data in self._graph.out_edges(symbol, data=True)
            if data.get("label") == "reference"
        ]
        result_dict: Dict[StrPath, List[SymbolReference]] = {}

        for file_path, symbol_reference in search_results:
            if file_path in result_dict:
                result_dict[file_path].append(symbol_reference)
            else:
                result_dict[file_path] = [symbol_reference]

        return result_dict

    def get_symbol_context(self, symbol) -> str:
        """
        Gets the context for a given symbol.
        This includes its documentation, its file, references, and relationships.

        Args:
            symbol (Symbol): The symbol to explain
        Returns:
            A string containing the explanation
        """

        result = ""
        docs = ["\n"]

        result += "Symbol Context for %s --> \n" % (symbol)
        doc_decorator = "  >> Symbol Docs       --> "
        spacer = " " * (0 + len(doc_decorator))
        result += f"{doc_decorator}%s\n" % (("\n" + spacer).join(docs)) + "\n"

        containing_file = self._get_symbol_containing_file(symbol)
        result += " >>  Symbol File       --> %s \n" % containing_file

        references = self.get_references_to_symbol(symbol)
        result += " >>  Symbol Ref Count  --> %s \n" % len(references.keys())

        symbol_references = "\n"
        for occurrence_file, outputs in references.items():
            for output in outputs:
                line_number = output.line_number
                roles = str(list(output.roles.keys()))
                symbol_references += f"{spacer}{occurrence_file}: L{line_number}, {roles} \n"

        result += " >>  Symbol Refs (All) --> %s" % (symbol_references)

        return result

    def _build_symbol_info_graph(self, index: Index) -> nx.MultiDiGraph:
        """
        Builds a multidirectional graph from a given index.

        Args:
            index: The index from which the graph is to be built.
        Returns:
            nx.MultiDiGraph: The built multidirectional graph.
        """
        G = nx.MultiDiGraph()
        for document in index.documents:
            # Add FilePath Vertices
            document_path: StrPath = cast(StrPath, document.relative_path)

            G.add_node(
                document_path,
                file=File(document_path, occurrences=document.occurrences),
                label="file",
            )

            for symbol_information in document.symbols:
                try:
                    symbol = parse_symbol(symbol_information.symbol)
                except Exception as e:
                    logger.error(f"Parsing symbol {symbol.uri} failed with error {e}")
                    continue

                # Add Symbol Vertices
                G.add_node(
                    symbol,
                    label="symbol",
                )
                G.add_edge(document_path, symbol, label="contains")
        # process occurrences and relationships
        for document in index.documents:
            information_document_path: StrPath = cast(StrPath, document.relative_path)
            for symbol_information in document.symbols:
                try:
                    symbol = parse_symbol(symbol_information.symbol)
                except Exception as e:
                    logger.error(f"Parsing symbol {symbol.uri} failed with error {e}")
                    continue

                for relationship in symbol_information.relationships:
                    relationship_labels = MessageToDict(relationship)
                    relationship_labels.pop("symbol")
                    related_symbol = parse_symbol(relationship.symbol)
                    G.add_edge(
                        symbol,
                        related_symbol,
                        label="relationship",
                        **relationship_labels,
                    )

            for occurrence in document.occurrences:
                try:
                    occurrence_symbol = parse_symbol(occurrence.symbol)
                except Exception as e:
                    logger.error(f"Parsing symbol {symbol.uri} failed with error {e}")
                    continue

                occurrence_range = tuple(occurrence.range)
                occurrence_roles = self._process_symbol_roles(occurrence.symbol_roles)
                occurrence_reference = SymbolReference(
                    symbol=occurrence_symbol,
                    line_number=occurrence_range[0],
                    column_number=occurrence_range[1],
                    roles=occurrence_roles,
                )
                G.add_edge(
                    occurrence_symbol,
                    information_document_path,
                    symbol_reference=occurrence_reference,
                    label="reference",
                )
                if occurrence_roles.get(SymbolRole.Name(SymbolRole.Definition)):
                    # TODO this is gross
                    incorrect_contains_edges = [
                        (source, target)
                        for source, target, data in G.in_edges(occurrence_symbol, data=True)
                        if data.get("label") == "contains"
                    ]
                    for source, target in incorrect_contains_edges:
                        G.remove_edge(source, target)

                    G.add_edge(
                        information_document_path,
                        occurrence_symbol,
                        label="contains",
                    )

        return G

    def _get_symbol_containing_file(self, symbol: Symbol) -> str:
        """
        Gets the file that contains the given symbol.

        Args:
            symbol (Symbol): The symbol to get the containing file for.
        Returns:
            str: The file that contains the symbol.
        """
        parent_file_list = [
            source
            for source, _, data in self._graph.in_edges(symbol, data=True)
            if data.get("label") == "contains"
        ]
        assert (
            len(parent_file_list) == 1
        ), f"{symbol.uri} should have exactly one parent file, but has {len(parent_file_list)}"
        return parent_file_list.pop()

    def _get_symbol_dependencies(self, symbol: Symbol) -> Set[Symbol]:
        """
        Gets the set of symbols referenced inside the scope of the given symbol (including children scopes).

        Args:
            symbol (Symbol): The symbol to get dependencies for.
        Returns:
            Set[Symbol]: The list of dependencies for the symbol.

        # TODO: Consider implications of using list instead of set
        """
        references_in_range = self._get_symbol_references_in_scope(symbol)
        symbols_in_range = set([ref.symbol for ref in references_in_range])
        return symbols_in_range

    def _get_symbol_references_in_scope(self, symbol: Symbol) -> List[SymbolReference]:
        """
        Gets the list of symbols referenced inside the scope of the given symbol (including children scopes)

        Args:
            symbol (Symbol): The symbol to get references for.
        Returns:
            List[SymbolReference]: The list of references for the symbol.
        """
        module_name = self._get_symbol_containing_file(symbol)
        if module_name not in self.converter._module_dict:  # TODO
            return []
        fst_object = self.converter.convert_to_fst_object(symbol)

        # RedBaron POSITIONS ARE 1 INDEXED AND SCIP ARE 0!!!!
        parent_symbol_start_line, parent_symbol_start_col, parent_symbol_end_line = (
            fst_object.absolute_bounding_box.top_left.line - 1,
            fst_object.absolute_bounding_box.top_left.column - 1,
            fst_object.absolute_bounding_box.bottom_right.line - 1,
        )

        references_in_parent_module = self.get_references_to_module(module_name)
        references_in_range = [
            ref
            for ref in references_in_parent_module
            if parent_symbol_start_line <= ref.line_number < parent_symbol_end_line
            and ref.column_number >= parent_symbol_start_col
        ]

        return references_in_range

    def _get_symbol_relationships(self, symbol: Symbol) -> Set[Symbol]:
        """
        Gets the set of symbols with relationships to the given symbol.

        Args:
            symbol (Symbol): The symbol to get relationships for.
        Returns:
            Set[Symbol]: The list of relationships for the symbol.

        # TODO: Consider implications of using list instead of set
        """
        related_symbol_nodes = set(
            [
                target
                for _, target, data in self._graph.out_edges(symbol, data=True)
                if data.get("label") == "relationship"
            ]
        )
        return related_symbol_nodes

    @staticmethod
    def _process_symbol_roles(role: int) -> Dict[str, bool]:
        """
        Gets a dictionary of symbol roles from a role Bitset.

        Args:
            role (int): Role Bitset
        Returns:
            Dict[str, bool]: A dictionary of symbol roles
        """
        result = {}
        for role_name, role_value in SymbolRole.items():
            if (role & role_value) > 0:
                result[role_name] = (role & role_value) > 0
        return result

    @staticmethod
    def _load_index_protobuf(path: StrPath) -> Index:
        """
        Loads an index from a protobuf file.

        Args:
            path (StrPath): The path of the protobuf file
        Returns:
            Index: The loaded index
        """
        index = Index()
        with open(path, "rb") as f:
            index.ParseFromString(f.read())
        return index
