# import pytest
# from automata.eval.tool import (
#     SymbolSearchEvalResult,
#     SymbolSearchAction,
#     ToolEvalResult,
# )
# from automata.experimental.tools import SymbolSearchToolkitBuilder

# from automata.llm import LLMChatMessage, FunctionCall


# def test_tool_eval(tool_eval, function_call, expected_action, tool_executor):
#     result = tool_eval.generate_eval_result(
#         function_call, [expected_action], tool_executor
#     )
#     assert isinstance(result, ToolEvalResult)
#     assert result.expected_action == expected_action
#     assert result.observed_action == expected_action


# def test_tool_eval_result(tool_eval_result):
#     assert tool_eval_result.is_full_match
#     assert tool_eval_result.is_partial_match
#     assert tool_eval_result.is_match
#     assert tool_eval_result.get_details() == {
#         "expected_action": tool_eval_result.expected_action,
#         "observed_action": tool_eval_result.observed_action,
#     }


# def test_symbol_search_action(symbol_search_action):
#     payload = symbol_search_action.to_payload()
#     assert payload["query"] == symbol_search_action.query
#     assert payload["search_results"] == symbol_search_action.search_results
#     assert SymbolSearchAction.from_payload(payload) == symbol_search_action


# def test_symbol_search_eval_result(symbol_search_eval_result):
#     assert symbol_search_eval_result.is_full_match
#     assert symbol_search_eval_result.is_partial_match
#     assert symbol_search_eval_result.get_details() == {
#         "expected_match": symbol_search_eval_result.expected_match,
#         "observed_action": symbol_search_eval_result.observed_action,
#     }


# def test_symbol_search_toolkit_builder(symbol_search_toolkit_builder, query):
#     tools = symbol_search_toolkit_builder.build()
#     for tool in tools:
#         assert tool.function(
#             query
#         ) == symbol_search_toolkit_builder.process_query(tool.name, query)


# def test_symbol_search_open_ai_toolkit_builder(
#     symbol_search_open_ai_toolkit_builder,
# ):
#     tools = symbol_search_open_ai_toolkit_builder.build_for_open_ai()
#     assert len(tools) == len(
#         symbol_search_open_ai_toolkit_builder.search_tools
#     )
