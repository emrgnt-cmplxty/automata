import logging
from typing import Dict, List, Set

import networkx as nx

from automata.tools.search.local_types import File, Symbol, SymbolReference
from automata.tools.search.scip_pb2 import Index, SymbolRole
from automata.tools.search.symbol_converter import SymbolConverter
from automata.tools.search.symbol_parser import parse_uri_to_symbol

logger = logging.getLogger(__name__)


class SymbolGraph:
    def __init__(
        self, index_path: str, symbol_converter: SymbolConverter, do_shortened_symbols: bool = True
    ):
        """
        Initialize SymbolGraph with the path of an index protobuf file.

        :param index_path: Path to index protobuf file
        """
        self.converter = symbol_converter

        self._index = self._load_index_protobuf(index_path)
        self._do_shortened_symbols = do_shortened_symbols
        self._graph = self._build_symbol_graph(self._index)

    def get_all_files(self) -> List[File]:
        """
        Get all file nodes in the graph.
        :param data_type: Optional filter for data type

        :return: List of all file nodes.
        """
        return [data for _, data in self._graph.nodes(data=True) if data.get("label") == "file"]

    def get_all_defined_symbols(self) -> List[Symbol]:
        """
        Get all file nodes in the graph.
        :param data_type: Optional filter for data type

        :return: List of all file nodes.
        """
        return [
            node for node, data in self._graph.nodes(data=True) if data.get("label") == "symbol"
        ]

    def get_symbol_references(self, symbol: Symbol) -> Dict[str, List[SymbolReference]]:
        """
        Finds all references of a given symbol in the symbol graph.

        :param symbol: Symbol to search for
        :return: List of tuples (file, symbol details)
        """
        search_results = [
            (file_path, symbol_reference)
            for file_path, symbol_reference, label in self._graph.out_edges(symbol, data=True)
            if label == "reference"
        ]
        result_dict: Dict[str, List[SymbolReference]] = {}

        for file_path, symbol_reference in search_results:
            if file_path in result_dict:
                result_dict[file_path].append(symbol_reference)
            else:
                result_dict[file_path] = [symbol_reference]

        return result_dict

    def get_symbols_occurrences_at_symbol(self, file_path: str) -> Set[Symbol]:
        """
        Gets all symbols defined at a specific file path

        :param file_path: The file_path to to get occurrences at
        :return: Set of symbols that follow the file path
        """
        obs_symbols = set([])
        symbols = self.get_all_defined_symbols()
        for symbol in symbols:
            if file_path not in symbol.uri:
                continue
            obs_symbols.add(symbol)
        return obs_symbols

    def get_defined_symbols_along_path(self, partial_path: str) -> Set[Symbol]:
        """
        Gets all symbols which contain a specified partial path

        :param partial_path: The partial_path to explain
        :return: Set of symbols that follow the partial path
        """
        obs_symbols = set([])
        symbols = self.get_all_defined_symbols()
        for symbol in symbols:
            if partial_path not in symbol.uri:
                continue
            obs_symbols.add(symbol)
        return obs_symbols

    def get_symbol_context(self, symbol) -> str:
        """
        Get the context for a given symbol. This includes its documentation, its file, references, and relationships.

        :param symbol: The symbol to explain
        :return: A string containing the explanation
        """

        result = ""
        docs = ["\n"]

        result += "Symbol Context for %s --> \n" % (symbol)
        doc_decorator = "  >> Symbol Docs       --> "
        spacer = " " * (0 + len(doc_decorator))
        result += f"{doc_decorator}%s\n" % (("\n" + spacer).join(docs)) + "\n"

        containing_file = [edge[0] for edge in self._graph.in_edges(symbol)][0]
        result += " >>  Symbol File       --> %s \n" % containing_file

        references = self.get_symbol_references(symbol)
        result += " >>  Symbol Ref Count  --> %s \n" % len(references.keys())

        symbol_references = "\n"
        for occurrence_file, outputs in references.items():
            for output in outputs:
                line_number = output.line_number
                roles = str(list(output.roles.keys()))
                symbol_references += f"{spacer}{occurrence_file}: L{line_number}, {roles} \n"

        result += " >>  Symbol Refs (All) --> %s" % (symbol_references)

        return result

    def _build_symbol_graph(self, index: Index) -> nx.MultiDiGraph:
        """
        Build a multidirectional graph from a given index.

        :param index: The index from which the graph is to be built.
        :return: The built multidirectional graph.
        """
        G = nx.MultiDiGraph()
        for document in index.documents:
            # Add File Vertices
            document_path = document.relative_path
            G.add_node(
                document_path,
                file=File(path=document.relative_path, occurrences=document.occurrences),
                label="file_path",
            )

            for symbol_information in document.symbols:
                symbol = parse_uri_to_symbol(symbol_information.symbol)
                # Add Symbol Vertices
                G.add_node(
                    symbol,
                    label="symbol",
                )
                # Add Contains Edge (File <-> Symbol)
                G.add_edge(
                    document_path,
                    parse_uri_to_symbol(symbol_information.symbol),
                    label="contains",
                )

            for occurrence_information in document.occurrences:
                occurrence_symbol = parse_uri_to_symbol(occurrence_information.symbol)
                occurrence_range = tuple(occurrence_information.range)
                occurrence_roles = self._get_symbol_roles_dict(occurrence_information.symbol_roles)
                occurrence_reference = SymbolReference(
                    line_number=occurrence_range[0],
                    roles=occurrence_roles,
                )
                # Add Occurrence Edges (Symbol <-> File)
                G.add_edge(
                    occurrence_symbol,
                    document.relative_path,
                    symbol_reference=occurrence_reference,
                    label="reference",
                )

        return G

    @staticmethod
    def _get_symbol_roles_dict(role) -> Dict[str, bool]:
        """
        Get a dictionary of symbol roles from a role Bitset.

        :param role: Role Bitset
        :return: A dictionary of symbol roles
        """
        result = {}
        for role_name, role_value in SymbolRole.items():
            if (role & role_value) > 0:
                result[role_name] = (role & role_value) > 0
        return result

    @staticmethod
    def _load_index_protobuf(path: str) -> Index:
        """
        Load an index from a protobuf file.

        :param path: The path of the protobuf file
        :return: The loaded index
        """
        index = Index()
        with open(path, "rb") as f:
            index.ParseFromString(f.read())
        return index
