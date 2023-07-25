# import pytest

# from automata.llm.eval.eval_providers import OpenAIFunctionCallAction
# from automata.core.run_handlers import run_agent_and_get_eval


# @pytest.mark.ignore
# @pytest.mark.evaluation
# @pytest.mark.parametrize(
#     "instructions, agent_config_name, toolkit_list, model, max_iterations, expected_actions",
#     [
#         (
#             "Return what looks like to be the most relevant class for searching the codebase for relevant symbols, with no additional context",
#             "automata-main",
#             ["symbol-search"],
#             "gpt-4",
#             2,
#             [
#                 OpenAIFunctionCallAction(
#                     name="call_termination",
#                     arguments={
#                         "result": "automata.experimental.search.symbol_search.SymbolSearch"
#                     },
#                 )
#             ],
#         ),
#     ],
# )
# def test_eval_search(
#     instructions,
#     agent_config_name,
#     toolkit_list,
#     model,
#     max_iterations,
#     expected_actions,
# ):
#     eval_result = run_agent_and_get_eval(
#         instructions,
#         agent_config_name,
#         toolkit_list,
#         model,
#         max_iterations,
#         expected_actions,
#     )

#     # TODO - Add support for 'partial' matches, since the agent seems to enjoy
#     # returning results with extra text, like `autom...arching the codebase for relevant symbols appears to be `automata.experimental.search.symbol_search.SymbolSearch`....
#     assert (
#         eval_result.full_match
#     ), f"Expected actions were not fully matched. Match result: {eval_result.match_result}"
