from enum import Enum
from typing import Callable, List, Optional, Union

from automata.core.base.tool import Tool
from automata.core.symbol.search.symbol_search import (
    ExactSearchResult,
    SourceCodeResult,
    SymbolRankResult,
    SymbolReferencesResult,
    SymbolSearch,
)


class SearchTool(Enum):
    SYMBOL_RANK_SEARCH = "symbol-rank-search"
    SYMBOL_REFERENCES = "symbol-references"
    RETRIEVE_SOURCE_CODE_BY_SYMBOL = "retrieve-source-code-by-symbol"
    EXACT_SEARCH = "exact-search"


class SymbolSearchTool:
    def __init__(
        self,
        symbol_search: SymbolSearch,
        search_tools: Optional[List[SearchTool]] = None,
        post_processing: Optional[Callable] = None,
    ):
        self.symbol_search = symbol_search
        self.search_tools = search_tools or list(SearchTool)
        self.post_processing = post_processing

    def build_tool(self, tool_type: SearchTool) -> Tool:
        tool_funcs = {
            SearchTool.SYMBOL_RANK_SEARCH: self._symbol_rank_search_processor,
            SearchTool.SYMBOL_REFERENCES: self._symbol_symbol_references_processor,
            SearchTool.RETRIEVE_SOURCE_CODE_BY_SYMBOL: self._retrieve_source_code_by_symbol_processor,
            SearchTool.EXACT_SEARCH: self._exact_search_processor,
        }
        tool_descriptions = {
            SearchTool.SYMBOL_RANK_SEARCH: "Performs a ranked search of symbols based on a given query string.",
            SearchTool.SYMBOL_REFERENCES: "Finds all the references to a given symbol within the codebase.",
            SearchTool.RETRIEVE_SOURCE_CODE_BY_SYMBOL: "Returns the source code corresponding to a given symbol.",
            SearchTool.EXACT_SEARCH: "Performs an exact search for a given pattern across the codebase.",
        }
        if tool_type in tool_funcs:
            return Tool(
                name=tool_type.value,
                func=tool_funcs[tool_type],
                description=tool_descriptions[tool_type],
            )
        raise ValueError(f"Invalid tool type: {tool_type}")

    def build(self) -> List[Tool]:
        return [self.build_tool(tool_type) for tool_type in self.search_tools]

    def process_query(
        self, tool_type: SearchTool, query: str
    ) -> Union[SymbolReferencesResult, SymbolRankResult, SourceCodeResult, ExactSearchResult,]:
        tools_dict = {tool.name: tool.func for tool in self.build()}
        result = tools_dict[tool_type.value](query)
        if self.post_processing:
            result = self.post_processing(result)
        return result

    # TODO - Cleanup these processors to ensure they behave well.
    # -- Right now these are just simplest implementations I can rattle off
    def _symbol_rank_search_processor(self, query: str) -> str:
        query_result = self.symbol_search.symbol_rank_search(query)
        return "\n".join([symbol.uri for symbol, _rank in query_result])

    def _symbol_symbol_references_processor(self, query: str) -> str:
        query_result = self.symbol_search.symbol_references(query)
        return "\n".join(
            [f"{symbol}:{str(reference)}" for symbol, reference in query_result.items()]
        )

    def _retrieve_source_code_by_symbol_processor(self, query: str) -> str:
        query_result = self.symbol_search.retrieve_source_code_by_symbol(query)
        return query_result or "No Result Found"

    def _exact_search_processor(self, query: str) -> str:
        query_result = self.symbol_search.exact_search(query)
        processed_result = "\n".join(
            [f"{symbol}:{str(references)}" for symbol, references in query_result.items()]
        )
        return processed_result
