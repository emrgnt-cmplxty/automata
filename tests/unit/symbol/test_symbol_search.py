import ast
from unittest.mock import patch

import pytest

from automata.symbol.parser import parse_symbol


def test_retrieve_source_code_by_symbol(symbols, symbol_search):
    with patch(
        "automata.experimental.search.symbol_search.convert_to_ast_object",
        return_value=ast.parse("def f(x):\n    return True"),
    ) as mock_method:
        result = symbol_search.retrieve_source_code_by_symbol(symbols[0].uri)
        assert result.strip() == "def f(x):\n    return True".strip()
    mock_method.assert_called_once_with(symbols[0])


def test_symbol_references(symbols, symbol_search, symbol_graph_mock):
    symbol_graph_mock.get_references_to_symbol.return_value = ["ref1", "ref2"]
    result = symbol_search.symbol_references(symbols[0].uri)
    assert result == ["ref1", "ref2"]
    symbol_graph_mock.get_references_to_symbol.assert_called_once_with(
        parse_symbol(symbols[0].uri)
    )


def test_exact_search(symbol_search):
    with patch(
        "automata.experimental.search.symbol_search.SymbolSearch._find_pattern_in_modules",
        return_value=["file1", "file2"],
    ):
        result = symbol_search.exact_search("pattern1")
        assert result == ["file1", "file2"]


def test_process_queries(symbols, symbol_search, symbol_graph_mock):
    with patch.object(
        symbol_search, "symbol_references", return_value=["ref1", "ref2"]
    ) as mock_method_0:
        result = symbol_search.process_query("type:symbol_references %s" % symbols[0].uri)
        assert result == ["ref1", "ref2"]
    mock_method_0.assert_called_once_with(symbols[0].uri)

    with patch.object(symbol_search, "exact_search", return_value={"test": 0}) as mock_method_1:
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
        symbol_search, "get_symbol_rank_results", return_value=[("ref1", 0.5), ("ref2", 0.4)]
    ) as mock_method_4:
        result = symbol_search.process_query("type:symbol_rank %s" % symbols[0].uri)
        assert result == [("ref1", 0.5), ("ref2", 0.4)]
    mock_method_4.assert_called_once_with(symbols[0].uri)

    with pytest.raises(ValueError):
        symbol_search.process_query("invalid_query")

    with pytest.raises(ValueError):
        symbol_search.process_query("type:unknown query")
