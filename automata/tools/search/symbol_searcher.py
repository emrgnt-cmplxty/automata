from typing import Dict, List, Optional, Union

from automata.tools.search.local_types import SymbolReference
from automata.tools.search.symbol_graph import SymbolGraph
from automata.tools.search.symbol_parser import parse_uri_to_symbol
from automata.tools.search.symbol_utils import find_and_replace_in_modules, find_pattern_in_modules


class SymbolSearcher:
    def __init__(self, symbol_graph: SymbolGraph):
        self.symbol_graph = symbol_graph
        self._helper = symbol_graph.helper

    def retrieve_source_code_by_symbol(self, symbol_uri: str) -> Optional[str]:
        """
        Fetch the raw text of a module, class, method, or standalone function

        :param symbol: The symbol to retrieve
        :return: The raw text of the symbol or None if not found
        """
        node = self._helper.convert_to_fst_object(parse_uri_to_symbol(symbol_uri))
        return str(node) if node is not None else None

    def symbol_search(self, symbol_uri: str) -> Dict[str, List[SymbolReference]]:
        """
        Perform a symbol-based search

        :param query: The symbol to search for
        :return: A list of symbols that match the query
        """
        # TODO - Add parsing upstream or here to parse references
        return self.symbol_graph.get_symbol_references(parse_uri_to_symbol(symbol_uri))

    def exact_search(self, pattern: str) -> Dict[str, List[int]]:
        """
        Perform a exact search across the indexed codebase

        :param pattern: The pattern to search for
        :return: A dict of paths to files that contain the pattern and corresponding line numbers

        """
        return find_pattern_in_modules(self._helper, pattern)

    def find_and_replace(self, find: str, replace: str, do_write: bool) -> int:
        """
        Perform a exact replace on the in-memory codebase and write the result

        :param find: The string to find
        :param replace: The string to replace
        :return: The number of replacements made
        """
        return find_and_replace_in_modules(self._helper, find, replace, do_write)

    def process_query(
        self, query: str
    ) -> Union[Dict[str, List[SymbolReference]], Dict[str, List[int]], int, Optional[str]]:
        """
        Process an NLP-formatted query and return the results of the appropriate search

        :param query: The query to process
        :return: The results of the search
        """
        parts = query.split()
        if len(parts) < 2:
            raise ValueError(
                "Invalid NLP query. It must have at least two parts: 'type:...' and 'query...'"
            )

        search_type = parts[0][len("type:") :].lower()
        query_remainder = " ".join(parts[1:])

        if search_type == "symbol":
            return self.symbol_search(query_remainder)
        elif search_type == "exact":
            return self.exact_search(query_remainder)
        if search_type == "source":
            return self.retrieve_source_code_by_symbol(query_remainder)
        if search_type == "replace":
            find, replace, do_write = query_remainder.split(" ")
            assert do_write in ["True", "False"]
            return self.find_and_replace(find, replace, do_write == "True")
        else:
            raise ValueError(f"Unknown search type: {search_type}")
