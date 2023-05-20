import pytest


def test_retrieve_source_code_by_symbol(symbols, symbol_searcher, symbol_graph_mock):
    symbol_graph_mock.helper.convert_to_fst_object.return_value = "module1"
    result = symbol_searcher.retrieve_source_code_by_symbol(symbols[0].uri)
    assert result == "module1"
    symbol_graph_mock.helper.convert_to_fst_object.assert_called_once_with(symbols[0])


def test_symbol_search(symbols, symbol_searcher, symbol_graph_mock):
    symbol_graph_mock.get_symbol_references.return_value = ["ref1", "ref2"]
    result = symbol_searcher.symbol_search(symbols[0].uri)
    assert result == ["ref1", "ref2"]
    symbol_graph_mock.get_symbol_references.assert_called_once_with(symbols[0].uri)


def test_exact_search(symbol_searcher, symbol_graph_mock):
    symbol_graph_mock.helper.find_pattern_in_modules.return_value = ["file1", "file2"]
    result = symbol_searcher.exact_search("pattern1")
    assert result == ["file1", "file2"]
    symbol_graph_mock.helper.find_pattern_in_modules.assert_called_once_with("pattern1")


def test_find_and_replace(symbol_searcher, symbol_graph_mock):
    symbol_graph_mock.helper.find_and_replace_in_modules.return_value = 5
    result = symbol_searcher.find_and_replace("find1", "replace1", True)
    assert result == 5
    symbol_graph_mock.helper.find_and_replace_in_modules.assert_called_once_with(
        "find1", "replace1", True
    )


def test_process_query(symbols, symbol_searcher, symbol_graph_mock):
    symbol_graph_mock.get_symbol_references.return_value = ["ref1", "ref2"]
    result = symbol_searcher.process_query("type:symbol %s" % symbols[0].uri)
    assert result == ["ref1", "ref2"]

    with pytest.raises(ValueError):
        symbol_searcher.process_query("invalid_query")

    with pytest.raises(ValueError):
        symbol_searcher.process_query("type:unknown query")
