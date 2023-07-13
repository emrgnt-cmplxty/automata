import ast
from unittest.mock import MagicMock

import pytest
from astunparse import unparse as py_ast_unparse

from automata.tools.base import Tool
from automata.tools.builders.symbol_search import SymbolSearchToolkitBuilder


@pytest.fixture
def symbol_search_tool_builder():
    symbol_search_mock = MagicMock()
    return SymbolSearchToolkitBuilder(symbol_search=symbol_search_mock)


@pytest.mark.parametrize(
    "tool_name,function_return,expected",
    [
        ("symbol-references", {"ref": "Found references"}, "ref:Found references"),
        (
            "retrieve-source-code-by-symbol",
            ast.parse("def f(x):\n    return True"),
            "\n\ndef f(x):\n    return True\n".strip(),
        ),
        ("exact-search", {"symbol": "Exact match found"}, "symbol:Exact match found"),
        ("process-query", "Processed query", "Processed query"),
    ],
)
def test_tools_without_symbols(symbol_search_tool_builder, tool_name, function_return, expected):
    mock_func = MagicMock(return_value=function_return)
    setattr(symbol_search_tool_builder.symbol_search, tool_name.replace("-", "_"), mock_func)

    tools = symbol_search_tool_builder.build()
    for tool in tools:
        if tool.name == tool_name:
            assert tool.function("query") == expected


def test_tools_with_symbols(symbol_search_tool_builder, symbols):
    tool_name = "symbol-rank-search"
    function_return = [(symbols[0], 1)]
    expected = symbols[0]

    mock_func = MagicMock(return_value=function_return)
    setattr(symbol_search_tool_builder.symbol_search, tool_name.replace("-", "_"), mock_func)

    tools = symbol_search_tool_builder.build()
    for tool in tools:
        if tool.name == tool_name:
            assert tool.function("query") == expected
