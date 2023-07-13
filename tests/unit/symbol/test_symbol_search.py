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


def test_process_queries(symbols, symbol_search, symbol_graph_mock):
    with patch.object(
        symbol_search, "symbol_references", return_value=["ref1", "ref2"]
    ) as mock_method_0:
        result = symbol_search.process_query(
            "type:symbol_references %s" % symbols[0].uri
        )
        assert result == ["ref1", "ref2"]
    mock_method_0.assert_called_once_with(symbols[0].uri)

    with patch.object(
        symbol_search, "exact_search", return_value={"test": 0}
    ) as mock_method_1:
        result = symbol_search.process_query("type:exact %s" % symbols[0].uri)
        assert result == {"test": 0}
    mock_method_1.assert_called_once_with(symbols[0].uri)

    with patch.object(
        symbol_search, "retrieve_source_code_by_symbol", return_value="test"
    ) as mock_method_2:
        result = symbol_search.process_query("type:source %s" % symbols[0].uri)
        assert result == "test"
    mock_method_2.assert_called_once_with(symbols[0].uri)

    with patch.object(
        symbol_search,
        "get_symbol_rank_results",
        return_value=[("ref1", 0.5), ("ref2", 0.4)],
    ) as mock_method_4:
        result = symbol_search.process_query(
            "type:symbol_rank %s" % symbols[0].uri
        )
        assert result == [("ref1", 0.5), ("ref2", 0.4)]
    mock_method_4.assert_called_once_with(symbols[0].uri)


@pytest.mark.parametrize(
    "invalid_query", ["invalid_query", "type:unknown query"]
)
def test_process_queries_errors(symbol_search, invalid_query):
    with pytest.raises(ValueError):
        symbol_search.process_query(invalid_query)
