from unittest.mock import patch

import pytest

from automata.tools.search.symbol_parser import parse_symbol


def test_retrieve_source_code_by_symbol(symbols, symbol_searcher):
    with patch.object(
        symbol_searcher.converter, "convert_to_fst_object", return_value="module1"
    ) as mock_method:
        result = symbol_searcher.retrieve_source_code_by_symbol(symbols[0].uri)
        assert result == "module1"
    mock_method.assert_called_once_with(symbols[0])


def test_symbol_search(symbols, symbol_searcher, symbol_graph_mock):
    symbol_graph_mock.get_symbol_references.return_value = ["ref1", "ref2"]
    result = symbol_searcher.symbol_search(symbols[0].uri)
    assert result == ["ref1", "ref2"]
    symbol_graph_mock.get_symbol_references.assert_called_once_with(parse_symbol(symbols[0].uri))


def test_exact_search(symbol_searcher):
    with patch(
        "automata.tools.search.symbol_searcher.find_pattern_in_modules",
        return_value=["file1", "file2"],
    ) as mock_method:
        result = symbol_searcher.exact_search("pattern1")
        assert result == ["file1", "file2"]
    mock_method.assert_called_once_with(symbol_searcher.converter, "pattern1")


def test_find_and_replace(symbols, symbol_searcher):
    with patch(
        "automata.tools.search.symbol_searcher.find_and_replace_in_modules", return_value=5
    ):
        result = symbol_searcher.find_and_replace("find1", "replace1", True)
        assert result == 5


def test_process_query(symbols, symbol_searcher, symbol_graph_mock):
    with patch.object(
        symbol_searcher, "symbol_search", return_value=["ref1", "ref2"]
    ) as mock_method:
        result = symbol_searcher.process_query("type:symbol %s" % symbols[0].uri)
        assert result == ["ref1", "ref2"]
    mock_method.assert_called_once_with(symbols[0].uri)

    with pytest.raises(ValueError):
        symbol_searcher.process_query("invalid_query")

    with pytest.raises(ValueError):
        symbol_searcher.process_query("type:unknown query")
