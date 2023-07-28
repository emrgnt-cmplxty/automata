from unittest.mock import MagicMock

import pytest

from automata.eval.tool import (
    SymbolSearchAction,
    SymbolSearchEval,
    SymbolSearchEvalResult,
)
from automata.experimental.tools import SymbolSearchToolkitBuilder
from automata.llm import FunctionCall

# Define fixtures for the test cases


@pytest.fixture
def symbol_search_eval():
    return SymbolSearchEval()


@pytest.fixture
def function_call():
    return FunctionCall(name="TestTool", arguments={"test": "test"})


@pytest.fixture
def expected_action():
    return SymbolSearchAction(
        query="test_query", search_results=["result1", "result2", "result3"]
    )


@pytest.fixture
def symbol_search_tool_builder(symbol_search):
    return SymbolSearchToolkitBuilder(symbol_search).build()


def test_symbol_search_action(expected_action):
    payload = {
        "query": "test_query",
        "search_results": "result1,result2,result3",
    }
    search_action = SymbolSearchAction.from_payload(payload)
    assert search_action.search_results == expected_action.search_results
    assert search_action.query == expected_action.query


def test_symbol_search_eval_result(expected_action):
    observed_action = SymbolSearchAction.from_payload(
        {"query": "test_query", "search_results": "result1,result2"}
    )
    symbol_search_eval_result = SymbolSearchEvalResult(
        expected_action, observed_action
    )
    assert expected_action.query == observed_action.query
    assert symbol_search_eval_result.is_full_match
    assert symbol_search_eval_result.is_partial_match


def test_symbol_search_eval_result_partial_match(expected_action):
    observed_action = SymbolSearchAction.from_payload(
        {
            "query": "test_query",
            "search_results": "result2,result1",
        }  # Partial match b/c result1 is not top result
    )
    symbol_search_eval_result = SymbolSearchEvalResult(
        expected_action, observed_action
    )
    assert expected_action.query == observed_action.query
    assert not symbol_search_eval_result.is_full_match
    assert symbol_search_eval_result.is_partial_match


def test_symbol_search_eval_result_not_match(expected_action):
    observed_action = SymbolSearchAction.from_payload(
        {
            "query": "test_query",
            "search_results": "result2,result3",
        }  # Partial match b/c result1 is not top result
    )
    symbol_search_eval_result = SymbolSearchEvalResult(
        expected_action, observed_action
    )
    assert expected_action.query == observed_action.query
    assert not symbol_search_eval_result.is_full_match
    assert not symbol_search_eval_result.is_partial_match


def test_symbol_search_eval_result_from_payload(expected_action):
    observed_action = SymbolSearchAction.from_payload(
        {"query": "test_query", "search_results": "result1,result2"}
    )
    symbol_search_eval_result = SymbolSearchEvalResult(
        expected_action, observed_action
    )

    result_payload = symbol_search_eval_result.to_payload()
    symbol_search_eval_result = symbol_search_eval_result.from_payload(
        result_payload
    )
    assert expected_action.query == observed_action.query
    assert symbol_search_eval_result.is_full_match
    assert symbol_search_eval_result.is_partial_match


def test_symbol_search_eval_to_tool_result(
    symbol_search_eval, expected_action
):
    observed_action = SymbolSearchAction.from_payload(
        {"query": "test_query", "search_results": "result1,result2"}
    )

    result = symbol_search_eval.to_tool_result(
        expected_action, observed_action
    )
    assert isinstance(result, SymbolSearchEvalResult)
    assert result.expected_action == expected_action
    assert result.observed_action == observed_action
    assert result.is_full_match
    assert result.is_partial_match


def test_symbol_search_eval_extract_action(symbol_search_eval):
    observed_action = SymbolSearchAction.from_payload(
        {"query": "test_query", "search_results": "result1,result2"}
    )

    action_tuple = (
        FunctionCall(
            name="symbol-rank-search", arguments={"query": "test_query"}
        ),
        "result1\nresult2",
    )
    result = symbol_search_eval.extract_action(action_tuple)

    assert result == observed_action


def test_generate_eval_result(symbol_search_eval):
    function_call = FunctionCall(
        name="symbol-rank-search", arguments={"query": "test_query"}
    )
    expected_action = SymbolSearchAction.from_payload(
        {"query": "test_query", "search_results": "result1,result2"}
    )

    mock_tool_exec = MagicMock()
    mock_tool_exec.execute.return_value = "result1\nresult2\nresult3"

    result = symbol_search_eval.generate_eval_result(
        function_call, expected_action, mock_tool_exec
    )

    assert result.is_full_match
    assert result.is_partial_match
    mock_tool_exec.execute.assert_called_once_with(function_call)
