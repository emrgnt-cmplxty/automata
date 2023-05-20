import logging
from typing import Dict, List, Optional, Set

import networkx as nx
from google.protobuf.json_format import MessageToDict

from automata.tools.search.local_types import Descriptor, File, Symbol, SymbolReference
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

        self._class_to_symbol_lookup: Dict[str, Symbol] = self._build_class_to_symbol_lookup()
        self._symbol_to_return_type: Dict[
            Symbol, Optional[Symbol]
        ] = self._build_symbol_to_return_type()

    def get_all_files(self) -> List[File]:
        """
        Get all file nodes in the graph.
        :param data_type: Optional filter for data type

        :return: List of all file nodes.
        """
        return [node for node, data in self._graph.nodes(data=True) if data.get("label") == "file"]

    def get_all_symbols(self) -> List[Symbol]:
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
            (file_name, details)
            for _, file_name, details in self._graph.out_edges(symbol, data=True)
            if details.get("label") == "occurs_in"
        ]
        result_dict: Dict[str, List[SymbolReference]] = {}

        for item in search_results:
            file_name, details = item
            line_number = details["range"][0]
            entry = SymbolReference(
                line_number=line_number,
                details={k: v for k, v in details.items() if k != "range" and k != "label"},
            )

            if file_name in result_dict:
                result_dict[file_name].append(entry)
            else:
                result_dict[file_name] = [entry]

        return result_dict

    def get_symbols_along_path(self, partial_path: str) -> Set[Symbol]:
        """
        Finds all symbols which contain a specified partial path

        :param partial_path: The partial_path to explain
        :return: Set of symbols that follow the partial path
        """
        obs_symbols = set([])
        symbols = self.get_all_symbols()
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
        for doc in self._graph.nodes[symbol]["documentation"]:
            docs.extend(doc.split("\n"))

        result += "Symbol Context for %s --> \n" % (symbol)
        result += "  >> Symbol Type       --> %s\n" % self._graph.nodes[symbol]["symbol_kind"]
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
                details = str(list(output.details.keys()))
                symbol_references += f"{spacer}{occurrence_file}: L{line_number}, {details} \n"

        result += " >>  Symbol Refs (All) --> %s" % (symbol_references)

        return result

    def find_return_symbol(self, symbol: Symbol) -> Optional[Symbol]:
        """
        Finds the return symbol for a corresponding symbol
        Note - A match will only be found for methods

        :return: The return symbol, if it exists
        """
        return self._symbol_to_return_type.get(symbol)

    def _build_symbol_to_return_type(self) -> Dict[Symbol, Optional[Symbol]]:
        """
        Builds a mapping of symbol to return symbol type (if it exists).

        :return: A dictionary mapping symbols to their return types.
        """
        symbol_to_return_type = {}

        for symbol in self._graph.nodes():
            if not isinstance(symbol, Symbol):
                continue

            #  If the symbol is not a method, skip
            if not (
                Descriptor.convert_scip_to_python_suffix(symbol.descriptors[-1])
                == Descriptor.PythonTypes.Method
            ):
                continue
            # Get the FST object
            try:
                fst_object = self.converter.convert_to_fst_object(symbol)
            except Exception:
                logger.info("Exception occurred while fetching FST object for symbol = ", symbol)
                continue

            # Get the return type
            return_type = self.converter.find_return_type(fst_object)
            if return_type:
                # If return type exists, perform a reverse lookup to get its corresponding symbol
                return_type_symbol = self._class_to_symbol_lookup.get(return_type)
                # Add to the mapping
                symbol_to_return_type[symbol] = return_type_symbol

        return symbol_to_return_type

    def _build_class_to_symbol_lookup(self) -> Dict[str, Symbol]:
        """
        Builds a mapping of return type to symbol.

        :return: A dictionary mapping return types to their symbols.
        """
        return_type_to_symbol = {}

        for symbol in self._graph.nodes():
            if not isinstance(symbol, Symbol):
                continue

            if not (
                Descriptor.convert_scip_to_python_suffix(symbol.descriptors[-1])
                == Descriptor.PythonTypes.Class
            ):
                continue
            class_name = symbol.descriptors[-1].name
            return_type_to_symbol[class_name] = symbol

        return return_type_to_symbol

    def _build_symbol_graph(self, index: Index) -> nx.MultiDiGraph:
        """
        Build a multidirectional graph from a given index.

        :param index: The index from which the graph is to be built.
        :return: The built multidirectional graph.
        """
        G = nx.MultiDiGraph()
        # first add all the files and symbols
        for document in index.documents:
            G.add_node(document.relative_path, label="file")
            for symbol_information in document.symbols:
                G.add_node(
                    parse_uri_to_symbol(symbol_information.symbol),
                    label="symbol",
                    symbol_kind=Descriptor.symbol_kind_by_suffix(symbol_information.symbol),
                    documentation=list(symbol_information.documentation),
                )
                G.add_edge(
                    document.relative_path,
                    parse_uri_to_symbol(symbol_information.symbol),
                    label="contains",
                )
        # process occurrences and relationships
        for document in index.documents:
            for symbol_information in document.symbols:
                for relationship in symbol_information.relationships:
                    relationship_labels = MessageToDict(relationship)
                    relationship_labels.pop("symbol")
                    G.add_edge(
                        parse_uri_to_symbol(symbol_information.symbol),
                        relationship.symbol,
                        label="relates_to",
                        **relationship_labels,
                    )

            for occurrence in document.occurrences:
                occurrence_range = tuple(occurrence.range)
                roles = self._get_symbol_roles_dict(occurrence.symbol_roles)
                G.add_edge(
                    parse_uri_to_symbol(occurrence.symbol),
                    document.relative_path,
                    label="occurs_in",
                    range=occurrence_range,
                    **roles,
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
