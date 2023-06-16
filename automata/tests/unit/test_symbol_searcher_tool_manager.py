# from unittest.mock import MagicMock

# import pytest

# from automata.core.base.tool import Tool
# from automata.core.agent.tool_management.symbol_searcher_manager import SymbolSearcherToolManager


# @pytest.fixture
# def symbol_searcher_tool_builder():
#     symbol_searcher_mock = MagicMock()
#     return SymbolSearcherToolManager(symbol_searcher=symbol_searcher_mock)


# def test_init(symbol_searcher_tool_builder):
#     assert isinstance(symbol_searcher_tool_builder.symbol_searcher, MagicMock)


# def test_build_tools(symbol_searcher_tool_builder):
#     tools = symbol_searcher_tool_builder.build_tools()
#     assert len(tools) == 4
#     for tool in tools:
#         assert isinstance(tool, Tool)


# def test_symbol_rank_search(symbol_searcher_tool_builder):
#     symbol_searcher_tool_builder.symbol_searcher.symbol_rank_search = MagicMock(
#         return_value=[("Found symbol", 1)]
#     )

#     tools = symbol_searcher_tool_builder.build_tools()
#     for tool in tools:
#         if tool.name == "symbol-rank-search":
#             assert tool.func(("module.path", "symbol")) == "Found symbol"


# def test_symbol_references(symbol_searcher_tool_builder):
#     symbol_searcher_tool_builder.symbol_searcher.symbol_references = MagicMock(
#         # TODO - replace with real symbol ref if that remains return type in the manager
#         return_value={"ref": "Found references"}
#     )

#     tools = symbol_searcher_tool_builder.build_tools()
#     for tool in tools:
#         if tool.name == "symbol-references":
#             assert tool.func(("module.path", "symbol")) == "ref:Found references"


# def test_retrieve_source_code_by_symbol(symbol_searcher_tool_builder):
#     symbol_searcher_tool_builder.symbol_searcher.retrieve_source_code_by_symbol = MagicMock(
#         return_value="Source code"
#     )

#     tools = symbol_searcher_tool_builder.build_tools()
#     for tool in tools:
#         if tool.name == "retrieve-source-code-by-symbol":
#             assert tool.func(("module.path", "symbol")) == "Source code"


# def test_exact_search(symbol_searcher_tool_builder):
#     symbol_searcher_tool_builder.symbol_searcher.exact_search = MagicMock(
#         return_value={"symbol": "Exact match found"}
#     )

#     tools = symbol_searcher_tool_builder.build_tools()
#     for tool in tools:
#         if tool.name == "exact-search":
#             assert tool.func(("module.path", "pattern")) == "symbol:Exact match found"


# def test_process_query(symbol_searcher_tool_builder):
#     symbol_searcher_tool_builder.symbol_searcher.process_query = MagicMock(
#         return_value="Processed query"
#     )

#     tools = symbol_searcher_tool_builder.build_tools()
#     for tool in tools:
#         if tool.name == "process-query":
#             assert tool.func(("module.path", "query")) == "Processed query"
