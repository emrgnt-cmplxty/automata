import ast
from unittest.mock import MagicMock

import pytest
from astunparse import unparse as py_ast_unparse

from automata.experimental.tools import SymbolSearchToolkitBuilder
from automata.tools.tool_base import Tool


@pytest.fixture
def symbol_search_tool_builder():
    symbol_search_mock = MagicMock()
    return SymbolSearchToolkitBuilder(symbol_search=symbol_search_mock)


def test_init(symbol_search_tool_builder):
    assert isinstance(symbol_search_tool_builder.symbol_search, MagicMock)


def test_build(symbol_search_tool_builder):
    tools = symbol_search_tool_builder.build()
    assert len(tools) == 4
    for tool in tools:
        assert isinstance(tool, Tool)


def test_symbol_rank_search(symbols, symbol_search_tool_builder):
    symbol_search_tool_builder.symbol_search.get_symbol_rank_results = (
        MagicMock(return_value=[(symbols[0], 1)])
    )

    tools = symbol_search_tool_builder.build()
    for tool in tools:
        if tool.name == "symbol-rank-search":
            assert tool.function("symbol") == symbols[0]


def test_symbol_references(symbol_search_tool_builder):
    symbol_search_tool_builder.symbol_search.symbol_references = MagicMock(
        # TODO - replace with real symbol ref if that remains return type in the manager
        return_value={"ref": "Found references"}
    )

    tools = symbol_search_tool_builder.build()
    for tool in tools:
        if tool.name == "symbol-references":
            assert tool.function("symbol") == "ref:Found references"


def test_retrieve_source_code_by_symbol(symbol_search_tool_builder):
    symbol_search_tool_builder.symbol_search.retrieve_source_code_by_symbol = (
        MagicMock(return_value=ast.parse("def f(x):\n    return True"))
    )

    tools = symbol_search_tool_builder.build()
    for tool in tools:
        if tool.name == "retrieve-source-code-by-symbol":
            assert (
                py_ast_unparse(tool.function("symbol")).strip()
                == "\n\ndef f(x):\n    return True\n".strip()
            )


def test_exact_search(symbol_search_tool_builder):
    symbol_search_tool_builder.symbol_search.exact_search = MagicMock(
        return_value={"symbol": "Exact match found"}
    )

    tools = symbol_search_tool_builder.build()
    for tool in tools:
        if tool.name == "exact-search":
            assert tool.function("pattern") == "symbol:Exact match found"


def test_process_query(symbol_search_tool_builder):
    symbol_search_tool_builder.symbol_search.process_query = MagicMock(
        return_value="Processed query"
    )

    tools = symbol_search_tool_builder.build()
    for tool in tools:
        if tool.name == "process-query":
            assert tool.function("query") == "Processed query"
