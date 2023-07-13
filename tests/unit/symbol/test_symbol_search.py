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


@pytest.mark.parametrize(
    "query_type,method_name,method_return,expected",
    [
        ("symbol_references", "symbol_references", ["ref1", "ref2"], ["ref1", "ref2"]),
        ("exact", "exact_search", {"test": 0}, {"test": 0}),
        ("source", "retrieve_source_code_by_symbol", "test", "test"),
        (
            "symbol_rank",
            "symbol_rank_search",
            [("ref1", 0.5), ("ref2", 0.4)],
            [("ref1", 0.5), ("ref2", 0.4)],
        ),
    ],
)
def test_process_queries(
    symbols, symbol_search, symbol_graph_mock, query_type, method_name, method_return, expected
):
    with patch.object(symbol_search, method_name, return_value=method_return) as mock_method:
        result = symbol_search.process_query(f"type:{query_type} {symbols[0].uri}")
        assert result == expected
    mock_method.assert_called_once_with(symbols[0].uri)


@pytest.mark.parametrize("invalid_query", ["invalid_query", "type:unknown query"])
def test_process_queries_errors(symbol_search, invalid_query):
    with pytest.raises(ValueError):
        symbol_search.process_query(invalid_query)
